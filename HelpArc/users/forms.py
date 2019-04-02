from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile
from HelpArcApp.models import Technology, Class, Title
import copy

# Registration
class profileRegisterForm(forms.ModelForm):
    #userClass = forms.ChoiceField(required=False, label="Classe")
    picture = forms.ImageField(required=False, label="Photo de profil")
    is_prof = forms.BooleanField(required=False, label="Je suis un professeur")
    class Meta():
        model = Profile
        fields = ('picture', )#'userClass', )      

class userRegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="Prénom")
    last_name = forms.CharField(required=True, label="Nom")
    email = forms.EmailField(required=True)
    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


# Update for profile
class profileUpdateForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ('picture', 'classId', )

class userUpdateForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('first_name', 'last_name')

# Update for account
class accountUpdateForm(UserCreationForm):
    class Meta():
        model = User
        fields = ('email', 'password1', 'password2')
        #fields = ('email', 'password1', 'password2')

# Update for Helper
class HelperUpdateForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ('titleId', )#'skills')


# Registration non-user
class registerTechnology(forms.ModelForm):
    name = forms.CharField(required=True, label='Nom')
    logo = forms.ImageField(required=False, label="Logo")
    class Meta():
        model = Technology
        fields = ('name', 'logo')

class registerClass(forms.ModelForm):
    name = forms.CharField(required=True, label='Nom')
    class Meta():
        model = Class
        fields = ('name',)

class registerTitle(forms.ModelForm):
    name = forms.CharField(required=True, label='Nom')
    class Meta():
        model = Title   
        fields = ('name',)