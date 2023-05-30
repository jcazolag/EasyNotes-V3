from django.db import models
from django.contrib.auth.models import User

class UserGroups(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, null=True,on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)


class UserNotes(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    group = models.ForeignKey(UserGroups, null=True,on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

class noteDeadline(models.Model):
    description = models.TextField()
    note = models.ForeignKey(UserNotes, null=True,on_delete=models.CASCADE)

class noteSummary(models.Model):
    text = models.TextField()
    note = models.ForeignKey(UserNotes, null=True,on_delete=models.CASCADE)

class noteStudyMaterial(models.Model):
    text = models.TextField()
    note = models.ForeignKey(UserNotes, null=True,on_delete=models.CASCADE)