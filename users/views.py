from django.shortcuts import render, get_object_or_404
from .forms import *


# Create your views here.
# signin view
def signin_view(request):
    form = SigninForm(request.POST or None)
    if form.is_valid():
        form.save()
        return render(request, 'home.html')
    return render(request, 'users/signin.html', {'form': form})


# signout view
def signout_view(request):
    if request.user.is_authenticated:
        request.user.logout()
    return render(request, 'home.html')


# signup view
def signup_view(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
        form.save()
        return render(request, 'home.html')
    return render(request, 'users/signup.html', {'form': form})

# profile view
def profile_view(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    return render(request, 'profile.html', {
        'profile_user': profile_user,
    })


# edit profile view
def edit_profile_view(request):
    form = EditProfileForm(request.POST or None)
    if form.is_valid():
        form.save()
        return render(request, 'profile.html')
    return render(request, 'users/edit_profile.html', {'form': form})
