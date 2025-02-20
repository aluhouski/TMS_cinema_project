from django.contrib import admin
from .models import Director, Actor, Genre, Movie, Session, Ticket


class ActorInline(admin.TabularInline):
    model = Movie.actors.through
    extra = 1


class MovieAdmin(admin.ModelAdmin):
    list_display = ('movie_name', 'short_description', 'director', 'get_actors', 'get_genres', 'release_date')
    list_filter = ('director', 'genres', 'release_date')
    search_fields = ('name', 'description', 'genres__genre_name')
    ordering = ('-release_date',)
    inlines = [ActorInline]

    def short_description(self, obj):
        if len(obj.description) > 40:
            return obj.description[:40] + '...'
        else:
            return obj.description
        
    short_description.short_description = 'Description'

    def get_genres(self, obj):
        return ", ".join([genre.genre_name for genre in obj.genres.all()])
    
    get_genres.short_description = 'Genres'

    def get_actors(self, obj):
        return ", ".join([actor.name for actor in obj.actors.all()])
    
    get_actors.short_description = 'Actors'


class DirectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'sex', 'film_count')
    list_filter = ('age', 'sex',)
    search_fields = ('name',)
    ordering = ('name',)


class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'sex', 'oscars')
    list_filter = ('age', 'sex', 'oscars',)
    search_fields = ('name',)
    ordering = ('name',)


class SessionAdmin(admin.ModelAdmin):
    list_display = ('movie', 'start_time', 'end_time', 'tickets_sold', 'tickets_total')
    list_filter = ('movie', 'start_time', 'tickets_total',)
    search_fields = ('movie__movie_name',)
    ordering = ('-start_time',)


class TicketAdmin(admin.ModelAdmin):
    list_display = ('session', 'user', 'ticket_price')
    list_filter = ('session__start_time',)
    search_fields = ('user__username', 'session__movie__movie_name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('genre_name', 'pg_rating')
    list_filter = ('pg_rating',)
    search_fields = ('genre_name',)


admin.site.register(Movie, MovieAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Ticket, TicketAdmin)