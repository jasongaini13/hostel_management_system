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
