from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    password = models.CharField(max_length=100)
    
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth', 'password']
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True
    objects = CustomUserManager()
    def __str__(self):
        return self.first_name + ' ' + self.last_name
