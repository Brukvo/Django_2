from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView


class OrderListView(ListView):
    pass


class OrderCreateView(CreateView):
    pass


class OrderDetailView(DetailView):
    pass


class OrderUpdateView(UpdateView):
    pass


class OrderDeleteView(DeleteView):
    pass


def order_forming_complete(request, pk):
    pass
