from django.urls import path
from .import views


urlpatterns = [
    path('moje_konto/moje_wpisy/', views.user_entries, name='my_entries'),
    path('moje_konto/moje_wpisy/dodaj_wpis/', views.add_blog_entry, name='add_entry'),
    path('moje_konto/moje_wpisy/zaktualizuj/<id>/', views.update_entry, name='update_entry'),
    path('moje_konto/moje_wpisy/usun/<id>', views.delete_entry, name='delete_entry'),
]