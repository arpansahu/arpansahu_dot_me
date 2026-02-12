"""arpansahu_dot_me URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from .views import (
    Home,
    ProjectDetailedView,
    ContactView,
    AboutView,
    ProjectsView,
    ResumeView,
    GetOTPView,
    ResumeDownloadView,
    PrivacyView,
    TAndCView,
)

from account.views import (
    LoginView,
    LogoutView,
    RegistrationView,
    AccountView,
    activate,
    CustomPasswordResetView,
    SocialDisconnectView,
    DeleteAccountView,
)

def trigger_error(request):
    division_by_zero = 1 / 0

def large_resource(request):
   time.sleep(4)
   return HttpResponse("Done!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name='home'),
    path('blog/', include('blog.urls')),
    path('comments/', include('comments.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    # Redirect allauth login/logout to custom pages (must be BEFORE allauth.urls)
    path('accounts/login/', RedirectView.as_view(pattern_name='login', permanent=False)),
    path('accounts/logout/', RedirectView.as_view(pattern_name='logout', permanent=False)),
    
    # Social Authentication (django-allauth) - For OAuth callbacks
    path('accounts/', include('allauth.urls')),
    
    # Account URLs
    path('account/login/', LoginView.as_view(), name='login'),
    path('account/logout/', LogoutView.as_view(), name='logout'),
    path('account/register/', RegistrationView.as_view(), name='register'),
    path('account/profile/', AccountView.as_view(), name='account'),
    path('account/activate/<uidb64>/<token>/', activate, name='activate'),
    path('account/social/disconnect/<str:provider_id>/', SocialDisconnectView.as_view(), name='social_disconnect'),
    path('account/delete/', DeleteAccountView.as_view(), name='delete_account'),
    
    # Password Reset URLs (Custom)
    path('account/password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('account/', include('django.contrib.auth.urls')),  # This includes password_reset_done, confirm, complete
    
    path('projects/<str:project_name>', ProjectDetailedView.as_view(), name='project-detailed-view'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('about/', AboutView.as_view(), name='about'),
    path('projects/', ProjectsView.as_view(), name='projects'),
    path('resume/', ResumeView.as_view(), name='resume'),
    path('privacy/', PrivacyView.as_view(), name='privacy'),
    path('t_and_c/', TAndCView.as_view(), name='t_and_c'),
    path('get-otp', GetOTPView.as_view(), name='get-otp'),
    path('download/resume/', ResumeDownloadView.as_view(), name='resume_download'),

    #sentry test view 
    path('sentry-debug/', trigger_error),
    path('large_resource/', large_resource)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'account.views.error_404'
handler500 = 'account.views.error_500'
handler403 = 'account.views.error_403'
handler400 = 'account.views.error_400'
