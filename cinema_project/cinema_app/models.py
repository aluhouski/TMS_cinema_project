from django.db import models
from django.contrib.auth.models import User



class BaseModel(models.Model):
    name = models.CharField(max_length = 100)
    age = models.IntegerField()
    sex = models.CharField(max_length = 6)

    class Meta:
        abstract = True


class Director(BaseModel):
    film_count = models.IntegerField()
    image = models.ImageField(upload_to='directors/', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class Actor(BaseModel):
    oscars = models.IntegerField()
    image = models.ImageField(upload_to='actors/', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class Genre(models.Model):
    genre_name = models.CharField(max_length = 100)
    pg_rating = models.IntegerField()

    def __str__(self):
        return self.genre_name


class Movie(models.Model):
    movie_name = models.CharField(max_length = 100)
    director = models.ForeignKey(Director, related_name = 'director', on_delete=models.CASCADE)
    actors = models.ManyToManyField(Actor)
    genres = models.ManyToManyField(Genre)
    release_date = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to='movies/', blank=True, null=True)

    def __str__(self):
        return self.movie_name


class Session(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    tickets_total = models.IntegerField()
    tickets_sold = models.IntegerField()
    movie = models.ForeignKey(Movie, related_name='movie', on_delete=models.CASCADE, blank=True, null=True)

    def tickets_left(self):
        return self.tickets_total - self.tickets_sold

    def __str__(self):
        return f"{self.movie.movie_name} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"


class Ticket(models.Model):
    session = models.ForeignKey(Session, related_name='session', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    ticket_price = models.FloatField(default=15.0)

    def __str__(self):
        return f"{self.user.username} - {self.session.movie.movie_name} - {self.session.start_time.strftime('%Y-%m-%d %H:%M')}"