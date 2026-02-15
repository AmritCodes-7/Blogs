from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from apps.readlist.models import ReadList
from django.contrib.auth import get_user_model
from django.db import transaction


User = get_user_model()


# Create your views here.
class UserLoginView(LoginView):
    template_name = "login.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["username"].widget.attrs.update(
            {
                "class": "w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            }
        )
        form.fields["password"].widget.attrs.update(
            {
                "class": "w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            }
        )
        return form


class UserSignUpView(CreateView):
    template_name = "signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("login_page")

    def get_form(self, form_class=None):
        # Get the default form instance
        form = super().get_form(form_class)

        # Add Tailwind classes to all fields
        for field_name, field in form.fields.items():
            field.widget.attrs.update(
                {
                    "class": "w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "placeholder": field.label,  # optional: show placeholder same as label
                }
            )

        return form

    def post(self, request: HttpRequest, *args: str, **kwargs):

        with transaction.atomic():
            response = super().post(request, *args, **kwargs)

        user = self.get_form().instance

        # creating new readlist for each user while registering
        ReadList.objects.create(
            user=user,
            title="Saved Blogs",
            description="Collections of your liked or readlist",
        )

        return response


class UserLogOutView(LogoutView):
    # Where to redirect after logout
    next_page = reverse_lazy("home_page")
