from django.db import models
from django.conf import settings

# Create your models here.
from mainapp.models import Product


class Order(models.Model):
    PROCESSING = 'PR'
    SENT_TO_FORM = "STF"
    SENT = 'ST'
    PAID = 'PD'
    READY = 'RD'
    CANCELLED = 'CD'

    ORDER_STATUS_CHOICES = (
        (PROCESSING, 'Обрабатывается'),
        (SENT_TO_FORM, 'Отправлен на сборку'),
        (SENT, 'Передан в службу доставки'),
        (PAID, 'Оплачен, ожидает отправки'),
        (READY, 'Доставлен'),
        (CANCELLED, 'Отменён'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='дата и время создания заказа', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='дата и время обновления заказа', auto_now=True)
    state = models.CharField(choices=ORDER_STATUS_CHOICES, verbose_name='статус заказа', max_length=3, default=PROCESSING)
    is_active = models.BooleanField(verbose_name='активен', default=True)

    def __str__(self):
        return f'Заказ №{self.pk} от {self.created_at}'

    def get_total_quantity(self):
        items = self.order_items.select_related('product')
        return sum(list(map(lambda x: x.quantity, items)))

    def get_total_cost(self):
        items = self.order_items.select_related('product')
        return sum(list(map(lambda x: x.get_product_cost(), items)))

    def get_items(self):
        pass

    def delete(self, using=None, keep_parents=False):
        for item in self.order_items.select_related('product'):
            item.product.quantity += item.quantity
            item.save()
        self.is_active = False
        self.save()

    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='заказ', related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='товар', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity


