from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect, reverse 
from .models import *
import requests  # Импорт библиотеки
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth import logout
from django.db.models import F
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
#IsAuthenticated
class PlaceModelAPIView(APIView):
    permission_classes = [IsAuthenticated]
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
            return Response({'places': serializer.data}, template_name='place/places.html')
        else:
            # Возвращаем конкретное место по place_id
            place = self.get_object(place_id)
            serializer = PlaceSerializer(place)
            return Response({'place': serializer.data}, template_name='place/place.html')


    def delete(self, request, *args, **kwargs):

        place_id = kwargs.get("place_id", None)
        if not place_id:
            return Response({"error": "Primary key is not found"})
        
        try:
            instance = PlaceModel.objects.get(place_id = place_id)
        except:
             return Response({"error": "Object is not found"})
        instance.delete()
        return Response({"status": "success"}, status=status.HTTP_200_OK)
    

class PlaceModelCreateView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        return Response(template_name='place/create_place.html')


    def post(self, request):
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return redirect('all_places')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PlaceModelUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, place_id): 
        try:
            place = PlaceModel.objects.get(place_id=place_id)
            serializer = PlaceSerializer(place)
            return Response({'place': serializer.data}, template_name='place/update_place.html')
        except PlaceModel.DoesNotExist:
            return Response({'error': 'Место не найдено'}, status=status.HTTP_404_NOT_FOUND)
    

    def post(self, request, place_id):
        # Явно говорим, что POST = PUT для этой вьюхи
        return self.put(request, place_id)
    
    def put(self, request, place_id):

        try:
            place = PlaceModel.objects.get(place_id=place_id)
        except PlaceModel.DoesNotExist:
            return Response({"error": "Primary key is not found"})
    
        try:
            instance = PlaceModel.objects.get(place_id = place_id)
        except:
             return Response({"error": "Object is not found"})
        
        serializer = PlaceSerializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return redirect('place', place_id=place_id)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

#-----------------------------------------------------------------------------------------------------------#
# CustomUser
class CustomUserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]

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
            return Response({'users': serializer.data}, template_name='user/users.html')
        else:
            # Возвращаем конкретного пользователя по id
            user = self.get_object(id)
            serializer = UserSerializer(user)
            return Response({'user': serializer.data}, template_name='user/user.html')
    

    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            return Response({"error": "Primary key is not found"})
        
        try:
            instance = CustomUser.objects.get(id = id)
        except:
             return Response({"error": "Object is not found"})
        instance.delete()
        return Response({"status": "success"}, status=status.HTTP_200_OK)
    
class CustomUserUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, id): 
        try:
            user = CustomUser.objects.get(id = id)
            serializer = UserSerializer(user)
            return Response({'user': serializer.data}, template_name='user/update_user.html')
        except CustomUser.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
    

    def post(self, request, id):
        # Явно говорим, что POST = PUT для этой вьюхи
        return self.put(request, id)
    
    def put(self, request, id):
        if not id:
            return Response({"error": "Primary key is not found"})
        
        try:
            instance = CustomUser.objects.get(id = id)
        except:
             return Response({"error": "Object is not found"})
        serializer = UserSerializer(data=request.data, instance=instance)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return redirect('info_about_user', id = id)
#--------------------------------------------------------------------------------------------------#
# Login
class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Отправляем запрос к JWT-эндпоинту
        response = requests.post(
            'http://localhost:8000/api/token/',
            data={'username': username, 'password': password}
        )
        
        if response.status_code == 200:
            data = response.json()
            access_token = data.get('access')
            refresh_token = data.get('refresh')
            # Сохраняем токен в куки (или сессию)
            response = redirect('all_places')
            response.set_cookie('access_token', access_token, httponly=True)
            response.set_cookie('refresh_token', refresh_token, httponly=True)
            return response
        else:
            return render(request, 'auth/login.html', {'error': 'Неправильные имя аккаунта или пароль'})

#--------------------------------------------------------------------------------------------------#
# Logout
class LogoutView(View):
    def get(self, request):
        # Проверяем, не находится ли уже пользователь на странице входа
        if request.path == reverse('login'):
            return redirect('home')  # Перенаправляем на главную, чтобы избежать цикла
        
        # Выход из системы
        logout(request)  # Важно: очищаем сессию Django
        
        response = redirect('login')
        
        # Очищаем JWT-куки
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        
        # Добавляем хедер, чтобы избежать кэширования
        response['Cache-Control'] = 'no-cache, no-store'
        return response

    
#--------------------------------------------------------------------------------------------------#
# Register
class RegisterView(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request):
        # Рендерим страницу регистрации (если используете шаблоны)
        return render(request, 'auth/register.html')

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            
            # Редирект на страницу входа после успешной регистрации
            return redirect('login')  # Используем имя URL-маршрута для login
            
        # Если ошибки валидации, показываем форму с ошибками
        return render(request, 'auth/register.html', {'errors': serializer.errors})
