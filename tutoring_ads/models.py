
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from reg_log.models import Client
# Create your models here.

class Notice(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=CASCADE)
    title = models.CharField(max_length=50, null=True)
    text = models.TextField(max_length=2000, null=True)
    profile_pic = models.ImageField(null=True)
    price = models.CharField(max_length=3, null=True)
    age = models.CharField(max_length=2, null=True)
    city = models.CharField(max_length=30, null=True)

    data = models.ForeignKey(Client, default=None, on_delete=CASCADE)

    SUBJECTS = (
        ('angielski', 'angielski'),
        ('matematyka', 'matematyka'),
        ('polski', 'polski'),
    )

    subject = models.CharField(max_length=200, null=True, choices=SUBJECTS)

    def __str__(self):
        return str(self.user)



class ReserveTutoring(models.Model):

    accept = (
        ('1', 'Zaakceptuj korepetycje'),
        ('2', 'Odrzuć korepetycje'),
    )


    user = models.ForeignKey(User, default=None, on_delete=CASCADE, null=True)
    tutor = models.ForeignKey(Notice, default=None, on_delete=CASCADE, null=True)
    accept = models.CharField(max_length=200, null=True, choices=accept, blank=True)
    agree = models.BooleanField(default=False, blank=True)
    city = models.CharField(max_length=200, null=True)
    street = models.CharField(max_length=200, null=True)
    number = models.CharField(max_length=4, null=True)
    phone_number = models.CharField(max_length=9, null=True)
    expiration_date = models.DateField(null=True)
    hours = models.TimeField(null=True)
    
    def __str__(self):
        return str(self.tutor)