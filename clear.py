import os
import sys

# Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsp.settings')

# Импортируем модели
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from tsp_database_app.models import *
from django.core.validators import MaxValueValidator, MinValueValidator

# Удаление всех данных из моделей
CustomUser.objects.all().delete()
PlaceModel.objects.all().delete()
ListOfPlaces.objects.all().delete()
FeedbackModel.objects.all().delete()
