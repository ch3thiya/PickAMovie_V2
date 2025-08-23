from django.contrib import admin
from .models import UserMovieList, UserProfile

# Register your models here.
admin.site.register(UserMovieList)
admin.site.register(UserProfile)