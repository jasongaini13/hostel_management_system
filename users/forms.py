from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from users.models import FacultyProfile, StudentProfile

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address ending with @iiit-bh.ac.in.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@iiit-bh.ac.in') or not email.startswith('b') or not email[1:7].isdigit():
            raise forms.ValidationError("Student email must start with 'b', followed by 6 digits, and end with '@iiit-bh.ac.in'")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username.startswith('b') or not username[1:].isdigit() or len(username) != 7:
            raise forms.ValidationError("Username must start with 'b' followed by 6 digits.")
        return username

class FacultyRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address ending with @iiit-bh.ac.in.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        local_part = email.split('@')[0]
        if any(char.isdigit() for char in local_part):
            raise forms.ValidationError("Faculty email must not contain digits in the local part.")
        return email

class StudentAuthenticationForm(AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data['username']
        if not username.startswith('b') or not username[1:].isdigit() or len(username) != 7:
            raise forms.ValidationError("Username will start with 'b' followed by 6 digits.")
        return username

class FacultyAuthenticationForm(AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data['username']
        if username.startswith('b') and username[1:7].isdigit():
            raise forms.ValidationError("Students are not allowed to log in from the faculty login page.")
        return username


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['email','fullname', 'address', 'profile_image', 'branch', 'year','mobile_no']

class FacultyProfileForm(forms.ModelForm):
    class Meta:
        model = FacultyProfile
        fields = ['user','email','fullname', 'address', 'profile_image', 'short_intro', 'mobile_no']


 # forms.py
# from django import forms
# from .models import Notice

# class NoticeForm(forms.ModelForm):
#     class Meta:
#         model = Notice
#         fields = ['subject', 'message']

# forms.py
from django import forms
from .models import Complaint, Notice,Room,Booking

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['subject', 'message']



from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from users.models import FacultyProfile, StudentProfile, LeaveApplication ,DoctorAppointment,CloakRoomEntry, CloakRoomSettings

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address ending with @iiit-bh.ac.in.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@iiit-bh.ac.in') or not email.startswith('b') or not email[1:7].isdigit():
            raise forms.ValidationError("Student email must start with 'b', followed by 6 digits, and end with '@iiit-bh.ac.in'")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username.startswith('b') or not username[1:].isdigit() or len(username) != 7:
            raise forms.ValidationError("Username must start with 'b' followed by 6 digits.")
        return username

class FacultyRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address ending with @iiit-bh.ac.in.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        local_part = email.split('@')[0]
        if any(char.isdigit() for char in local_part):
            raise forms.ValidationError("Faculty email must not contain digits in the local part.")
        return email

class StudentAuthenticationForm(AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data['username']
        if not username.startswith('b') or not username[1:].isdigit() or len(username) != 7:
            raise forms.ValidationError("Username will start with 'b' followed by 6 digits.")
        return username

class FacultyAuthenticationForm(AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data['username']
        if username.startswith('b') and username[1:7].isdigit():
            raise forms.ValidationError("Students are not allowed to log in from the faculty login page.")
        return username


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['email','fullname', 'address', 'profile_image', 'branch', 'year','mobile_no']

class FacultyProfileForm(forms.ModelForm):
    class Meta:
        model = FacultyProfile
        fields = ['user','email','fullname', 'address', 'profile_image', 'short_intro', 'mobile_no']


class LeaveApplicationForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = LeaveApplication
        fields = ['reason', 'start_date', 'end_date']
        widgets = {
            'reason': forms.Textarea(attrs={'placeholder': 'Purpose'}),
        }

#For Doctor Appointment
class DoctorAppointmentForm(forms.ModelForm):
    class Meta:
        model = DoctorAppointment
        fields = ['category_of_issue', 'description']
        widgets = {
            'category_of_issue': forms.TextInput(attrs={
                'placeholder': 'Category of Issue',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Description',
                'class': 'form-control',
                'rows': 4
            })
        }
class AppointmentDateForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = DoctorAppointment
        fields = ['date', 'time']


from django import forms

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'small-textarea'}),
        }


#guest room allotment
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['guest_name', 'relation', 'num_people', 'check_in_date', 'check_out_date', 'room']
    
    check_in_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    check_out_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    room = forms.ModelChoiceField(queryset=Room.objects.filter(is_available=True), empty_label="Select a room")
    widgets = {
            'guest_name': forms.TextInput(attrs={'class': 'form-control'}),
            'relation': forms.TextInput(attrs={'class': 'form-control'}),
            'num_people': forms.NumberInput(attrs={'class': 'form-control'}),
            'check_in_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'room': forms.Select(attrs={'class': 'form-control'}),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'is_available']


#Cloak Room Form
class CloakRoomEntryForm(forms.ModelForm):
    class Meta:
        model = CloakRoomEntry
        fields = ['items']

class CloakRoomSettingsForm(forms.ModelForm):
    class Meta:
        model = CloakRoomSettings
        fields = ['is_enabled']

