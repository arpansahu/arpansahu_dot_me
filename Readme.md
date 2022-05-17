
# arpansahu | Django Portfolio Website

This project is implementation for the following topics related to technologies used with Django

-Build Portfolio Using Bootstrap 5.
    
1. Used Bootstrap for building UI and Django as Backend.
2. Used DropBox API for showing updated Resumes.
3. Used Javascript / Jquery for making templates Dynamic
4. Used SMTP to notify my whenever someone tries to message me on arpansahu.me
5. Used AWS S3 Bucket
6. Since Heroku doesn't allow to send mail using SMTP, Integrated Mail Jet

-Deployed on Heroku

1. Used Heroku Postgres 


## Tech Stack

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Jquery](https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white)](https://jquery.com/)
[![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Glossary/HTML5)
[![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Javascript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)](https://www.javascript.com/)
[![Heroku](https://img.shields.io/badge/-Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)](https://heroku.com/)
[![AWS](https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com/)
[![Github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://www.github.com/)

## Demo

Available at: https://www.arpansahu.me/

## License

[MIT](https://choosealicense.com/licenses/mit/)


## Installation

Installing Pre requisites

```bash
  pip install -r requirements.txt

```

Run Server
```bash
  python manage.py runserver

```

## Tech Stack

**Client:** HTML, Jinja, CSS, BootStrap, Jquery

**Server:** Django, Gunicorn, Heroku

## Integrating AWS S3 Bucket 

Install two python packages
``` 
pip install boto3
pip install django-storages
```

create a new file named ```storage_backends.py``` with this code inside it.

``` 
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = settings.AWS_STATIC_LOCATION


class PublicMediaStorage(S3Boto3Storage):
    location = settings.AWS_PUBLIC_MEDIA_LOCATION
    file_overwrite = False


class PrivateMediaStorage(S3Boto3Storage):
    location = 'private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False

```

Change settings.py static files and media files settings
``` 
if not DEBUG:
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400'
    }
    AWS_LOCATION = 'static'
    AWS_QUERYSTRING_AUTH = False
    AWS_HEADERS = {
        'Access-Control-Allow-Origin': '*',
    }
    # s3 static settings
    AWS_STATIC_LOCATION = 'portfolio/arpansahu.me/static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'arpansahu_dot_me.storage_backends.StaticStorage'
    # s3 public media settings
    AWS_PUBLIC_MEDIA_LOCATION = 'portfolio/arpansahu.me/media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'arpansahu_dot_me.storage_backends.PublicMediaStorage'
    # s3 private media settings
    PRIVATE_MEDIA_LOCATION = 'portfolio/arpansahu.me/private'
    PRIVATE_FILE_STORAGE = 'arpansahu_dot_me.storage_backends.PrivateMediaStorage'
else:
    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.2/howto/static-files/

    STATIC_URL = '/static/'

    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"), ]
```

run below command ```python manage.py collectstatic```  and you are good to go


## Deployment on Heroku

Installing Heroku Cli from : https://devcenter.heroku.com/articles/heroku-cli
Create your account in Heroku.

Inside your project directory

Login Heroku CLI
```bash
  heroku login

```

Create Heroku App

```bash
  heroku create [app_name]

```

Push Heroku App
```
    git push heroku master
```

Configure Heroku App Env Variables
```bash
  heroku config:set GITHUB_USERNAME=joesmith
```
Configuring Django App for Heroku

Install whitenoise 
```
pip install whitenoise 
```

Include it in Middlewares.
```
MIDDLEWARE = [
    # ...
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # ...
]
```

Create Procfile and include this code snippet in it.
```
web: gunicorn arpansahu_dot_me.wsgi
```

## Documentation

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Jquery](https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white)](https://jquery.com/)
[![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Glossary/HTML5)
[![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Javascript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)](https://www.javascript.com/)
[![Heroku](https://img.shields.io/badge/-Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)](https://heroku.com/)
[![AWS](https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com/)
[![Github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://www.github.com/)

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

SECRET_KEY=

DEBUG=

EMAIL=

PASS=

ALLOWED_HOSTS=

DROPBOX_ACCESS_TOKEN=

MAIL_JET_API_KEY=

MAIL_JET_API_SECRET=

MY_EMAIL_ADDRESS=

AWS_ACCESS_KEY_ID=

AWS_SECRET_ACCESS_KEY=

AWS_STORAGE_BUCKET_NAME=