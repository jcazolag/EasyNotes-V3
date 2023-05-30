from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('whisper', views.whisper, name="whisper"),
    path('chat', views.chat, name="chat"),
]