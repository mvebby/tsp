from django import forms
from tsp_database_app.models import *

class SearchForm(forms.Form):
    search_by = forms.ChoiceField(label="Поиск по:", choices=[
        ('name', 'Название'),
        ('city', 'Город'),
        ('country', 'Страна')
    ])
    search_query = forms.CharField(label="Введите запрос", max_length=255)


class PlaceChoiceForm(forms.Form):
    placemodel = forms.ModelChoiceField(queryset=PlaceModel.objects.all(), label="Выберите место")


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedbackModel
        fields = ['placemodel', 'rating', 'feedback_text']
        
    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if not (1 <= rating <= 5):
            raise forms.ValidationError("Рейтинг должен быть от 1 до 5")
        return rating