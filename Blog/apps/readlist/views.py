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
from .models import ReadList, ReadListItem


# Create your views here.
class ReadListView(ListView, LoginRequiredMixin):
    model = ReadList
    template_name = "read_list.html"
    context_object_name = "readlist"
    paginate_by = 10

    def get_queryset(self):
        return ReadList.objects.filter(user=self.request.user)
