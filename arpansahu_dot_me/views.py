import argparse
import os
import traceback
from datetime import datetime

from braces.views import AjaxResponseMixin
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import ContactForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from braces import views

import dropbox
import base64
import pyotp

from django.conf import settings
from mailjet_rest import Client

from emails_otp.models import EmailsOtpRecord

mailjet = Client(auth=(settings.MAIL_JET_API_KEY, settings.MAIL_JET_API_SECRET), version='v3.1')


class Home(View):
    def get(self, *args, **kwargs):
        form = ContactForm()
        return render(self.request, template_name='index.html',
                      context={'form': form, 'message_sent_done': 'get', 'home': 'active'})

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        message_sent = False

        if form.is_valid():
            name = request.POST['name']
            email = request.POST['email']
            contact = request.POST['contact']
            subject = request.POST['subject']
            message_form = request.POST['message']

            text = """\
                        Hi message from {0},
                        How are you?<br>
                        Subject: {1}
                        www.arpansahu.me""".format(name, subject)
            html = """\
                        <html>
                          <body>
                            <p>Hi {0} contacted from your Portfolio,<br>
                                Message:{2} <br>
                                Contact Details:<br>
                                <p>{3}<br>{4}</p>
                               <a href="https://www.arpansahu.me">arpansahu.me</a> 
                            </p>
                          </body>
                        </html>
                        """.format(name, subject, message_form, contact, email)

            data = {
                'Messages': [
                    {
                        "From": {
                            "Email": "admin@arpansahu.me",
                            "Name": "arpansahu.me"
                        },
                        "To": [
                            {
                                "Email": settings.MY_EMAIL_ADDRESS,
                                "Name": "Arpan Sahu"
                            }
                        ],
                        "Subject": f'{name} Contacted you on arpansahu.me',
                        "TextPart": text,
                        "HTMLPart": html,
                        "CustomID": f"{email}"
                    }
                ]
            }

            try:
                result = mailjet.send.create(data=data)
                if result.status_code == 200:
                    message_sent = True
            except Exception as e:
                tb = traceback.format_exc()
                print(tb)
                raise e

        form = ContactForm()
        return render(self.request, template_name='index.html',
                      context={'form': form, 'message_sent_done': message_sent})


class ProjectDetailedView(View):
    def get(self, *args, **kwargs):
        project_id = self.kwargs['pk']
        template_name = f'modules/project_detailed/project{project_id}.html'
        return render(self.request, template_name=template_name, context={'project_id': project_id})


class AboutView(View):
    def get(self, *args, **kwargs):
        return render(self.request, template_name='about.html', context={'about': 'active'})


class ProjectsView(View):
    def get(self, *args, **kwargs):
        return render(self.request, template_name='projects.html', context={'project': 'active'})


