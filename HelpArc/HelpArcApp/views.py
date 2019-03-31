from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic, View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from users.models import Profile
from django.contrib.auth.models import User

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
    if requested.accountLevel == 1 and requested.titleId is None:
        context = {'info': "bite"}
    else:    
        context = {'info': "ouais"}
    return render(request, 'askhelp.html', context)

@login_required
def completeprofile(request):
    context = {}
    return render(request, 'completeprofile.html', context)