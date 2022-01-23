from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView
from mainapp.mixin import BaseClassContextMixin
from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderItemsForm
from baskets.models import Basket


class OrderListView(ListView, BaseClassContextMixin):
    model = Order
    title = 'GeekShop // Заказы'

    def get_queryset(self):
        return Order.objects.filter(is_active=True)


class OrderCreateView(CreateView, BaseClassContextMixin):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:list')
    title = 'GeekShop // Создание заказа'

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        order_formset = inlineformset_factory(Order, OrderItem, OrderItemsForm, extra=1)

        if self.request.POST:
            formset = order_formset(self.request.POST)
        else:
            basket_item = Basket.objects.filter(user=self.request.user)
            if basket_item:
                order_formset = inlineformset_factory(Order, OrderItem, OrderItemsForm, extra=1)
                formset = order_formset()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_item[num].product
                    form.initial['quantity'] = basket_item[num].quantity
                    form.initial['price'] = basket_item[num].product.price
                # basket_item.delete()
            else:
                formset = order_formset()
        context['order_items'] = formset

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context['order_items']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if order_items.is_valid():
                order_items.instance = self.object
                order_items.save()
                
            if self.object.get_total_cost() == 0:
                self.object.delete()
                
        return super(OrderCreateView, self).form_valid(form)


class OrderDetailView(DetailView, BaseClassContextMixin):
    model = Order
    title = 'GeekShop // Детали заказа'


class OrderUpdateView(UpdateView, BaseClassContextMixin):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:list')
    title = 'GeekShop // Изменение заказа'

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)
        order_formset = inlineformset_factory(Order, OrderItem, OrderItemsForm, extra=1)

        if self.request.POST:
            formset = order_formset(self.request.POST, instance=self.object)
        else:
            formset = order_formset()
            for form in formset:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price

        context['order_items'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context['order_items']

        with transaction.atomic():
            self.object = form.save()
            if order_items.is_valid():
                order_items.instance = self.object
                order_items.save()

            if self.object.get_total_cost() == 0:
                self.object.delete()

        return super(OrderUpdateView, self).form_valid(form)


class OrderDeleteView(DeleteView, BaseClassContextMixin):
    model = Order
    success_url = reverse_lazy('orders:list')
    title = 'GeekShop // Удаление заказа'


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_FORM
    order.save()
    return HttpResponseRedirect(reverse('orders:list'))
