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
    path('places/', views.PlaceModelAPIView.as_view()),
    path('places/<int:place_id>/', views.PlaceModelAPIView.as_view()),
    path('users/', views.CustomUserAPIView.as_view()),
    path('users/<int:id>/', views.CustomUserAPIView.as_view()),
    path('register/', views.UserRegisterAPIView.as_view()),
    path('change-password/', views.PasswordChangeAPIView.as_view()),
    path('logout/', views.BlackListLogoutAPIView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('listofplaces/', views.ListOfPlacesAPIView.as_view()),
    path('listofplaces/<int:pk>/', views.ListOfPlacesAPIView.as_view()),
    path('feedbacks/<int:placemodel_id>/', views.FeedbackModelAPIView.as_view()),
    path('feedbacks/', views.FeedbackModelAPIView.as_view()),
    path('feedbacks-delete/<int:pk>/', views.FeedbackDeleteAPIView.as_view()),
    path('feedbacks-update/<int:pk>/', views.FeedbackUpdateAPIView.as_view()),
]