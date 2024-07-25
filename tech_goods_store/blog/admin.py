from django.contrib import admin, messages
from django.utils import timezone

from .models import Posts, Category, Comment

# Register your models here.
# class AnyTagFilter(admin.SimpleListFilter):
#     title = 'Тег'
#     parameter_name = 'tag'
#     def lookups(self, request, model_admin):
#         return [
#             ('notag', 'Без тега'),
#             ('anytag', 'Есть тег(-и)')
#         ]
#     def queryset(self, request, queryset):
#         if self.value() == 'notag':
#             return queryset.filter(tags__isnull=True)
#         elif self.value() == 'anytag':
#             return queryset.filter(tags__isnull=True)



@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'date_publish', 'is_published', 'cats']
    list_display_links = ['id', 'title']
    list_editable = ['is_published', 'cats']
    list_per_page = 5
    list_filter = ['is_published', 'date_create', 'date_publish', 'author', 'cats']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'date_publish'
    ordering = ['title', 'is_published', 'date_publish']
    readonly_fields = ('date_create', 'date_update')
    actions = ['set_published', 'set_draft']
    @admin.action(description='Опубликовать')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Posts.Status.PUBLISH)
        queryset.update(date_publish=timezone.now())
        self.message_user(request, f'Опубликовано {count} записей', messages.WARNING)

    @admin.action(description='Снять с публикации')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Posts.Status.DRAFT)
        self.message_user(request, f'Снято с публикации {count} записей')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'post', 'name', 'email', 'date_create', 'active']
    list_display_links = ['pk']
    ordering = ['-date_create', 'name']
    search_fields = ['name', 'email', 'body']
    actions = ['set_published', 'set_draft']
    @admin.action(description='Опубликовать')
    def set_published(self, request, queryset):
        count = queryset.update(active=Comment.Status.PUBLISH)
        self.message_user(request, f'Опубликовано {count} комментариев', messages.WARNING)

    @admin.action(description='Снять с публикации')
    def set_draft(self, request, queryset):
        count = queryset.update(active=Comment.Status.DRAFT)
        self.message_user(request, f'Снято с публикации {count} комментариев')

