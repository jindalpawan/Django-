from django import forms
from .models import Post
from datetime import datetime
class NewpostForm(forms.ModelForm):
	title= forms.CharField(widget=forms.Textarea)
	content=forms.CharField(widget=forms.Textarea)
	create_date=forms.DateTimeField(required= False)

	class Meta:
		model= Post
		fields=['title', 'content']