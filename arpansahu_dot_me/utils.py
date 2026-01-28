"""
Utility functions for the arpansahu_dot_me project
"""
from django.conf import settings
from mailjet_rest import Client

mailjet = Client(auth=(settings.MAIL_JET_API_KEY, settings.MAIL_JET_API_SECRET), version='v3.1')


def send_email(to_email, to_name, subject, text_part, html_part, custom_id=None):
    """
    Send email using MailJet API
    
    Args:
        to_email: Recipient email address
        to_name: Recipient name
        subject: Email subject
        text_part: Plain text version of email
        html_part: HTML version of email
        custom_id: Optional custom ID for tracking
        
    Returns:
        tuple: (success: bool, status_code: int)
    """
    data = {
        'Messages': [
            {
                "From": {
                    "Email": settings.MAIL_JET_EMAIL_ADDRESS,
                    "Name": "arpansahu.space"
                },
                "To": [
                    {
                        "Email": to_email,
                        "Name": to_name
                    }
                ],
                "Subject": subject,
                "TextPart": text_part,
                "HTMLPart": html_part,
                "CustomID": custom_id or to_email
            }
        ]
    }
    
    try:
        result = mailjet.send.create(data=data)
        return result.status_code == 200, result.status_code
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise e
