from django.urls import path
from .import views
from my_account.views import my_account_page, settings_page, change_data
from blog.views import all_blog_entries, entry_detail
from tutoring_ads.views import tutors_view, detail_tutor_view

urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('moje_konto/', my_account_page, name='account'),
    path('ustawienia/', settings_page, name='settings'),
    path('ustawienia/zmien_dane/', change_data, name='change_user_data'),
    path('blog/', all_blog_entries, name='all_blog_entries'),
    path('blog/artykuł/<id>', entry_detail, name='entry_detail'),
    path('korepetytorzy/', tutors_view, name='tutors'),
    path('korepetytorzy/wpis/<id>', detail_tutor_view, name='detail_tutor_view'),
    path('kontakt/', views.contact_form, name='contact-form')
]