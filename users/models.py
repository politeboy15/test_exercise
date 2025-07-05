from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    password = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=100)
    
    REQUIRED_FIELDS = ['__all__']
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True
    def __str__(self):
        return self.first_name + ' ' + self.last_name
