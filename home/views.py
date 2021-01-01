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
from django.views.decorators.http import require_POST
import pdfkit

def HomePage(request):

	context={'is_authenticated':False}
	if request.user.is_authenticated:

		profile = Profile.objects.get(user_auth = request.user)
		context = {
	        'is_authenticated': True,
	        'profile': profile
    	}
	
	return render(request, 'home.html', context)

def login_page(request):

	context={}
	if request.user.is_authenticated:
		return redirect('/dashboard')

	return render(request, 'login.html', context)

def login_request(request):

	context={}
	username = "not logged in"

	if request.method == 'POST':
		MyLoginForm=LoginForm(request.POST)

		if MyLoginForm.is_valid():
			username = MyLoginForm.cleaned_data['username']
			password = MyLoginForm.cleaned_data['password']
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('/dashboard')

			else:
				messages.info(request,"Invalid Username or Password!")


	else:
		MyLoginForm=LoginForm()

	return redirect('/login')

@require_POST
def register_val(request):

	context={}

	if request.method == 'POST':
		MyUserForm=UserForm(request.POST)

		if MyUserForm.is_valid():
			
			tmp=User.objects.filter(username=MyUserForm.cleaned_data['username'])
			
			if len(tmp) != 0 :

				messages.info(request,"The username "+MyUserForm.cleaned_data['username']+" has already been used.")
				return redirect('/register')

			MyUserForm.save()
			user_auth = User.objects.get(username = MyUserForm.cleaned_data['username'])
			MyProfileForm = ProfileForm(request.POST)
			
			if MyProfileForm.is_valid():

				MyProfileForm.save(user_auth)
				messages.info(request,"You have been registered successfully!!")
				redirect("/")

			else:

				messages.info(request,"Registration Successful.. Please login to complete your profile")
				redirect("/")

		else:

			messages.info(request,MyUserForm.errors)
			redirect("/")
	else:
		MyLoginForm=LoginForm()

	return redirect("/")
	

def logout_page(request):

    logout(request)
    return redirect('/')

def dash(request):

	context={'is_authenticated':False}
	if request.user.is_authenticated:

		profile = Profile.objects.get(user_auth = request.user)
		print(profile)
		context = {
	        'is_authenticated': True,
	        'profile': profile,
	        'ondashboard': True
    	}
		return render(request, 'dash.html', context)

	return redirect('/403')

def getkey(item):

	return item.first_name.lower()

def getkey1(item):

	return item.e_year

def people(request):

	context={'is_authenticated':False}
	if request.user.is_authenticated:

		profile = Profile.objects.get(user_auth = request.user)
		context = {
	        'is_authenticated': True,
	        'profile': profile,
	        'people': sorted(Profile.objects.all(), key=getkey),
	        'onpeople': True
    	}
		return render(request, 'people.html', context)

	return redirect('/403')

def editmainfields(request):

	context={'is_authenticated':False}
	if request.user.is_authenticated:

		profile = Profile.objects.get(user_auth = request.user)
		context = {
	        'is_authenticated': True,
	        'profile': profile,
	        'onfields': True,
	        'onmainfield': True
    	}
		return render(request, 'fields_main.html', context)

	return redirect('/403')

@require_POST
def submitmainfields(request):

	context={}

	if request.method == 'POST':
		profile = Profile.objects.get(user_auth = request.user)
		MyForm=ProfileForm(request.POST, instance = profile)

		if MyForm.is_valid():
			
			MyForm.save(profile.user_auth)
			messages.info(request,"Fields updated Successfully!!")		

	else:
		print("here")

	return redirect("/editprofile/main")

@require_POST
def add_edu(request):

	if not request.user.is_authenticated:

		return redirect('/403')

	profile=Profile.objects.get(user_auth=request.user)

	if request.method == 'POST':
		MyRegForm=EduForm(request.POST)

		if MyRegForm.is_valid():

			MyRegForm.save(profile)
			messages.info(request,"Field Added Successfully!!")

	else:
		MyRegForm=EduForm()

	return redirect('/editprofile/education')

def editedufields(request):

	context={'is_authenticated':False}
	if request.user.is_authenticated:

		profile = Profile.objects.get(user_auth = request.user)
		edufields = sorted(profile.education_set.all(),key=getkey1,reverse=True)
		context = {
	        'is_authenticated': True,
	        'profile': profile,
	        'edufields': edufields,
	        'onfields': True,
	        'onedufield': True
    	}
		return render(request, 'fields_edu.html', context)

	return redirect('/403')

@require_POST
def edufielddelete(request):

	if request.method == 'POST':
		
		edu_id = request.POST['id']
		edu_object = education.objects.get(pk=edu_id)

		if request.user.is_authenticated:

			user = Profile.objects.get(user_auth=request.user)

			if edu_object.user == user:

				edu_object.delete()
				messages.info(request,"Field deleted Successfully!")
				return redirect("/editprofile/education")


	return redirect('/403')

@require_POST
def edufieldsubmit(request):

	context={}
	if request.method == 'POST':
		edu_id = request.POST['Id']
		edu_object = education.objects.get(pk=edu_id)

		if request.user.is_authenticated:
			user = Profile.objects.get(user_auth=request.user)

			if edu_object.user == user:

				MyForm=EduForm(request.POST,instance = edu_object)

				if MyForm.is_valid():
					
					MyForm.save(user)
					messages.info(request,"Fields updated Successfully!!")		

	else:
		pass

	return redirect("/editprofile/education")

