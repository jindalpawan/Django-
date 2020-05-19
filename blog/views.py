from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Post , User
from django.views.generic import TemplateView
from .forms import NewpostForm, SignupForm
from django.utils import timezone
from datetime import datetime


class Signup(TemplateView):
	def get(self,request):
		sig=SignupForm(request.GET)
		return render(request,"blog/signup.html",)

	def post(self, request):
		sig=SignupForm(request.POST)
		if sig.is_valid():
			username= sig.cleaned_data['username']
			name=sig.cleaned_data['name']
			email=sig.cleaned_data['email']
			password=sig.cleaned_data['password']
			vpass=sig.cleaned_data['vpass']
			exist1=get_object_or_404(User, username=username)
			exist2=get_object_or_404(User, email=email)

			p=User(username=username, name=name, email= email, password=password)
			p.save()
			return redirect(reverse('blog:home',))

		else:
			username= sig.cleaned_data['username']
			name=sig.cleaned_data['name']
			email=sig.cleaned_data['email']
			password=sig.cleaned_data['password']
			vpass=sig.cleaned_data['vpass']
			print(vpass)
			print(sig.errors)
			return render(request,'blog/signup.html',{'username': username, 'name':name, 'email':email})	



class HomePage(TemplateView):
	def get(self, request):
		posts= Post.objects.filter(create_date__lte=timezone.now()).order_by('create_date')
		return render(request, 'blog/front.html', {'alldata':posts})


class Perma(TemplateView):
	def get(self,request, pk):
		obj= get_object_or_404(Post, pk=pk)
		return render(request, "blog/perma.html",{'post':obj})
		

class NewPost(TemplateView):
	def get(self,request):
		bg=NewpostForm(request.GET)
		return render(request,"blog/newpost.html",)

	def post(self, request):
		bg=NewpostForm(request.POST)
		if bg.is_valid():
			title= bg.cleaned_data['title']
			content=bg.cleaned_data['content']
			p=Post(title= title, content=content)
			p.save()
			return redirect(reverse('blog:onepost',args=(p.pk,)))

		else:
			title= bg.cleaned_data['title']
			content=bg.cleaned_data['content']
			print(bg.errors)
			return render(request, 'blog/newpost.html',{'title': title, 'content':content})
