from django.contrib import admin

# Register your models here.
from . models import FacultyProfile, StudentProfile

admin.site.register(FacultyProfile)
admin.site.register(StudentProfile)