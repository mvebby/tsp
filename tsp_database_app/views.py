from django.shortcuts import render, get_object_or_404, redirect
from tsp_database_app.models import *
from .forms import *
from django.contrib import messages
# Create your views here.
# READ PlaceModel
def get_all_places(request):
    places = PlaceModel.objects.all()
    return render(request, 'places.html', {'places':places})


def get_places_by_name(request, place_name):
    places_by_curr_name = PlaceModel.objects.filter(name=place_name)
    return render(request, 'place_name.html', {'places_by_curr_name':places_by_curr_name})


def get_places_from_country(request, country_name):
    places_in_curr_country = PlaceModel.objects.filter(country=country_name)
    return render(request, 'country.html', {'places_in_curr_country':places_in_curr_country})


def get_places_from_city(request, city_name):
    places_in_curr_city = PlaceModel.objects.filter(city=city_name)
    return render(request, 'city.html', {'places_in_curr_city':places_in_curr_city})


def get_place(request, id):
    place = get_object_or_404(PlaceModel, place_id=id)
    return render(request, 'place.html', {'place':place})


def search_places(request):
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_by = form.cleaned_data['search_by']
            search_query = form.cleaned_data['search_query']

            if search_by == 'name':
                return redirect('places_by_current_name', place_name=search_query)
            elif search_by == 'city':
                return redirect('places_from_current_city', city_name=search_query)
            elif search_by == 'country':
                return redirect('places_from_current_country', country_name=search_query)

    return render(request, 'search.html', {'form': form})

# CREATE PlaceModel
def create_place(request):
    if request.method == "POST":
        PlaceModel.objects.create(
            place_id=request.POST.get("place_id"),
            name=request.POST.get("name"),
            city=request.POST.get("city"),
            country=request.POST.get("country"),
            address=request.POST.get("address")
        )
        return redirect('all_places')
    return render(request, 'create_place.html')

# UPDATE PlaceModel
def update_place(request, id):
    place = get_object_or_404(PlaceModel, place_id=id)
    if request.method == "POST":
        PlaceModel.objects,filter(place_id=id).update(
            name = request.POST.get("name"),
            city = request.POST.get("city"),
            country = request.POST.get("country"),
            address = request.POST.get("address")
        )
        return redirect('all_places')
    return render(request, "update_place.html", {'place': place})

# Delete PlaceModel
def delete_place(request, id):
    place = get_object_or_404(PlaceModel, place_id=id)
    if request.method == "POST":
        PlaceModel.objects.filter(place_id=id).delete()
        return redirect('all_places')
    return render(request, 'delete_place.html', {'place': place})
#-----------------------------------------------------------------------------------------------------------#
# READ CustomUser
def get_all_users(request):
    users = CustomUser.objects.all()
    return render(request, 'users.html', {'users':users})


def get_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'user.html', {'user':user})

# CREATE CustomUser
def create_user(request):
    if request.method == "POST":
        CustomUser.objects.create(
            id=request.POST.get("id"),
            username=request.POST.get("username"),
            age=request.POST.get("age"),
            email=request.POST.get("email"),
            password=request.POST.get("password")
        )
        return redirect('all_users')
    return render(request, 'create_user.html')

# UPDATE CustomUser
def update_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id) # нужно для проверки, что пользователь существует
    if request.method == "POST":
        CustomUser.objects.filter(id=user_id).update(
            id=request.POST.get("id"),
            username = request.POST.get("username"),
            age = request.POST.get("age"),
            email = request.POST.get("email"),
            password = request.POST.get("password")
        )
        return redirect('all_users')
    return render(request, "update_user.html", {'user': user})

# DELETE CustomUser
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == "POST":
        CustomUser.objects.filter(id=user_id).delete()
        return redirect('all_users')
    return render(request, 'delete_user.html', {'user': user})
#-------------------------------------------------------------------------------------------------#
# READ ListOfPlaces
def get_list_of_places(request, user_id):
    list_of_places = ListOfPlaces.objects.filter(usermodel_id=user_id)
    info = [{'name': place.placemodel.name, 'status': place.status, 'user_id': place.usermodel.id, 'place_id': place.placemodel.place_id, 'list_id': place.pk}
            for place in list_of_places]
    return render(request, 'listofplaces.html', {'info':info, 'user_id': user_id})

