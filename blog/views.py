from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Post , User
from django.views.generic import TemplateView
from .forms import NewpostForm, SignupForm, LoginForm
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
			dic={}
			if password != vpass:
				dic['error_vpass']="Password not matched"
			if (User.objects.filter(username=username)):
				dic['error_username']="This username already exist"
			if (User.objects.filter(email=email)):
				dic['error_email']="This email already exist"

			if dic:
				dic['username']=username
				dic['name']=name
				dic['email']=email
				return render(request,'blog/signup.html',dic)
			else:
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
			dic={'username': username, 'name':name, 'email':email}
			return render(request,'blog/signup.html',dic)	



class Login(TemplateView):
	def get(self, request):
		log=LoginForm(request.GET)
		return render(request,"blog/login.html",)

	def post(self, request):
		log=LoginForm(request.POST)
		if log.is_valid():
			username= log.cleaned_data['username']
			password=log.cleaned_data['password']
			obj=User.objects.filter(username=username)
			print(obj)
			if obj.password==password:
				return redirect(reverse('blog:home',))				
			else:
				dic={'username':username, 'password':password,'error_password':"Username or Password not matcheds"}
				return render(request,"blog/login.html",dic)


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
