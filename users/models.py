# users/models.py
from django.contrib.auth.models import User
from django.db import models

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    fullname = models.CharField(max_length=255)
    branch = models.CharField(max_length=100)
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
