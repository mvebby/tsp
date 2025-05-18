from django.shortcuts import get_object_or_404
from .models import *
#from .forms import *
#from django.contrib import messages
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework_simplejwt.views import TokenObtainPairView
# Create your views here.
# PlaceModel

class PlaceModelAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = [TemplateHTMLRenderer]

    def get_object(self, place_id):
        try:
            return PlaceModel.objects.get(place_id=place_id)
        except PlaceModel.DoesNotExist:
            raise Http404

        
    def get(self, request, place_id=None):
        if place_id is None:
            # Возвращаем список всех мест
            places = PlaceModel.objects.all()
            serializer = PlaceSerializer(places, many=True)
            return Response({'places': serializer.data}, template_name='places.html')
        else:
            # Возвращаем конкретное место по place_id
            place = self.get_object(place_id)
            serializer = PlaceSerializer(place)
            return Response({'place': serializer.data}, template_name='place.html')

    def post(self, request):
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request, *args, **kwargs):

        place_id = kwargs.get("place_id", None)
        if not place_id:
            return Response({"error": "Primary key is not found"})
    
        try:
            instance = PlaceModel.objects.get(place_id = place_id)
        except:
             return Response({"error": "Object is not found"})
        serializer = PlaceSerializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    

    def delete(self, request, *args, **kwargs):

        place_id = kwargs.get("place_id", None)
        if not place_id:
            return Response({"error": "Primary key is not found"})
        
        try:
            instance = PlaceModel.objects.get(place_id = place_id)
        except:
             return Response({"error": "Object is not found"})
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#-----------------------------------------------------------------------------------------------------------#
# CustomUser
class CustomUserAPIView(APIView):
    permission_classes = (AllowAny, )

    def get_object(self, id):
        try:
            return CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            raise Http404

        
    def get(self, request, id=None):
        if id is None:
            # Возвращаем список всех пользователей
            users = CustomUser.objects.all()
            serializer = UserSerializer(users, many=True)
        else:
            # Возвращаем конкретного пользователя по id
            user = self.get_object(id)
            serializer = UserSerializer(user)
        return Response(serializer.data)
    

    def put(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            return Response({"error": "Primary key is not found"})
        
        try:
            instance = CustomUser.objects.get(id = id)
        except:
             return Response({"error": "Object is not found"})
        serializer = UserSerializer(data=request.data, instance=instance)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    

    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            return Response({"error": "Primary key is not found"})
        
        try:
            instance = CustomUser.objects.get(id = id)
        except:
             return Response({"error": "Object is not found"})
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#--------------------------------------------------------------------------------------------------#
# Register
class UserRegisterAPIView(APIView):
    permission_classes = (AllowAny, )
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#--------------------------------------------------------------------------------------------------#
# Change password
class PasswordChangeAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = PasswordChangeSerializator(data = request.data)
        if serializer.is_valid(raise_exception=True):
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not user.check_password(old_password):
                return Response({"old_password": ["Неверный старый пароль."]}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Пароль успешно изменён."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# BlackList
class BlackListLogoutAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Refresh token обязателен'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Заносим токен в blacklist
            return Response({'success': 'Токен успешно отозван'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': 'Неверный или уже отозванный refresh token'}, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
#--------------------------------------------------------------------------------------------------#
# ListOfPlaces
class ListOfPlacesAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    
    def get_object(self, pk):
        try:
            return ListOfPlaces.objects.get(pk=pk)
        except ListOfPlaces.DoesNotExist:
            raise Http404

        
    def get(self, request):
        places = ListOfPlaces.objects.filter(usermodel_id=request.user)
        serializer = ListOfPlacesSerializer(places, many=True)
        return Response(serializer.data)

        
    def post(self, request):
        serializer = ListOfPlacesSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def patch(self, request, *args, **kwargs):
        #тут айди, а не пк
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Primary key is not found"})
    
        try:
            instance = self.get_object(pk)
        except:
             return Response({"error": "Object is not found"})
        serializer = ListOfPlacesSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    

    def delete(self, request, *args, **kwargs):

        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Primary key is not found"})
        
        try:
            instance = self.get_object(pk)
        except:
             return Response({"error": "Object is not found"})
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#--------------------------------------------------------------------------------------------------#
# FeedbackModel
class FeedbackModelAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request, placemodel_id=None):
        feedbacks = FeedbackModel.objects.filter(placemodel_id=placemodel_id)
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)

        
    def post(self, request, name=None):
        serializer = FeedbackSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class FeedbackUpdateAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    def put(self, request, *args, **kwargs):
        #тут айди, а не пк
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Primary key is not found"})
    
        try:
            instance = FeedbackModel.objects.get(pk=pk)
        except:
             return Response({"error": "Object is not found"})
        serializer = FeedbackUpdateSerializer(instance, data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    

class FeedbackDeleteAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Primary key is not found"})
        
        try:
            instance = FeedbackModel.objects.get(pk=pk)
        except:
             return Response({"error": "Object is not found"})
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)