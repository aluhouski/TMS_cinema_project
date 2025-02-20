from django.urls import path
from . import views



urlpatterns = [
    path('', views.sessions_list, name='sessions_list'),
    path('session/<int:pk>/', views.session_details, name='session_details'),
    path('session/<int:pk>/purchase', views.ticket_purchase, name='ticket_purchase'),
    path('movie/<int:pk>/', views.movie_details, name='movie_details'),
    path('register/', views.register, name='register'),
    path('actors/', views.actors_list, name='actors_list'),
    path('actors/<int:pk>/', views.actor_details, name='actor_details'),
    path('directors/', views.directors_list, name='directors_list'),
    path('directors/<int:pk>/', views.director_details, name='director_details'),
    path('genres/', views.genres_list, name='genres_list'),
    path('genre/<int:pk>/', views.genre_details, name='genre_details'),
]