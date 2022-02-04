from django.urls import path
from .import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Registriation process
    path('rejestracja_korepetytor/', views.register_tutor, name='register_tutor'),
    path('rejestracja_uczen/', views.register_customer, name='register_customer'),
    path('wylogowywanie/', views.logout_user, name='logout'),
    path('aktywacja/<uidb64>/<token>/', views.activate, name='activate'),
    path('weryfikacja_email/', views.send_mail, name='email_verification'),
    
    # Reset password process
    path("resetowanie_hasła/", views.password_reset_request, name="password_reset"),
    path('resetowanie_hasła/gotowe/', auth_views.PasswordResetDoneView.as_view(template_name='reg_log/change_password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reg_log_r/change_password_r/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/gotowe/', auth_views.PasswordResetCompleteView.as_view(template_name='reg_log_r/change_password_r/password_reset_complete.html'), name='password_reset_complete'),
    path('zmien_hasło/', views.MyPasswordChangeView.as_view(), name='password_change_view'),
    path('zmien_hasło/gotowe/', views.MyPasswordResetDoneView.as_view(), name='password_change_done_view'),

]