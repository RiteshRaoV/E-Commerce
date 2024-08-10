from django.urls import path

from brands_and_categories.views import BrandsRetrieveUpdateDestroyView, BrandsView, CategoriesRetrieveUpdateDestroyView, CategoriesView


urlpatterns = [
    path('brand/', BrandsView.as_view()),
    path('brand/<int:pk>', BrandsRetrieveUpdateDestroyView.as_view()),
    path('category/', CategoriesView.as_view()),
    path('category/<int:pk>', CategoriesRetrieveUpdateDestroyView.as_view())
]
