from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Post , User, Comment
from django.views.generic import TemplateView, DetailView
from .forms import NewpostForm, SignupForm, LoginForm, EditProfileForm, EditPasswordForm, CommentForm
from django.utils import timezone
from datetime import datetime
import urllib3
import json
import random
import hashlib
from django.views.decorators.csrf import csrf_exempt

str1="asdfghjklpoiuytrewqzxcvbnm"

def make_salt(length = 5):
    return ''.join(random.choice(str1) for x in range(length))

def make_pw_hash(name, pw, salt = None):
	if not salt:
		salt = make_salt()
	h = (hashlib.sha256((name + pw + salt).encode()).hexdigest())
	return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
	salt = h.split(',')[0]
	return h == make_pw_hash(name, password, salt)

salt="asdfgh"

def make_secure_value(value):
	val=str(value)
	h = (hashlib.sha256((val+ salt).encode()).hexdigest())
	return '%s|%s' % (val,h)

def check_secure_value(h):
	val = h.split('|')[0]
	if h == make_secure_value(val):
		return int(val)
	else:
		return 0



class HomePage(TemplateView):
	def get(self, request):
		userid=request.COOKIES.get('user_id',0)
		user=""
		userid= check_secure_value(userid)
		if userid:
			user=User.objects.filter(id=userid).first()
		posts= Post.objects.filter(create_date__lte=timezone.now()).order_by('create_date').reverse()
		return render(request, 'blog/front.html', {'alldata':posts,'user':user})


class Perma(TemplateView):
	def get(self,request, pk):
		obj= Post.objects.filter(pk=pk).first()
		userid=request.COOKIES.get('user_id',0)
		user=""
		userid= check_secure_value(userid)
		cmnts=Comment.objects.filter(post=obj)
		if userid:
			user=User.objects.filter(id=userid).first()
			return render(request, "blog/perma.html",{'post':obj,'user':user,'cmnts':cmnts})
		else:
			return render(request, "blog/perma.html",{'post':obj,'cmnts':cmnts})
	

@csrf_exempt
def comments(request):
	if request.method== 'POST':
		userid=request.COOKIES.get('user_id',0)
		user=""
		userid= check_secure_value(userid)
		if userid:
			user=User.objects.filter(id=userid).first()
			postid=request.POST['postid']
			msg=request.POST['msg']
			if len(msg)>0:
				post= Post.objects.filter(pk=postid).first()
				cmt=Comment(user=user,post=post,msg=msg)
				cmt.save()
			return JsonResponse({"msg":msg},)
		return JsonResponse({},)	

class NewPost(TemplateView):
	def get(self,request):
		bg=NewpostForm(request.GET)
		userid=request.COOKIES.get('user_id',0)
		user=""
		userid= check_secure_value(userid)
		if userid:
			user=User.objects.filter(id=userid).first()
			return render(request,"blog/newpost.html",{'user':user})
		else:
			return redirect(reverse('blog:signup',))

	def post(self, request):
		bg=NewpostForm(request.POST)
		if bg.is_valid():
			userid=request.COOKIES.get('user_id',0)
			userid= check_secure_value(userid)
			author=User.objects.filter(id=userid).first()
			title= bg.cleaned_data['title']
			content=bg.cleaned_data['content']
			content=content.replace('\n', '<br>')
			p=Post(title= title, content=content,author= author)
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
		userid= check_secure_value(userid)
		if userid:
			posts=Post.objects.filter(author=userid)
			user=User.objects.filter(id=userid).first()
			return render(request, "blog/profile.html",{'user':user,'posts':posts})
		else:
			return redirect(reverse('blog:signup',))

class EditProfile(TemplateView):
	def get(self,request):
		sig=EditProfileForm(request.GET)
		userid=request.COOKIES.get('user_id',0)
		user=""
		dic={}
		userid= check_secure_value(userid)
		if userid:
			user=User.objects.filter(id=userid).first()
			dic['username']=user.username
			dic['email']=user.email
			dic['name']=user.name
			return render(request,"blog/edit_profile.html",dic)
		else:
			return redirect(reverse('blog:signup',))

	def post(self, request):
		sig=EditProfileForm(request.POST)
		if sig.is_valid():
			username=sig.cleaned_data['username']
			name=sig.cleaned_data['name']
			email=sig.cleaned_data['email']
			userid=request.COOKIES.get('user_id',0)
			userid= check_secure_value(userid)
			p=User.objects.filter(id=userid).first()
			p.username=username
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


class EditPassword(TemplateView):
	def get(self,request):
		sig=EditPasswordForm(request.GET)
		userid=request.COOKIES.get('user_id',0)
		user=""
		dic={}
		userid= check_secure_value(userid)
		if userid:
			return render(request,"blog/edit_pass.html",)
		else:
			return redirect(reverse('blog:signup',))

	def post(self, request):
		sig=EditPasswordForm(request.POST)
		if sig.is_valid():
			userid=request.COOKIES.get('user_id',0)
			userid= check_secure_value(userid)
			user=User.objects.filter(id=userid).first()
			password=sig.cleaned_data['password']
			newpass=sig.cleaned_data['newpass']
			vpass=sig.cleaned_data['vpass']
			dic={}
			if user.password!=password:
				dic['error_password']="Wrong Password!!!!!!"
			if newpass!= vpass:
				dic['error_vpass']="Password not match!!!!!!"
			
			if not dic:
				user.password=newpass
				user.save()
				return redirect(reverse('blog:profile',))
			else:
				return render(request,'blog/edit_pass.html',dic)
			
		else:
			return render(request,'blog/edit_pass.html',)	


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
				cookie_id=make_secure_value(obj.id)
				response.set_cookie('user_id',cookie_id)
				return response				
			else:
				dic={'username':username, 'password':password,'error_password':"Username or Password not matcheds"}
				return render(request,"blog/login.html",dic)


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
				cookie_id=make_secure_value(p.id) 
				response=redirect(reverse('blog:home',))
				response.set_cookie('user_id',cookie_id)
				return response
		else:
			return render(request,'blog/signup.html',)	


class FacebookData(TemplateView):
	def get(self, request):
		URL= 'https://graph.facebook.com/v6.0/oauth/access_token?client_id=&redirect_uri=http://localhost:8000/blog/dataa&client_secret=&code='
		URL2="https://graph.facebook.com/me?access_token="
		code=request.GET['code']
		code=URL+str(code)
		lib = urllib3.PoolManager()
		r = lib.request('GET', code)
		data=json.loads(r.data.decode('utf-8'))
		token= str(data["access_token"])
		URL2= URL2+(token)+"&fields=id,name"
		rr= lib.request('GET', URL2)
		data2= json.loads(rr.data.decode('utf-8'))
		username= str(data2['id'])
		name= str(data2['name'])
		password=username
		obj= User.objects.filter(username=username).first()
		if not obj:
			obj= User(username=username, name=name, email="", password=password)
			obj.save()
		cookie_id=make_secure_value(obj.id)
		response=redirect(reverse('blog:home',))
		response.set_cookie('user_id',cookie_id)
		return response
