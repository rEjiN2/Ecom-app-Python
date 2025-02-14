from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator
import uuid

class UserProfile(models.Model):
    USER_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('pending', 'Pending Verification')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    wallet_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00)]
    )
    userStatus = models.CharField(
        max_length=20,
        choices=USER_STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.name or 'No Name'}"

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

# Signal to automatically create or update UserProfile when User is created/updated
# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(
#             user=instance,
#             email=instance.email,
#             username=instance.username,
#             userStatus='active'
#         )
#     else:
#         try:
#             instance.userprofile.save()
#         except UserProfile.DoesNotExist:
#             UserProfile.objects.create(
#                 user=instance,
#                 email=instance.email,
#                 username=instance.username,
#                 userStatus='active'
#             )