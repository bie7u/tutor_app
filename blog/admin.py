from django.contrib import admin
from .models import BlogEntry, EntryComments, RatingSystem
# Register your models here.

admin.site.register(BlogEntry)
admin.site.register(EntryComments)
admin.site.register(RatingSystem)