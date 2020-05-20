from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Post , User
from django.views.generic import TemplateView
from .forms import NewpostForm, SignupForm, LoginForm, EditProfileForm
from django.utils import timezone
from datetime import datetime
import urllib3
import json
import random
import hashlib

str="asdfghjklpoiuytrewqzxcvbnm"

def make_salt(length = 5):
    return ''.join(random.choice(str) for x in range(length))

def make_pw_hash(name, pw, salt = None):
	if not salt:
		salt = make_salt()
	h = (hashlib.sha256((name + pw + salt).encode()).hexdigest())
	return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
	salt = h.split(',')[0]
	return h == make_pw_hash(name, password, salt)

class HomePage(TemplateView):
	def get(self, request):
		userid=request.COOKIES.get('user_id',0)
		user=""
		if userid:
			user=User.objects.filter(id=userid).first()
		posts= Post.objects.filter(create_date__lte=timezone.now()).order_by('create_date').reverse()
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
			userid=request.COOKIES.get('user_id',0)
			user=User.objects.filter(id=userid).first()
			title= bg.cleaned_data['title']
			content=bg.cleaned_data['content']
			content=content.replace('\n', '<br>')
			p=Post(title= title, content=content,user= user)
			p.save()
			return redirect(reverse('blog:onepost',args=(p.pk,)))

		else:
			title= bg.cleaned_data['title']
			content=bg.cleaned_data['content']
			return render(request, 'blog/newpost.html',{'title': title, 'content':content})


class Profile(TemplateView):
	def get(self,request):
		userid=request.COOKIES.get('user_id',0)
		user=""
		if userid:
			posts=Post.objects.filter(user=userid)
			user=User.objects.filter(id=userid).first()
		return render(request, "blog/profile.html",{'user':user,'posts':posts})


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
			p=User.objects.filter(username=username).first()
			p.name= name
			p.email=email
			p.save()
			return redirect(reverse('blog:home',))
		
		else:
			username=sig.cleaned_data['username']
			name=sig.cleaned_data['name']
			email=sig.cleaned_data['email']
			dic={'username': username, 'name':name, 'email':email}
			return render(request,'blog/edit_profile.html',dic)	


class FacebookData(TemplateView):
	def get(self, request):
		URL= 'https://graph.facebook.com/v6.0/oauth/access_token?client_id=&redirect_uri=http://localhost:8000/blog/dataa&client_secret=&code='
		URL2="https://graph.facebook.com/me?access_token="
		code=request.GET['code']
		code=URL+(code)
		lib = urllib3.PoolManager()
		r = lib.request('GET', code)
		data=json.loads(r.data.decode('utf-8'))
		token= data["access_token"]
		URL2= URL2+(token)+"&fields=id,name"
		rr= lib.request('GET', URL2)
		data2= json.loads(rr.data.decode('utf-8'))
		username= (data2['id'])
		name=(data2['name'])
		password=username
		obj= User.objects.filter(username=username).first()
		if obj:
			response=redirect(reverse('blog:home',))
			response.set_cookie('user_id',obj.id)
			return response
		else:
			obj= User(username=username, name=name, email="", password=password)
			obj.save()
			response=redirect(reverse('blog:home',))
			response.set_cookie('user_id',obj.id)
			return response


class Signup(TemplateView):
	def get(self,request):
		sig=SignupForm(request.GET)
		response=render(request,"blog/signup.html",)
		response.set_cookie('user_id','')
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
				password=make_pw_hash(username, password)
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
			if obj and valid_pw(username, password, obj.password):
				response=redirect(reverse('blog:home',))
				response.set_cookie('user_id',obj.id)
				return response				
			else:
				dic={'username':username, 'password':password,'error_password':"Username or Password not matcheds"}
				return render(request,"blog/login.html",dic)