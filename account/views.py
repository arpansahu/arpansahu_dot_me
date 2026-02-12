import ssl

from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import FormView, RedirectView
from django.utils.translation import gettext_lazy as _

from django.views.generic import ListView, UpdateView, DetailView, CreateView, FormView
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm, PasswordResetForm, LoginForm
from django.conf import settings
from django.contrib.auth.views import PasswordContextMixin

from account.models import Account
from account.token import account_activation_token

DOMAIN = settings.DOMAIN
PROTOCOL = settings.PROTOCOL

from mailjet_rest import Client

mailjet = Client(auth=(settings.MAIL_JET_API_KEY, settings.MAIL_JET_API_SECRET), version='v3.1')


# Create your views here.

class CustomPasswordResetView(PasswordContextMixin, FormView):
    email_template_name = "registration/password_reset_email.html"
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = "registration/password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")
    template_name = "registration/password_reset_form.html"
    title = _("Password reset")
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "subject_template_name": self.subject_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


def send_mail_account_activate(reciever_email, user, SUBJECT="Confirm Your Email - Arpan Sahu"):
    html_message = render_to_string(template_name='account/activate_account_mail.html', context={
        'user': user,
        'protocol': PROTOCOL,
        'domain': DOMAIN,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    
    # Plain text version for email clients that don't support HTML
    text_message = f"""
    Hi {user.username},
    
    Thank you for registering at arpansahu.space!
    
    To activate your account, please click the link below:
    {PROTOCOL}://{DOMAIN}/account/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{account_activation_token.make_token(user)}/
    
    If you didn't request this, please ignore this email.
    
    This link will expire in 24 hours.
    
    Best regards,
    Arpan Sahu
    {PROTOCOL}://{DOMAIN}
    """

    data = {
        'Messages': [
            {
                "From": {
                    "Email": "admin@arpansahu.space",
                    "Name": "Arpan Sahu"
                },
                "To": [
                    {
                        "Email": reciever_email,
                        "Name": user.username
                    }
                ],
                "Subject": SUBJECT,
                "TextPart": text_message,
                "HTMLPart": html_message,
                "CustomID": f"account_activation_{user.pk}"
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(f"Account activation email sent to {reciever_email}")
    return result


def send_welcome_email(reciever_email, user):
    """Send welcome email after successful account activation"""
    html_message = render_to_string(template_name='account/welcome_email.html', context={
        'user': user,
        'protocol': PROTOCOL,
        'domain': DOMAIN,
    })
    
    text_message = f"""
    Hi {user.username},
    
    Welcome aboard! Your account has been successfully activated.
    
    You're now part of the community and can access all features:
    • Comment on blog posts and engage with content
    • Receive notifications when someone replies to you
    • Manage your profile and customize settings
    • Like posts and comments to show appreciation
    
    Explore the blog: {PROTOCOL}://{DOMAIN}/blog/
    
    Best regards,
    Arpan Sahu
    {PROTOCOL}://{DOMAIN}
    """

    data = {
        'Messages': [
            {
                "From": {
                    "Email": "admin@arpansahu.space",
                    "Name": "Arpan Sahu"
                },
                "To": [
                    {
                        "Email": reciever_email,
                        "Name": user.username
                    }
                ],
                "Subject": "Welcome to Arpan Sahu!",
                "TextPart": text_message,
                "HTMLPart": html_message,
                "CustomID": f"welcome_email_{user.pk}"
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(f"Welcome email sent to {reciever_email}")
    return result


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # Send welcome email after activation
        send_welcome_email(user.email, user)
        return render(request, 'account/account_activation_done.html', context={'message': 'Thank you for your email '
                                                                                           'confirmation. Now you can '
                                                                                           'login your account.'})
    else:
        return render(request, 'account/account_activation_done.html', context={'message': 'Activation link is invalid!'})


class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        form = RegistrationForm()
        context['registration_form'] = form
        return render(request, 'account/register.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = RegistrationForm(request.POST)
        if form.is_valid():
            account = form.save()
            email = form.cleaned_data.get('email')
            send_mail_account_activate(email, account)
            return render(request, 'account/account_activation_done.html', {'message': 'Check your mail and activate your account'})
        else:
            context['registration_form'] = form
        return render(request, 'account/register.html', context)


@method_decorator(login_required(redirect_field_name=''), name='dispatch')
class LogoutView(RedirectView):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


class LoginView(View):
    def get(self, request):
        form = LoginForm(request.POST or None)
        msg = None
        if request.user.is_authenticated:
            # If already authenticated, redirect to next or home
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        return render(request, "account/login.html", {"form": form, "msg": msg})

    def post(self, request):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(email=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to next parameter or home
                next_url = request.GET.get('next') or request.POST.get('next', '/')
                return redirect(next_url)
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

        return render(request, "account/login.html", {"form": form, "msg": msg})


@method_decorator(login_required(redirect_field_name=''), name='dispatch')
class AccountView(View):
    def _get_social_context(self, user):
        """Build a list of all enabled providers with their connection status."""
        from allauth.socialaccount.models import SocialAccount
        connected = {sa.provider: sa for sa in SocialAccount.objects.filter(user=user)}
        
        providers = [
            {
                'id': 'google',
                'name': 'Google',
                'icon': 'fab fa-google',
                'color': '#ea4335',
                'connected': 'google' in connected,
                'login_url': '/accounts/google/login/?process=connect',
            },
            {
                'id': 'github',
                'name': 'GitHub',
                'icon': 'fab fa-github',
                'color': '#24292e',
                'connected': 'github' in connected,
                'login_url': '/accounts/github/login/?process=connect',
            },
            {
                'id': 'facebook',
                'name': 'Facebook',
                'icon': 'fab fa-facebook-f',
                'color': '#1877f2',
                'connected': 'facebook' in connected,
                'login_url': '/accounts/facebook/login/?process=connect',
            },
            {
                'id': 'twitter_oauth2',
                'name': 'X (Twitter)',
                'icon': 'fab fa-x-twitter',
                'color': '#000000',
                'connected': 'twitter_oauth2' in connected,
                'login_url': '/accounts/twitter_oauth2/login/?process=connect',
            },
            {
                'id': 'linkedin',
                'name': 'LinkedIn',
                'icon': 'fab fa-linkedin-in',
                'color': '#0a66c2',
                'connected': 'linkedin' in connected,
                'login_url': '/accounts/openid_connect/login/?provider_id=linkedin&process=connect',
            },
        ]
        return providers

    def get(self, request, *args, **kwargs):
        context = {}
        form = AccountUpdateForm(
            initial={
                "email": request.user.email,
                "username": request.user.username,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
            }
        )
        context["account"] = request.user
        context['account_form'] = form
        context['social_providers'] = self._get_social_context(request.user)
        # Add unread notification count
        try:
            from blog.models import Notification
            context['unread_notification_count'] = Notification.objects.filter(
                recipient=request.user, is_read=False
            ).count()
        except Exception:
            context['unread_notification_count'] = 0
        return render(request, 'account/account.html', context)

    def post(self, request, *args, **kwargs):
        from django.contrib import messages as django_messages
        
        context = {}
        # Update user fields manually
        user = request.user
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        
        try:
            user.save()
            django_messages.success(request, 'Your profile has been updated successfully!')
        except Exception as e:
            django_messages.error(request, f'Error updating profile: {str(e)}')
        
        form = AccountUpdateForm(
            initial={
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        )
        context["account"] = user
        context['account_form'] = form
        context['social_providers'] = self._get_social_context(user)
        return render(request, 'account/account.html', context)


@method_decorator(login_required(redirect_field_name=''), name='dispatch')
class SocialDisconnectView(View):
    """Disconnect a social account from the current user."""
    
    def post(self, request, provider_id):
        from allauth.socialaccount.models import SocialAccount
        from django.contrib import messages
        
        try:
            account = SocialAccount.objects.get(user=request.user, provider=provider_id)
            
            # Safety: ensure user still has a way to log in (password or another social account)
            other_socials = SocialAccount.objects.filter(user=request.user).exclude(pk=account.pk).count()
            has_password = request.user.has_usable_password()
            
            if not has_password and other_socials == 0:
                messages.error(
                    request,
                    "Cannot disconnect — you have no password set and this is your only sign-in method. "
                    "Please set a password first."
                )
                return redirect('account')
            
            provider_name = {
                'google': 'Google', 'github': 'GitHub', 'facebook': 'Facebook',
                'twitter_oauth2': 'X (Twitter)', 'linkedin': 'LinkedIn',
            }.get(provider_id, provider_id.title())
            
            account.delete()
            messages.success(request, f'{provider_name} account disconnected successfully.')
        except SocialAccount.DoesNotExist:
            messages.error(request, 'Social account not found.')
        
        return redirect('account')


@method_decorator(login_required(redirect_field_name=''), name='dispatch')
class DeleteAccountView(View):
    """View for account deletion with confirmation.
    
    Admin accounts cannot be fully deleted - they will be disabled instead,
    and their blog posts will be hidden from public view.
    """
    
    def get(self, request, *args, **kwargs):
        """Show confirmation page before deletion"""
        context = {
            'is_admin': request.user.is_admin,
        }
        return render(request, 'account/delete_account_confirm.html', context)
    
    def post(self, request, *args, **kwargs):
        """Handle account deletion or deactivation"""
        user = request.user
        is_admin = user.is_admin
        
        if is_admin:
            # Admin accounts are disabled, not deleted
            user.is_active = False
            user.save()
            
            # Log user out
            logout(request)
            
            return render(request, 'account/delete_account_done.html', {
                'message': 'Your admin account has been disabled. Your blog posts will no longer be displayed publicly. Contact system administrator if you wish to reactivate.',
                'is_admin': True,
            })
        else:
            # Regular users can delete their account
            # Log user out before deletion
            logout(request)
            
            # Delete the user account
            user.delete()
            
            return render(request, 'account/delete_account_done.html', {
                'message': 'Your account has been successfully deleted. We\'re sorry to see you go!',
                'is_admin': False,
            })


def error_404(request, exception):
    return render(request, 'error/error_404.html')


def error_400(request, exception):
    return render(request, 'error/error_400.html')


def error_403(request, exception):
    return render(request, 'error/error_403.html')


def error_500(request):
    return render(request, 'error/error_500.html')