from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Post , User
from django.views.generic import TemplateView
from .forms import NewpostForm

class HomePage(TemplateView):
	def get(self, request):
		posts= Post.objects.all()
		alldata={'posts': posts ,}
		return render(request, 'blog/home.html', {'alldata':alldata})

class NewPost(TemplateView):
	def get(self,request):
		bg=NewpostForm(request.GET)
		return render(request,"blog/newpost.html",)

	def post(self, request):
		bg=NewpostForm(request.POST)
		if bg.is_valid():
			bg.save()
			redirect('/blog')

		else:
			title= bg.cleaned_data['title']
			content=bg.cleaned_data['content']
			return render(request, 'blog/newpost.html',{'title': title, 'content':content})
