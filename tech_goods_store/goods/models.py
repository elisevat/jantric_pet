from django.db import models
from django.urls import reverse

# Create your models here.

class NotEmptyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(prods=None)


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=210, unique=True, blank=True, null=True, verbose_name='URL')

    not_empty = NotEmptyManager()
    objects = models.Manager()

    class Meta:
        verbose_name = "Категорию товаров"
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("goods:category", kwargs={"category_slug": self.slug})

    


class Products(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=210, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='goods_images/', blank=True, null=True, verbose_name='Изображение')
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name='Скидка в %')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория', related_name='prods')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('id',)

    def __str__(self):
        return self.name[:25]
    
    def get_absolute_url(self):
        return reverse("goods:product", kwargs={"product_slug": self.slug})

    def price_with_discount(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        return self.price
    