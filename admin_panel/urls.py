from django.urls import path
from .import views


urlpatterns = [
    path('admin-panel/', views.admin_menu, name='admin-panel'),
    path('admin-panel/użytkownicy', views.admin_users, name='admin-users'),

    path('admin-panel/użytkownicy/usun_użytkownika/<id>', views.admin_delete_user, name='admin-delete-user'),

    path('admin-panel/użytkownicy/korepetytor/<id>', views.admin_tutor_detail, name='admin-tutor-detail'),
    path('admin-panel/użytkownicy/uczen/<id>', views.admin_customer_detail, name='admin-customer-detail'),
    path('admin-panel/użytkownicy/korepetytor/usun/<id>', views.admin_delete_entry, name='admin-delete-entry'),
    path('admin-panel/użytkownicy/korepetytor/usun-ogloszenie/<id>', views.admin_delete_notice, name='admin-delete-notice'),
    path('admin-panel/admin-wpisy/', views.admin_add_blog_entry, name='admin-add-blog-entry'),
    path('admin-panel/admin-wpisy/dodaj_na_glowna/<id>', views.admin_publish_article, name='admin-publish-article'),
    path('admin-panel/admin-wpisy/zdejmij_z_glownej/<id>', views.admin_withdraw_article, name='admin-withdraw-article'),

    path('admin-panel/admin-wpisy/zaktualizuj/<id>/', views.admin_update_blog_entry, name='admin-update-entry'),
    path('admin-panel/admin-wpisy/usun/<id>', views.admin_delete_blog_entry, name='admin-delete-entry'),
    path('admin-panel/admin-wpisy/dodaj_wpis/', views.add_blog_entry_admin, name='add-entry-admin'),
    path('admin-panel/usun_komentarz/<id>', views.admin_delete_com, name='admin-delete-com'),
]