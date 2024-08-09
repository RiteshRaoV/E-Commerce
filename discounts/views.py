from django.shortcuts import render
from rest_framework import generics

from discounts.models import ProductDiscount
from discounts.serializers import ProductDiscountDetailSerializer, ProductDiscountSerializer, ShopDiscountDetailSerializer, StoreDiscountSerializer
# Create your views here.


class CreateProductDiscountView(generics.CreateAPIView):
    queryset = ProductDiscount.objects.all()
    serializer_class = ProductDiscountSerializer


class CreateStoreDiscountView(generics.CreateAPIView):
    queryset = ProductDiscount.objects.all()
    serializer_class = StoreDiscountSerializer


class UpdateDestroyProductDiscountView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductDiscount.objects.all()
    serializer_class = ProductDiscountDetailSerializer


class UpdateDestroyStoreDiscountView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductDiscount.objects.all()
    serializer_class = ShopDiscountDetailSerializer
