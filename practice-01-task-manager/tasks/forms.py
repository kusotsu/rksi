from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        label="Срок выполнения",
        required=False,
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
        error_messages={"invalid": "Введите корректные дату и время."},
    )

    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "priority", "completed"]
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}

