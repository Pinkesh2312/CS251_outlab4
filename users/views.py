from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .data import profile_info
from django.contrib.auth.models import User
from .models import Profile, Repository
from django.utils.timezone import now
import requests
from requests.exceptions import Timeout

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            data = profile_info(username)
            profile = Profile(username = username, followers = data["followers"], lastUpdated = now, user = User.objects.get(username = username))
            profile.save()
            for repo in data["repos"].keys():
                repository = Repository(name = repo, stars = data["repos"][repo], profile = profile)
                repository.save()

            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def home(request):
    users = Profile.objects.all()
    context = {"users":users, "current_user":Profile.objects.get(user= request.user)}
    return render(request, 'users/home.html', context= context)

@login_required
def display_profile(request, profile_id):
    if request.method == "POST":
        profile = Profile.objects.get(id=profile_id)
        data = profile_info(profile.username)
        profile.lastUpdated = now()
        profile.followers = data["followers"]
        profile.save()
        repositories = Repository.objects.filter(profile = profile)
        for repo in repositories:
            repo.stars = data["repos"][repo.name]
            repo.save()
        context = {"profile":profile, "current_user":request.user, "repositories":repositories, "current_profile":Profile.objects.get(user= request.user)}
        return render(request, 'users/profile.html', context = context)
    profile = Profile.objects.get(id=profile_id)
    repositories = Repository.objects.filter(profile = profile)
    context = {"profile":profile, "current_user":request.user, "repositories":repositories, "current_profile":Profile.objects.get(user= request.user)}
    return render(request, 'users/profile.html', context = context)
