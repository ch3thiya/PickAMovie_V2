from django.urls import path
from . import views # import views from the current directory

urlpatterns = [
    # Path for the landing page
    path('', views.landing_page, name='landing_page'),

    # Path for the filter page
    path('find/', views.filter_page, name='filter_page'),

    # Path for the signup page
    path('signup/', views.signup_page, name='signup'),

    path('movie/<int:movie_id>/', views.movie_recommendation_page, name='movie_recommendation'),

    path('list/add/', views.add_to_list, name='add_to_list'),

    path('profile/', views.profile_page, name='profile_page'), 

    path('next/', views.next_movie, name='next_movie'),

    path('my-movie/<int:movie_id>/', views.my_movie_details, name='my_movie_details'),

    path('list/delete/', views.delete_from_list, name='delete_from_list'), 
    
    path('list/move-to-watched/', views.move_to_watched, name='move_to_watched'), 

    path('profile/delete/', views.delete_profile, name='delete_profile'),
]