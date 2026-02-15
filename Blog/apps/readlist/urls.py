from django.urls import path
from .views import ReadListView

urlpatterns = [
    path(
        "user/<str:username>/<int:id>/",
        ReadListView.as_view(),
        name="read_list_page",
    ),
]
