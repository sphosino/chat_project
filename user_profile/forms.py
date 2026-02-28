from django import forms
from .models import Profile
from accounts.models import CustomUser

class ProfileEditForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = [
			'bio',
			'avatar'
		]

class UserNotifyForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['notify_room_create']