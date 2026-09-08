from django import forms

from .models import Entry, Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["text"]
        labels = {"text": "Название темы"}
        widgets = {"text": forms.TextInput(attrs={"placeholder": "Например, Python"})}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["text"]
        labels = {"text": "Что вы узнали?"}
        widgets = {
            "text": forms.Textarea(
                attrs={"rows": 8, "placeholder": "Сформулируйте новую мысль или наблюдение"}
            )
        }
