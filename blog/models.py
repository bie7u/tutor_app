from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case
from django.db.models.fields.related import ForeignKey
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class BlogEntry(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=CASCADE)

    title = models.CharField(max_length=60)
    text = models.TextField(max_length=2000)
    blog_pic = models.ImageField(null=True)
    
    admin_agree = models.BooleanField(default=False, blank=True)
    average_rate = models.CharField(default=False, max_length=200000000000000000, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

class EntryComments(models.Model):
    user = ForeignKey(User, default=None, on_delete=CASCADE)
    comment = models.ForeignKey(BlogEntry, default=None, on_delete=CASCADE)
    text = models.TextField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + "-" + str(self.comment)

class RatingSystem(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=CASCADE)
    rating = models.ForeignKey(BlogEntry, default=None, on_delete=CASCADE)
    score = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
            ]
        )

    def __str__(self):
        return str(self.rating.user)