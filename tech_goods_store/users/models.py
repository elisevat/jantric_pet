from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'male', 'Мужчина'
        FEMALE = 'female', 'Женщина'
        NOT_CHOSEN = 'not_chosen', 'Не выбрано'

    class IsSubs(models.IntegerChoices):
        SUB = 1, 'Подписан(-а)'
        UNSUB = 0, 'Не подписан(-а)'

    middle_name = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=Gender.choices, blank=True, default=Gender.NOT_CHOSEN, verbose_name='Пол')
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address_delivery = models.TextField(blank=True, null=True, verbose_name='Адрес доставки')
    date_birth = models.DateField(blank=True, default=None, null=True, verbose_name='Дата рождения')
   # orders
    subs_news = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), IsSubs.choices)), default=IsSubs.SUB,
                                    verbose_name='Подписка на рассылку')
    photo = models.ImageField(upload_to='users/photo/%Y/%m/%d/', blank=True, default=None, null=True, verbose_name='Фото')

    class Meta:
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
    

