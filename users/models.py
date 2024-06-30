from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


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

from django.contrib.auth.models import User
from django.db import models

class Notice(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

from django.db import models
from django.contrib.auth.models import User

class Complaint(models.Model):
    student_id = models.CharField(max_length=20)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_id}: {self.description[:20]}..."


#guest room allotment
class Room(models.Model):
    room_number = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.room_number
    class Meta:
        permissions = [
            ("can_manage_rooms", "Can manage rooms"),
        ]

class Booking(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=100)
    relation = models.CharField(max_length=50)
    num_people = models.IntegerField()
    check_in_date = models.DateField()
    check_out_date = models.DateField()

    def __str__(self):
        return f"Booking for {self.guest_name} by {self.student.username}"
    class Meta:
        permissions = [
            ("can_view_bookings", "Can view bookings"),
        ]

#cloak room allotment
class CloakRoomEntry(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)    #, limit_choices_to={'groups__name': 'Students'}
    items = models.TextField()
    date_time_stored = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.student.username} - {self.items}'

class CloakRoomSettings(models.Model):
    is_enabled = models.BooleanField(default=False)
    
    def __str__(self):
        return 'Cloak Room Settings'