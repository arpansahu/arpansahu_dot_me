import markdown
import os
import shutil
from django.core.management import BaseCommand
from django.conf import settings

urls = [
        "https://github.com/arpansahu/django-project/",
        "https://github.com/arpansahu/django-chat-app-tortise-with-sqlite3",
        "https://github.com/arpansahu/django-numeric-calculator",
        "https://github.com/arpansahu/django-react-frontend",
        "https://github.com/arpansahu/django-react-backend-with-social",
        "https://github.com/arpansahu/djnago-custom-user-model",
        "https://github.com/arpansahu/django-all-auth",
        "https://github.com/arpansahu/Third-Eye-Complete-With-a-web-app",
        "https://github.com/arpansahu/premium-collection-point"
    ]


def startup():
    print("---------------------Update Readme Command Started----------------------")

    os.mkdir(str(settings.BASE_DIR) + '/markdown')

    folder = 'markdown/'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    for i in range(len(urls)):
        from git.repo.base import Repo
        Repo.clone_from(urls[i], f'markdown/project{i + 1}')
        shutil.copyfile(str(settings.BASE_DIR) + f'/markdown/project{i + 1}/Readme.md',
                        str(settings.BASE_DIR) + f'/markdown/project{i + 1}.md')

        with open(f'markdown/project{i + 1}.md', 'r') as f:
            text = f.read()
            html = markdown.markdown(text)

        with open(f'templates/markdown/project{i + 1}.html', 'w') as f:
            f.write(html)

        folder = 'markdown/'

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    os.rmdir(str(settings.BASE_DIR) + '/markdown')
    print("---------------------Update Readme Command Ended----------------------")


class Command(BaseCommand):
    def handle(self, *args, **options):
        startup()
