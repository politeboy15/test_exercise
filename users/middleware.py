from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from .jwt_utils import JWTUtils

class JWTAuthMiddleware(MiddlewareMixin):
    """Middleware для определения пользователя из JWT токена"""
    
    def process_request(self, request):
        # Получаем токен из заголовка Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            user = JWTUtils.get_user_from_token(token)
            
            if user:
                request.user = user
                request.user.is_authenticated = True
            else:
                request.user = None
                request.user.is_authenticated = False
        else:
            # Если токена нет, пользователь не аутентифицирован
            request.user = None
            if hasattr(request, 'user'):
                request.user.is_authenticated = False