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
from .models import Technology, SkillLevels, Message, Request, Title
from django.http import JsonResponse
from users.forms import profileUpdateForm, userUpdateForm, accountUpdateForm
from django.http import JsonResponse
from django.contrib import messages as dMessage


def check_is_completed(request):
    # Check if user is a helper without completed profile
    current_user_profile = request.user.profile
    if current_user_profile.accountLevel == 1 and not current_user_profile.is_complete:
        dMessage.warning(request, "Pour pouvoir utiliser pleinement notre site en tant qu'Helper, veuillez compléter votre profil sous Profil > Helper.")


@login_required
def index(request):
    most_requested = User.objects.filter(profile__accountLevel='1') # Get most requested
    
    check_is_completed(request)
    
    context = {'users': most_requested}
    return render(request, 'index.html', context)

@login_required
def profile(request):

    check_is_completed(request)

    context = {}
    context['profile_profileform'] = profileUpdateForm(instance=request.user.profile)
    context['profile_userform'] = userUpdateForm(instance=request.user)

    SkillsFormSet = modelformset_factory(SkillLevels, form=SkillsForm)
    context['form'] = SkillsFormSet(queryset=SkillLevels.objects.filter(userId=request.user))
    context['UserTitleForm'] = UserTitleForm(instance=request.user.profile)

    return render(request, 'profile.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_form = profileUpdateForm(request.POST, request.FILES)
        #user_form = userUpdateForm(request.POST)
        if profile_form.is_valid():# and user_form.is_valid():
            user = request.user
            profile = user.profile

            # We need to manually update the 
            profile.classId = profile_form.cleaned_data['classId']
            if profile_form.cleaned_data['picture'] is not 'default.png':
                profile.classId = profile_form.cleaned_data['classId']
            
            profile.save()
            #user_form.save()
            #profile_form.save()
            

            return JsonResponse({'res': True})
        else:
            return JsonResponse({'res': False})



@login_required
def update_account(request):
    if request.method == 'POST':
        
        form = request.POST;
        if form['mail'] != None:
            user = request.user
            user.email = form['mail']
            user.save()

            return JsonResponse({'res': True})
        

    return JsonResponse({'res': False})

@login_required
def update_helper(request):

    if request.method == 'POST':
        SkillsFormSet = modelformset_factory(SkillLevels, form=SkillsForm)
        # create a form instance and populate it with data from the request:
        formSet = SkillsFormSet(request.POST)
        titleForm = UserTitleForm(request.POST)
        #Checking the if the form is valid
        if formSet.is_valid() and titleForm.is_valid():
            request.user.profile.is_complete = True
            request.user.profile.titleId = Title.objects.filter(id=titleForm.cleaned_data['titleId'].id).first()
            request.user.profile.save()
            
            #To save we have loop through the formset
            for skill in formSet:
                #Saving in the skill models	
                s = skill.cleaned_data['id']
                if s is None:
                    s = SkillLevels()
                
                s.userId = request.user
                s.level = skill.cleaned_data['level']
                s.technologyId = skill.cleaned_data['technologyId']
                s.save()
            # context['form'] = SkillsFormSet(request.POST)
            # context['UserTitleForm'] = UserTitleForm(request.POST, instance=current_user)
            #return render(request, 'completeprofile.html', context)


            return JsonResponse({ 'res':True })
        # else:            
        #     context={
        #             'contact_form': SkillsFormSet(),
        #             'error' : formSet.errors,
        #             }
        #     return render(request, 'completeprofile.html', context)
        return JsonResponse( { 'res': False })
        
    # elif request.method == 'GET':
    #     context['form'] = SkillsFormSet(queryset=SkillLevels.objects.filter(userId=current_user))
    #     context['UserTitleForm'] = titleForm
    #     return render(request, 'completeprofile.html', context)


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
        if messageForm.is_valid():
            message = messageForm.save(commit=False)
            message.requestId = helpRequest
            message.senderId = request.user
            message.save()
        return render(request, 'request.html', context)
    
    
    if request.method == 'GET':        
        return render(request, 'request.html', context)

@login_required
def myRequests(request):
    context = {}  
    
    current_user_profile = request.user.profile
    if current_user_profile.accountLevel == 1 and not current_user_profile.is_complete:
        myHelpRequests = Request.objects.filter(helperId=request.user)
    elif current_user_profile.accountLevel == 0:
        myHelpRequests = Request.objects.filter(studentId=request.user)        
    else:
        return redirect('index')
    context['helpRequests'] = myHelpRequests
    return render(request, 'myRequests.html', context)