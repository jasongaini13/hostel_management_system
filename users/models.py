from django.contrib.auth.models import User
from django.db import models



class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    fullname = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)  # ForeignKey relationship with Branch
    year = models.CharField(max_length=10)
    mobile_no = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

class FacultyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    fullname = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=15)
    short_intro = models.TextField()

    def __str__(self):
        return self.user.username

class LeaveApplication(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied')
    ], default='pending')
    token = models.CharField(max_length=100, unique=True, null=True, blank=True)  # For email links

    def __str__(self):
        return f'{self.student.username} - {self.status}'

class DoctorAppointment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    category_of_issue = models.CharField(max_length=100)
    description = models.TextField()
    appointment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} - {self.category_of_issue}"


# models.py
from django.contrib.auth.models import User
from django.db import models

class Notice(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


# users/models.py
from django.db import models
from django.contrib.auth.models import User

class Complaint(models.Model):
    student_id = models.CharField(max_length=20)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_id}: {self.description[:20]}..."

