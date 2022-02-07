from django.contrib.auth.models import Group
from django.shortcuts import render
from django.http import HttpResponse
from base.forms import ContactForm
from reg_log.views import login_user
from django.contrib.auth.models import User
from blog.models import BlogEntry, RatingSystem
from django.core.mail import EmailMessage, send_mail
# Create your views here.



def home_page_view(request):
    login_user(request)
    admin_entry = [i for i in BlogEntry.objects.all() if str(i.user.groups.get()) == 'admin' and  i.admin_agree == True]


    b = [i.average_rate for i in BlogEntry.objects.all() if i.average_rate != 'False']
    entries = sorted(b)[len(b)-3:]
    high_entry = [i for i in BlogEntry.objects.all() if i.average_rate in entries]

    context = {'admin_entry': admin_entry, 'high_entry': high_entry}

    return render(request, 'base_r/home.html', context)


def contact_form(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            if request.user.is_authenticated:
                email = request.user.client.email
            elif not request.user.is_authenticated:
                email = form.cleaned_data['email']
            email_subject = 'Masz nową wiadomość od klienta od ' + str(email)
            email_message = form.cleaned_data['text']
            send_mail(
            email_subject, 
            email_message,
            email,
            [''], # Miejsce na email
            fail_silently=False
            )
    context = {'form': form}
    return render(request, 'base_r/contact_form.html', context)
