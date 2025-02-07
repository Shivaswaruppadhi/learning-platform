"""
URL configuration for ActualProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from app.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/',registration,name='registration'),
    path('home/',home,name='home'),
    path('user_login/',user_login,name='user_login'),
    path('user_logout/',user_logout,name='user_logout'),
    path('profile_page/',profile_page,name='profile_page'),
    path('change_password/',change_password,name='change_password'),
    path('reset_password/',reset_password,name='reset_password'),
    path('otp_page/',otp_page,name='otp_page'),
    path('reset_continuation/',reset_continuation,name='reset_continuation'),
    path('courseData/',courseData,name='courseData'),
    path('courses/',courses,name='courses'),
    path('EnrollmentDetails/',EnrollmentDetails,name='EnrollmentDetails'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
