import argparse
import os
import traceback

from django.conf import settings
from django.http import HttpResponse, FileResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from .forms import ContactForm
import dropbox

from django.conf import settings
from mailjet_rest import Client

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

            # import smtplib, ssl
            # from email.mime.text import MIMEText
            # from email.mime.multipart import MIMEMultipart

            # sender_email = "contact@arpansahu.me"
            # receiver_email = settings.EMAIL
            # password = settings.PASS
            #
            # message = MIMEMultipart("alternative")
            # message["Subject"] = f"{name} Contacted you on arpansahu.me"
            # message["From"] = sender_email
            # message["To"] = receiver_email

            # Create the plain-text and HTML version of your message
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

            # Turn these into plain/html MIMEText objects
            # part1 = MIMEText(text, "plain")
            # part2 = MIMEText(html, "html")

            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            # message.attach(part1)
            # message.attach(part2)

            # Create secure connection with server and send email
            # context = ssl.create_default_context()

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
                # with smtplib.SMTP_SSL("smtppro.zoho.in", 465, context=context) as server:
                #     server.login(sender_email, password)
                #     server.sendmail(
                #         sender_email, receiver_email, message.as_string()
                #     )
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


class ContactView(View):
    def get(self, *args, **kwargs):
        form = ContactForm()
        return render(self.request, template_name='contact.html',
                      context={'form': form, 'message_sent_done': 'get', 'contact': 'active'})

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        message_sent = False

        if form.is_valid():
            name = request.POST['name']
            email = request.POST['email']
            contact = request.POST['contact']
            subject = request.POST['subject']
            message_form = request.POST['message']
            # import smtplib, ssl
            # from email.mime.text import MIMEText
            # from email.mime.multipart import MIMEMultipart

            # sender_email = "contact@arpansahu.me"
            # receiver_email = settings.EMAIL
            # password = settings.PASS
            #
            # message = MIMEMultipart("alternative")
            # message["Subject"] = f"{name} Contacted you on arpansahu.me"
            # message["From"] = sender_email
            # message["To"] = receiver_email

            # Create the plain-text and HTML version of your message
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

            # Turn these into plain/html MIMEText objects
            # part1 = MIMEText(text, "plain")
            # part2 = MIMEText(html, "html")

            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            # message.attach(part1)
            # message.attach(part2)

            # Create secure connection with server and send email
            # context = ssl.create_default_context()

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
                # with smtplib.SMTP_SSL("smtppro.zoho.in", 465, context=context) as server:
                #     server.login(sender_email, password)
                #     server.sendmail(
                #         sender_email, receiver_email, message.as_string()
                #     )
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