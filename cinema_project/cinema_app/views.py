from django.shortcuts import render, get_object_or_404, redirect
from .models import Director, Actor, Genre, Movie, Session, Ticket
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages



def sessions_list(request):
    sessions = Session.objects.all()
    return render(request, template_name = 'sessions_list.html', context = {'sessions': sessions})


def session_details(request, pk):
    session = get_object_or_404(Session, pk=pk)
    movie = session.movie
    director = movie.director
    actors = movie.actors.all()
    genres = movie.genres.all()

    # Вычисляем количество доступных билетов
    available_tickets = session.tickets_total - session.tickets_sold

    return render(request, template_name='session_details.html', 
                  context={
                      'session': session, 
                      'movie': movie,
                      'director': director, 
                      'actors': actors, 
                      'genres': genres,
                      'available_tickets': available_tickets
                  })


def movie_details(request, pk):
    movie = get_object_or_404(Movie, pk = pk)
    return render(request, template_name = 'movie_details.html', context = {'movie': movie})


def ticket_purchase(request, pk):
    session = get_object_or_404(Session, pk=pk)

    if not request.user.is_authenticated:
        messages.error(request, 'Log in to buy a ticket.')
        return redirect('login')

    if session.tickets_sold >= session.tickets_total:
        messages.error(request, 'We ran out of tickets for the session!')
        return redirect('session_details', pk=pk)

    ticket = Ticket.objects.create(
        session=session,
        user=request.user,
        ticket_price=15.0
    )

    session.tickets_sold += 1
    session.save()

    messages.success(request, 'The ticket is purchased!')
    return redirect('session_details', pk=pk)

    
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def actors_list(request):
    actors = Actor.objects.all()
    return render(request, 'actors_list.html', {'actors': actors})


def actor_details(request, pk):
    actor = get_object_or_404(Actor, pk=pk)
    return render(request, 'actor_details.html', {'actor': actor})


def directors_list(request):
    directors = Director.objects.all()
    return render(request, 'directors_list.html', {'directors': directors})


def director_details(request, pk):
    director = get_object_or_404(Director, pk=pk)
    return render(request, 'director_details.html', {'director': director})

def genres_list(request):
    genres = Genre.objects.all()
    return render(request, 'genres_list.html', {'genres': genres})

def genre_details(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    movies = genre.movie_set.all()
    return render(request, 'genre_details.html', {'genre': genre, 'movies': movies})