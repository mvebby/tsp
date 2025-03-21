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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('places/', views.get_all_places, name='all_places'),
    path('places/<int:id>/', views.get_place, name='current_place'),
    path('user/<int:user_id>/', views.get_user, name='info_about_user'),
    path('country/<str:country_name>/', views.get_places_from_country, name='places_from_current_country'),
    path('city/<str:city_name>/', views.get_places_from_city, name='places_from_current_city'),
    path('listofplaces/<int:user_id>/', views.get_list_of_places, name='list_of_current_person'),
    path('feedbacks/<int:id>/', views.get_feedbacks, name='all_feedbacks'),
]