from django.urls import path
from . import views

urlpatterns = [
    path('student/register/', views.student_register, name='student_register'),
    path('', views.home, name='home'),
    path('faculty/register/', views.faculty_register, name='faculty_register'),
    path('student/login/', views.student_login, name='student_login'),
    path('faculty/login/', views.faculty_login, name='faculty_login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('faculty/dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    # path('profiles/', views.profiles, name='profile'),

    path('student/profile/', views.student_profile, name='student_profile'),
    path('faculty/profile/', views.faculty_profile, name='faculty_profile'),

    path('update-student-profile/', views.update_student_profile, name='update-student-profile'),
    path('update-faculty-profile/', views.update_faculty_profile, name='update-faculty-profile'),
]




