from django.db import models
from django.conf import settings # To get the User model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
import random

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar_choice = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(6)])
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_avatar_url(self):
        return f'movies/images/avatars/avatar{self.avatar_choice}.png'

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Assign a random avatar (1-6) when user is created
        random_avatar = random.randint(1, 6)
        UserProfile.objects.create(user=instance, avatar_choice=random_avatar)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    # Create profile if it doesn't exist (for existing users)
    if not hasattr(instance, 'userprofile'):
        random_avatar = random.randint(1, 6)
        UserProfile.objects.create(user=instance, avatar_choice=random_avatar)
class UserMovieList(models.Model):
    STATUS_CHOICES = [
        ('watch_later', 'Watch Later'),
        ('watched', 'Watched'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Movie ID: {self.movie_id} ({self.get_status_display()})"

    class Meta:
        unique_together = ('user', 'movie_id')
