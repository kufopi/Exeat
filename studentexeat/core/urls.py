from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


from .views import custom_login_view



urlpatterns = [
    path('hod_dashboard/', views.hod_dashboard, name='hod_dashboard'),
    path("studentaffairs/", views.student_affairs_dashboard, name="student_affairs_dashboard"),
    path('female_hall_warden_dashboard/', views.female_hall_warden_dashboard, name='female_hall_warden_dashboard'),
    path('male_hall_warden_dashboard/', views.male_hall_warden_dashboard, name='male_hall_warden_dashboard'),
    path('login/', custom_login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), 
    path('', views.home, name='home'),
    path('create_exeat_request/', views.create_exeat_request, name='create_exeat_request'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path("profile/", views.update_profile, name="profile"),
    path('approve-exeat-request/<int:request_id>/', views.approve_exeat_request, name='approve_exeat_request'), 
    path('reject-exeat-request/<int:request_id>/', views.reject_exeat_request, name='reject_exeat_request'),
    path('approve-student-affairs-exeat-request/<int:request_id>/', views.approve_student_affairs_exeat_request, name='approve_student_affairs_exeat_request'), 
    path('reject-student-affairs-exeat-request/<int:request_id>/', views.reject_student_affairs_exeat_request, name='reject_student_affairs_exeat_request'),
    path('approve-exeat-request-female-warden/<int:request_id>/', views.approve_exeat_request_female_warden, name='approve_exeat_request_female_warden'), 
    path('reject-exeat-request-female-warden/<int:request_id>/', views.reject_exeat_request_female_warden, name='reject_exeat_request_female_warden'), 
    path('approve-exeat-request-male-warden/<int:request_id>/', views.approve_exeat_request_male_warden, name='approve_exeat_request_male_warden'), 
    path('reject-exeat-request-male-warden/<int:request_id>/', views.reject_exeat_request_male_warden, name='reject_exeat_request_male_warden'),
    path('create-emergency-exeat-by-officer/', views.create_emergency_exeat_by_officer, name='create_emergency_exeat_by_officer'),
    path('pending-returns-female-warden/', views.pending_returns_female_warden, name='pending_returns_female_warden'), 
    path('pending-returns-male-warden/', views.pending_returns_male_warden, name='pending_returns_male_warden'), 
    path('mark-return-female-warden/<int:request_id>/', views.mark_return_female_warden, name='mark_return_female_warden'), 
    path('mark-return-male-warden/<int:request_id>/', views.mark_return_male_warden, name='mark_return_male_warden'),
    
]+static(settings.STATIC_URL,document_root=settings.STATICFILES_DIR)
