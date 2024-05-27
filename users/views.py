from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (
    StudentRegistrationForm, FacultyRegistrationForm, 
    StudentAuthenticationForm, FacultyAuthenticationForm, 
    StudentProfileForm, FacultyProfileForm
)
from .models import StudentProfile, FacultyProfile

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
    student_profile = StudentProfile.objects.get(user=request.user)
    return render(request, 'student_profile.html', {'student_profile': student_profile})

@login_required
def faculty_profile(request):
    faculty_profile = FacultyProfile.objects.get(user=request.user)
    return render(request, 'faculty_profile.html', {'faculty_profile': faculty_profile})

@login_required(login_url='student_login')
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
def notice_board(request):
    return render(request,'noticeboard.html')






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
            return redirect('notice_board')
    else:
        form = NoticeForm()
    return render(request, 'add_notice.html', {'form': form})

@login_required
def edit_notice(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if request.user != notice.posted_by:
        return redirect('notice_board')  # Prevent unauthorized edits
    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            return redirect('notice_board')
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'edit_notice.html', {'form': form})

@login_required
def delete_notice(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if request.user != notice.posted_by:
        return redirect('notice_board')  # Prevent unauthorized deletions
    if request.method == 'POST':
        notice.delete()
        return redirect('notice_board')
    return render(request, 'delete_notice.html', {'notice': notice})
