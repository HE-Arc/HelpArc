from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib import messages
from .forms import profileRegisterForm, userRegisterForm, registerTechnology, registerClass
import logging
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from HelpArcApp.models import Technology, Class

logger = logging.getLogger("__name__")

def register(request):
    if request.method == 'POST':
        user_form = userRegisterForm(request.POST)
        profile_form = profileRegisterForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            
            #Django user
            user = user_form.save()
            
            #Custom profile
            profile = profile_form.save(commit=False)
            profile.user = user

            if profile_form.cleaned_data['is_prof']:
                profile.asked_helper = True
            else:
                profile.asked_helper = False

            profile.save()
            
            return redirect('index')
    else:
        user_form = userRegisterForm()
        profile_form = profileRegisterForm()
    return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def admin_dashboard(request):
    context = {}

    if request.user.profile.accountLevel != 2:
        # add message not admin
        return redirect('index')

    return render(request, 'users/admin_dashboard.html', context)

@login_required
def admin_helper_request_accept(request):
    context = {}

    if request.user.profile.accountLevel != 2:
        # add message not admin
        return redirect('index')

    id = request.POST.get('id', None)
    data = { 'result':True, 'message':"This exist" }

    helper = User.objects.filter(id=id).first()
    if helper is None:
        return JsonResponse({ 'result' : False, 'message':"This id doesn't exist" })

    helper.profile.accountLevel = 1
    helper.profile.asked_helper = False
    helper.profile.is_complete = False
    helper.profile.save()

    return JsonResponse(data)

@login_required
def admin_helper_request_reject(request):
    context = {}

    if request.user.profile.accountLevel != 2:
        # add message not admin
        return redirect('index')

    id = request.POST.get('id', None)
    data = { 'result':True, 'message':"This exist" }

    helper = User.objects.filter(id=id).first()
    if helper is None:
        return JsonResponse({ 'result' : False, 'message':"This id doesn't exist" })

    
    helper.profile.asked_helper = False
    helper.profile.save()

    return JsonResponse(data)

@login_required
def admin_helper_requests(request):
    if request.user.profile.accountLevel != 2:
        # add message not admin
        return redirect('index')

    context = {}
    helpers = User.objects.filter(profile__accountLevel= 1)
    ask_helpers = User.objects.filter(profile__asked_helper=True)

    context['helpers'] = helpers
    context['ask_helpers'] = ask_helpers

    res = render_to_string(request=request, template_name='users/admin_helpers.html', context=context)
    data = {'result':True, 'html': res}
    return JsonResponse(data)

@login_required
def admin_technologies(request):
    if request.user.profile.accountLevel != 2:
        # add message not admin
        return redirect('index')

    context = {}
    technologies = Technology.objects.all()
    for techs in technologies:
        print(techs.id)
    context['technologies'] = technologies
    context['form'] = registerTechnology()
    res = render_to_string(request=request, template_name='users/admin_technologies.html', context=context)
    data = {'result':True, 'html': res}
    return JsonResponse(data)

@login_required
def admin_classes(request):
    if request.user.profile.accountLevel != 2:
        # add message not admin
        return redirect('index')

    context = {}
    classes = Class.objects.all()

    context['classes'] = classes
    context['form'] = registerClass()
    res = render_to_string(request=request, template_name='users/admin_classes.html', context=context)
    data = {'result':True, 'html': res}
    return JsonResponse(data)

@login_required
def admin_helper_revoke(request):
    if request.user.profile.accountLevel != 2:
        # add message not admin
        return redirect('index')

    id = request.POST.get('id', None)
    data = { 'result':True, 'message':"This exist" }

    helper = User.objects.filter(id=id).first()
    if helper is None:
        return JsonResponse({ 'result' : False, 'message':"This id doesn't exist" })

    
    helper.profile.accountLevel = 0
    helper.profile.save()

    return JsonResponse(data)

@login_required
def admin_technology_add(request):

    if request.user.profile.accountLevel != 2:
        # add message not admin
        return redirect('index')

    if request.POST:
        technology_form = registerTechnology(request.POST, request.FILES)
        
        if technology_form.is_valid():
            technology_form.save()

            return JsonResponse( { 'res':True })
    

    return JsonResponse({ 'res': False })

@login_required
def admin_technology_delete(request):

    if request.user.profile.accountLevel != 2:
        # add message not admin
        return redirect('index')

    id = request.POST.get('id', None)
    data = { 'result':True, 'message':"This exist" }

    tech = Technology.objects.filter(id=id).first()
  
    if tech is None:
        return JsonResponse({ 'result' : False, 'message':"This id doesn't exist" })

    
    tech.delete()

    return JsonResponse(data)


@login_required
def admin_class_add(request):

    if request.user.profile.accountLevel != 2:
        # add message not admin
        return redirect('index')

    if request.POST:
        class_form = registerClass(request.POST, request.FILES)
        
        if class_form.is_valid():
            class_form.save()

            return JsonResponse( { 'res':True })
    

    return JsonResponse({ 'res': False })

@login_required
def admin_class_delete(request):
    if request.user.profile.accountLevel != 2:
        # add message not admin
        return redirect('index')

    id = request.POST.get('id', None)
    data = { 'result':True, 'message':"This exist" }

    classe = Class.objects.filter(id=id).first()
  
    if classe is None:
        return JsonResponse({ 'result' : False, 'message':"This id doesn't exist" })

    
    classe.delete()

    return JsonResponse(data)