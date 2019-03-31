from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic, View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from users.models import Profile
from django.contrib.auth.models import User
from .forms import SkillsForm, UserTitleForm, MessageForm, RequestForm
from django.forms import formset_factory
from django.forms.models import modelformset_factory
from .models import Technology, SkillLevels
from django.http import JsonResponse


import logging

logger = logging.getLogger("__name__")


@login_required
def index(request):
    most_requested = User.objects.filter(profile__accountLevel='1') # Get most requested
    
    # Check if user is a helper without completed profile
    current_user_profile = request.user.profile
    if current_user_profile.accountLevel == 1 and not current_user_profile.is_complete:
        logger.error("Not completed")
        #create message to ask for completion

    context = {'users': most_requested}
    return render(request, 'index.html', context)

@login_required
def profile(request):
    context = {}
    return render(request, 'profile.html', context)

@login_required
# askhelp/user_id
def askhelp(request, id):
    requested = Profile.objects.get(id=id)
    context = {}
    '''if requested.accountLevel == 1 and requested.titleId is None:
        context = {'info': "bite"}
    else:    
        context = {'info': "ouais"}
    return render(request, 'askhelp.html', context)'''
    requestForm = RequestForm()
    messageForm = MessageForm()
    if request.method == 'GET':
        context = {}
        context['requestForm'] = requestForm
        context['messageForm'] = messageForm
        return render(request, 'askhelp.html', context)
    if request.method == 'POST':
        requestForm = RequestForm(request.POST)
        messageForm = MessageForm(request.POST)
        if requestForm.is_valid and messageForm.is_valid:
            helpRequest = requestForm.save(commit=False)
            helpRequest.studentId = request.user
            helpRequest.helperId = requested.user
            helpRequest.read = False
            helpRequest.closed = False
            helpRequest.save()

            message = messageForm.save(commit=False)
            message.requestId = helpRequest
            message.save()
        return render(request, 'index.html', context)
    return render(request, 'completeprofile.html', context)



@login_required
def completeprofile(request):
    try:
        current_user = request.user
        profile = Profile.objects.filter(user=request.user).first()
        #user = CustomUser.objects.get(user_name=current_user)
    except Exception:
        return render(request, 'users/login.html', {})
    context = {}    
    SkillsFormSet = modelformset_factory(SkillLevels, form=SkillsForm)
    titleForm = UserTitleForm(instance=profile)
    if request.method == 'POST':
        
        # create a form instance and populate it with data from the request:
        formSet = SkillsFormSet(request.POST)
        titleForm = UserTitleForm(request.POST, instance=profile)
        #Checking the if the form is valid
        if formSet.is_valid() and titleForm.is_valid():
            titleForm.save()
            #To save we have loop through the formset
            for skill in formSet:
                #Saving in the skill models	
                preSaveSkill = skill.save(commit=False)
                preSaveSkill.userId = current_user
                preSaveSkill.save()
            context['form'] = SkillsFormSet(request.POST)
            context['UserTitleForm'] = UserTitleForm(request.POST, instance=current_user)
            return render(request, 'completeprofile.html', context)
        else:            
            context={
                    'contact_form': SkillsFormSet(),
                    'error' : formSet.errors,
                    }
            return render(request, 'completeprofile.html', context)
        
    elif request.method == 'GET':
        context['form'] = SkillsFormSet(queryset=SkillLevels.objects.filter(userId=current_user))
        context['UserTitleForm'] = titleForm
        return render(request, 'completeprofile.html', context)
