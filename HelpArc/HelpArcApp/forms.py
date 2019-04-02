from django import forms
from .models import SkillLevels
from .models import Technology
from .models import Title
from .models import Profile
from .models import Message
from .models import Request
from django.forms.formsets import formset_factory

class SkillsForm(forms.ModelForm):
    class Meta():
        model= SkillLevels
        fields=['technologyId', 'level']
        labels = {
            'technologyId' : 'Technologie',
            'level' : 'Niveau',
        }
        widgets = {
            'technologyId': forms.Select(choices=Technology.objects.all(), attrs={'required' : True}),
            'level': forms.NumberInput(attrs={'max': 10, 'min': 0, 'value' : 0, 'required' : True})
        }

class UserTitleForm(forms.ModelForm):
    
    class Meta():
        model= Profile
        fields=['titleId']
        labels = {
            'titleId' : 'Titre',
        }
        widgets = {
            'titleId' : forms.Select(choices=Title.objects.all(), attrs={'required' : True})
        }

class MessageForm(forms.ModelForm):
    class Meta():
        model= Message
        fields=['content']
        labels = {
            'content' : 'Question',
        }
        widgets = {
            'content' : forms.Textarea(attrs={'placeholder' : "Entrez votre question"})
        }

class RequestForm(forms.ModelForm):
    class Meta():
        model= Request
        fields=['title', 'technologyId']
        labels = {
            'technologyId' : 'Technologie',
            'title' : 'Titre',
        }
        widgets = {
            'technologyId': forms.Select(choices=Technology.objects.all(), attrs={'required' : True}),
            'title': forms.TextInput(attrs={'placeholder' : "Entrez le titre"})
        }

#class SearchForm(forms.Form):
#    things = forms.ModelMultipleChoiceField(queryset=Technology.objects.all(), widget=ModelSelect2Mixin)
