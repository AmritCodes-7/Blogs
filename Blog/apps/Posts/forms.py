from django import forms
from .models import Blogs
from django_ckeditor_5.widgets import CKEditor5Widget


class BlogCreateForm(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = ["title", "body", "featured_image"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full text-4xl md:text-5xl font-bold border-none outline-none focus:ring-0 bg-transparent",
                    "placeholder": "Title",
                }
            ),
            "body": CKEditor5Widget(
                attrs={"class": "ckeditor-field"},
                config_name="extends",
            ),
            "featured_image": forms.FileInput(
                attrs={"class": "hidden", "accept": "image/*"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove labels
        for field in self.fields:
            self.fields[field].label = ""
            self.fields[field].required = False

        # Explicit required fields
        self.fields["title"].required = True
        self.fields["body"].required = True

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if not title or not title.strip():
            raise forms.ValidationError("Please add a title to your story")
        if len(title) > 200:
            raise forms.ValidationError("Title must be less than 200 characters")
        return title.strip()

    def clean_body(self):
        body = self.cleaned_data.get("body")
        if not body or not body.strip():
            raise forms.ValidationError("Your story needs content")
        if len(body) < 50:
            raise forms.ValidationError(
                "Your story is too short. Write at least 50 characters."
            )
        return body
