from django.urls import path
from . import views

urlpatterns = [
    path('', views.userhome, name='userhome'),
    path('config/', views.userconfig, name='userconfig'),
    path('groups/', views.groups, name='groups'),
    path('creategroups/', views.createGroups, name='creategroups'),
    path('createnote/', views.createNote, name='createnote'),
    path('group/', views.showGroup, name='group'),
    path('quicktranscribe/', views.quickTranscribe, name="quicktranscribe"),
    path('newnote/', views.newNote, name="newnote"),
    path('note/', views.showNote, name="note"),
    path('update/', views.update, name="update"),
    path('delete/', views.delete, name="delete"),
    path('create/', views.create, name="create"),
]