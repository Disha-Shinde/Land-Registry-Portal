"""Land_Registry_Portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', views.signup_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('land_registry_portal_index/', views.land_registry_portal_index, name='land_registry_portal_index'),
    path('upload_details/', views.upload_details, name='upload_details'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('retrieve_details/', views.retrieve_details, name='retrieve_details'),
    path('retrieve_file/', views.retrieve_file, name='retrieve_file'),
    
]