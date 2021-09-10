from rest_framework import serializers
from .models import Products, Marketplace


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['product_name', 'stocks', 'price']


class MarketplaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marketplace
        fields = ['name']
