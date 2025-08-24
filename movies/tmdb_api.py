import requests
import random
from django.conf import settings
from django.core.cache import cache

BASE_URL = "https://api.themoviedb.org/3"
API_KEY = settings.TMDB_API_KEY
    
def discover_and_prefetch_movies(filters):
    """
    Fetches a shuffled list of movies from a single, random page
    within the top 10 pages of TMDB results.
    """
    endpoint = f"{BASE_URL}/discover/movie"
    params = {
        'api_key': API_KEY,
        'sort_by': 'popularity.desc',
        'vote_count.gte': 100,
        'page': 1
    }

    # Add user's filters to the request params
    if filters.get('genre'):
        params['with_genres'] = filters['genre']
    if filters.get('year_from'):
        params['primary_release_date.gte'] = f"{filters['year_from']}-01-01"
    if filters.get('year_to'):
        params['primary_release_date.lte'] = f"{filters['year_to']}-12-31"
    if filters.get('rating'):
        params['vote_average.gte'] = filters['rating']
    if filters.get('language'):
        params['with_original_language'] = filters['language']

    try:
        # First call to get the total number of pages
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        total_pages = data.get('total_pages', 1)

        # Limit the random page selection to the first 10 pages
        random_page = random.randint(1, min(total_pages, 10))
        params['page'] = random_page

        # Second call to get the movies from our chosen random page
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        results = data.get('results', [])

        if not results:
            return []

        # Shuffle the list of movies and return it
        random.shuffle(results)
        return results

    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return []
    
def get_movie_details(movie_id):
    """Fetches detailed info for a movie, using cache if available."""
    cache_key = f"movie_details_{movie_id}"
    cached_data = cache.get(cache_key)

    if cached_data:
        return cached_data # Return cached data if it exists
    
    """Fetches the detailed information for a specific movie from TMDB."""
    endpoint = f"{BASE_URL}/movie/{movie_id}"
    params = {'api_key': API_KEY}

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status() # Raise an error for bad responses
        data = response.json()
        cache.set(cache_key, data, 60 * 60 * 24)
        return data
    
    except requests.RequestException as e:
        print(f"API request failed for movie ID {movie_id}: {e}")
        return None
    
# In movies/tmdb_api.py

def get_movie_credits(movie_id):
    """
    Fetches the cast (top 3) and the director for a specific movie, using cache.
    Returns a dictionary: {'cast': [...], 'director': ...}
    """
    cache_key = f"movie_credits_and_director_{movie_id}"
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return cached_data

    endpoint = f"{BASE_URL}/movie/{movie_id}/credits"
    params = {'api_key': API_KEY}
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()

        cast = data.get('cast', [])[:3]
        director = None
        # Find the director in the crew list
        for member in data.get('crew', []):
            if member.get('job') == 'Director':
                director = member
                break # Stop after finding the first director

        credits = {'cast': cast, 'director': director}
        cache.set(cache_key, credits, 60 * 60 * 24) 
        return credits

    except requests.RequestException as e:
        print(f"API request for credits failed for movie ID {movie_id}: {e}")
        return {'cast': [], 'director': None} 