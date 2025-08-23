from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# 1. Hardcoded list of genres with their TMDB IDs
GENRE_CHOICES = [
    ('', 'Any Genre'),
    (28, 'Action'),
    (12, 'Adventure'),
    (16, 'Animation'),
    (35, 'Comedy'),
    (80, 'Crime'),
    (99, 'Documentary'),
    (18, 'Drama'),
    (10751, 'Family'),
    (14, 'Fantasy'),
    (36, 'History'),
    (27, 'Horror'),
    (10402, 'Music'),
    (9648, 'Mystery'),
    (10749, 'Romance'),
    (878, 'Science Fiction'),
    (10770, 'TV Movie'),
    (53, 'Thriller'),
    (10752, 'War'),
    (37, 'Western'),
]

# 2. New dropdown choices for minimum rating
RATING_CHOICES = [
    ('', 'Any Rating'),
    (9, '9+'),
    (8, '8+'),
    (7, '7+'),
    (6, '6+'),
    (5, '5+'),
    (4, '4+'),
]

# 3. New expanded list of languages
LANGUAGE_CHOICES = [
    ('', 'Any Language'),
    ('en', 'English'),
    ('zh', 'Mandarin Chinese'),
    ('hi', 'Hindi'),
    ('es', 'Spanish'),
    ('fr', 'French'),
    ('ar', 'Arabic'),
    ('bn', 'Bengali'),
    ('ru', 'Russian'),
    ('pt', 'Portuguese'),
    ('id', 'Indonesian'),
    ('de', 'German'),
    ('ja', 'Japanese'),
    ('te', 'Telugu'),
    ('tr', 'Turkish'),
    ('ta', 'Tamil'),
    ('zh', 'Cantonese'),
    ('ko', 'Korean'),
    ('vi', 'Vietnamese'),
    ('it', 'Italian'),
    ('gu', 'Gujarati'),
    ('pl', 'Polish'),
    ('uk', 'Ukrainian'),
    ('fa', 'Persian'),
    ('ml', 'Malayalam'),
    ('pa', 'Punjabi'),
    ('th', 'Thai'),
    ('nl', 'Dutch'),
    ('ro', 'Romanian'),
    ('cs', 'Czech'),
    ('el', 'Greek'),
]


class MovieFilterForm(forms.Form):
    # Common Tailwind classes for form elements
    form_select_classes = 'w-full p-3 border border-dark-border rounded bg-dark-surface text-white text-base appearance-none bg-[url(\'data:image/svg+xml;charset=UTF-8,%3csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"%3e%3cpolyline points="6 9 12 15 18 9"%3e%3c/polyline%3e%3c/svg%3e\')] bg-no-repeat bg-[position:right_10px_center] bg-[length:20px] pr-10'
    form_input_classes = 'flex-1 p-3 border border-dark-border rounded bg-dark-surface text-white text-base'

    genre = forms.ChoiceField(
        label="Genre",
        choices=GENRE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': form_select_classes})
    )
    year_from = forms.IntegerField(
        label="From Year",
        required=False,
        widget=forms.NumberInput(attrs={'class': form_input_classes, 'placeholder': 'From'})
    )
    year_to = forms.IntegerField(
        label="To Year",
        required=False,
        widget=forms.NumberInput(attrs={'class': form_input_classes, 'placeholder': 'To'})
    )
    rating = forms.ChoiceField(
        label="Minimum Rating",
        choices=RATING_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': form_select_classes})
    )
    language = forms.ChoiceField(
        label="Language",
        choices=LANGUAGE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': form_select_classes})
    )

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))