from .models import Quotes
from django.forms import ModelForm, TextInput, Textarea, NumberInput


# Форма для добавления цитаты
class AddQuote(ModelForm):
    class Meta:
        model = Quotes
        fields = ['quote', 'source', 'character', 'weight']

        widgets = {
            'quote': Textarea(attrs={
                'rows': 2
            }),
            'source': TextInput(),
            'character': TextInput(),
            'weight': NumberInput(),
        }