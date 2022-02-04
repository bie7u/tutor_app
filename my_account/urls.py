from django.urls import path

from blog.views import delete_entry
from .import views
from .views import all_orders, delete_order, tutoring_order, detail_tutoring_order

urlpatterns = [
    path('moje_korepetycje/', tutoring_order, name='tutoring_order'),
    path('moje_korepetycje/szczegóły/<id>', detail_tutoring_order, name='detail_order_tutoring'),
    path('moje_korepetycje/wszystkie_lekcje/', all_orders, name='all_orders'),
    path('moje_korepetycje/wszystkie_lekcje/usun/<id>', delete_order, name='delete_order'),
]