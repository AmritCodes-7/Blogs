from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Blogs
from .forms import BlogCreateForm


# ----------------- Utility Mixin for Sorting -----------------
class BlogSortMixin:
    """
    Adds sorting functionality to ListViews.
    Reads ?sort=latest|oldest|author from URL query params.
    """

    def get_queryset(self):
        qs = self.base_queryset()
        sort = self.request.GET.get("sort", "latest")

        if sort == "author":
            qs = qs.order_by("author__username")
        elif sort == "oldest":
            qs = qs.order_by("created_at")
        else:  # latest by default
            qs = qs.order_by("-created_at")

        return qs

    def base_queryset(self):
        """
        Base queryset with author prefetching.
        Override in subclasses if needed.
        """
        return Blogs.objects.select_related("author")


# ----------------- Home / Blog List -----------------
class HomeListView(BlogSortMixin, ListView):
    model = Blogs
    template_name = "home.html"
    context_object_name = "blogs"
    paginate_by = 3


# ----------------- Blog Detail -----------------
class ReadMoreDetailView(DetailView):
    model = Blogs
    template_name = "read_more.html"
    context_object_name = "blog"

    def get_queryset(self):
        return Blogs.objects.select_related("author")


# ----------------- Blog Create -----------------
class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blogs
    form_class = BlogCreateForm
    template_name = "blog_create.html"
    success_url = reverse_lazy("home_page")
    login_url = "login_page"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# ----------------- My Blogs (Author-specific) -----------------
class MyBlogsListView(BlogSortMixin, LoginRequiredMixin, ListView):
    model = Blogs
    template_name = "home.html"
    context_object_name = "blogs"
    paginate_by = 3
    login_url = "login_page"

    def base_queryset(self):
        user_id = self.kwargs["user_id"]
        return Blogs.objects.filter(author__id=user_id).select_related("author")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blogs_author"] = self.kwargs["username"]
        context["no_author_sort"] = True
        return context


# ----------------- Blog Update -----------------
class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blogs
    form_class = BlogCreateForm
    template_name = "blog_update.html"
    success_url = reverse_lazy("home_page")
    login_url = "login_page"

    def get_queryset(self):
        # Only allow current user to update their own blogs
        return Blogs.objects.filter(author=self.request.user)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# ----------------- Blog Search -----------------
class SearchView(BlogSortMixin, ListView):
    model = Blogs
    template_name = "search_results.html"
    context_object_name = "blogs"
    paginate_by = 3

    def base_queryset(self):
        qs = Blogs.objects.select_related("author")
        query = self.request.GET.get("q", "")
        if query:
            qs = qs.filter(Q(title__icontains=query) | Q(body__icontains=query))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sort"] = self.request.GET.get("sort", "latest")
        return context


class BlogDeleteView(DeleteView):
    model = Blogs
    template_name = "blog_delete.html"
    success_url = reverse_lazy("home_page")  # Redirect after deletion

    def get_queryset(self):
        # Ensure only the author can delete their own blog
        return super().get_queryset().filter(author=self.request.user)
