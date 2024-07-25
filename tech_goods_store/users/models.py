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


    gender = models.CharField(max_length=20, choices=Gender.choices, blank=True, default=Gender.NOT_CHOSEN)
  #  address = models.ManyToManyField('Address', blank=True, verbose_name='Адреса доставки', related_name='users')
    date_birth = models.DateField(blank=True, default=None, null=True, verbose_name='Дата рождения')
   # orders
    subs_news = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), IsSubs.choices)), default=IsSubs.SUB,
                                    verbose_name='Подписка на рассылку')
    photo = models.ImageField(upload_to='users/photo/%Y/%m/%d/', blank=True, default=None, null=True, verbose_name='Фото')

