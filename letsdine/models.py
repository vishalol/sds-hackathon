from __future__ import unicode_literals
from django.utils import timezone
#from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models

# Create your models here.

class Intrest(models.Model):
  name = models.CharField(max_length=40)
  def __str__(self):
   return self.name

class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE) 
  display_pic = models.ImageField(default='pic_folder/user.jpg' , upload_to = 'pic_folder/',null=True, blank=True,)
  contact_no = models.BigIntegerField(default=000000000,blank=True )
  city_name = models.CharField(max_length=40, blank=True)
  Gender_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )
  gender = models.CharField(max_length=20,choices=Gender_CHOICES, blank=True )
  age = models.IntegerField(default=18,blank=True )
  occupation = models.CharField(max_length=40, blank=True)
  about_you = models.CharField(max_length=500, blank=True)
  intrests = models.ManyToManyField(Intrest, blank=True)
  fb_link = models.URLField(max_length=100, blank=True)
  twitter_link = models.URLField(max_length=100, blank=True)
  insta_link = models.URLField(max_length=100, blank=True)
  def __str__(self):
   return self.user.username


class Plan(models.Model):
  created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
  created_on = models.DateTimeField(auto_now_add=True)
  going_time = models.DateTimeField() 
  other_users = models.ManyToManyField(User, blank=True, related_name = 'iplans')
  Food_CHOICES = (
        ('Veg', 'Veg'),
        ('Non-Veg', 'Non-Veg'),
        ('Both', 'Both')
    )
  food_type = models.CharField(max_length=20,choices=Food_CHOICES)
  place = models.PointField()


class Plan_request(models.Model):
  user  = models.ForeignKey(User, on_delete=models.CASCADE)
  created_on = models.DateTimeField(auto_now_add=True)
  Status_CHOICES = (
        ('A', 'Accepted'),
        ('R', 'Rejected'),
        ('P', 'Pending')
    )
  status =  models.CharField(max_length=1, choices=Status_CHOICES, default='P')
  plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null = True)
  def __str__(self):
   return self.user.username

class Message(models.Model):
  created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
  message = models.CharField(max_length=400)
  created_on = models.DateTimeField(auto_now_add=True)
  plan = models.ForeignKey(Plan, on_delete=models.CASCADE)


