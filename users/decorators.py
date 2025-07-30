from functools import wraps
from django.http import JsonResponse

def jwt_required(view_func):
    """Декоратор для проверки JWT токена"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request, 'user') or not request.user or not request.user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    """Декоратор для проверки прав администратора"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request, 'user') or not request.user or not request.user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        
        # Здесь будет проверка роли администратора (после создания системы ролей)
        # if not request.user.is_admin:
        #     return JsonResponse({'error': 'Forbidden'}, status=403)
        
        return view_func(request, *args, **kwargs)
    return wrapper
