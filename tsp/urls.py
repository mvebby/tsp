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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    #Places urls
    path('places/', views.PlaceModelAPIView.as_view(), name='all_places'),
    path('places/<int:place_id>/', views.PlaceModelAPIView.as_view(), name='place'),
    path('places/create/', views.PlaceModelCreateView.as_view(), name='create_place'),
    path('places/<int:place_id>/update/', views.PlaceModelUpdateView.as_view(), name='update_place'),
    path('places/<int:place_id>/delete/', views.PlaceModelAPIView.as_view(), name='delete_place'),

    #Users urls
    path('users/', views.CustomUserAPIView.as_view(), name='all_users'),
    path('users/<int:id>/', views.CustomUserAPIView.as_view(), name='info_about_user'),
    path('users/<int:id>/update/', views.CustomUserUpdateView.as_view(), name='update_user'),
    path('users/<int:id>/delete/', views.CustomUserAPIView.as_view(), name='delete_user'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('change-password/', views.PasswordChangeAPIView.as_view(), name='password_change'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  

    #Listofplaces urls
    path('listofplaces/', views.ListOfPlacesAPIView.as_view(), name='listofplaces'),
    path('listofplaces/<int:pk>/', views.ListOfPlacesAPIView.as_view(), name='user_listofplaces'),
    path('listofplaces/create/', views.ListOfPlacesCreateView.as_view(), name='create_listofplaces'),
    path('listofplaces/<int:pk>/update/', views.ListOfPlacesUpdateView.as_view(), name='update_listofplaces'),
    path('listofplaces/<int:pk>/delete/', views.ListOfPlacesCreateView.as_view(), name='create_listofplaces'),

    #Feedbacks urls
    path('places/<int:placemodel_id>/feedbacks/', views.FeedbackModelAPIView.as_view(), name='place_feedbacks'),
    path('places/<str:name>/feedbacks/create', views.FeedbackModelAPIView.as_view(), name='create_feedback'),
    path('feedbacks-update/<int:pk>/', views.FeedbackUpdateAPIView.as_view(), name='update_feedback'),
    path('feedbacks-delete/<int:pk>/', views.FeedbackDeleteAPIView.as_view(), name='delete_feedback'),
]