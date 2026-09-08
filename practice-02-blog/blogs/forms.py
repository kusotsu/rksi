from django import forms

from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "text"]
        widgets = {"text": forms.Textarea(attrs={"rows": 10})}

