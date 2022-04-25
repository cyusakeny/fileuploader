import uuid

from django.db import models
from User.models import Profile


# Create your models here.

class File(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    shared = models.ManyToManyField('SharedFile', blank=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    extension = models.CharField(max_length=200)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)

    def __str__(self):
        return self.name


class SharedFile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    File = models.ForeignKey(File, on_delete=models.CASCADE)
    sent = models.DateTimeField(auto_now_add=True)
    to = models.ForeignKey(Profile,  on_delete=models.CASCADE)
