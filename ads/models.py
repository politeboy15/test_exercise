from django.db import models

# Create your models here.
class Ad(models.Model):
    STATUS_CHOICES = [
        ('sold', 'Продано'),
        ('active', 'Активно'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    image = models.ImageField(upload_to='media/ads/', blank=False, null=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)