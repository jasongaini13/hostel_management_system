from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentProfile, FacultyProfile
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.username.startswith('b') and instance.username[1:].isdigit():
            student_profile, created = StudentProfile.objects.get_or_create(user=instance, defaults={'email': instance.email})
            if created:
                subject = 'Welcome to my app'
                message = 'We are glad to see you here!'
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [student_profile.email],
                    fail_silently=False
                )
        else:
            faculty_profile, created = FacultyProfile.objects.get_or_create(user=instance, defaults={'email': instance.email})
            if created:
                subject = 'Welcome to my app'
                message = 'We are glad to see you here!'
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [faculty_profile.email],
                    fail_silently=False
                )
