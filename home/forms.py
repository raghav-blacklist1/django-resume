from django import forms

class LoginForm(forms.Form):

   username = forms.CharField(max_length = 100)
   password = forms.CharField(widget = forms.PasswordInput())

class RegisterForm(forms.Form):

   fname = forms.CharField(max_length = 100)
   lname = forms.CharField(max_length = 100)
   username = forms.CharField(max_length = 100)
   Email = forms.CharField(max_length = 100)
   password1 = forms.CharField(widget = forms.PasswordInput())
   password2 = forms.CharField(widget = forms.PasswordInput())
   mobile = forms.IntegerField()
   linked = forms.CharField(max_length = 100)
   git = forms.CharField(max_length = 100)
   lang = forms.CharField(max_length = 100)

class UpdateProfileForm(forms.Form):

   fname = forms.CharField(max_length = 100)
   lname = forms.CharField(max_length = 100)
   Email = forms.CharField(max_length = 100)
   mobile = forms.IntegerField()
   linked = forms.CharField(max_length = 100)
   git = forms.CharField(max_length = 100)
   lang = forms.CharField(max_length = 100)

class EduForm(forms.Form):

	instname = forms.CharField(max_length = 100)
	syear = forms.IntegerField()
	eyear = forms.IntegerField()
	deg = forms.CharField(max_length = 100)
	score = forms.CharField(max_length = 100)

class UpdateEduForm(forms.Form):

   Id = forms.IntegerField()
   instname = forms.CharField(max_length = 100)
   syear = forms.IntegerField()
   eyear = forms.IntegerField()
   deg = forms.CharField(max_length = 100)
   score = forms.CharField(max_length = 100)

class ExpForm(forms.Form):

	comp = forms.CharField(max_length = 100)
	title = forms.CharField(max_length = 100)
	syear = forms.IntegerField()
	eyear = forms.IntegerField()
	work = forms.CharField(max_length = 100)

class SkillForm(forms.Form):

	skill = forms.CharField(max_length = 100)