@method_decorator(csrf_exempt, name='dispatch')
class GetOTPView(views.JSONResponseMixin, views.AjaxResponseMixin, View):

    def dispatch(self, request, *args, **kwargs):
        request_method = request.method.lower()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request_method in self.http_method_names:
            handler = getattr(
                self,
                "{0}_ajax".format(request_method),
                self.http_method_not_allowed,
            )
            self.request = request
            self.args = args
            self.kwargs = kwargs
            return handler(request, *args, **kwargs)

        return super(AjaxResponseMixin, self).dispatch(
            request, *args, **kwargs
        )

    def post_ajax(self, request, *args, **kwargs):
        email = self.request.POST.get('email').lower()
        email_status_obj = EmailsOtpRecord.objects.filter(email=email, date=datetime.today()).first()
        status = None
        message = None
        otp = None
        status_code = None
        subject = 'One Time Password for Contacting on arpansahu.me'

        if email_status_obj and email_status_obj.count >= 5:
            status_code = 400
            status = 'Failed'
            message = 'Same Email address cannot generate more than 5 otp in a day'

        else:
            key = base64.b32encode((email + settings.SECRET_KEY).encode())  # Key is generated
            otp_obj = pyotp.TOTP(key, interval=settings.OTP_EXPIRY_TIME)
            otp = otp_obj.now()
            text = """\
                        Hi message from {0},
                        How are you?<br>
                        Subject: {1}
                        www.arpansahu.me""".format(email, subject)
            html = """\
                        <html>
                          <body>
                            <p>Hi {0} here is otp from for contacting on arpansahu.me <br>
                                OTP:{2} <br>
                                <p> this otp is valid for 60 seconds. </p><br>
                               <a href="https://www.arpansahu.me">arpansahu.me</a> 
                            </p>
                          </body>
                        </html>
                        """.format(email, subject, otp)

            data = {
                'Messages': [
                    {
                        "From": {
                            "Email": "admin@arpansahu.me",
                            "Name": "arpansahu.me"
                        },
                        "To": [
                            {
                                "Email": email,
                                "Name": f"{email}"
                            }
                        ],
                        "Subject": subject,
                        "TextPart": text,
                        "HTMLPart": html,
                        "CustomID": f"{email}"
                    }
                ]
            }

            try:
                result = mailjet.send.create(data=data)
                if result.status_code == 200:
                    status_code = 200
                    status = 'Success'
                    message = 'OTP Sent to your email Successful'

                    if email_status_obj:
                        email_status_obj.count += 1
                        email_status_obj.save()
                    else:
                        email_status_obj = EmailsOtpRecord(email=email).save()

            except Exception as e:
                tb = traceback.format_exc()
                print(tb)
                raise e

        return self.render_json_response({'status': status, 'message': message}, status=status_code)


class ContactView(View):
    def get(self, *args, **kwargs):
        form = ContactForm()
        return render(self.request, template_name='contact.html',
                      context={'form': form, 'message_sent_done': 'get', 'contact': 'active'})

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        message_sent = False
        breakpoint()
        if form.is_valid():
            name = request.POST.get('name', 'None')
            email = request.POST.get('email', None).lower()
            contact = request.POST.get('contact', None)
            subject = request.POST.get('subject')
            message_form = request.POST.get('message', None)
            otp = request.POST.get('otp', None)

            key = base64.b32encode((email + settings.SECRET_KEY).encode())
            otp_obj = pyotp.TOTP(key, interval=settings.OTP_EXPIRY_TIME)

            if otp_obj.verify(otp):

                text = """\
                Hi message from {0},
                How are you?<br>
                Subject: {1}
                www.arpansahu.me""".format(name, subject)
                html = """\
                <html>
                  <body>
                    <p>Hi {0} contacted from your Portfolio,<br>
                        Message:{2} <br>
                        Contact Details:<br>
                        <p>{3}<br>{4}</p>
                       <a href="https://www.arpansahu.me">arpansahu.me</a> 
                    </p>
                  </body>
                </html>
                """.format(name, subject, message_form, contact, email)

                data = {
                    'Messages': [
                        {
                            "From": {
                                "Email": "admin@arpansahu.me",
                                "Name": "arpansahu.me"
                            },
                            "To": [
                                {
                                    "Email": settings.MY_EMAIL_ADDRESS,
                                    "Name": "Arpan Sahu"
                                }
                            ],
                            "Subject": f'{name} Contacted you on arpansahu.me',
                            "TextPart": text,
                            "HTMLPart": html,
                            "CustomID": f"{email}"
                        }
                    ]
                }

                try:
                    result = mailjet.send.create(data=data)
                    if result.status_code == 200:
                        message_sent = True
                except Exception as e:
                    tb = traceback.format_exc()
                    print(tb)
                    raise e

        form = ContactForm()
        return render(self.request, template_name='contact.html',
                      context={'form': form, 'message_sent_done': message_sent})


class ResumeView(View):
    def get(self, *args, **kwargs):
        # dbx = dropbox.Dropbox(app_secret='3ff49y21jcyqcy6', app_key='70ccz9td03ypgr7')
        # dbx.files_download_to_file('arpansahuresume.pdf', '/' + 'arpansahuresume.pdf')
        # file_path = os.path.join(str(settings.BASE_DIR) + '/', 'arpansahuresume.pdf')
        # return FileResponse(open(file_path, 'rb'), content_type='application/pdf')

        return HttpResponseRedirect('https://certificates.arpansahu.me/resume')
