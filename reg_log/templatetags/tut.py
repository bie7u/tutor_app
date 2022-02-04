from tutoring_ads.models import ReserveTutoring
from tutoring_ads.forms import ReserveTutoringForm
from django.shortcuts import get_object_or_404, render, redirect
from django import template

register = template.Library()

@register.filter(name='tut')
def tut(id, request):
    obj = get_object_or_404(ReserveTutoring, id=id)
    form = ReserveTutoringForm(instance=obj)
    if request.method == 'POST':
        form = ReserveTutoringForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('/')
    return form