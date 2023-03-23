from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class ServicePage(models.Model):

	serviceID = models.AutoField(primary_key=True)
	name = models.CharField(max_length=32)
	location = models.CharField(max_length=32)
	body = models.CharField(max_length=256)
	logo = models.ImageField(upload_to='logo_images', blank=True)
	slug = models.SlugField(unique=True, blank=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name+"_"+self.location)
		super(ServicePage, self).save(*args, **kwargs)

	def __str__(self): 
		return self.name

class Review(models.Model):

	serviceID = models.ForeignKey(ServicePage, on_delete=models.CASCADE) 
	userID = models.ForeignKey(User, on_delete=models.CASCADE) 

	reviewID = models.AutoField(primary_key=True)
	date = models.DateTimeField(auto_now_add=True)

	location = models.CharField(max_length=32)
	service = models.CharField(max_length=32)
	rating = models.IntegerField(default=0)
	title = models.CharField(max_length=128)
	body = models.CharField(max_length=256)

	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)

	def __str__(self):
		return self.title

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	accountUser = models.BooleanField(default=True)
	picture = models.ImageField(upload_to='media', blank=True)

	def __str__(self):
		return self.user.username
		