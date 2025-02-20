from django.core.management.base import BaseCommand
from django_seed import Seed
from cinema_app.models import Actor, Director, Movie, Session, Genre, Ticket, User
import random
from django.utils import timezone
from datetime import timedelta



# Патчинг make_aware() для совместимости с Django 5.x
def patched_make_aware(value, tz):
    return timezone.make_aware(value, tz)

# Заменяем функцию в django-seed
import django_seed.guessers
django_seed.guessers._timezone_format = lambda value: patched_make_aware(value, timezone.get_current_timezone())



class Command(BaseCommand):
    help = 'Seeds the database with fake data.'

    def handle(self, *args, **options):
        seeder = Seed.seeder()

        seeder.add_entity(User, 6, {})

        seeder.add_entity(Actor, 10, {
            'name': lambda x: seeder.faker.name(),
            'age': lambda x: random.randint(20, 80),
            'sex': lambda x: random.choice(['Male', 'Female']),
            'oscars': lambda x: random.randint(0, 3),
            'image': None
        })

        seeder.add_entity(Director, 5, {
            'name': lambda x: seeder.faker.name(),
            'age': lambda x: random.randint(30, 90),
            'sex': lambda x: random.choice(['Male', 'Female']),
            'film_count': lambda x: random.randint(1, 20),
            'image': None
        })

        seeder.add_entity(Genre, 5, {
            'genre_name': lambda x: seeder.faker.word(),
            'pg_rating': lambda x: random.choice([0, 6, 12, 16, 18])
        })

        inserted_pks = seeder.execute()

        actors = list(Actor.objects.all())
        directors = list(Director.objects.all())
        genres = list(Genre.objects.all())

        for _ in range(15):
            movie = Movie.objects.create(
                movie_name=seeder.faker.sentence(nb_words=3),
                description=seeder.faker.text(max_nb_chars=200),
                release_date=seeder.faker.date_this_decade(),
                director=random.choice(directors),
                image=None
            )

            random_actors = random.sample(actors, k=random.randint(2, 5))
            movie.actors.set(random_actors)

            random_genres = random.sample(genres, k=random.randint(1, 3))
            movie.genres.set(random_genres)

            movie.save()

        movies = list(Movie.objects.all())
        for _ in range(20):
            movie = random.choice(movies)
            start_time = timezone.now() + timedelta(days=random.randint(1, 30))
            end_time = start_time + timedelta(hours=2)

            Session.objects.create(
                movie=movie,
                start_time=start_time,
                end_time=end_time,
                tickets_total=random.randint(50, 200),
                tickets_sold=random.randint(0, 50)
            )

        users = list(User.objects.all())
        sessions = list(Session.objects.all())

        for _ in range(30):
            session = random.choice(sessions)
            user = random.choice(users)
            ticket_price = random.uniform(5.0, 20.0)  # Цена билета от 5 до 20

            Ticket.objects.create(
                session=session,
                user=user,
                ticket_price=round(ticket_price, 2)
            )

        self.stdout.write(self.style.SUCCESS('Seeded data successfully!'))