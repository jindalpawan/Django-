from django import forms
from .models import Post
from datetime import datetime
class NewpostForm(forms.ModelForm):
	title= forms.CharField(widget=forms.Textarea)
	content=forms.CharField(widget=forms.Textarea)

	class Meta:
		model= Post
		fields='__all__'