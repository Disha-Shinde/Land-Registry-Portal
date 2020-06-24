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
    path('logout/', views.logout_user, name='logout'),
    path('land_registry_portal_index/', views.land_registry_portal_index, name='land_registry_portal_index'),
    path('upload_details/', views.upload_details, name='upload_details'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('search_property_by_user_details/', views.search_property_by_user_details, name='search_property_by_user_details'),
    path('transact/', views.transact, name='transact'),
    path('transaction/', views.transaction, name='transaction'),
    path('search_property_by_address/', views.search_property_by_address, name='search_property_by_address'),
    path('view_property_details/', views.view_property_details, name='view_property_details'),
    path('login_user/', views.login_user, name='login_user'),
    path('about_land_registry_portal/', views.about_land_registry_portal, name='about_land_registry_portal'),
    path('contact_us/', views.contact_us, name='contact_us'),
    
    
]