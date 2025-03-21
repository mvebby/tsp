import os
import sys
from datetime import date


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsp.settings')


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from tsp_database_app.models import *
from django.core.validators import MaxValueValidator, MinValueValidator


def places_db():
    places_data = [
        {"place_id": 1, "name": "Colosseum", "country": "Italy", "city": "Rome"},
        {"place_id": 2, "name": "Eiffel tower", "country": "France", "city": "Paris"},
        {"place_id": 3, "name": "Sagrada familia", "country": "Spain", "city": "Barcelona"},
        {"place_id": 4, "name": "Statue of liberty", "country": "USA", "city": "New-York"},
        {"place_id": 5, "name": "The Great Wall of China", "country": "China", "city": "Beijing"},
        {"place_id": 6, "name": "Victoria Falls", "country": "South Africa", "city": "Zimbabwe"},
        {"place_id": 7, "name": "The Taj Mahal", "country": "India", "city": "Agra"},
        {"place_id": 8, "name": "The Acropolis", "country": "Greece", "city": "Athens"},
        {"place_id": 9, "name": "The Pyramid of Cheops", "country": "Egypt", "city": "Giz Plateau"},
        {"place_id": 10, "name": "Sydney Opera House", "country": "Australia", "city": "Sydney"}
    ]

    for place in places_data:
        new_place = PlaceModel(
            place_id=place['place_id'],
            name=place['name'],
            country=place['country'],
            city=place['city'],
            address=place.get('address', None)
        )
        new_place.save()


def users_db():
    users_data = [
        {"username": "Viktor", "email": "viktor@example.com", "password": "password1", "age": 19},
        {"username": "Lera", "email": "lera@example.com", "password": "password2", "age": 20},
        {"username": "Daniil", "email": "daniil@example.com", "password": "password3", "age": 24},
        {"username": "Esenya", "email": "esenya@example.com", "password": "password4", "age": 28},
        {"username": "Ilya", "email": "ilya@example.com", "password": "password5", "age": 42}
    ]

    for user in users_data:
        new_user = CustomUser(
        username=user['username'],
        email=user['email'],
        age=user['age'])

        new_user.set_password(user['password'])
        new_user.save()


def listofplaces_db():
    listofplaces_data = [
        {"user_id": 1, "place_id": 1, "status": True},
        {"user_id": 2, "place_id": 2, "status": True},
        {"user_id": 3, "place_id": 3, "status": True},
        {"user_id": 4, "place_id": 6, "status": False},
        {"user_id": 1, "place_id": 4, "status": False}
    ]

    for listofplace in listofplaces_data:
        user = CustomUser.objects.get(id=listofplace['user_id'])
        place = PlaceModel.objects.get(place_id=listofplace['place_id'])

        new_listofplaces = ListOfPlaces(
        usermodel=user,
        placemodel=place,
        status=listofplace['status'])

        new_listofplaces.save()


def feedbacks_db():
    feedbacks_data = [
        {"user_id": 1, "place_id": 1, "rating": 4, "feedback_text": "Good"},
        {"user_id": 2, "place_id": 2, "rating": 5, "feedback_text": "Excellent"},
        {"user_id": 3, "place_id": 3, "rating": 5, "feedback_text": "I like it"},
    ]

    for feedback in feedbacks_data:
        user = CustomUser.objects.get(id=feedback['user_id'])
        place = PlaceModel.objects.get(place_id=feedback['place_id'])

        listofplaces = ListOfPlaces.objects.filter(usermodel=user, placemodel=place).first()

        if listofplaces and listofplaces.status:
            new_feedback = FeedbackModel(
                usermodel=user,
                placemodel=place,
                rating=feedback['rating'],
                feedback_text=feedback.get('feedback_text', None))
            
            new_feedback.save()
        else:
            print(f"Cannot create feedback for user {user.username} and place {place.name} because status is False.")


places_db()
users_db()
listofplaces_db()
feedbacks_db()