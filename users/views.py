from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (
    StudentRegistrationForm, FacultyRegistrationForm, 
    StudentAuthenticationForm, FacultyAuthenticationForm, 
    StudentProfileForm, FacultyProfileForm , LeaveApplicationForm , 
    DoctorAppointmentForm ,AppointmentDateForm
)
from .models import StudentProfile, FacultyProfile, LeaveApplication ,DoctorAppointment
from django.core.mail import send_mail,EmailMessage, EmailMultiAlternatives
from datetime import datetime, timedelta
from django.conf import settings
import uuid

def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Ensure StudentProfile is created
            student_profile, created = StudentProfile.objects.get_or_create(user=user, defaults={'email': user.email})
            login(request, user)
            return redirect('student_dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'auth/student_register.html', {'form': form})

def faculty_register(request):
    if request.method == 'POST':
        form = FacultyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Ensure FacultyProfile is created
            faculty_profile, created = FacultyProfile.objects.get_or_create(user=user, defaults={'email': user.email})
            login(request, user)
            return redirect('faculty_login')
    else:
        form = FacultyRegistrationForm()
    return render(request, 'auth/faculty_register.html', {'form': form})

def student_dashboard(request):
    return render(request, 'student_dashboard.html')

def faculty_dashboard(request):
    return render(request, 'faculty_dashboard.html')

def student_login(request):
    if request.method == 'POST':
        form = StudentAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('student_dashboard')
    else:
        form = StudentAuthenticationForm()
    return render(request, 'auth/student_login.html', {'form': form})

def faculty_login(request):
    if request.method == 'POST':
        form = FacultyAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('faculty_dashboard')
    else:
        form = FacultyAuthenticationForm()
    return render(request, 'auth/faculty_login.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('student_login')
@login_required
def student_profile(request):
    if hasattr(request.user, 'studentprofile'):
        student_profile = request.user.studentprofile
        return render(request, 'student_profile.html', {'student_profile': student_profile})
    else:
        messages.error(request, "You are not authorized to view this page.")
        return redirect(request, 'home.html')
@login_required
def faculty_profile(request):
    if hasattr(request.user, 'facultyprofile'):
        faculty_profile = request.user.facultyprofile
        return render(request, 'faculty_profile.html', {'faculty_profile': faculty_profile})
    else:
        messages.error(request, "You are not authorized to view this page.")
        return redirect(request, 'home.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import StudentProfileForm
from .models import StudentProfile

@login_required
def update_student_profile(request):
    student_profile = StudentProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=student_profile)
        if form.is_valid():
            form.save()
            return redirect('student_dashboard')  # Redirect to student dashboard after profile update
    else:
        form = StudentProfileForm(instance=student_profile)
    return render(request, 'update_student_profile.html', {'form': form})


@login_required
def update_faculty_profile(request):
    faculty_profile = FacultyProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = FacultyProfileForm(request.POST, request.FILES, instance=faculty_profile)
        if form.is_valid():
            form.save()
            return redirect('faculty_dashboard')
    else:
        form = FacultyProfileForm(instance=faculty_profile)
    return render(request, 'update_faculty_profile.html', {'form': form})

@login_required
def view_student_profile(request):
    student_profile = StudentProfile.objects.get(user=request.user)
    return render(request, 'student_profile.html', {'profile': student_profile})

@login_required
def view_faculty_profile(request):
    faculty_profile = FacultyProfile.objects.get(user=request.user)
    return render(request, 'faculty_profile.html', {'profile': faculty_profile})
# def notice_board(request):
#     return render(request,'noticeboard.html')






# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
# from .models import Notice
# from .forms import NoticeForm

# @login_required
# def notice_list(request):
#     query = request.GET.get('q')
#     if query:
#         notices = Notice.objects.filter(Q(subject__icontains=query) | Q(posted_by__username__icontains=query)).order_by('-date_posted')
#     else:
#         notices = Notice.objects.all().order_by('-date_posted')
#     return render(request, 'noticeboard.html', {'notices': notices})

# @login_required
# def notice_detail(request, pk):
#     notice = get_object_or_404(Notice, pk=pk)
#     return render(request, 'notice_detail.html', {'notice': notice})

# @login_required
# def add_notice(request):
#     if request.method == 'POST':
#         form = NoticeForm(request.POST)
#         if form.is_valid():
#             notice = form.save(commit=False)
#             notice.posted_by = request.user
#             notice.date_posted = timezone.now()
#             notice.save()
#             return redirect('notice_board')
#     else:
#         form = NoticeForm()
#     return render(request, 'add_notice.html', {'form': form})

# @login_required
# def edit_notice(request, pk):
#     notice = get_object_or_404(Notice, pk=pk)
#     if request.user != notice.posted_by:
#         return redirect('notice_board')  # Prevent unauthorized edits
#     if request.method == 'POST':
#         form = NoticeForm(request.POST, instance=notice)
#         if form.is_valid():
#             form.save()
#             return redirect('notice_board')
#     else:
#         form = NoticeForm(instance=notice)
#     return render(request, 'edit_notice.html', {'form': form})

# @login_required
# def delete_notice(request, pk):
#     notice = get_object_or_404(Notice, pk=pk)
#     if request.user != notice.posted_by:
#         return redirect('notice_board')  # Prevent unauthorized deletions
#     if request.method == 'POST':
#         notice.delete()
#         return redirect('notice_board')
#     return render(request, 'delete_notice.html', {'notice': notice})

def apply_leave(request):
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            leave_application = form.save(commit=False)
            leave_application.student = request.user
            leave_application.token = str(uuid.uuid4())
            leave_application.save()
            send_approval_email(leave_application)
            return redirect('leave_success')
    else:
        form = LeaveApplicationForm()
    return render(request, 'leave_app/apply_leave.html', {'form': form})

def send_approval_email(leave_application):
    student_email = "leave_application.student.email"
    approval_url = f'{settings.SITE_URL}/approve_leave/{leave_application.token}/'
    denial_url = f'{settings.SITE_URL}/deny_leave/{leave_application.token}/'
    subject = 'Leave Application Approval Needed'
    text_content = f'''
    A student has requested leave. Please review the request:

    Student: {leave_application.student}
    Reason: {leave_application.reason}
    Start Date: {leave_application.start_date}
    End Date: {leave_application.end_date}

    Click this URL for approving the Student's Leave Permission: {approval_url}
    Click this URL for denying the Student's Leave Permission: {denial_url}
    '''
    html_content = f'''
    <p>A student has requested leave. Please review the request:</p>
    <p><strong>Student:</strong> {leave_application.student}</p>
    <p><strong>Reason:</strong> {leave_application.reason}</p>
    <p><strong>Start Date:</strong> {leave_application.start_date}</p>
    <p><strong>End Date:</strong> {leave_application.end_date}</p>
    <p>
        <a href="{approval_url}">Click this URL for approving the Student's Leave Permission</a><br>
        <a href="{denial_url}">Click this URL for denying the Student's Leave Permission</a>
    </p>
    '''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['chiefwardena@gmail.com']  
    
    msg = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def process_leave_request(request, token, action):
    leave_application = get_object_or_404(LeaveApplication, token=token)
    if action == 'approve':
        leave_application.status = 'approved'
        leave_application.approval_date = datetime.now()
        leave_application.save()
        send_response_email(leave_application, 'approved')
    elif action == 'deny':
        leave_application.status = 'denied'
        leave_application.save()
        send_response_email(leave_application, 'denied')
    return redirect('leave_response')

def send_response_email(leave_application, status):
    student_email = leave_application.student.email
    subject = 'Leave Application Status'
    
    # Calculate the expiration date
    approval_date = datetime.now()
    expiration_date = approval_date + timedelta(days=1)
    
    if status == 'approved':
        text_content = (f'Your leave application has been approved.\n\n'
                        f'Please note that this approval is valid only until {expiration_date.strftime("%Y-%m-%d %H:%M:%S")}. '
                        'After this date and time, the leave will be automatically disapproved.')
        
        html_content = (f'<p>Your leave application has been <strong>approved</strong>.</p>'
                        f'<p>Please note that this approval is valid only until <strong>{expiration_date.strftime("%Y-%m-%d %H:%M:%S")}</strong>. '
                        'After this date and time, the leave will be automatically disapproved.</p>')
    else:
        text_content = f'Your leave application has been {status}.'
        
        html_content = f'<p>Your leave application has been <strong>{status}</strong>.</p>'
    
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [student_email]

    msg = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def approve_leave(request, token):
    return process_leave_request(request, token, 'approve')

def deny_leave(request, token):
    return process_leave_request(request, token, 'deny')

def leave_success(request):
    return render(request, 'leave_app/leave_success.html')

def leave_response(request):
    return render(request, 'leave_app/leave_response.html')


@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = DoctorAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.student = request.user
            appointment.save()

            # Prepare email
            subject = 'New Doctor Appointment Request'
            text_content = f"Student ID: {appointment.student.username}\n" \
                           f"Category of Issue: {appointment.category_of_issue}\n" \
                           f"Description: {appointment.description}"

            html_content = f"""
                <p><strong>Student ID:</strong> {appointment.student.username}</p>
                <p><strong>Category of Issue:</strong> {appointment.category_of_issue}</p>
                <p><strong>Description:</strong> {appointment.description}</p>
                <p><a href="{request.build_absolute_uri('/appoint-date/')}{appointment.id}/">Set Appointment Date</a></p>
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['chiefwardena@gmail.com']  

            msg = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return redirect('appointment_success')
    else:
        form = DoctorAppointmentForm()
    return render(request, 'doctor_appointment/book_appointment.html', {'form': form})

def appointment_success(request):
    return render(request, 'doctor_appointment/appointment_success.html')

def set_appointment_date(request, appointment_id):
    appointment = get_object_or_404(DoctorAppointment, id=appointment_id)
    if request.method == 'POST':
        form = AppointmentDateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            appointment_date = f"{date} {time}"
            appointment.appointment_date = appointment_date
            appointment.save()

            # Send confirmation email to student
            subject = 'Doctor Appointment Scheduled'
            text_content = f"Your doctor appointment date has been scheduled on {appointment_date}."
            html_content = f"""
                <p>Your doctor appointment date has been scheduled for <strong>{appointment_date}</strong>.</p>
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [appointment.student.email]

            msg = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return redirect('appointment_date_success')
    else:
        form = AppointmentDateForm()
    return render(request, 'doctor_appointment/set_appointment_date.html', {'form': form, 'appointment': appointment})
def appointment_date_success(request):
    return render(request, 'doctor_appointment/appointment_date_success.html')