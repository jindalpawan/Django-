from django.db import models
from django.utils import timezone
import datetime
# Create your models here.
class User(models.Model):
	username= models.CharField(max_length= 40)
	name= models.CharField(max_length= 40)
	email= models.EmailField(max_length= 40)
	password=models.CharField(max_length= 70)
	def __str__(self):
		return self.username

class Post(models.Model):
	author= models.ForeignKey(User, on_delete=models.CASCADE)
	title= models.TextField()
	content=models.TextField()
	create_date=models.DateTimeField(auto_now_add= True)

	def __str__(self):
		return self.title

	def datecreated(self):
		return self.create_date.strftime('%d %b, %Y')

	def Content(self):
		return self.content[:200]+"..."

	def Contents(self):
		return self.content[:100]+"..."


class Comment(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	post=models.ForeignKey(Post, on_delete=models.CASCADE)
	msg=models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.msg