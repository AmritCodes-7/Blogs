from django.urls import path
from .views import (
    HomeListView,
    ReadMoreDetailView,
    BlogCreateView,
    MyBlogsListView,
    BlogUpdateView,
    SearchView,
    BlogDeleteView,
)

# urlpatterns = [
#     path("", HomeListView.as_view(), name="home_page"),
#     path("blog/<int:pk>", ReadMoreDetailView.as_view(), name="read_more_page"),
#     path("blog/create/", BlogCreateView.as_view(), name="blog_create_page"),
#     path(
#         "blogs/<slug:username>/<int:user_id>/",
#         MyBlogsListView.as_view(),
#         name="my_blogs_list_page",
#     ),
#     path("blog/update/<int:pk>/", BlogUpdateView.as_view(), name="blog_update_page"),
# ]


urlpatterns = [
    path("", HomeListView.as_view(), name="home_page"),
    path("search/", SearchView.as_view(), name="blog_search_page"),
    path("blog/create/", BlogCreateView.as_view(), name="blog_create_page"),
    path("blog/update/<int:pk>/", BlogUpdateView.as_view(), name="blog_update_page"),
    path("blog/delete/<int:pk>/", BlogDeleteView.as_view(), name="blog_delete_page"),
    path("blog/<slug:slug>/", ReadMoreDetailView.as_view(), name="read_more_page"),
    path(
        "user/<str:username>/<int:user_id>/blogs/",
        MyBlogsListView.as_view(),
        name="my_blogs_list_page",
    ),
]
