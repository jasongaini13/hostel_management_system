from django.contrib import admin

# Register your models here.
from . models import FacultyProfile, StudentProfile,Notice,Complaint

admin.site.register(FacultyProfile)
admin.site.register(StudentProfile)
admin.site.register(Notice)
admin.site.register(Complaint)