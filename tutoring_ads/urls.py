from django.urls import path
from .import views


urlpatterns = [
    path('moje_konto/dodaj_ogłoszenie', views.add_notice, name='add_notice'),
    path('moje_konto/dodaj_ogłoszenie/zaktualizuj/<id>', views.update_notice, name='update_notice'),
    path('moje_konto/dodaj_ogłoszenie/usun/<id>', views.delete_notice, name='delete_notice'),
]