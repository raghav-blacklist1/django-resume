from django.db import models
from django import forms
import datetime
from django.utils.timezone import utc
from django.db import connection
from django.contrib.auth.models import User

class Profile(models.Model):

	username = models.CharField(max_length=150,default="none",primary_key=True)
	fname = models.CharField(max_length=150,default="")
	lname = models.CharField(max_length=150,default="")
	email = models.CharField(max_length=150,default="")
	mob = models.CharField(max_length=20,default="")
	link_in = models.CharField(max_length=150,default="")
	github = models.CharField(max_length=150,default="")
	lang = models.CharField(max_length=200,default="")

class education(models.Model):

	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	id_cnt = models.AutoField(primary_key=True)
	insti_name = models.CharField(max_length=200,default="")
	s_year = models.IntegerField(default=0)
	e_year = models.IntegerField(default=0)
	degree = models.CharField(max_length=150,default="")
	score = models.CharField(max_length=20,default="")

class experience(models.Model):

	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	id_cnt = models.AutoField(primary_key=True)
	company = models.CharField(max_length=150,default="")
	title = models.CharField(max_length=200,default="")
	s_year = models.IntegerField(default=0)
	e_year = models.IntegerField(default=0)
	work = models.CharField(max_length=200,default="")

class skills(models.Model):

	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	id_cnt = models.AutoField(primary_key=True)
	skill = models.CharField(max_length=150,default="")	
	