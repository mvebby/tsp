from django import forms
from tsp_database_app.models import *

class SearchForm(forms.Form):
    search_by = forms.ChoiceField(label="Поиск по:", choices=[
        ('name', 'Название'),
        ('city', 'Город'),
        ('country', 'Страна')
    ])
    search_query = forms.CharField(label="Введите запрос", max_length=255)