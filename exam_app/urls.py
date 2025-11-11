
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/fill-form/', views.fill_exam_form, name='fill_exam_form'),
    path('student/payment/', views.payment, name='payment'),
    path('student/receipt/<int:form_id>/', views.download_receipt, name='download_receipt'),
    path('student/receipts/', views.receipts, name='receipts'),
    path('student/edit-profile/', views.edit_profile, name='edit_profile'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/register/', views.register_view, name='admin_register'),
    path('admin/approve/<int:form_id>/', views.approve_form, name='approve_form'),
    path('status/<int:form_id>/', views.view_status, name='view_status'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('get-subjects/', views.get_subjects, name='get_subjects'),
    path('extend-session/', views.extend_session, name='extend_session'),
    path('check-username/', views.check_username, name='check_username'),
    path('check-email/', views.check_email, name='check_email'),
]
