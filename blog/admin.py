from django.contrib import admin
from .models import User, Post

class UserAdmin(admin.ModelAdmin):
	fields= ['username', 'name', 'email','password']

class PostAdmin(admin.ModelAdmin):
	fields= ['title', 'content','user']

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
# Register your models here.
