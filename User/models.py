import uuid

from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    username = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(max_length=500, unique=True, blank=False, null=False)
    phone = models.IntegerField(unique=True, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)


