from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .data import profile_info
from django.contrib.auth.models import User
from .models import Profile, Repository
import requests
from requests.exceptions import Timeout

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            data = profile_info(username)
            profile = Profile(username = username, followers = data["followers"], lastUpdated = data["last_updated"], user = User.objects.get(username = username))
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
    context = {"users":users}
    return render(request, 'users/home.html', context= context)

@login_required
def display_profile(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    context = {"profile":profile, "current_user":request.user}
    return render(request, 'users/profile.html', context = context)
