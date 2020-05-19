from django import forms
from .models import Post, User
from datetime import datetime
class NewpostForm(forms.ModelForm):
	title= forms.CharField(widget=forms.Textarea)
	content=forms.CharField(widget=forms.Textarea)
	create_date=forms.DateTimeField(required= False)

	class Meta:
		model= Post
		fields=['title', 'content']

class SignupForm(forms.ModelForm):
	username= forms.CharField(max_length= 40)
	name= forms.CharField(max_length= 40)
	email= forms.EmailField(max_length= 40)
	password=forms.CharField(widget=forms.PasswordInput)
	vpass=forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model=User
		fields=['username', 'name', 'email', 'password']


class LoginForm(forms.ModelForm):
	username= forms.CharField(max_length= 40)
	password=forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model=User
		fields=['username', 'password']


class EditProfileForm(forms.ModelForm):
	username= forms.CharField(max_length= 40)
	name= forms.CharField(max_length= 40)
	email= forms.EmailField(max_length= 40)
	password=forms.CharField(widget=forms.PasswordInput)
	vpass=forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model=User
		fields=['username', 'name', 'email', 'password']