@require_POST
def add_exp(request):

	if not request.user.is_authenticated:

		return redirect('/403')

	profile=Profile.objects.get(user_auth=request.user)

	if request.method == 'POST':
		MyRegForm=ExpForm(request.POST)

		if MyRegForm.is_valid():
			
			MyRegForm.save(profile)

	else:
		MyRegForm=ExpForm()

	return redirect('/editprofile/experience')

def editexpfields(request):

	context={'is_authenticated':False}
	if request.user.is_authenticated:

		profile = Profile.objects.get(user_auth = request.user)
		expfields = sorted(profile.experience_set.all(),key=getkey1,reverse=True)
		context = {
	        'is_authenticated': True,
	        'profile': profile,
	        'expfields': expfields,
	        'onfields': True,
	        'onexpfield': True
    	}
		return render(request, 'fields_exp.html', context)

	return redirect('/403')

@require_POST
def expfielddelete(request):

	if request.method == 'POST':
		
		exp_id = request.POST['id']
		exp_object = experience.objects.get(pk=exp_id)

		if request.user.is_authenticated:

			user = Profile.objects.get(user_auth = request.user)

			if exp_object.user == user:

				exp_object.delete()
				messages.info(request,"Field deleted Successfully!")
				return redirect("/editprofile/education")


	return redirect('/403')

@require_POST
def expfieldsubmit(request):

	context={}
	if request.method == 'POST':
		exp_id = request.POST['Id']
		exp_object = experience.objects.get(pk=exp_id)

		if request.user.is_authenticated:
			user = Profile.objects.get(user_auth=request.user)

			if exp_object.user == user:

				MyForm=ExpForm(request.POST, instance = exp_object)

				if MyForm.is_valid():

					MyForm.save(user)
					messages.info(request,"Fields updated Successfully!!")		

	else:
		pass

	return redirect("/editprofile/experience")

@require_POST
def add_skill(request):

	if not request.user.is_authenticated:

		return redirect('/403')

	profile=Profile.objects.get(user_auth=request.user)

	if request.method == 'POST':
		MyRegForm=SkillForm(request.POST)

		if MyRegForm.is_valid():
			
			MyRegForm.save(profile)

	else:
		MyRegForm=SkillForm()

	return redirect('/editprofile/skills')


def editskillfields(request):

	context={'is_authenticated':False}
	if request.user.is_authenticated:

		profile = Profile.objects.get(user_auth = request.user)
		skillfields = profile.skills_set.all()
		context = {
	        'is_authenticated': True,
	        'profile': profile,
	        'skillfields': skillfields,
	        'onfields': True,
	        'onskillfield': True
    	}
		return render(request, 'fields_skill.html', context)

	return redirect('/403')

@require_POST
def skillfielddelete(request):

	if request.method == 'POST':
		
		skill_id = request.POST['id']
		skill_object = skills.objects.get(pk=skill_id)

		if request.user.is_authenticated:

			user = Profile.objects.get(user_auth = request.user)

			if skill_object.user == user:

				skill_object.delete()
				messages.info(request,"Field deleted Successfully!")
				return redirect("/editprofile/skills")


	return redirect('/403')

@require_POST
def skillfieldsubmit(request):

	context={}
	if request.method == 'POST':
		skill_id = request.POST['Id']
		skill_object = skills.objects.get(pk=skill_id)

		if request.user.is_authenticated:
			username = request.user.username
			user = Profile.objects.get(username=username)

			if skill_object.user == user:

				MyForm=SkillForm(request.POST, instance = skill_object)

				if MyForm.is_valid():

					MyForm.save(user)
					messages.info(request,"Field updated Successfully!!")		

	else:
		pass

	return redirect("/editprofile/skills")

def denied_acc(request):

	return render(request,'403.html',{})

def no_res(request):

	return render(request,'404.html',{})


def register_page(request):

	if request.user.is_authenticated:
		return redirect('/dashboard')

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
		if string=='sample':
			string='parv1010'
		usr=User.objects.get(username=string)
		prof = Profile.objects.get(user_auth=usr)
		context['obj']=prof
	except:
		return redirect('/404')
	context['edu']=sorted(prof.education_set.all(),key=getkey1,reverse=True)
	context['ski']=prof.skills_set.all()
	context['exp']=sorted(prof.experience_set.all(),key=getkey1,reverse=True)

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
		usr=User.objects.get(username=string)
		prof = Profile.objects.get(user_auth=usr)
		context['obj']=prof
	except:
		return redirect('/404')
	context['edu']=sorted(prof.education_set.all(),key=getkey1,reverse=True)
	context['ski']=prof.skills_set.all()
	context['exp']=sorted(prof.experience_set.all(),key=getkey1,reverse=True)

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
		usr=User.objects.get(username=string)
		prof = Profile.objects.get(user_auth=usr)
		context['obj']=prof
	except:
		return redirect('/404')
	context['edu']=sorted(prof.education_set.all(),key=getkey1,reverse=True)
	context['ski']=prof.skills_set.all()
	context['exp']=sorted(prof.experience_set.all(),key=getkey1,reverse=True)

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
		usr=User.objects.get(username=string)
		prof = Profile.objects.get(user_auth=usr)
		context['obj']=prof
	except:
		return redirect('/404')
	context['edu']=sorted(prof.education_set.all(),key=getkey1,reverse=True)
	context['ski']=prof.skills_set.all()
	context['exp']=sorted(prof.experience_set.all(),key=getkey1,reverse=True)

	return render(request,'style4.html',context)

def dtemp4(request,string):

	my_url = request.get_host() + '/temp4/' + string
	pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
	print(my_url)
	pdf = pdfkit.from_url(my_url, False)
	response = HttpResponse(pdf,content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="{0}_4.pdf"'.format(string)

	return response