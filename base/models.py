from django.db import models

# Create your models here.


class Contact(models.Model):
    email = models.EmailField(blank=True)
    text = models.TextField(max_length=500)
    
    def __str__(self):
        return str(self.email)