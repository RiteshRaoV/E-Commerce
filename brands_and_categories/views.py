from django.shortcuts import render
from rest_framework import generics

from brands_and_categories.models import Brand, Category
from brands_and_categories.serializers import BrandSerializer, CategorySerializer
from rest_framework.parsers import MultiPartParser, FormParser


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
