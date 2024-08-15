from django.db import models

from goods.models import Products
from users.models import User

# Create your models here.
class CartQueryset(models.QuerySet):
    
    def total_price(self):
        if self:
            return sum(cart.product_total_price() for cart in self)
        return 0

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0
    
    def quant_user_cats(self):
        return len(self)

class Cart(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь', related_name='cart')
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name='Количество')
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    objects = CartQueryset().as_manager()

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        ordering = ['-created_timestamp']

    def product_total_price(self):
        return round(self.product.price_with_discount() * self.quantity, 2)
    
    def __str__(self):
        return f'Корзина {self.user} | Товар {self.product.name[:40]}... | Количество {self.quantity}'
    