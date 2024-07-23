
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (
    StudentRegistrationForm, FacultyRegistrationForm, 
    StudentAuthenticationForm, FacultyAuthenticationForm, 
    StudentProfileForm, FacultyProfileForm , LeaveApplicationForm , 
    DoctorAppointmentForm ,AppointmentDateForm,BookingForm,RoomForm,
    CloakRoomEntryForm,CloakRoomSettingsForm,
)
from .models import (StudentProfile, FacultyProfile, LeaveApplication ,
    DoctorAppointment,Room,Booking ,CloakRoomEntry, CloakRoomSettings)
from django.core.mail import send_mail,EmailMessage, EmailMultiAlternatives
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from django.db import transaction
import uuid
from django.views.decorators.csrf import csrf_protect

from users import models

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

@csrf_protect
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

@csrf_protect
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
@login_required
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
@login_required
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

@login_required
def approve_leave(request, token):
    return process_leave_request(request, token, 'approve')
@login_required
def deny_leave(request, token):
    return process_leave_request(request, token, 'deny')
@login_required
def leave_success(request):
    return render(request, 'leave_app/leave_success.html')
@login_required
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



# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from .models import Notice
from .forms import NoticeForm

@login_required
def notice_list(request):
    query = request.GET.get('q')
    if query:
        notices = Notice.objects.filter(Q(subject__icontains=query) | Q(posted_by__username__icontains=query)).order_by('-date_posted')
    else:
        notices = Notice.objects.all().order_by('-date_posted')
    return render(request, 'noticeboard.html', {'notices': notices})

@login_required
def notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    return render(request, 'notice_detail.html', {'notice': notice})

@login_required
def add_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.posted_by = request.user
            notice.date_posted = timezone.now()
            notice.save()
            return redirect('notice_list')
    else:
        form = NoticeForm()
    return render(request, 'add_notice.html', {'form': form})

@login_required
def edit_notice(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if request.user != notice.posted_by:
        return redirect('notice_list')  # Prevent unauthorized edits
    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            return redirect('notice_list')
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'edit_notice.html', {'form': form})

