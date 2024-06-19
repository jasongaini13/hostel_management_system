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
    path('notice_board/', views.notice_list, name='notice_list'),
    path('notices/add/', views.add_notice, name='add_notice'),
    path('notices/edit/<int:pk>/', views.edit_notice, name='edit_notice'),
    path('notices/delete/<int:pk>/', views.delete_notice, name='delete_notice'),
    path('notices/<int:pk>/', views.notice_detail, name='notice_detail'),
    path('student/profile/', views.student_profile, name='student_profile'),
    path('faculty/profile/', views.faculty_profile, name='faculty_profile'),
    path('update-student-profile/', views.update_student_profile, name='update-student-profile'),
    path('update-faculty-profile/', views.update_faculty_profile, name='update-faculty-profile'),
    #leave application
    path('apply_leave/', views.apply_leave, name='apply_leave'),
    path('approve_leave/<str:token>/', views.approve_leave, name='approve_leave'),
    path('deny_leave/<str:token>/', views.deny_leave, name='deny_leave'),
    path('leave_success/', views.leave_success, name='leave_success'),
    path('leave_response/', views.leave_response, name='leave_response'),
    #doctor appointment
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('appointment-success/', views.appointment_success, name='appointment_success'),
    path('appoint-date/<int:appointment_id>/', views.set_appointment_date, name='set_appointment_date'),
    path('appointment-date-success/', views.appointment_date_success, name='appointment_date_success'),
    #notice board
    path('faculty/notices/', views.notice_list, name='notice_list'),
    path('faculty/notice/<int:pk>/', views.notice_detail, name='notice_view'),
    path('student/notices/', views.student_notice_list, name='student_notice_list'),
    path('student/notice/<int:pk>/', views.student_notice_detail, name='student_notice_detail'),
    #complaints
    path('complaints/', views.student_complaints_list, name='student_complaints_list'),
    path('complaints/add/', views.add_complaint, name='add_complaint'),
    path('complaints/delete/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),
    path('faculty/complaints/', views.faculty_complaints_list, name='faculty_complaints_list'),
    path('complaints/<int:complaint_id>/', views.complaint_detail, name='complaint_detail'),
    # For guest room allotment
    path('book-room/', views.book_room, name='book_room'),
    path('booking-confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('manage_rooms/', views.manage_rooms, name='manage_rooms'),
    path('add_room/', views.add_room, name='add_room'),
    path('delete_room/<int:room_id>/', views.delete_room, name='delete_room'),
    path('view_bookings/', views.view_bookings, name='view_bookings'),
    #cloak room allotment
    path('cloak_room/add/', views.add_cloak_room_entry, name='add_cloak_room_entry'),
    path('cloak_room/view/', views.view_cloak_room_entry, name='view_cloak_room_entry'),
    path('cloak_room/settings/', views.manage_cloak_room_settings, name='manage_cloak_room_settings'),
    path('cloak_room/entries/', views.view_all_cloak_room_entries, name='view_all_cloak_room_entries'),
    path('cloak_room/entries/delete/<int:entry_id>/', views.delete_cloak_room_entry, name='delete_cloak_room_entry'),
]

