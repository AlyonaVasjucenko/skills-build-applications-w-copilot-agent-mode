
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        from django.conf import settings
        import pymongo

        client = pymongo.MongoClient(settings.DATABASES['default']['CLIENT']['host'])
        db = client['octofit_db']

        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email
        db.users.create_index([('email', 1)], unique=True)

        # Sample users (superheroes)
        users = [
            {"name": "Bruce Wayne", "email": "batman@dc.com", "team": "DC"},
            {"name": "Clark Kent", "email": "superman@dc.com", "team": "DC"},
            {"name": "Diana Prince", "email": "wonderwoman@dc.com", "team": "DC"},
            {"name": "Tony Stark", "email": "ironman@marvel.com", "team": "Marvel"},
            {"name": "Steve Rogers", "email": "captain@marvel.com", "team": "Marvel"},
            {"name": "Natasha Romanoff", "email": "blackwidow@marvel.com", "team": "Marvel"},
        ]
        db.users.insert_many(users)

        # Teams
        teams = [
            {"name": "Marvel"},
            {"name": "DC"},
        ]
        db.teams.insert_many(teams)

        # Activities
        activities = [
            {"user": "Bruce Wayne", "type": "Running", "duration": 30},
            {"user": "Clark Kent", "type": "Flying", "duration": 60},
            {"user": "Diana Prince", "type": "Weightlifting", "duration": 45},
            {"user": "Tony Stark", "type": "Cycling", "duration": 40},
            {"user": "Steve Rogers", "type": "Swimming", "duration": 50},
            {"user": "Natasha Romanoff", "type": "Martial Arts", "duration": 35},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {"team": "Marvel", "points": 135},
            {"team": "DC", "points": 135},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {"name": "Super Strength", "difficulty": "Hard"},
            {"name": "Flight Training", "difficulty": "Medium"},
            {"name": "Stealth Ops", "difficulty": "Easy"},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data!'))