@login_required
def delete_notice(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if request.user != notice.posted_by:
        return redirect('notice_list')  # Prevent unauthorized deletions
    if request.method == 'POST':
        notice.delete()
        return redirect('notice_list')
    return render(request, 'delete_notice.html', {'notice': notice})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notice

@login_required
def student_notice_list(request):
    notices = Notice.objects.all()
    query = request.GET.get('q')
    if query:
        notices = Notice.objects.filter(Q(subject__icontains=query) | Q(posted_by__username__icontains=query)).order_by('-date_posted')
    else:
        notices = Notice.objects.all().order_by('-date_posted')
    return render(request, 'student_noticeboard.html', {'notices': notices})

from django.shortcuts import render, get_object_or_404
from .models import Notice

def student_notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    return render(request, 'student_notice_detail.html', {'notice': notice})






from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ComplaintForm
from .models import Complaint

@login_required
def add_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            user = request.user
            complaint.student_id = user.username
            complaint.save()
            return redirect('student_complaints_list')
    else:
        form = ComplaintForm()
    return render(request, 'add_complaint.html', {'form': form})

@login_required
def student_complaints_list(request):
    user_id = request.user.username
    search_query = request.GET.get('search_query', '')
    complaints = Complaint.objects.filter(student_id=user_id).order_by('-date_created')
    if search_query:
        complaints = complaints.filter(description__icontains=search_query) | complaints.filter(student_id__icontains=search_query)
    return render(request, 'student_complaints_list.html', {'complaints': complaints, 'user_id': user_id})





# Add other views for editing and deleting complaints as needed
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Complaint

def faculty_complaints_list(request):
    query = request.GET.get('search_query')
    if query:
        complaints = Complaint.objects.filter(
            Q(student_id__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        complaints = Complaint.objects.all().order_by('-date_created')  # Newest complaints first

    context = {
        'complaints': complaints,
    }
    return render(request, 'faculty_complaints_list.html', context)







# @login_required
# def edit_complaint(request, complaint_id):
#     complaint = get_object_or_404(Complaint, id=complaint_id, student=request.user)
#     if request.method == 'POST':
#         form = ComplaintForm(request.POST, instance=complaint)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Complaint updated successfully.')
#             return redirect('student_complaints_list')
#     else:
#         form = ComplaintForm(instance=complaint)
#     return render(request, 'edit_complaint.html', {'form': form})

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required
from .models import Complaint

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Complaint, StudentProfile
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Complaint, StudentProfile,Room,Booking
from django.contrib.auth.decorators import login_required

@login_required
def delete_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    try:
        student_profile = StudentProfile.objects.get(user__username=complaint.student_id)
        student_email = student_profile.email  # Correct attribute
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('faculty_complaints_list')

    complaint_description = complaint.description  # Save description before deletion
    complaint.delete()
    messages.success(request, 'Complaint deleted successfully.')
    
    send_mail(
        'Complaint Solved',
        f'Your complaint "{complaint_description}" has been resolved and deleted by the faculty.',
        settings.DEFAULT_FROM_EMAIL,
        [student_email],
    )

    return redirect('faculty_complaints_list')





from django.shortcuts import render, get_object_or_404
from .models import Complaint

def complaint_detail(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    return render(request, 'complaint_detail.html', {'complaint': complaint})

# For guest room
@login_required
def book_room(request):
    update_room_availability()

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.student = request.user
            room = form.cleaned_data['room']
            room.is_available = False
            room.save()
            booking.save()
            send_confirmation_email(request.user.email, booking)
            return redirect('booking_confirmation')
    else:
        form = BookingForm()
    return render(request, 'guest_room/book_room.html', {'form': form})

def update_room_availability():
    bookings = Booking.objects.filter(check_out_date__lt=timezone.now())
    for booking in bookings:
        if not booking.room.is_available:
            booking.room.is_available = True
            booking.room.save()
def send_confirmation_email(email, booking):
    subject = 'Room Booking Confirmation'
    text_content = (f"Dear {booking.student.username},\n\n"
               f"Your booking for {booking.guest_name} has been confirmed.\n"
               f"Room Allotted: {booking.room.room_number}\n"
               f"Check-in Date: {booking.check_in_date}\n"
               f"Check-out Date: {booking.check_out_date}\n\n"
               f"Please pay the charges at the accounts office.\n\n"
               f"Thank you!")

    html_content=f"""
                <p>Dear <strong>{booking.student.username}</strong> </p>
                <p>Your booking for <strong>{booking.guest_name}</strong> has been confirmed.</p>
                <p>Room Allotted: <strong>{booking.room.room_number}</strong></p>
                <p>Check-in Date: <strong>{booking.check_in_date}</strong></p>
                <p>Check-out Date: <strong>{booking.check_out_date}</strong></p>
                <p>Please pay the charges at the accounts office.</p>
                <p>Thank You!</p>
            """
    email_from = settings.EMAIL_HOST_USER

    msg = EmailMultiAlternatives(subject, text_content, email_from, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
def booking_confirmation(request):
    return render(request,'guest_room/booking_confirmation.html')

@login_required
# @permission_required('users.can_manage_rooms', raise_exception=True)
def manage_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'guest_room/manage_rooms.html', {'rooms': rooms})

@login_required
# @permission_required('users.can_manage_rooms', raise_exception=True)
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room added successfully.')
            return redirect('manage_rooms')
    else:
        form = RoomForm()
    return render(request, 'guest_room/add_room.html', {'form': form})

@login_required
# @permission_required('users.can_manage_rooms', raise_exception=True)
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.delete()
    messages.success(request, 'Room deleted successfully.')
    return redirect('manage_rooms')

@login_required
# @permission_required('users.can_view_bookings', raise_exception=True)
def view_bookings(request):
    current_date = timezone.now().date()
    bookings = Booking.objects.filter(check_out_date__lt=current_date)
    
    # Delete bookings whose check-out date has passed
    for booking in bookings:
        booking.delete()
    
    # Retrieve all remaining bookings after deletion
    bookings = Booking.objects.all()

    return render(request, 'guest_room/view_bookings.html', {'bookings': bookings})


#cloak room allotment
@login_required
# @user_passes_test(is_student)
def add_cloak_room_entry(request):
    settings = CloakRoomSettings.objects.first()
    if not settings or not settings.is_enabled:
        return render(request, 'cloak_room/disabled.html')
    
    existing_entry = CloakRoomEntry.objects.filter(student=request.user).first()
    if existing_entry:
        # messages.error(request, 'You have already submitted an entry. Please wait until the cloak room is disabled to submit again.')
        return redirect('view_cloak_room_entry')


    if request.method == 'POST':
        form = CloakRoomEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.student = request.user
            entry.save()
            # messages.success(request, 'Cloak room entry added successfully.')
            return redirect('view_cloak_room_entry')
    else:
        form = CloakRoomEntryForm()
    return render(request, 'cloak_room/add_cloak_room_entry.html', {'form': form})

@login_required
# @user_passes_test(is_student)
def view_cloak_room_entry(request):
    entries = CloakRoomEntry.objects.filter(student=request.user)
    return render(request, 'cloak_room/view_cloak_room_entry.html', {'entries': entries})



@login_required
def manage_cloak_room_settings(request):
    settings, created = CloakRoomSettings.objects.get_or_create(id=1)
    previous_state = settings.is_enabled
    
    if request.method == 'POST':
        form = CloakRoomSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            settings = form.save(commit=False)
            new_state = settings.is_enabled
            with transaction.atomic():
                if previous_state == False and new_state == True:
                    # Delete all existing entries
                    CloakRoomEntry.objects.all().delete()
                settings.save()
            # messages.success(request, 'Cloak room settings updated successfully.')
            if settings.is_enabled:
                return redirect('view_all_cloak_room_entries')
            else:
                return redirect('manage_cloak_room_settings')
    else:
        form = CloakRoomSettingsForm(instance=settings)
    
    return render(request, 'cloak_room/manage_cloak_room_settings.html', {'form': form})

@login_required
# @user_passes_test(is_faculty)
def view_all_cloak_room_entries(request):
    query = request.GET.get('q')
    if query:
        entries = CloakRoomEntry.objects.filter(Q(student__username__icontains=query)
                                              | Q(items__icontains=query)
                                              | Q(date_time_stored__icontains=query))
    else:
        entries = CloakRoomEntry.objects.all()
    return render(request, 'cloak_room/view_all_cloak_room_entries.html', {'entries': entries})

@login_required
# @user_passes_test(is_faculty)
def delete_cloak_room_entry(request, entry_id):
    entry = get_object_or_404(CloakRoomEntry, id=entry_id)
    entry.delete()
    # messages.success(request, 'Cloak room entry deleted successfully.')
    return redirect('view_all_cloak_room_entries')



    
def mess(request):
    return render(request, 'mess.html')

def laundry(request):
    return render(request, 'laundry.html')
