from django.shortcuts import render, get_object_or_404
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.
# home view
def home_view(request):
    return render(request, 'home.html')

# signin view
def signin_view(request):
    form = SigninForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('profile', args=[user.id]))
            else:
                messages.error(request, 'Invalid email or password.')
    
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
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(request, user)  # Авторизуем пользователя после регистрации
        return redirect('profile', user_id=user.id)  # Перенаправление на профиль
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
        user = form.save(commit=False)  # не сохраняем сразу
        user.set_password(form.cleaned_data['password'])  # если используешь хеширование пароля
        user.save()
        return render(request, 'profile.html')
    return render(request, 'users/edit_profile.html', {'form': form})
