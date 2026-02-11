from django import forms
from .models import Blogs


class BlogCreateForm(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = ["title", "body", "featured_image"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full text-4xl font-bold border-none outline-none focus:ring-0 placeholder-gray-400",
                    "placeholder": "Title",
                }
            ),
            "body": forms.Textarea(
                attrs={
                    "class": "w-full text-lg border-none outline-none focus:ring-0 placeholder-gray-400 resize-none",
                    "rows": 20,
                    "placeholder": "Tell your story...",
                }
            ),
            "featured_image": forms.FileInput(
                attrs={
                    "class": "hidden",
                    "id": "featured-image-input",
                    "accept": "image/*",
                }
            ),
        }
