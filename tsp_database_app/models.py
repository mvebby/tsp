from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.
class PlaceModel(models.Model):
    place_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    country = models.CharField(max_length=57, null=False)
    city = models.CharField(max_length=170, null=False)
    address = models.TextField(null=True, blank=True)

class CustomUser(AbstractUser):
    age = models.SmallIntegerField(null=True, blank=True)

    def __str__(self):
       return self.username


class ListOfPlaces(models.Model):
    usermodel = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    placemodel = models.ForeignKey(PlaceModel, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = (('usermodel', 'placemodel'),)

class FeedbackModel(models.Model):
    usermodel = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    placemodel = models.ForeignKey(PlaceModel, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(null=False, blank=False, validators=[MaxValueValidator(5), MinValueValidator(1)])
    feedback_text = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('usermodel', 'placemodel'),)
