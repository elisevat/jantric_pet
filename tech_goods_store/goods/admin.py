from django.contrib import admin
from .models import Categories, Products

# Register your models here.


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name",)


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "discount", "quantity", "category")
    list_editable = ("price", "discount")
    list_filter = ("category",)
    search_fields = ("name", "description", "category__name")
    prepopulated_fields = {"slug": ("name",)}

    fields = (
        "name",
        "category",
        "slug",
        ("price", "discount"),
        "quantity",
        "image",
        "description",
    )
