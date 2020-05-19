from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Post , User
from django.views.generic import TemplateView
from .forms import NewpostForm, SignupForm, LoginForm, EditProfileForm
from django.utils import timezone
from datetime import datetime



class Logout():
	def logout(self):
		response=render(request,"blog/signup.html",)
		response.set_cookie('user_id', "")
		return response

	
class Signup(TemplateView):
	def get(self,request):
		sig=SignupForm(request.GET)
		response=render(request,"blog/signup.html",)
		response.set_cookie('user_id', "")
		return response

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
			if (User.objects.filter(username=username).first()):
				dic['error_username']="This username already exist"
			if (User.objects.filter(email=email).first()):
				dic['error_email']="This email already exist"

			if dic:
				dic['username']=username
				dic['name']=name
				dic['email']=email
				return render(request,'blog/signup.html',dic)
			else:
				p=User(username=username, name=name, email= email, password=password)
				p.save()
				response=redirect(reverse('blog:home',))
				response.set_cookie('user_id',p.id)
				return response
		else:
			username= sig.cleaned_data['username']
			name=sig.cleaned_data['name']
			email=sig.cleaned_data['email']
			password=sig.cleaned_data['password']
			vpass=sig.cleaned_data['vpass']
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
			obj=User.objects.filter(username=username).first()
			if obj.password==password:
				response=redirect(reverse('blog:home',))
				response.set_cookie('user_id',obj.id)
				return response				
			else:
				dic={'username':username, 'password':password,'error_password':"Username or Password not matcheds"}
				return render(request,"blog/login.html",dic)


class EditProfile(TemplateView):
	def get(self,request):
		sig=EditProfileForm(request.GET)
		userid=request.COOKIES.get('user_id',0)
		user=""
		dic={}
		if userid:
			user=User.objects.filter(id=userid).first()
			dic['username']=user.username
			dic['email']=user.email
			dic['name']=user.name
		return render(request,"blog/edit_profile.html",dic)

	def post(self, request):
		sig=EditProfileForm(request.POST)
		if sig.is_valid():
			username=sig.cleaned_data['username']
			name=sig.cleaned_data['name']
			email=sig.cleaned_data['email']
			password=sig.cleaned_data['password']
			vpass=sig.cleaned_data['vpass']
			dic={}
			if password != vpass:
				dic['error_vpass']="Password not matched"
			
			if dic:
				dic['username']=username
				dic['name']=name
				dic['email']=email
				return render(request,'blog/edit_profile.html',dic)
			else:
				p=User.objects.get(username=username)
				p.name= name
				p.email=email
				p.password=password
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
			return render(request,'blog/edit_profile.html',dic)	

class Profile(TemplateView):
	def get(self,request):
		userid=request.COOKIES.get('user_id',0)
		user=""
		if userid:
			user=User.objects.filter(id=userid).first()
		return render(request, "blog/profile.html",{'user':user})


class HomePage(TemplateView):
	def get(self, request):
		userid=request.COOKIES.get('user_id',0)
		user=""
		if userid:
			user=User.objects.filter(id=userid).first()
		posts= Post.objects.filter(create_date__lte=timezone.now()).order_by('create_date')
		return render(request, 'blog/front.html', {'alldata':posts,'user':user})


class Perma(TemplateView):
	def get(self,request, pk):
		obj= Post.objects.filter(pk=pk).first()
		userid=request.COOKIES.get('user_id',0)
		user=""
		if userid:
			user=User.objects.filter(id=userid).first()
		return render(request, "blog/perma.html",{'post':obj,'user':user})
		

class NewPost(TemplateView):
	def get(self,request):
		bg=NewpostForm(request.GET)
		userid=request.COOKIES.get('user_id',0)
		user=""
		if userid:
			user=User.objects.filter(id=userid).first()
			return render(request,"blog/newpost.html",{'user':user})
		else:
			return render(request,"blog/signup.html",)

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
			return render(request, 'blog/newpost.html',{'title': title, 'content':content})