# CREATE ListOfPlaces
def create_list_of_places(request):
    if request.method == "POST":
        id = request.POST.get("placemodel")
        user_id = request.POST.get("username")
        ListOfPlaces.objects.create(
            usermodel=get_object_or_404(CustomUser, id=user_id),
            placemodel=get_object_or_404(PlaceModel, place_id=id),
            status=request.POST.get("status") == 'on'
        )
        return redirect('list_of_current_person', user_id = user_id)
    
    places = PlaceModel.objects.all()
    return render(request, 'create_list_of_places.html', {'places': places})


# UPDATE ListOfPlaces
def update_list_of_places(request, list_id):
    list_item = get_object_or_404(ListOfPlaces, pk=list_id) # проверка

    user_id_list = list_item.usermodel.id
    
    if request.method == "POST":
        ListOfPlaces.objects.filter(pk=list_id).update(
            status=request.POST.get("status") == 'on'
        )
        return redirect('list_of_current_person', user_id=user_id_list)
    
    return render(request, 'update_list.html', {'list_item': list_item})


# DELETE ListOfPlaces
def delete_list_of_places(request, list_id):
    list_item = get_object_or_404(ListOfPlaces, pk=list_id) # проверка
    
    user_id_list = list_item.usermodel.id
    
    if request.method == "POST":
        ListOfPlaces.objects.filter(pk=list_id).delete() # удалчем с помощью менеджера модели
        return redirect('list_of_current_person', user_id=user_id_list)
    
    return render(request, 'delete_list.html', {'list_item': list_item})
#--------------------------------------------------------------------------------------------------#
# READ FeedbackModel
def get_feedbacks_by_place(request, id):
    feedbacks_of_place = FeedbackModel.objects.filter(placemodel_id=id)
    info = [{'user_name':feedback.usermodel.username,'place_id':feedback.placemodel.place_id, 'rating':feedback.rating, 'feedback_text':feedback.feedback_text, 'feedback_id': feedback.pk}
            for feedback in feedbacks_of_place]
    return render(request, 'feedbacks_of_place.html', {'info':info, 'place_id': id})


def get_feedbacks_by_user(request, user_id):
    feedbacks_of_user = FeedbackModel.objects.filter(usermodel_id=user_id)
    info = [{'place_name':feedback.placemodel.name,'user_id':feedback.usermodel.id, 'rating':feedback.rating, 'feedback_text':feedback.feedback_text, 'feedback_id': feedback.pk}
            for feedback in feedbacks_of_user]
    return render(request, 'feedbacks_of_user.html', {'info':info, 'user_id': user_id})


def create_feedbacks(request):
    if request.method == "POST":
        id = request.POST.get("placemodel")
        user_id_feedback = request.POST.get("username")

        user = get_object_or_404(CustomUser, id=user_id_feedback)
        place = get_object_or_404(PlaceModel, place_id=id)

        if not ListOfPlaces.objects.filter(
            usermodel_id=user,
            placemodel_id=place,
            status=True
        ).exists():
            messages.error(request, "Нельзя оставить отзыв для этого места")
            return redirect('create_feedback')

        FeedbackModel.objects.create(
            usermodel=user,
            placemodel=place,
            rating=request.POST.get("rating"),
            feedback_text=request.POST.get("feedback_text"),
        )
        return redirect('feedbacks_of_user', user_id = user_id_feedback)
    places = PlaceModel.objects.all()
    return render(request, 'create_feedback.html', {'places': places})


def update_feedbacks(request, feedback_id):
    feedback_current = get_object_or_404(FeedbackModel, pk=feedback_id)
    user_id_feedback = feedback_current.usermodel.id

    if request.method == "POST":
        FeedbackModel.objects.filter(pk=feedback_id).update(
            rating = request.POST.get("rating"),
            feedback_text = request.POST.get("feedback_text")
        )
        return redirect('feedbacks_of_user', user_id = user_id_feedback)
    return render(request, 'update_feedback.html', {'feedback_current': feedback_current, 'user_id_feedback': user_id_feedback})


def delete_feedbacks(request, feedback_id):
    feedback_current = get_object_or_404(FeedbackModel, pk=feedback_id)
    user_id_feedback = feedback_current.usermodel.id

    if request.method == "POST":
        FeedbackModel.objects.filter(pk=feedback_id).delete()
        return redirect('feedbacks_of_user', user_id = user_id_feedback)
    return render(request, 'delete_feedback.html', {'feedback_current': feedback_current})
