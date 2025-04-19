from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

CustomUser = get_user_model()

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceModel
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class ListOfPlacesSerializer(serializers.ModelSerializer):
    usermodel = UserSerializer(read_only=True)
    placemodel = PlaceSerializer(read_only=True)
    usermodel_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source='usermodel', write_only=True
    )
    placemodel_id = serializers.PrimaryKeyRelatedField(
        queryset=PlaceModel.objects.all(), source='placemodel', write_only=True
    )

    class Meta:
        model = ListOfPlaces
        fields = '__all__'

    def create(self, validated_data):
        return ListOfPlaces.objects.create(**validated_data)


class FeedbackSerializer(serializers.ModelSerializer):
    usermodel = UserSerializer(read_only=True)
    placemodel = PlaceSerializer(read_only=True)
    usermodel_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source='usermodel', write_only=True
    )
    placemodel_id = serializers.PrimaryKeyRelatedField(
        queryset=PlaceModel.objects.all(), source='placemodel', write_only=True
    )

    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = FeedbackModel
        fields = '__all__'

    def create(self, validated_data):
        return FeedbackModel.objects.create(**validated_data)
