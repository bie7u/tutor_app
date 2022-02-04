from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.models import Group
from django.core.checks import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.http import  HttpResponse
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
#
from .models import *
from .forms import *
#
from django.core.mail import EmailMessage, send_mail
#
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
#
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.views import PasswordChangeView, PasswordResetDoneView
from django.urls.base import reverse_lazy
#
# Create your views here.




# Send email verification
def send_mail(request, user, form):
    current_site = get_current_site(request) 
    mail_subject = 'Aktywuj swoje konto na korki.pl'
    message = render_to_string('reg_log_r/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
        })
    to_email = form.cleaned_data.get('email')
    email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
    email.send()


# Activate method (email verification)
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return render(request, 'reg_log_r/email_verification_done.html')
    else:
        return HttpResponse('Link aktywacyjny jest nieaktywny!')

# Register Customer
def register_customer(request):
    form = CreateCustomerForm
    all_emails = [i.email for i in Client.objects.all()]
    if request.method == 'POST':
        form = CreateCustomerForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data.get('email') in all_emails:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                
                group = Group.objects.get(name='customer')
                user.groups.add(group)
                Client.objects.create(
                    user = user,
                    first_name = form.cleaned_data.get('first_name'),
                    email = form.cleaned_data.get('email'),
                )
                send_mail(request, user, form)
                context = {'email': form.cleaned_data.get('email')}
                return render(request, 'reg_log_r/email_verification.html', context)
            else:
                messages.success(request, 'Email znajduje sie już w naszej bazie')
                return redirect('register_customer')

    context = {'form': form}
    return render(request, 'reg_log_r/register_customer.html', context)


# Register tutor
def register_tutor(request):
    form  = CreateTutorForm
    all_emails = [i.email for i in Client.objects.all()]
    if request.method == 'POST':
        form = CreateTutorForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data.get('email') in all_emails:
                user = form.save()
                
                group = Group.objects.get(name='tutor')
                user.groups.add(group)

                Client.objects.create(
                    user = user,
                    first_name = form.cleaned_data.get('first_name'),
                    last_name = form.cleaned_data.get('last_name'),
                    email = form.cleaned_data.get('email')
                )
                send_mail(request, user, form)
                context = {'email': form.cleaned_data.get('email')}
                return render(request, 'reg_log_r/email_verification.html', context)
            else:
                print('sth')
                messages.success(request, 'Email znajduje sie już w naszej bazie')
                return redirect('register_tutor')
    context = {'form': form}
    return render(request, 'reg_log_r/register_tutor.html', context)

# Function responsible for login
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponse('dasfas')

# Function responsible  for logout
def logout_user(request):
    logout(request)
    return redirect('home') 


# Reset and change password
def password_reset_request(request):

    def failed_email():
        messages.success(request, 'Błędny email')
        return redirect('password_reset')

    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    current_site = get_current_site(request) 
                    subject = "Password Reset Requested"
                    email_template_name = "reg_log_r/change_password_r/password_reset_email.txt"
                    c = {
                    'for': associated_users[0],
                    "email":user.email,
                    'domain':current_site.name,
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    reset_email = EmailMessage(subject, email, 'companybiela@gmail.com' , [user.email])
                    reset_email.send(fail_silently=False)

                return render(request, 'reg_log_r/change_password_r/password_wait.html') #Pamietaj 

            else:
                return failed_email()
        else:
            return failed_email()
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="reg_log_r/change_password_r/password_reset.html", context={"password_reset_form":password_reset_form})

class MyPasswordChangeView(PasswordChangeView):
    template_name = 'reg_log_r/change_password_r/password_change.html'
    success_url = reverse_lazy('password_change_done_view')

class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'reg_log/change_password/password_reset_done.html'



