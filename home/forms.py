from django import forms
from home.models import *

class LoginForm(forms.Form):

   username = forms.CharField(max_length = 100)
   password = forms.CharField(widget = forms.PasswordInput())

class UserForm(forms.ModelForm):

   password = forms.CharField(widget = forms.PasswordInput())
   confirmpassword = forms.CharField(widget = forms.PasswordInput())
   class Meta:
        model = User
        fields = ('username', )

   def clean(self):

      super().clean()
      cd = self.cleaned_data
      password1 = cd.get("password")
      password2 = cd.get("confirmpassword")

      if password1 != password2:
        raise forms.ValidationError("Passwords did not match")

      return cd

   def save(self):
      user = super(UserForm, self).save(commit=False)
      user.set_password(self.cleaned_data["password"])
      user.save()
      return user

class ProfileForm(forms.ModelForm):

   class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'mob', 'link_in', 'github', 'lang')

   def save(self,user_auth):
      user = super(ProfileForm, self).save(commit=False)
      user.user_auth = user_auth 
      user.save()
      return user

class EduForm(forms.ModelForm):

   class Meta:
        model = education
        fields = ('insti_name', 's_year', 'e_year', 'degree', 'score')
	
   def clean(self):

      super().clean()
      cd = self.cleaned_data
      l = cd.get("s_year")
      r = cd.get("e_year")

      if l>r:
        raise forms.ValidationError("Start year can't be greater than End year")

      return cd

   def save(self,profile):
      user = super(EduForm, self).save(commit=False)
      user.user = profile
      user.save()
      return user

class ExpForm(forms.ModelForm):

   class Meta:
        model = experience
        fields = ('company', 'title', 's_year', 'e_year', 'work')

   def clean(self):

      super().clean()
      cd = self.cleaned_data
      l = cd.get("s_year")
      r = cd.get("e_year")

      if l>r:
        raise forms.ValidationError("Start year can't be greater than End year")

      return cd
   
   def save(self,profile):
      user = super(ExpForm, self).save(commit=False)
      user.user = profile
      user.save()
      return user

class SkillForm(forms.ModelForm):

   class Meta:
        model = skills
        fields = ('skill',)
   
   def save(self,profile):
      user = super(SkillForm, self).save(commit=False)
      user.user = profile
      user.save()
      return user