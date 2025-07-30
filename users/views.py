from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .forms import *
from .jwt_utils import JWTUtils, PasswordUtils
from .decorators import jwt_required
from ads.models import Ad

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
        'date_of_birth': user.date_of_birth
    })

@jwt_required
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_user_api(request):
    """API для мягкого удаления пользователя"""
    user = request.user
    user.soft_delete()
    return JsonResponse({'message': 'User deleted successfully'})
