from django.contrib import admin
from .models import Post
from django.contrib.auth.models import User

class UserAdmin(admin.ModelAdmin):
	fields= ['username', 'password','email']

class PostAdmin(admin.ModelAdmin):
	fields= ['title', 'content','user']
admin.site.register(Post, PostAdmin)
# Register your models here.
