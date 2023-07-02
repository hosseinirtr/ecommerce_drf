from django.contrib import admin

from .models import Brand, Categories, Product, ProductLine

# Register your models here.


class ProductLineInline(admin.TabularInline):
    model = ProductLine


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductLineInline]


admin.site.register(Brand)
admin.site.register(Categories)
# admin.site.register(Product)
