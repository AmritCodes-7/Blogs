from django.urls import path
from .views import UserLoginView, UserSignUpView, UserLogOutView

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login_page"),
    path("signup/", UserSignUpView.as_view(), name="signup_page"),
    path("logout/", UserLogOutView.as_view(), name="logout_page"),
]
