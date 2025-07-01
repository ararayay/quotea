from .models import Quotes
from django.forms import ModelForm, TextInput, Textarea, NumberInput


# Форма для добавления цитаты
class AddQuote(ModelForm):
    class Meta:
        model = Quotes
        fields = ['quote', 'source', 'character', 'weight']

        widgets = {
            'quote': Textarea(attrs={
                'placeholder': 'Цитата',
                'rows': 2
            }),
            'source': TextInput(attrs={
                'placeholder': 'Источник'
            }),
            'character': TextInput(attrs={
                'placeholder': 'Персонаж'
            }),
            'weight': NumberInput(attrs={
                'placeholder': 'Вес'
            }),
        }