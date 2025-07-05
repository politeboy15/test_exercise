from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

class User(AbstractUser):
    # Оставляем username, но не спрашиваем его у пользователя напрямую
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth']

    def save(self, *args, **kwargs):
        # Если username не задан, генерируем его автоматически
        if not self.username:
            base_slug = slugify(f"{self.first_name} {self.last_name}")
            slug = base_slug
            counter = 1
            # Проверяем уникальность username
            while User.objects.filter(username=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.username = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email