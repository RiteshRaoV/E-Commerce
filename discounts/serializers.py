
from rest_framework import serializers

from discounts.models import ProductDiscount, StoreDiscount


class ProductDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDiscount
        fields = '__all__'


class StoreDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreDiscount
        fields = '__all__'


class ProductDiscountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDiscount
        fields = '__all__'


class ShopDiscountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDiscount
        fields = '__all__'
