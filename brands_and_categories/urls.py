from django.urls import path

from brands_and_categories.views import BrandProductsView, BrandsRetrieveUpdateDestroyView, BrandsView, CategoriesRetrieveUpdateDestroyView, CategoriesView, CategoryProductsView


urlpatterns = [
    path('brand/', BrandsView.as_view()),
    path('brand/<int:pk>', BrandsRetrieveUpdateDestroyView.as_view()),
    path('brand/products/<int:brand_id>',BrandProductsView.as_view()),
    path('category/', CategoriesView.as_view()),
    path('category/<int:pk>', CategoriesRetrieveUpdateDestroyView.as_view()),
    path('category/products/<int:category_id>',CategoryProductsView.as_view()),
]
