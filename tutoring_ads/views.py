from django.db.models.query import RawQuerySet
from django.shortcuts import get_object_or_404, redirect, render
from admin_panel.decorators import group_required
from reg_log.models import Client
from .models import Notice
from .forms import NoticeForm,  ReserveTutoringForm
from .decorators import access
# Create your views here.


def tutors_view(request):
    form = Notice.objects.all()
    context = {'form': form}
    return render(request, 'base_r/tutors.html', context)

def detail_tutor_view(request, id):
    form = Notice.objects.get(id=id)
    reserve = ReserveTutoringForm
    if request.method == 'POST':
        reserve = ReserveTutoringForm(request.POST, request.FILES)
        if reserve.is_valid():
            i = reserve.save(commit=False)
            i.user = request.user
            i.tutor = form
            i.save()
            return redirect('/')
    context = {'form': form, 'reserve': reserve}
    return render(request, 'tutoring_ads_r/tutor_detail.html', context)

@group_required('tutor')
def add_notice(request):
    note = Notice.objects.filter(user=request.user)
    form = NoticeForm
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.data = request.user.client
            f.user = request.user
            f.save()
    context = {'form': form, 'note': note}

    return render(request, 'tutoring_ads_r/add_notice.html', context)

@group_required('tutor')
def update_notice(request, id):
    obj = get_object_or_404(Notice, id=id, user=request.user)
    form = NoticeForm(instance=obj)
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('add_notice')
    context = {'form': form}
    return render(request, 'tutoring_ads_r/update_notice.html', context)


@group_required('tutor')
def delete_notice(request, id):
    obj = get_object_or_404(Notice, id=id, user=request.user)
    if request.method == 'POST':
        obj.delete()
        return redirect('add_notice')
    return render(request, 'tutoring_ads_r/delete_notice.html')
