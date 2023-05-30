from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about', views.about, name="about"),
    path('auth/', include('Apps.Authentication.urls')),
    path('user/', include('Apps.User.urls')),
    path('logic/', include('Apps.Logic.urls')),
]