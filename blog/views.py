from django.shortcuts import get_object_or_404, redirect, render
from admin_panel.decorators import group_required
from tutoring_ads.models import ReserveTutoring
from .forms import BlogEntryForm, EntryCommentsForm, RatingSystemForm
from .models import BlogEntry, EntryComments, RatingSystem
# Create your views here.


@group_required('tutor')
def user_entries(request):
    form = BlogEntry.objects.filter(user=request.user)
    context = {'form': form}
    return render(request, 'blog_r/user_entries.html', context)


@group_required('tutor')
def add_blog_entry(request):
    form = BlogEntryForm
    if request.method == 'POST':
        form = BlogEntryForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user.save()
            return redirect('my_entries')
    context = {'form': form}

    return render(request, 'blog_r/add_entry.html', context)


@group_required('tutor')
def update_entry(request, id):
    obj = get_object_or_404(BlogEntry, id=id, user=request.user)
    form = BlogEntryForm(instance=obj)
    if request.method == 'POST':
        form = BlogEntryForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('my_entries')
    context = {'form': form}
    return render(request, 'blog_r/update_entry.html', context)


@group_required('tutor')
def delete_entry(request, id):
    obj =  get_object_or_404(BlogEntry, id=id)
    if request.method == 'POST':
        obj.delete()
        return redirect('my_entries')
    return render(request, 'blog_r/delete_entry.html')


def all_blog_entries(request):
    form = BlogEntry.objects.all()
    context = {'form': form}
    return render(request, 'base_r/blog.html', context)

def entry_detail(request, id):
    # All entry comments
    com = reversed(EntryComments.objects.all().filter(comment=BlogEntry.objects.get(id=id)))

    article = BlogEntry.objects.get(id=id)
    score = None
    
    num = [i.score for i in RatingSystem.objects.filter(rating=article)]
    avarage = False
    users = None
    if len(num) > 0:
        users = len(num)
        avarage = sum(num)/len(num)
        obj = get_object_or_404(BlogEntry, id=id)
        obj.average_rate = avarage
        obj.save()
    for i in RatingSystem.objects.all():
        if i.user == request.user and i.rating == article:
            score = f'Oceniłeś artykuł na {i.score} gwiazdek'


    rate = RatingSystemForm
    add_com = EntryCommentsForm
    if request.method == 'POST':
        # Add comment
        add_com = EntryCommentsForm(request.POST, request.FILES)
        if add_com.is_valid():
            new_com = add_com.save(commit=False)
            new_com.user = request.user
            new_com.comment = BlogEntry.objects.get(id=id)
            new_com.save()
            return redirect('/blog/artykuł/'+id)
        
        # Rate entry
        rate = RatingSystemForm(request.POST, request.FILES)
        if rate.is_valid():
            r = rate.save(commit=False)
            r.user = request.user
            r.rating = article
            r.save()
            return redirect('/blog/artykuł/'+id)



    form = BlogEntry.objects.get(id=id)
    context = {'form': form, 'com': com, 'add_com': add_com, 'rate': rate, 'score': score, 'avarage': avarage, 'users': users}
    return render(request, 'blog_r/entry_detail.html', context)

