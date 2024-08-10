
from rest_framework import serializers

from discounts.models import Coupon, ProductDiscount, StoreDiscount
from shop.models import Product


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


class CouponSerializer(serializers.ModelSerializer):
    applicable_products = serializers.PrimaryKeyRelatedField(
        queryset = Product.objects.all(),
        many = True,
        required = False
    )
    
    excluded_products = serializers.PrimaryKeyRelatedField(
        queryset = Product.objects.all(),
        many=True,
        required = False
    )
    
    class Meta:
        model = Coupon
        exclude = ['code']
        
    def create(self, validated_data):
        applicable_products = validated_data.pop('applicable_products',[])
        excluded_products = validated_data.pop('excluded_products',[])
        
        coupon = super().create(validated_data)
        coupon.applicable_products.set(applicable_products)
        coupon.excluded_products.set(excluded_products)
        return coupon