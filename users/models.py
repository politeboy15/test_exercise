from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    password = models.CharField(max_length=128)  # Увеличил длину для bcrypt
    is_active = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Добавляем поля для Django admin
    is_staff = models.BooleanField(default=False)
    
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Убираем password из REQUIRED_FIELDS
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def set_password(self, raw_password):
        """Переопределяем для использования bcrypt"""
        # Импорт внутри метода - избегаем циклического импорта
        from .jwt_utils import PasswordUtils
        self.password = PasswordUtils.hash_password(raw_password)
    
    def check_password(self, raw_password):
        """Переопределяем для использования bcrypt"""
        # Импорт внутри метода - избегаем циклического импорта
        from .jwt_utils import PasswordUtils
        return PasswordUtils.check_password(raw_password, self.password)
    
    def soft_delete(self):
        """Мягкое удаление пользователя"""
        self.is_active = False
        self.save()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'