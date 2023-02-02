from django.shortcuts import render, redirect
from django.contrib.auth import login , logout ,authenticate
from .models import Profile
from django.contrib import messages
from .forms import CostomUserCreationForm, ProfileForm, SkillForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "this username does not exsit")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'username or password is incorrect')

    return render(request, 'users/login_register.html')


def logoutPage(request):
    logout(request)
    messages.info(request, 'the user successfully logouted')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CostomUserCreationForm()
    if request.method == 'POST':
        form = CostomUserCreationForm(request.POST)
        if form.is_valid():
            user = form .save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'user account was created')

            login(request, user)
            return redirect('edit-account')

        else:
            messages.error(request, 'user can not registered')
    context ={'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)

def profiles_view(request):  
    profiles = Profile.objects.all()
    context ={'profiles': profiles}
    return render(request, 'users/profiles.html', context )


def userProfile(request,pk):
    profile = Profile.objects.get(pk=pk)
    topSkill = profile.skill_set.exclude(description__exact="")
    otherSkill = profile.skill_set.filter(description="")
    context = {
        'profile':profile,
        'topSkill':topSkill,
        'otherSkill':otherSkill
    
    }
    return render(request, 'users/user_profile.html', context)


@login_required(login_url="login")
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {
        'profile':profile,
        'skills':skills,
        'projects':projects
    }
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
        
    context = {
        'form': form
    }
    return render(request, 'users/profile_form.html' , context)



def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method =='POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            return redirect('account')
       

    context = {
        'form': form

    }
    return render(request, 'users/skill_form.html', context)