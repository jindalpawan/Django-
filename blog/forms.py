from django import forms
from .models import Post, User, Comment
from datetime import datetime
class NewpostForm(forms.ModelForm):
	class Meta:
		model= Post
		fields=['title', 'content']

class SignupForm(forms.ModelForm):
	vpass=forms.CharField(max_length=70)
	class Meta:
		model=User
		fields=['username', 'name', 'email', 'password']


class LoginForm(forms.ModelForm):
	class Meta:
		model=User
		fields=['username', 'password']


class EditProfileForm(forms.ModelForm):
	class Meta:
		model=User
		fields=['username', 'name', 'email']


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
