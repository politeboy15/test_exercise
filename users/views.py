from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import json
from .forms import *
from .jwt_utils import JWTUtils, PasswordUtils
from .decorators import jwt_required
from .models import User
from ads.models import Ad

# ---------------- ВЕБ-ФУНКЦИИ (для HTML шаблонов) ----------------

def home_view(request):
    """Главная страница"""
    ads = Ad.objects.filter(status='Active')  # Показываем только активные объявления
    return render(request, 'home.html', {'ads': ads})

def signin_view(request):
    """Вход в систему (веб-интерфейс)"""
    if request.user.is_authenticated:
        return redirect('profile', user_id=request.user.id)
        
    form = SigninForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                # Ищем пользователя в базе
                user = User.objects.get(email=email, is_active=True)
                if user.check_password(password):
                    # Используем стандартный Django login для веб-интерфейса
                    login(request, user)
                    messages.success(request, f'Добро пожаловать, {user.first_name}!')
                    return redirect('profile', user_id=user.id)
                else:
                    messages.error(request, 'Неверный email или пароль.')
            except User.DoesNotExist:
                messages.error(request, 'Неверный email или пароль.')
    
    return render(request, 'users/signin.html', {'form': form})

def signout_view(request):
    """Выход из системы"""
    if request.user.is_authenticated:
        user_name = request.user.first_name
        logout(request)
        messages.success(request, f'До свидания, {user_name}!')
    
    return redirect('home')

def signup_view(request):
    """Регистрация (веб-интерфейс)"""
    if request.user.is_authenticated:
        return redirect('profile', user_id=request.user.id)
        
    form = SignupForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            try:
                # Проверяем, не существует ли пользователь с таким email
                if User.objects.filter(email=form.cleaned_data['email']).exists():
                    messages.error(request, 'Пользователь с таким email уже существует.')
                    return render(request, 'users/signup.html', {'form': form})
                
                # Создаём пользователя
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                
                # Автоматически входим в систему после регистрации
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.first_name}! Регистрация прошла успешно.')
                return redirect('profile', user_id=user.id)
                
            except Exception as e:
                messages.error(request, f'Ошибка при регистрации: {str(e)}')
    
    return render(request, 'users/signup.html', {'form': form})

def profile_view(request, user_id):
    """Просмотр профиля пользователя"""
    profile_user = get_object_or_404(User, id=user_id, is_active=True)
    user_ads = Ad.objects.filter(user=profile_user)
    
    return render(request, 'users/profile.html', {
        'profile_user': profile_user, 
        'user_ads': user_ads,
        'user': profile_user  # Для совместимости с шаблоном
    })

@login_required
def edit_profile_view(request):
    """Редактирование профиля"""
    user = request.user
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            try:
                # Сохраняем изменения
                user = form.save(commit=False)
                
                # Если пароль был изменён, хешируем его
                new_password = form.cleaned_data.get('password')
                if new_password:
                    user.set_password(new_password)
                
                user.save()
                
                # Обновляем сессию, чтобы пользователь не вышел из системы
                login(request, user)
                
                messages.success(request, 'Профиль успешно обновлён!')
                return redirect('profile', user_id=user.id)
                
            except Exception as e:
                messages.error(request, f'Ошибка при обновлении профиля: {str(e)}')
    else:
        # Предзаполняем форму текущими данными пользователя
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'date_of_birth': user.date_of_birth,
        }
        form = EditProfileForm(initial=initial_data)
    
    return render(request, 'users/edit_profile.html', {
        'form': form,
        'user': user
    })

# ========== API ФУНКЦИИ (для JWT) ==========

@csrf_exempt
@require_http_methods(["POST"])
def signin_api(request):
    """API для входа с JWT токеном"""
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return JsonResponse({'error': 'Email and password required'}, status=400)
        
        try:
            user = User.objects.get(email=email, is_active=True)
            if user.check_password(password):
                token = JWTUtils.generate_token(user.id)
                return JsonResponse({
                    'token': token,
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name
                    }
                })
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def signup_api(request):
    """API для регистрации с JWT токеном"""
    try:
        data = json.loads(request.body)
        
        # Валидация данных
        required_fields = ['email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({'error': f'{field} is required'}, status=400)
        
        # Проверка на существование пользователя
        if User.objects.filter(email=data['email']).exists():
            return JsonResponse({'error': 'User with this email already exists'}, status=400)
        
        # Создание пользователя
        user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=data.get('date_of_birth')
        )
        user.set_password(data['password'])
        user.save()
        
        # Создание токена
        token = JWTUtils.generate_token(user.id)
        
        return JsonResponse({
            'token': token,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        }, status=201)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

@jwt_required
def profile_api(request):
    """API для получения профиля пользователя"""
    user = request.user
    return JsonResponse({
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'date_of_birth': str(user.date_of_birth) if user.date_of_birth else None,
        'is_active': user.is_active
    })

@jwt_required
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_user_api(request):
    """API для мягкого удаления пользователя"""
    user = request.user
    user.soft_delete()
    return JsonResponse({'message': 'User deleted successfully'})