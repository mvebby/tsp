from django.shortcuts import render, get_object_or_404
from tsp_database_app.models import *

# Create your views here.
def get_all_places(request):
    places = PlaceModel.objects.all()
    return render(request, 'places.html', {'places':places})


def get_place(request, id):
    place = get_object_or_404(PlaceModel, place_id=id)
    return render(request, 'place.html', {'place':place})


def get_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'user.html', {'user':user})


def get_places_from_country(request, country_name):
    places_in_curr_country = PlaceModel.objects.filter(country=country_name)
    return render(request, 'country.html', {'places_in_curr_country':places_in_curr_country})


def get_places_from_city(request, city_name):
    places_in_curr_city = PlaceModel.objects.filter(city=city_name)
    return render(request, 'city.html', {'places_in_curr_city':places_in_curr_city})


def get_list_of_places(request, user_id):
    list_of_places = ListOfPlaces.objects.filter(usermodel_id=user_id)
    info = [{'name': place.placemodel.name, 'status': place.status}
            for place in list_of_places]
    return render(request, 'listofplaces.html', {'info':info})


def get_feedbacks(request, id):
    feedbacks_of_place = FeedbackModel.objects.filter(placemodel_id=id)
    return render(request, 'feedbacks.html', {'feedbacks':feedbacks_of_place})