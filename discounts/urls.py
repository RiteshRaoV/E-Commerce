

from django.urls import path

from discounts.views import CreateProductDiscountView, CreateStoreDiscountView, UpdateDestroyProductDiscountView, UpdateDestroyStoreDiscountView


urlpatterns = [
    path('product/add-discount/', CreateProductDiscountView.as_view()),
    path('store/add-discount/', CreateStoreDiscountView.as_view()),
    path('product/discount/<int:pk>', UpdateDestroyProductDiscountView.as_view()),
    path('store/discount/<int:pk>', UpdateDestroyStoreDiscountView.as_view())
]
