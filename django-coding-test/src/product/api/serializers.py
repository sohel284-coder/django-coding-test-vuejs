
from dataclasses import fields
from rest_framework import serializers

from product.models import *


class ProductVariationPriceSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, default='')
    sku = serializers.SlugField()
    description = serializers.CharField(max_length=5000, default='')

    product_variant = serializers.ListField(child=serializers.JSONField())
    product_variant_prices = serializers.ListField(child=serializers.JSONField())


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'sku', 'description', )