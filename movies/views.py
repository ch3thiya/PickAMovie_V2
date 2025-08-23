from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .models import UserMovieList
from .forms import MovieFilterForm, CustomUserCreationForm, LANGUAGE_CHOICES
from . import tmdb_api

LANGUAGE_MAP = {code: name for code, name in LANGUAGE_CHOICES if code}

# ... your existing landing_page and filter_page views ...
def landing_page(request):
    return render(request, 'movies/landing_page.html')

# Add the new signup view
def signup_page(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) # Use the custom form
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Sign up successful!")
            return redirect('filter_page')
    else:
        form = CustomUserCreationForm() # Use the custom form
    return render(request, 'registration/signup.html', {'form': form})

def filter_page(request):
    """
    Handles the initial movie search, prefetching, and storing results in the session.
    """
    if request.method == 'GET' and 'genre' in request.GET:
        form = MovieFilterForm(request.GET)
        if form.is_valid():
            filters = form.cleaned_data
            # Call our new API function to get a list of movies
            prefetched_movies = tmdb_api.discover_and_prefetch_movies(filters)

            if prefetched_movies:
                # Get just the IDs from the movie list
                movie_ids = [movie['id'] for movie in prefetched_movies]

                # Pop the first movie ID to redirect to
                first_movie_id = movie_ids.pop(0)

                # Store the REMAINING list of IDs in the session
                request.session['prefetched_movie_ids'] = movie_ids

                # Redirect to the first movie's recommendation page
                return redirect('movie_recommendation', movie_id=first_movie_id)
            else:
                # No movies found, fall through to render the form again
                # (Consider adding an error message here)
                pass
    else:
        form = MovieFilterForm()

    return render(request, 'movies/filter_page.html', {'form': form})

def next_movie(request):
    """
    Gets the next movie ID from the session and redirects.
    If the list is empty, redirects to the filter page.
    """
    # Get the list of IDs from the session, default to an empty list
    movie_ids = request.session.get('prefetched_movie_ids', [])

    if movie_ids:
        # Pop the next ID from the list
        next_movie_id = movie_ids.pop(0)

        # Save the now-shorter list back to the session
        request.session['prefetched_movie_ids'] = movie_ids

        # Redirect to the next movie's page
        return redirect('movie_recommendation', movie_id=next_movie_id)
    else:
        # If the list is empty, send the user back to the start
        return redirect('filter_page')

def movie_recommendation_page(request, movie_id):
    movie = tmdb_api.get_movie_details(movie_id)
    if not movie:
        raise Http404("Movie not found.")

    # Get the new credits dictionary
    credits = tmdb_api.get_movie_credits(movie_id)
    cast = credits.get('cast')
    director = credits.get('director')

    # Look up the full language name
    full_language_name = LANGUAGE_MAP.get(movie.get('original_language'), movie.get('original_language'))

    query_params = request.GET.urlencode()

    context = {
        'movie': movie,
        'cast': cast,
        'director': director, # Pass the director
        'full_language_name': full_language_name, # Pass the full language name
    }
    return render(request, 'movies/movie_recommendation.html', context)

@login_required
def add_to_list(request):
    """
    Handles adding/updating a movie in a user's list.
    Expects a POST request with 'movie_id' and 'status'.
    """
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        status = request.POST.get('status')
        user = request.user

        # Use update_or_create to either find and update an existing entry,
        # or create a new one if it doesn't exist.
        # This cleverly handles both "Add to Watched" and "Move to Watch Later".
        UserMovieList.objects.update_or_create(
            user=user,
            movie_id=movie_id,
            defaults={'status': status}
        )

        messages.success(request, "Movie list updated successfully!")
        # Redirect back to the referrer page (the movie details page)
        return redirect(request.META.get('HTTP_REFERER', 'filter_page'))

    # If it's not a POST request, just redirect to the filter page
    return redirect('filter_page')

@login_required
def profile_page(request):
    user = request.user
    
    # Get or create user profile
    try:
        user_profile = user.userprofile
    except:
        # Create profile with random avatar if it doesn't exist
        import random
        from .models import UserProfile
        random_avatar = random.randint(1, 6)
        user_profile = UserProfile.objects.create(user=user, avatar_choice=random_avatar)
    
    watch_later_list = UserMovieList.objects.filter(user=user, status='watch_later')
    watched_list = UserMovieList.objects.filter(user=user, status='watched')

    watch_later_details = [tmdb_api.get_movie_details(item.movie_id) for item in watch_later_list]
    watched_details = [tmdb_api.get_movie_details(item.movie_id) for item in watched_list]

    context = {
        'user_profile': user_profile,
        'watch_later_movies': watch_later_details,
        'watched_movies': watched_details, # Changed back from watched_movies_data
        'watch_later_count': watch_later_list.count(),
        'watched_count': watched_list.count(),
    }
    return render(request, 'movies/profile_page.html', context)

@login_required
def my_movie_details(request, movie_id):
    movie = tmdb_api.get_movie_details(movie_id)
    if not movie:
        raise Http404("Movie not found in TMDB.")

    # Get the new credits dictionary
    credits = tmdb_api.get_movie_credits(movie_id)
    cast = credits.get('cast')
    director = credits.get('director')

    # Look up the full language name
    full_language_name = LANGUAGE_MAP.get(movie.get('original_language'), movie.get('original_language'))

    list_entry = get_object_or_404(UserMovieList, user=request.user, movie_id=movie_id)

    context = {
        'movie': movie,
        'cast': cast,
        'director': director,
        'full_language_name': full_language_name,
        'list_entry': list_entry,
    }
    return render(request, 'movies/my_movie_details.html', context)

@login_required
def delete_from_list(request):
    if request.method == 'POST':
        entry_id = request.POST.get('entry_id')
        # Ensure the user can only delete their own entries
        list_entry = get_object_or_404(UserMovieList, id=entry_id, user=request.user)
        list_entry.delete()

    messages.success(request, "Movie list updated successfully!")
    return redirect('profile_page') # Redirect back to the profile

@login_required
def move_to_watched(request):
    if request.method == 'POST':
        entry_id = request.POST.get('entry_id')
        list_entry = get_object_or_404(UserMovieList, id=entry_id, user=request.user)
        # Update the status
        list_entry.status = 'watched'
        list_entry.save()
        # Redirect back to the same details page to see the change
        messages.success(request, "Movie marked as watched!")
        return redirect('my_movie_details', movie_id=list_entry.movie_id)
    return redirect('profile_page')

@login_required
def delete_profile(request):
    # If the form has been submitted...
    if request.method == 'POST':
        user = request.user
        # Log the user out before deleting them
        logout(request)
        # Delete the user object from the database
        user.delete()
        # Add a success message to be displayed on the next page
        messages.success(request, 'Your account has been successfully deleted.')
        # Redirect to the landing page
        return redirect('landing_page')
    
    # If the request is a GET, just show the confirmation page
    return render(request, 'movies/delete_profile.html')
