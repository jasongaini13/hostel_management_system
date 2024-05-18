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
