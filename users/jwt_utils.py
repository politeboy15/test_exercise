import jwt
import bcrypt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# Секретный ключ для JWT (добавьте в settings.py)
JWT_SECRET = getattr(settings, 'JWT_SECRET', 'your-secret-key-here')
JWT_EXPIRATION_HOURS = getattr(settings, 'JWT_EXPIRATION_HOURS', 24)

class JWTUtils:
    @staticmethod
    def generate_token(user_id):
        """Создание JWT токена для пользователя"""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        return token
    
    @staticmethod
    def decode_token(token):
        """Декодирование JWT токена"""
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None  # Токен истек
        except jwt.InvalidTokenError:
            return None  # Невалидный токен
    
    @staticmethod
    def get_user_from_token(token):
        """Получение пользователя из токена"""
        payload = JWTUtils.decode_token(token)
        if payload:
            try:
                user = User.objects.get(id=payload['user_id'], is_active=True)
                return user
            except User.DoesNotExist:
                return None
        return None

class PasswordUtils:
    @staticmethod
    def hash_password(password):
        """Хеширование пароля с помощью bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def check_password(password, hashed):
        """Проверка пароля"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
