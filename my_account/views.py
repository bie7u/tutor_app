from typing import AsyncContextManager
from django.contrib.auth.models import User
from django.core.checks import messages
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from reg_log.models import Client
from reg_log.forms import ClientForm
from tutoring_ads.models import ReserveTutoring
from tutoring_ads.forms import ReserveTutoringForm, ReserveTutoringFormSecond
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage, send_mail
# Create your views here.

def search_id(request):
    for i in Client.objects.all():
        if request.user == i.user:
            return i.id


def my_account_page(request):
    form = [i for i in ReserveTutoring.objects.all() if str(i.tutor)==str(request.user) and i.agree==False]
    delete_tut = ReserveTutoring.objects.filter(agree=True, accept='2')
    delete_tut.delete()
    context = {'form': form}
    return render(request, 'my_account_r/account.html', context)


def settings_page(request):
    return render(request, 'my_account_r/settings.html')

def change_data(request):
    obj = get_object_or_404(Client, id=search_id(request))
    form = ClientForm(instance=obj)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'my_account_r/change_user_data.html', context)


def tutoring_order(request):
    res_tut = ReserveTutoring.objects.filter(user=request.user, agree=False)
    b = [i for i in ReserveTutoring.objects.all() if str(i.tutor)==str(request.user) and i.agree==False]
    context = {'res_tut': res_tut, 'b': b}
    return render(request, 'my_account_r/tutoring_orders.html', context)


def detail_tutoring_order(request, id):
    b = ' sadfas'
    obj = get_object_or_404(ReserveTutoring, id=id, tutor=request.user.notice)
    form = ReserveTutoringFormSecond(instance=obj)
    if request.method == 'POST':
        form = ReserveTutoringFormSecond(request.POST, instance=obj)
        if form.is_valid(): 
            b = form.cleaned_data.get('agree')
            if b == False:
                messages.success(request, 'Musisz potwierdzić wybór')
                return HttpResponseRedirect(request.path_info)
            a = form.save()
            return redirect('tutoring_order')
    context = {'form': form, 'obj': obj}
    return render(request, 'my_account_r/tutoring_order_detail.html', context)

  
def all_orders(request):
    form = [i for i in ReserveTutoring.objects.all() if str(i.tutor)==str(request.user) and i.agree==True and i.accept=='1']
    form_two = ReserveTutoring.objects.filter(user=request.user, agree=True)
    context = {'form': form, 'form_two': form_two}

    return render(request, 'my_account_r/all_orders.html', context)

def delete_order(request, id):
    obj =  get_object_or_404(ReserveTutoring, id=id, tutor=request.user.notice)
    email = str(obj.user.client.email)
    if request.method == 'POST':
        obj.delete()
        send_mail(
        'Wiadomość dotycząca twojej lekcji na korki.pl',
        'Korepetytor uznał, że zajęcia się już odbyły. Jeżeli jest to niezgodne z prawdą prosimy skontaktować się z obsługą korki.pl',
        '', # Miejsce na email
        [email],
        fail_silently=False,
        )
        return redirect('all_orders')
    return render(request, 'my_account_r/delete_order.html')


