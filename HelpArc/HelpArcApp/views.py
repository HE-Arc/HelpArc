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
from .models import Technology, SkillLevels, Message, Request
from django.http import JsonResponse
from django.core import serializers
from django.template import Context, Template


import logging

logger = logging.getLogger("__name__")


@login_required
def index(request):
    most_requested = User.objects.filter(profile__accountLevel='1') # Get helpers
    technologies = Technology.objects.all()
    # Check if user is a helper without completed profile
    current_user_profile = request.user.profile
    if current_user_profile.accountLevel == 1 and not current_user_profile.is_complete:
        logger.error("Not completed")
        #create message to ask for completion

    #get most requested
    scores = [0]
    most_r = []
    for requested in most_requested:
        temp = SkillLevels.objects.filter(userId=requested.pk)
        temp_count = len(temp)
        if temp_count >= scores[0]:
            most_r.insert(0,requested)
        elif temp_count >= scores[1]:
            most_r.insert(1,requested)
        elif temp_count >= scores[2]:
            most_r.insert(2,requested)
    if len(most_r)>2:
        most_requested = most_r[:3]
    else:
        most_requested = most_r

    context = {'users': most_requested, 'techs': technologies}
    return render(request, 'index.html', context)

@login_required
def updateindex(request):
    helpers = User.objects.filter(profile__accountLevel='1')
    for i in range(len(request.GET)):
        techid = Technology.objects.filter(name=request.GET.get(str(i))).first()
        helpers = helpers.filter(skilllevels__technologyId=str(techid.pk))
        if not helpers.exists():
            helpers = None
            break

    if helpers == None:
        html = "<p>No qualified helper found for this search<p>"
    else:
        template = Template("{% for user in users %}{% include 'profile_card.html' with firstname=user.first_name lastname=user.last_name picture=user.profile.picture.url title=user.profile.titleId only %}{% endfor %}")
        context = Context({'users': helpers})
        html = template.render(context)

    data = {'helpers': html}
    return JsonResponse(data)

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
            message.senderId = request.user
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
                s = SkillLevels.objects.filter(userId=current_user, technologyId=preSaveSkill.technologyId)
                print(len(s))
                if len(s) > 0:
                    s.update(level=preSaveSkill.level)
                else:
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

@login_required
def helpRequest(request, id):
    context = {}    
    helpRequest = Request.objects.get(id=id)
    messageForm = MessageForm()
    messages = Message.objects.filter(requestId=helpRequest)

    context['messageForm'] = messageForm
    context['messages'] = messages
    context['helpRequest'] = helpRequest

    if request.method == 'POST':
        messageForm = MessageForm(request.POST)
        if messageForm.is_valid:
            message = messageForm.save(commit=False)
            message.requestId = helpRequest
            message.senderId = request.user
            message.save()
        return render(request, 'request.html', context)
    
    
    if request.method == 'GET':        
        return render(request, 'request.html', context)