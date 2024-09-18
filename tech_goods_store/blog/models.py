from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from taggit.managers import TaggableManager

from common.utils import unique_slugify
from users.models import User
from django.db.models import Count

# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Posts.Status.PUBLISH)

class NotEmptyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(posts=None)


class Posts(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISH = 1, 'Опубликовано'
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = models.SlugField(max_length=250, unique=True, unique_for_date='date_publish', verbose_name='Слаг')
    image = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True, null=True, default=None, verbose_name='Изображение')
    content = models.TextField(blank=True, verbose_name='Контент')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', blank=True, verbose_name='Автор', null=True)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Изменен')
    date_publish = models.DateTimeField(default=timezone.now, verbose_name='Время публикации')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name='Статус')
    cats = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts', blank=True, verbose_name='Категория', null=True)
    tags = TaggableManager()

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-date_publish']
        indexes = [
            models.Index(fields=['-date_publish'])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail_post', kwargs={
                                                    'year': self.date_publish.year,
                                                    'month': self.date_publish.month,
                                                    'day': self.date_publish.day,
                                                    'post_slug': self.slug
                                                    })

    def save(self, *args, **kwargs):
        self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)


class Category(models.Model):
    slug = models.SlugField(max_length=250, unique=True, verbose_name='Слаг')
    name = models.CharField(max_length=150, verbose_name='Название')

    not_empty = NotEmptyManager()
    object = models.Manager()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:posts_cat', kwargs={'cat_slug': self.slug})




class Comment(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Скрыт'
        PUBLISH = 1, 'Опубликован'
    name = models.CharField(max_length=80, verbose_name='Имя пользователя')
    email = models.EmailField(verbose_name='Эл. почта')
    body = models.TextField(verbose_name='Текст комментария')
    post = models.ForeignKey(Posts,
                             on_delete=models.CASCADE,
                             related_name='comments',
                             verbose_name='Пост')
    date_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Дата создания')
    date_update = models.DateTimeField(auto_now=True,
                                       verbose_name='Дата редактирования')
    active = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.PUBLISH, verbose_name='Опубликован')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['date_create']
        indexes = [
            models.Index(fields=['date_create'])
        ]

    def __str__(self):
        return f'От {self.name} к {self.post}'