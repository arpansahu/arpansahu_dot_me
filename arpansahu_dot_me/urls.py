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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    Home,
    ProjectDetailedView,
    ContactView,
    AboutView,
    ProjectsView,
    ResumeView,
    GetOTPView,
    ResumeDownloadView
)

def trigger_error(request):
    division_by_zero = 1 / 0

def large_resource(request):
   time.sleep(4)
   return HttpResponse("Done!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name='home'),
    path('projects/<str:project_name>', ProjectDetailedView.as_view(), name='project-detailed-view'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('about/', AboutView.as_view(), name='about'),
    path('projects/', ProjectsView.as_view(), name='projects'),
    path('resume/', ResumeView.as_view(), name='resume'),
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
