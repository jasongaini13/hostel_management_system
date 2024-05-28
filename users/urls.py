# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('student/register/', views.student_register, name='student_register'),
    path('faculty/register/', views.faculty_register, name='faculty_register'),
    path('student/login/', views.student_login, name='student_login'),
    path('faculty/login/', views.faculty_login, name='faculty_login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('faculty/dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    
    path('logout/', views.logout_view, name='logout'),
    # path('notice_board/', views.notice_list, name='notice_board'),
    # path('notices/add/', views.add_notice, name='add_notice'),
    # path('notices/edit/<int:pk>/', views.edit_notice, name='edit_notice'),
    # path('notices/delete/<int:pk>/', views.delete_notice, name='delete_notice'),
    # path('notices/<int:pk>/', views.notice_detail, name='notice_detail'),
    path('student/profile/', views.student_profile, name='student_profile'),
    path('faculty/profile/', views.faculty_profile, name='faculty_profile'),
    path('update-student-profile/', views.update_student_profile, name='update-student-profile'),
    path('update-faculty-profile/', views.update_faculty_profile, name='update-faculty-profile'),
    # For leave application
    path('apply_leave/', views.apply_leave, name='apply_leave'),
    path('approve_leave/<str:token>/', views.approve_leave, name='approve_leave'),
    path('deny_leave/<str:token>/', views.deny_leave, name='deny_leave'),
    path('leave_success/', views.leave_success, name='leave_success'),
    path('leave_response/', views.leave_response, name='leave_response'),
    #For doctor appointment
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('appointment-success/', views.appointment_success, name='appointment_success'),
    path('appoint-date/<int:appointment_id>/', views.set_appointment_date, name='set_appointment_date'),
    path('appointment-date-success/', views.appointment_date_success, name='appointment_date_success'),
    path('update-student-profile/', views.update_student_profile, name='update-student-profile'),
]
