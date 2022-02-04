from email import message
from django.http import request
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from blog.models import BlogEntry
from blog.forms import BlogEntryForm, BlogEntrySecond
from django.core.mail import EmailMessage, send_mail

from blog.views import entry_detail
from .decorators import group_required
from tutoring_ads.models import Notice, ReserveTutoring
from blog.models import EntryComments
# Create your views here.

@group_required('admin')
def admin_menu(request):
    return render(request, 'admin_panel_r/admin_menu.html')

@group_required('admin')
def admin_users(request):
    tutors = [tutor for tutor in User.objects.all() if str(tutor.groups.get()) == 'tutor']
    customers = [customer for customer in User.objects.all() if str(customer.groups.get()) == 'customer']
    admins = [admin for admin in User.objects.all() if str(admin.groups.get()) == 'admin']

    context =  {'tutors': tutors, 'customers': customers, 'admins': admins}
    return render(request, 'admin_panel_r/admin_users.html', context)

@group_required('admin')
def admin_tutor_detail(request, id):
    user = User.objects.get(id=id)
    blog = BlogEntry.objects.filter(user=user)
    order = None
    order_accept = None
    if Notice.objects.filter(user=user):
        order = ReserveTutoring.objects.filter(tutor=user.notice, agree=False)
        order_accept = ReserveTutoring.objects.filter(tutor=user.notice, agree=True)
    
    context = {'user': user, 'blog': blog, 'order': order, 'order_accept': order_accept}
    return render(request, 'admin_panel_r/admin_tutor_detail.html', context)

@group_required('admin')
def admin_customer_detail(request, id):
    user = User.objects.get(id=id)

    order = ReserveTutoring.objects.filter(user=user, agree=False)
    order_accept = ReserveTutoring.objects.filter(user=user, agree=True)
    
    context = {'user': user, 'order': order, 'order_accept': order_accept}
    return render(request, 'admin_panel_r/admin_customer_detail.html', context)

@group_required('admin')
def admin_delete_entry(request, id):
    obj = get_object_or_404(BlogEntry, id=id)
    email = str(BlogEntry.objects.get(id=id).user.client.email)
    if request.method == 'POST':
        obj.delete()
        send_mail(
        'Wiadomość dotycząca twojego artykułu na korki.pl',
        'Administrator postanowił usunąć twój artykuł. Skontaktuj się z obsługą aby wyjaśnić sprawę',
        'companybiela@gmail.com',
        [email],
        fail_silently=False,
        )
        return redirect('admin-users')
    return render(request, 'admin_panel_r/admin_delete_entry.html')

@group_required('admin')
def admin_delete_notice(request, id):
    obj = get_object_or_404(Notice, id=id)
    email = str(obj.user.client.email)
    email_customer = []
    form = ReserveTutoring.objects.filter(tutor=obj)
    for i in form:
        email_customer.append(str(i.user.client.email))
    if request.method == 'POST':
        obj.delete()
        send_mail(
        'Wiadomość dotycząca twojego artykułu na korki.pl',
        'Administrator postanowił usunąć twoje ogłoszenie. Skontaktuj się z obsługą aby wyjaśnić sprawę',
        'companybiela@gmail.com',
        [email],
        fail_silently=False,
        )
        send_mail(
        'Wiadomość dotycząca twojej lekcji na korki.pl',
        'Z przykrością informujemy, że twoje korepetycje nie odbędą się. Pozdrawiamy korki.pl',
        'companybiela@gmail.com',
        email_customer,
        fail_silently=False,
        )
        return redirect('admin-users')
    return render(request, 'admin_panel_r/admin_delete_notice.html')


@group_required('admin')
def admin_add_blog_entry(request):
    form = [i for i in BlogEntry.objects.all() if str(i.user.groups.get()) == 'admin']
    home_entry = [i for i in BlogEntry.objects.all() if str(i.user.groups.get()) == 'admin' and i.admin_agree==True]
    form_two = False
    if len(home_entry) == 3:
        form_two = True

    context = {'form': form, 'form_two': form_two}
    return render(request, 'admin_panel_r/admin_blog.html', context)


@group_required('admin')
def add_blog_entry_admin(request):
    form = BlogEntryForm
    if request.method == 'POST':
        form = BlogEntryForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user.save()
            return redirect('admin-add-blog-entry')
    context = {'form': form}
    return render(request, 'admin_panel_r/admin_add_entry.html', context)


@group_required('admin')
def admin_update_blog_entry(request, id):
    obj = get_object_or_404(BlogEntry, id=id, user=request.user)
    form = BlogEntryForm(instance=obj)
    if request.method == 'POST':
        form = BlogEntryForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('admin-add-blog-entry')
    context = {'form': form}
    return render(request, 'admin_panel_r/admin_update_entry.html', context)


@group_required('admin')
def admin_delete_blog_entry(request, id):
    obj =  get_object_or_404(BlogEntry, id=id)
    if request.method == 'POST':
        obj.delete()
        return redirect('admin-add-blog-entry')
    return render(request, 'admin_panel_r/admin_delete_entry.html')

@group_required('admin')
def admin_publish_article(request, id):
    obj = get_object_or_404(BlogEntry, id=id)
    form = BlogEntrySecond(instance=obj)
    if request.method == 'POST':
        form = BlogEntrySecond(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('admin-add-blog-entry')
    context = {'form': form}    
    return render(request, 'admin_panel_r/confirm_entry.html', context)


@group_required('admin')
def admin_withdraw_article(request, id):
    obj = get_object_or_404(BlogEntry, id=id)
    if request.method == 'POST':
        obj.admin_agree = False
        obj.save()
        return redirect('admin-add-blog-entry')
    return render(request, 'admin_panel_r/withdraw_article.html')

@group_required('admin')
def admin_delete_com(request, id):
    obj = get_object_or_404(EntryComments, id=id)
    if request.method == 'POST':
        obj.delete()
        return entry_detail(request, id=obj.comment.id)
    return render(request, 'admin_panel_r/admin_delete_com.html')

@group_required('admin')
def admin_delete_user(request, id):
    obj = get_object_or_404(User, id=id)
    email = str(obj.client.email)
    if request.method == 'POST':
        send_mail(
        'Twoje konto na korki.pl',
        'Administrator postanowił usunąć twoje konto. Skontaktuj się z obsługą aby wyjaśnić sprawę',
        'companybiela@gmail.com',
        [email],
        fail_silently=False,
        )
        obj.delete()
        return redirect('admin-users')
    return render(request, 'admin_panel_r/admin_delete_user.html')