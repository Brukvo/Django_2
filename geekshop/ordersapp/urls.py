from django.urls import path

from ordersapp.views import OrderListView, OrderCreateView, OrderDetailView, OrderUpdateView, OrderDeleteView, order_forming_complete

app_name = 'ordersapp'
urlpatterns = [
    path('', OrderListView.as_view(), name='orders_list'),
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('update/<int:pk>/', OrderUpdateView.as_view(), name='order_update'),
    path('view/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('remove/<int:pk>/', OrderDeleteView.as_view(), name='order_delete'),
    path('remove/<int:pk>/', order_forming_complete, name='order_forming_complete'),
]
