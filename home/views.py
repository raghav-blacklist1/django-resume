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

		context = {
	        'is_authenticated': True,
	        'username': request.user.username,
	        'firstname': request.user.first_name,
	        'lastname': request.user.last_name
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
	

def logout_page(request):

    logout(request)
    return redirect('/')

def dash(request):

	context={'is_authenticated':False}
	if request.user.is_authenticated:

		context = {
	        'is_authenticated': True,
	        'username': request.user.username,
	        'firstname': request.user.first_name,
	        'lastname': request.user.last_name,
	        'ondashboard': True
    	}
		return render(request, 'dash.html', context)

	return redirect('/403')

def getkey(item):

	return item.fname.lower()

def getkey1(item):

	return item.e_year

def people(request):

	context={'is_authenticated':False}
	if request.user.is_authenticated:

		context = {
	        'is_authenticated': True,
	        'username': request.user.username,
	        'firstname': request.user.first_name,
	        'lastname': request.user.last_name,
	        'people': sorted(Profile.objects.all(), key=getkey),
	        'onpeople': True
    	}
		return render(request, 'people.html', context)

	return redirect('/403')

def editmainfields(request):

	context={'is_authenticated':False}
	if request.user.is_authenticated:

		username = request.user.username
		user = Profile.objects.get(username=username)
		context = {
	        'is_authenticated': True,
	        'username': request.user.username,
	        'firstname': request.user.first_name,
	        'lastname': request.user.last_name,
	        'user': user,
	        'onfields': True,
	        'onmainfield': True
    	}
		return render(request, 'fields_main.html', context)

	return redirect('/403')

@require_POST
def submitmainfields(request):

	context={}
	print("here0")

	if request.method == 'POST':
		print("here1")
		MyForm=UpdateProfileForm(request.POST)

		if MyForm.is_valid():
			print("here2")
			username = request.user.username

			fn=MyForm.cleaned_data['fname']
			ln=MyForm.cleaned_data['lname']
			print(ln)
			email=MyForm.cleaned_data['Email']
			mob=MyForm.cleaned_data['mobile']
			link=MyForm.cleaned_data['linked']
			git=MyForm.cleaned_data['git']
			lang=MyForm.cleaned_data['lang']
			Profile.objects.filter(pk=username).update(fname = fn, lname = ln, email = email, mob = mob, link_in = link, github = git, lang = lang)
			messages.info(request,"Fields updated Successfully!!")		

	else:
		print("here")

	return redirect("/editprofile/main")

def editedufields(request):

	context={'is_authenticated':False}
	if request.user.is_authenticated:

		username = request.user.username
		user = Profile.objects.get(username=username)
		edufields = sorted(user.education_set.all(),key=getkey1,reverse=True)
		context = {
	        'is_authenticated': True,
	        'username': request.user.username,
	        'firstname': request.user.first_name,
	        'lastname': request.user.last_name,
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

			username = request.user.username
			user = Profile.objects.get(username=username)

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
			username = request.user.username
			user = Profile.objects.get(username=username)

			if edu_object.user == user:

				MyForm=EduForm(request.POST)

				if MyForm.is_valid():
					inst = MyForm.cleaned_data['instname']
					sy=MyForm.cleaned_data['syear']
					ey=MyForm.cleaned_data['eyear']
					deg=MyForm.cleaned_data['deg']
					scr=MyForm.cleaned_data['score']
					education.objects.filter(pk=edu_id).update(insti_name=inst,s_year=sy,e_year=ey,degree=deg,score=scr)
					messages.info(request,"Fields updated Successfully!!")		

	else:
		pass

	return redirect("/editprofile/education")

def editexpfields(request):

	context={'is_authenticated':False}
	if request.user.is_authenticated:

		username = request.user.username
		user = Profile.objects.get(username=username)
		expfields = sorted(user.experience_set.all(),key=getkey1,reverse=True)
		context = {
	        'is_authenticated': True,
	        'username': request.user.username,
	        'firstname': request.user.first_name,
	        'lastname': request.user.last_name,
	        'expfields': expfields,
	        'onfields': True,
	        'onexpfield': True
    	}
		return render(request, 'fields_exp.html', context)

	return redirect('/403')

@require_POST
def expfielddelete(request):

	if request.method == 'POST':
		
		edu_id = request.POST['id']
		edu_object = experience.objects.get(pk=edu_id)

		if request.user.is_authenticated:

			username = request.user.username
			user = Profile.objects.get(username=username)

			if edu_object.user == user:

				edu_object.delete()
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
			username = request.user.username
			user = Profile.objects.get(username=username)

			if exp_object.user == user:

				MyForm=ExpForm(request.POST)

				if MyForm.is_valid():

					comp = MyForm.cleaned_data['comp']
					title=MyForm.cleaned_data['title']
					sy=MyForm.cleaned_data['syear']
					ey=MyForm.cleaned_data['eyear']
					wrk=MyForm.cleaned_data['work']
					experience.objects.filter(pk=exp_id).update(company=comp,title=title,s_year=sy,e_year=ey,work=wrk)
					messages.info(request,"Fields updated Successfully!!")		

	else:
		pass

	return redirect("/editprofile/experience")

def editskillfields(request):

	context={'is_authenticated':False}
	if request.user.is_authenticated:

		username = request.user.username
		user = Profile.objects.get(username=username)
		skillfields = user.skills_set.all()
		context = {
	        'is_authenticated': True,
	        'username': request.user.username,
	        'firstname': request.user.first_name,
	        'lastname': request.user.last_name,
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

			username = request.user.username
			user = Profile.objects.get(username=username)

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

				MyForm=SkillForm(request.POST)

				if MyForm.is_valid():

					skill = MyForm.cleaned_data['skill']
					skills.objects.filter(pk=skill_id).update(skill=skill)
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
		usr=Profile.objects.get(username=string)
		context['obj']=Profile.objects.get(username=string)
	except:
		return redirect('/404')
	context['edu']=sorted(usr.education_set.all(),key=getkey1,reverse=True)
	context['ski']=usr.skills_set.all()
	context['exp']=sorted(usr.experience_set.all(),key=getkey1,reverse=True)

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
		context['obj']=Profile.objects.get(username=string)
	except:
		return redirect('/404')
	context['edu']=sorted(usr.education_set.all(),key=getkey1,reverse=True)
	context['ski']=usr.skills_set.all()
	context['exp']=sorted(usr.experience_set.all(),key=getkey1,reverse=True)

	return render(request,'style4.html',context)

def dtemp4(request,string):

	my_url = request.get_host() + '/temp4/' + string
	pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
	print(my_url)
	pdf = pdfkit.from_url(my_url, False)
	response = HttpResponse(pdf,content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="{0}_4.pdf"'.format(string)

	return response

def register_val(request):

	context={}

	if request.method == 'POST':
		MyRegForm=RegisterForm(request.POST)

		if MyRegForm.is_valid():
			username = MyRegForm.cleaned_data['username']
			password1 = MyRegForm.cleaned_data['password1']
			password2 = MyRegForm.cleaned_data['password2']

			if(password1 != password2):
				messages.info(request,"The passwords you entered did not match!")
				return redirect('/register')

			fn=MyRegForm.cleaned_data['fname']
			ln=MyRegForm.cleaned_data['lname']
			email=MyRegForm.cleaned_data['Email']
			mob=MyRegForm.cleaned_data['mobile']
			link=MyRegForm.cleaned_data['linked']
			git=MyRegForm.cleaned_data['git']
			lang=MyRegForm.cleaned_data['lang']
			tmp=Profile.objects.filter(username=username)
			
			if len(tmp) != 0 :

				messages.info(request,"The username "+username+" has already been used.")
				return redirect('/register')

			obj=Profile(username=username,fname=fn,lname=ln,email=email,mob=mob,link_in=link,github=git,lang=lang)
			obj.save()
			user = User.objects.create_user(username, email, password1)
			user.first_name=fn
			user.last_name=ln
			user.save()
			context['fname']=fn
			context['lname']=ln

	else:
		MyLoginForm=LoginForm()

	return render(request,'success.html',context)

def add_edu(request):

	if not request.user.is_authenticated:

		return redirect('/403')

	usr=Profile.objects.get(username=request.user.username)

	if request.method == 'POST':
		MyRegForm=EduForm(request.POST)

		if MyRegForm.is_valid():
			inst = MyRegForm.cleaned_data['instname']
			sy=MyRegForm.cleaned_data['syear']
			ey=MyRegForm.cleaned_data['eyear']
			deg=MyRegForm.cleaned_data['deg']
			scr=MyRegForm.cleaned_data['score']

			obj=education(user=usr,insti_name=inst,s_year=sy,e_year=ey,degree=deg,score=scr)
			obj.save()
			messages.info(request,"Field Added Successfully!!")

	else:
		MyRegForm=EduForm()

	return redirect('/editprofile/education')

def add_exp(request):

	if not request.user.is_authenticated:

		return redirect('/403')

	usr=Profile.objects.get(username=request.user.username)

	if request.method == 'POST':
		MyRegForm=ExpForm(request.POST)

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

	return redirect('/editprofile/experience')

def add_skill(request):

	if not request.user.is_authenticated:

		return redirect('/403')

	usr=Profile.objects.get(username=request.user.username)

	if request.method == 'POST':
		MyRegForm=SkillForm(request.POST)

		if MyRegForm.is_valid():
			skill = MyRegForm.cleaned_data['skill']

			obj=skills(user=usr,skill=skill)
			obj.save()

	else:
		MyRegForm=SkillForm()

	return redirect('/dashboard')
