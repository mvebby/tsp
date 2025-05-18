from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import *
from django.http import Http404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceModel
        fields = '__all__'
    

    def create(self, validated_data):
        return PlaceModel.objects.create(**validated_data)
    

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.country = validated_data.get("country", instance.country)
        instance.city = validated_data.get("city", instance.city)
        instance.address = validated_data.get("address", instance.address)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'age']


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'age', 'password', 'password_confirm']
    
    def validate(self, input_data):
        if input_data['password'] != input_data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Error in password"})
        return input_data
    

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password', None)
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class PasswordChangeSerializator(serializers.Serializer):
    model = CustomUser
    old_password = serializers.CharField(required = True)
    new_password = serializers.CharField(required = True)
    new_password_confirm = serializers.CharField(required = True)

    def validate(self, input_data):
        if input_data['new_password'] != input_data['new_password_confirm']:
            raise serializers.ValidationError({"new_password_confirm": "Error in password"})
        return input_data
    

class ListOfPlacesSerializer(serializers.ModelSerializer):
    placemodel = serializers.PrimaryKeyRelatedField(queryset = PlaceModel.objects.all())
    usermodel = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = ListOfPlaces
        fields = '__all__'
        read_only_fields = ['date']
    
    def create(self, validated_data):
        return ListOfPlaces.objects.create(**validated_data)
    

    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance

class FeedbackSerializer(serializers.ModelSerializer):
    placemodel = serializers.PrimaryKeyRelatedField(read_only = True)
    usermodel = serializers.HiddenField(default=serializers.CurrentUserDefault())
    name = serializers.CharField(write_only=True)
    class Meta:
        model = FeedbackModel
        fields = ['usermodel', 'placemodel', 'rating', 'feedback_text', 'name']
        read_only_fields = ['placemodel']
    
    def validate(self, input_data):
        name = input_data.get('name')
        user = self.context['request'].user

        try:
            place = PlaceModel.objects.get(name=name)
        except PlaceModel.DoesNotExist:
            raise Http404
        check_status = ListOfPlaces.objects.filter(usermodel=user, placemodel=place, status=True).exists()
        if not check_status:
            raise ValidationError('Вы можете оставить отзыв только для мест, где вы были.')
        input_data['placemodel'] = place
        return input_data

    
    def create(self, validated_data):
        name = validated_data.pop('name')
        return FeedbackModel.objects.create(**validated_data)


class FeedbackUpdateSerializer(serializers.ModelSerializer):
    placemodel = serializers.PrimaryKeyRelatedField(read_only = True)
    usermodel = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = FeedbackModel
        fields = ['usermodel', 'placemodel', 'rating', 'feedback_text']
        read_only_fields = ['placemodel']

    def update(self, instance, validated_data):
        instance.rating = validated_data.get("rating", instance.rating)
        instance.feedback_text = validated_data.get("feedback_text", instance.feedback_text)
        instance.save()
        return instance