#--------------------------------------------------------------------------------------------------#
# Change password
class PasswordChangeAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'auth/password_change.html'  # Путь к шаблону

    def get(self, request):
        # Просто рендерим форму смены пароля
        return Response({'user': request.user})
    
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = PasswordChangeSerializator(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not user.check_password(old_password):
                # Возвращаем форму с ошибкой
                return Response({
                    'user': user,
                    'errors': {'old_password': ['Неверный старый пароль']}
                }, template_name='auth/password_change.html')

            user.set_password(new_password)
            user.save()
            # Редирект после успешной смены пароля
            return redirect('place')
        
        # Возвращаем форму с ошибками валидации
        return Response({
            'user': user,
            'errors': serializer.errors
        }, template_name='auth/password_change.html')


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



#--------------------------------------------------------------------------------------------------#
# ListOfPlaces
class ListOfPlacesAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    
    def get_object(self, pk):
        try:
            return ListOfPlaces.objects.get(pk=pk)
        except ListOfPlaces.DoesNotExist:
            raise Http404

        
    def get(self, request):
        places = ListOfPlaces.objects.filter(usermodel_id=request.user.id)
        serializer = ListOfPlacesSerializer(places, many=True)
        return Response({'user_listofplaces': serializer.data}, template_name='listofplaces/listofplaces.html')
    

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
    

class ListOfPlacesCreateView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'listofplaces/create_listofplaces.html'

    def get(self, request):
        # Получаем все места для выпадающего списка
        places = PlaceModel.objects.all()
        return Response({'places': places})
    
    def post(self, request):
        # Добавляем текущего пользователя в данные
        request.data._mutable = True
        request.data['user'] = request.user.id
        request.data._mutable = False

        serializer = ListOfPlacesSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # Редирект после успешного создания
            return redirect('listofplaces')  
        
        # Если есть ошибки, показываем форму снова
        places = PlaceModel.objects.all()
        return Response(
            {'places': places, 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
class ListOfPlacesUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'listofplaces/update_listofplaces.html'

    def get_object(self, pk):
        return get_object_or_404(
            ListOfPlaces,
            pk=pk,
            usermodel=self.request.user
        )

    def get(self, request, pk):
        list_item = self.get_object(pk)
        serializer = ListOfPlacesSerializer(list_item)
        return Response({
            'list_item': list_item,
            'serialized_data': serializer.data
        })
    
    def post(self, request, pk):
        # Явно говорим, что POST = PUT для этой вьюхи
        return self.patch(request, pk)

    def patch(self, request, pk):
        list_item = self.get_object(pk)
        
        # Инвертируем текущий статус
        data = {'status': not list_item.status}
        
        serializer = ListOfPlacesSerializer(
            list_item,
            data=data,
            partial=True
        )
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return redirect('listofplaces')
        
        return Response({'errors': serializer.errors}, status=400)
    
#--------------------------------------------------------------------------------------------------#
# FeedbackModel
class FeedbackModelAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'feedback/feedbacks_of_place.html'

    def get(self, request, placemodel_id=None):
        feedbacks = FeedbackModel.objects.filter(placemodel_id=placemodel_id).select_related('usermodel')
        
        user_feedback = feedbacks.filter(usermodel_id=request.user.id).first()
        
        feedbacks_list = []
        for fb in feedbacks:
            feedback_data = {
                'pk': fb.id,
                'user_id': fb.usermodel.id,
                'user_name': fb.usermodel.username,
                'rating': fb.rating,
                'feedback_text': fb.feedback_text
            }
            feedbacks_list.append(feedback_data)
        
        place = get_object_or_404(PlaceModel, pk=placemodel_id)
        
        return Response({
            'user_feedback': user_feedback,
            'info': feedbacks_list,
            'place_id': placemodel_id,
            'place_name': place.name
        })

        
    def post(self, request, placemodel_id=None):
        # Создаем изменяемую копию request.data
        mutable_data = request.data.copy()
        
        # Добавляем название места из URL параметра
        place = get_object_or_404(PlaceModel, pk=placemodel_id)
        mutable_data['name'] = place.name
        
        serializer = FeedbackSerializer(data=mutable_data, context={'request': request})
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return redirect('place_feedbacks', placemodel_id=placemodel_id)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class FeedbackUpdateAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'feedback/update_feedback.html'
    
    def get(self, request, pk):
        feedback = FeedbackModel.objects.get(id=pk)
        return Response({'feedback': feedback})
    
    def post(self, request, pk):
        # Явно говорим, что POST = PUT для этой вьюхи
        return self.put(request, pk)
    
    def put(self, request, pk):
        #тут айди, а не пк
        if not pk:
            return Response({"error": "Primary key is not found"})
    
        try:
            instance = FeedbackModel.objects.get(pk=pk)
        except:
             return Response({"error": "Object is not found"})
        serializer = FeedbackUpdateSerializer(instance, data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return redirect('place_feedbacks', placemodel_id = instance.placemodel_id)
    

class FeedbackDeleteAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, pk):
        # Явно говорим, что POST = PUT для этой вьюхи
        return self.delete(request, pk)

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