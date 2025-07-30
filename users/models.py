from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .jwt_utils import PasswordUtils

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)  # Для мягкого удаления
    created_at = models.DateTimeField(auto_now_add=True)
    
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth', 'password']
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True
    objects = CustomUserManager()

    def set_password(self, raw_password):
        """Переопределяем для использования bcrypt"""
        self.password = PasswordUtils.hash_password(raw_password)
    
    def check_password(self, raw_password):
        """Переопределяем для использования bcrypt"""
        return PasswordUtils.check_password(raw_password, self.password)
    
    def soft_delete(self):
        """Мягкое удаление пользователя"""
        self.is_active = False
        self.save()

    def __str__(self):
        return self.first_name + ' ' + self.last_name