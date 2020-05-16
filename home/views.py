from django.shortcuts import render,redirect
from django.shortcuts import render_to_response
from .models import *
from django.db import models
from .forms import *
import datetime
from django.utils.timezone import utc
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from home.forms import *
from django.contrib import messages
import pdfkit
import pymysql														#pymysql is used fo sql queries in this python scrript

def HomePage(request):

	context={'is_authenticated':False}
	if request.user.is_authenticated:						#homepage is the normal page that will be shown to evryone firstly

		context['is_authenticated']=True
		context['username']=request.user.username
		context['firstname']=request.user.first_name							
		context['lastname']=request.user.last_name
		#print('Logged in')
	
	return render(request, 'home.html', context)										#home.html is the homepage view on website

def login_page(request):

	context={}
	username = "not logged in"

	if request.method == 'POST':
		MyLoginForm=LoginForm(request.POST)
		#print("STEP 0")

		if MyLoginForm.is_valid():										#validation of our form
			username = MyLoginForm.cleaned_data['username']
			password = MyLoginForm.cleaned_data['password']
			user = authenticate(request, username=username, password=password)
			#print("STEP 1")
			if user is not None:
				login(request, user)
				#print("STEP 2")
				return redirect('/dashboard')	#if we have got valid request for username the person is redirected to dashboard with context dictionary containg user info

			else:
				messages.info(request,"Invalid Username or Password!")				#for showing a popup that invalid request has been made


	else:
		MyLoginForm=LoginForm()
		#print("STEP 3")

	#print("STEP 4")
	return redirect('/')
	

def logout_page(request):

    logout(request)
    return redirect('/')				#if user clicks on logout it django 'logout' function logouts the user and the himepage is shon to him

def dash(request):

	context={'is_authenticated':False}
	if request.user.is_authenticated:				#only dahboard is shown to the user who has logged in..otherwise redirected to /403

		context['is_authenticated']=True
		context['username']=request.user.username
		context['firstname']=request.user.first_name
		context['lastname']=request.user.last_name
		#raise ValueError('A very specific bad thing happened.')
		return render(request, 'dash.html', context)

	return redirect('/403')

def getkey(item):					#function used to sort the items according to first name of user

	return item.fname.lower()

def getkey1(item):					#to sort acc. to the year in which person completed

	return item.e_year

def people(request):

	context={'is_authenticated':False}								#the people page is for showuing templates of all the people who are signed in with our website
	if request.user.is_authenticated:

		context['is_authenticated']=True
		context['username']=request.user.username
		context['firstname']=request.user.first_name
		context['lastname']=request.user.last_name
		context['ppl']=sorted(Profile.objects.all(), key=getkey)
		return render(request, 'people.html', context)

	return redirect('/403')

def denied_acc(request):

	return render(request,'403.html',{})

def no_res(request):

	return render(request,'404.html',{})


def register_page(request):

	return render(request,'register.html',{})

def edu_page(request):

	if request.user.is_authenticated:

		return render(request,'add_edu.html',{})

	return redirect('/403')

def exp_page(request):

	if request.user.is_authenticated:

		return render(request,'add_exp.html',{})

	return redirect('/403')

def skill_page(request):

	if request.user.is_authenticated:

		return render(request,'add_ski.html',{})

	return redirect('/403')

def test(request,string):

	context={}
	context['m']=string

	return render(request,'1.html',context)

def temp1(request,string):

	context={}
	try:
		usr=Profile.objects.get(username=string)
		context['obj']=Profile.objects.get(username=string)				#to get main info
	except:
		return redirect('/404')
	context['edu']=sorted(usr.education_set.all(),key=getkey1,reverse=True)
	context['ski']=usr.skills_set.all()
	context['exp']=sorted(usr.experience_set.all(),key=getkey1,reverse=True)			#to get education ,skill and experience info

	return render(request,'style1.html',context)

