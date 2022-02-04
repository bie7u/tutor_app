from django.db.models import fields
from django.db.models.base import Model
from .models import BlogEntry, EntryComments, RatingSystem
from django.forms import ModelForm
from django import forms


class BlogEntryForm(ModelForm):

    class Meta:
        model = BlogEntry
        fields = '__all__'
        exclude = ['user']

class BlogEntrySecond(ModelForm):

    class Meta:
        model = BlogEntry
        fields = '__all__'
        exclude = ['user', 'title', 'text', 'blog_pic', 'created_on', 'modified', 'average_rate']

class EntryCommentsForm(ModelForm):

    class Meta:
        model = EntryComments
        fields = '__all__'
        exclude = ['comment', 'user']

class RatingSystemForm(ModelForm):

    class Meta:
        model = RatingSystem
        fields = '__all__'
        exclude = ['user', 'rating']

