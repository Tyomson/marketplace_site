from django.contrib import admin
from .models import Marketplace, Products, ShoppingCart


class MarketplaceAdmin(admin.ModelAdmin):
    list_display = ('name', )


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'stocks', 'price')


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_id', 'product_quantity')


admin.site.register(Marketplace, MarketplaceAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
