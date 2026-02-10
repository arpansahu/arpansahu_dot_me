from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from mailjet_rest import Client

mailjet = Client(auth=(settings.MAIL_JET_API_KEY, settings.MAIL_JET_API_SECRET), version='v3.1')


def send_password_reset_email(user, reset_url):
    """Send password reset email using MailJet"""
    
    html_message = render_to_string(template_name='registration/password_reset_email.html', context={
        'user': user,
        'protocol': settings.PROTOCOL,
        'domain': settings.DOMAIN,
        'uid': reset_url.split('/')[-3],
        'token': reset_url.split('/')[-2],
    })
    
    text_message = f"""
    Hi {user.username},
    
    You're receiving this email because you (or someone else) requested a password reset for your account at arpansahu.space.
    
    Click the link below to set a new password:
    {reset_url}
    
    This link expires in 24 hours.
    
    If you didn't request a password reset, please ignore this email. Your password won't change until you access the link above and create a new one.
    
    Best regards,
    Arpan Sahu
    {settings.PROTOCOL}://{settings.DOMAIN}
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
                        "Email": user.email,
                        "Name": user.username
                    }
                ],
                "Subject": "Password Reset Request - Arpan Sahu",
                "TextPart": text_message,
                "HTMLPart": html_message,
                "CustomID": f"password_reset_{user.pk}"
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(f"Password reset email sent to {user.email}")
    return result
