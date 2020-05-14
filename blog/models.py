from django.db import models
from django.utils import timezone
import datetime
# Create your models here.
class Post(models.Model):
	title= models.TextField()
	content=models.TextField()
	#create_date=models.DateTimeField('created')

	def __str__(self):
		return self.title

class User(models.Model):
	username= models.CharField(max_length= 40)
	name= models.CharField(max_length= 40)
	contact= models.CharField(max_length=10)
	email= models.EmailField(max_length= 40)

	def __str__(self):
		return self.username