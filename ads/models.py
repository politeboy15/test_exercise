from django.db import models
import uuid
from users.models import User
# Create your models here.
class Ad(models.Model):
    STATUS_CHOICES = [
        ('Sold', 'Продано'),
        ('Active', 'Активно'),
    ]
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,  # Оставляем uuid4
        editable=False
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Active'
    )
    image = models.ImageField(upload_to='ads/', blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)