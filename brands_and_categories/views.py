from django.shortcuts import render
from rest_framework import generics

from brands_and_categories.models import Brand, Category
from brands_and_categories.serializers import BrandSerializer, CategorySerializer
from rest_framework.parsers import MultiPartParser, FormParser

from shop.models import Product
from shop.serializers import ProductSerializer


# Create your views here.
class BrandsView(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    parser_classes = [MultiPartParser, FormParser]


class BrandsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoriesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BrandProductsView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        brand_id=self.kwargs.get('brand_id')
        return Product.objects.filter(brand=brand_id)
    
class CategoryProductsView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        category_id=self.kwargs.get('category_id')
        return Product.objects.filter(category=category_id)