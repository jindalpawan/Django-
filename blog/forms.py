from django import forms
from .models import Post, Comment
from datetime import datetime
from django.contrib.auth.models import User
class NewpostForm(forms.ModelForm):
	class Meta:
		model= Post
		fields=['title', 'content']

class SignupForm(forms.ModelForm):
	vpass=forms.CharField(max_length=70)
	class Meta:
		model=User
		fields=['username', 'first_name', 'last_name', 'email','password']


class EditProfileForm(forms.ModelForm):
	class Meta:
		model=User
		fields=['username', 'first_name', 'last_name', 'email']


class EditPasswordForm(forms.ModelForm):
	vpass=forms.CharField(max_length=70)
	newpass=forms.CharField(max_length=70)
	class Meta:
		model=User
		fields=['password']


class CommentForm(forms.ModelForm):
	class Meta:
		model=Comment
		fields=['msg']
