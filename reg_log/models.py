from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
# Create your models here.


class Client(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=CASCADE)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=9, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    email = models.CharField(max_length=50, null=True)

    def __str__(self):
        return str(self.user)