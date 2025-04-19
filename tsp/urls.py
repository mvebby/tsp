"""
URL configuration for tsp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tsp_database_app import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('places/', views.get_all_places, name='all_places'),
    path('places/<int:id>/', views.get_place, name='current_place'),
    path('search/name/<str:place_name>/', views.get_places_by_name, name='places_by_current_name'),
    path('search/country/<str:country_name>/', views.get_places_from_country, name='places_from_current_country'),
    path('search/city/<str:city_name>/', views.get_places_from_city, name='places_from_current_city'),
    path('search/', views.search_places, name='search_places'),
    path('places/create/', views.create_place, name='create_place'),
    path('places/update/<int:id>/', views.update_place, name='update_place'),
    path('places/delete/<int:id>/', views.delete_place, name='delete_place'),
    path('users/', views.get_all_users, name='all_my_users'),
    path('users/<int:user_id>/', views.get_user, name='info_about_user'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/update/<int:user_id>/', views.update_user, name='update_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('listofplaces/<int:user_id>/', views.get_list_of_places, name='list_of_current_person'),
    path('listofplaces/create/', views.create_list_of_places, name='create_list'),
    path('listofplaces/update/<int:list_id>/', views.update_list_of_places, name='update_list'),
    path('listofplaces/delete/<int:list_id>/', views.delete_list_of_places, name='delete_list'),
    path('feedbacks_place/<int:id>/', views.get_feedbacks_by_place, name='feedbacks_of_place'),
    path('feedbacks_user/<int:user_id>/', views.get_feedbacks_by_user, name='feedbacks_of_user'),
    path('feedbacks/create/', views.create_feedbacks, name='create_feedback'),
    path('feedbacks/update/<int:feedback_id>/', views.update_feedbacks, name='update_feedback'),
    path('feedbacks/delete/<int:feedback_id>/', views.delete_feedbacks, name='delete_feedback'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/refresh/', TokenVerifyView.as_view(), name='token_verify'),
]