def dtemp1(request,string):

	my_url = request.get_host() + '/temp1/' + string
	pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
	print(my_url)
	pdf = pdfkit.from_url(my_url, False)
	response = HttpResponse(pdf,content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="{0}_1.pdf"'.format(string)

	return response

def temp2(request,string):

	context={}

	try:
		usr=Profile.objects.get(username=string)
		context['obj']=Profile.objects.get(username=string)
	except:
		return redirect('/404')
	context['edu']=sorted(usr.education_set.all(),key=getkey1,reverse=True)
	context['ski']=usr.skills_set.all()
	context['exp']=sorted(usr.experience_set.all(),key=getkey1,reverse=True)

	return render(request,'style2.html',context)

def dtemp2(request,string):

	my_url = request.get_host() + '/temp2/' + string
	pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
	print(my_url)
	pdf = pdfkit.from_url(my_url, False)
	response = HttpResponse(pdf,content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="{0}_2.pdf"'.format(string)

	return response

def temp3(request,string):

	context={}

	try:
		usr=Profile.objects.get(username=string)
		context['obj']=Profile.objects.get(username=string)
	except:
		return redirect('/404')
	context['edu']=sorted(usr.education_set.all(),key=getkey1,reverse=True)
	context['ski']=usr.skills_set.all()
	context['exp']=sorted(usr.experience_set.all(),key=getkey1,reverse=True)

	return render(request,'style3.html',context)

def dtemp3(request,string):

	my_url = request.get_host() + '/temp3/' + string
	pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
	print(my_url)
	pdf = pdfkit.from_url(my_url, False)
	response = HttpResponse(pdf,content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="{0}_3.pdf"'.format(string)

	return response

def temp4(request,string):

	context={}

	try:
		usr=Profile.objects.get(username=string)
		context['obj']=Profile.objects.get(username=string)				#to get main info
	except:
		return redirect('/404')
	context['edu']=sorted(usr.education_set.all(),key=getkey1,reverse=True)
	context['ski']=usr.skills_set.all()
	context['exp']=sorted(usr.experience_set.all(),key=getkey1,reverse=True)			#to get education ,skill and experience info

	return render(request,'style4.html',context)

def dtemp4(request,string):

	my_url = request.get_host() + '/temp4/' + string
	pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
	print(my_url)
	pdf = pdfkit.from_url(my_url, False)
	response = HttpResponse(pdf,content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="{0}_4.pdf"'.format(string)

	return response

"""									// does the same thing as above, but with raw SQL queries

def temp4(request,string):

	context={}
	if not request.user.is_authenticated:				# checks if either the user is authenticated or the parameter is a sample
		if string != "sample":
			return redirect('/403')

	conn=pymysql.connect(host='127.0.0.1',user='root',password='12345000',db="resume6",charset="utf8mb4",cursorclass=pymysql.cursors.DictCursor)	# connects pymysql to database

	try:
		cursorObject = conn.cursor()		#init cursor
		Query1 = "select * from home_profile where username like '%"+string+"%'"
		cursorObject.execute(Query1)
		context['obj']=cursorObject.fetchall()[0]	#fetch main details
	except:
		return redirect('/404')

	Query2 = "select * from home_education where user_id like '%"+string+"%'"
	print(Query2)
	Query3 = "select * from home_experience where user_id like '%"+string+"%'"
	Query4 = "select * from home_skills where user_id like '%"+string+"%'"
	cursorObject.execute(Query2)
	context['edu']=sorted(cursorObject.fetchall(),key=getkey1,reverse=True)
	#print(context['edu'])
	cursorObject.execute(Query3)
	context['exp']=sorted(cursorObject.fetchall(),key=getkey1,reverse=True)
	cursorObject.execute(Query4)
	context['ski']=cursorObject.fetchall()		# gets education ,skill and experience details
	#context['edu']=sorted(education.objects.filter(username=string),key=getkey1,reverse=True)
	#context['ski']=skills.objects.filter(username=string)
	#context['exp']=sorted(experience.objects.filter(username=string),key=getkey1,reverse=True)

	return render(request,'style4.html',context)

"""

def register_val(request):

	context={}

	if request.method == 'POST':				# check method of registration
		MyRegForm=RegisterForm(request.POST)
		#print("STEP 0")

		if MyRegForm.is_valid():				# check if form corresponds to valid values of model
			username = MyRegForm.cleaned_data['username']
			password1 = MyRegForm.cleaned_data['password1']
			password2 = MyRegForm.cleaned_data['password2']		# fetch values from form object

			if(password1 != password2):
				messages.info(request,"The passwords you entered did not match!")	# password check
				return redirect('/register')

			fn=MyRegForm.cleaned_data['fname']
			ln=MyRegForm.cleaned_data['lname']
			email=MyRegForm.cleaned_data['Email']
			mob=MyRegForm.cleaned_data['mobile']
			link=MyRegForm.cleaned_data['linked']
			git=MyRegForm.cleaned_data['git']
			lang=MyRegForm.cleaned_data['lang']
			tmp=Profile.objects.filter(username=username)
			
			if len(tmp) != 0 :									# checks if username already exists 

				messages.info(request,"The username "+username+" has already been used.")
				return redirect('/register')

			obj=Profile(username=username,fname=fn,lname=ln,email=email,mob=mob,link_in=link,github=git,lang=lang)
			obj.save()											# create object.
			user = User.objects.create_user(username, email, password1)
			user.first_name=fn
			user.last_name=ln
			user.save()											# create user
			context['fname']=fn
			context['lname']=ln
			
			#print("STEP 1")


	else:
		MyLoginForm=LoginForm()
		#print("STEP 3")

	#print("STEP 4")
	return render(request,'success.html',context)

def add_edu(request):

	if not request.user.is_authenticated:						#add education field

		return redirect('/403')

	usr=Profile.objects.get(username=request.user.username)

	if request.method == 'POST':
		MyRegForm=EduForm(request.POST)
		#print("STEP 0")

		if MyRegForm.is_valid():
			inst = MyRegForm.cleaned_data['instname']
			sy=MyRegForm.cleaned_data['syear']
			ey=MyRegForm.cleaned_data['eyear']
			deg=MyRegForm.cleaned_data['deg']
			scr=MyRegForm.cleaned_data['score']

			obj=education(user=usr,insti_name=inst,s_year=sy,e_year=ey,degree=deg,score=scr)
			obj.save()

	else:
		MyRegForm=EduForm()

	return redirect('/dashboard')

def add_exp(request):										#add experience field

	if not request.user.is_authenticated:

		return redirect('/403')

	usr=Profile.objects.get(username=request.user.username)

	if request.method == 'POST':
		MyRegForm=ExpForm(request.POST)
		#print("STEP 0")

		if MyRegForm.is_valid():
			comp = MyRegForm.cleaned_data['comp']
			title=MyRegForm.cleaned_data['title']
			sy=MyRegForm.cleaned_data['syear']
			ey=MyRegForm.cleaned_data['eyear']
			wrk=MyRegForm.cleaned_data['work']

			obj=experience(user=usr,company=comp,title=title,s_year=sy,e_year=ey,work=wrk)
			obj.save()

	else:
		MyRegForm=ExpForm()

	return redirect('/dashboard')

def add_skill(request):										# add skills

	if not request.user.is_authenticated:

		return redirect('/403')

	usr=Profile.objects.get(username=request.user.username)

	if request.method == 'POST':
		MyRegForm=SkillForm(request.POST)
		#print("STEP 0")

		if MyRegForm.is_valid():
			skill = MyRegForm.cleaned_data['skill']

			obj=skills(user=usr,skill=skill)
			obj.save()

	else:
		MyRegForm=SkillForm()

	return redirect('/dashboard')
