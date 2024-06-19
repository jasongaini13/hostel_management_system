from django.contrib import admin

# Register your models here.
from . models import FacultyProfile, StudentProfile,Notice,Complaint,Room,Booking,CloakRoomSettings,CloakRoomEntry

admin.site.register(FacultyProfile)
admin.site.register(StudentProfile)
admin.site.register(Notice)
admin.site.register(Complaint)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(CloakRoomEntry)
admin.site.register(CloakRoomSettings)
