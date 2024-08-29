from django.db import models

from goods.models import Products
from users.models import User

# Create your models here.
class OrderitemQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.total_product_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0

class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Пользователь')
    last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Фамилия')
    first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Имя')
    middle_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Отчество')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    email = models.CharField(max_length=55, blank=True, null=True, verbose_name='E-mail')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    requires_delivery = models.BooleanField(default=False, verbose_name="Требуется доставка")
    address_delivery = models.TextField(null=True, blank=True, verbose_name='Адрес доставки')
    postcode = models.CharField(max_length=15, verbose_name='Почтовый индекс', null=True, blank=True)
    payment_on_get = models.BooleanField(default=True, verbose_name='Оплата при получении')
    notes = models.TextField(null=True, blank=True)
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    status = models.CharField(max_length=50, default='В обработке', verbose_name='Статус заказа')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self) -> str:
        return f'Заказ № {self.pk} | Покупатель: { self.last_name } { self.first_name}  {self.middle_name}'
    

class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(to=Products, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Товар')
    name = models.CharField(max_length=150, blank=True, null=True, verbose_name='Название товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')

    class Meta:
        verbose_name = 'Заказанный товар'
        verbose_name_plural = 'Заказанные товары'

    objects = OrderitemQueryset.as_manager()

    def total_product_price(self):
        return round(self.price * self.quantity, 2)
    
    def __str__(self) -> str:
        return f'Товар { self.name } | Заказ № { self.order.pk }'