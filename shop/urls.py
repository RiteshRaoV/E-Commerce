from django.urls import path

from shop.views import AddProductView, AddProductsToStoreView, AddToCartView, CancelOrderView, CreateOrderView, CreateStoreView, ListAllProducts, ListCartItemsView, ListOrdersView, ListSellersProductsView, ListStoreProductsView, UpdateCartItemsView, UpdateProductDetailsView, UploadProductImagesView


urlpatterns = [
    path('store/create/', CreateStoreView.as_view()),
    path('store/add-product/', AddProductsToStoreView.as_view()),
    path('store/products/<int:store_id>', ListStoreProductsView.as_view()),
    path('product/all/', ListAllProducts.as_view()),
    path('product/seller/<int:seller_id>', ListSellersProductsView.as_view()),
    path('product/add/', AddProductView.as_view()),
    path('product/upload-images/', UploadProductImagesView.as_view()),
    path('product/update/<int:product_id>',
         UpdateProductDetailsView.as_view()),
    path('cart/items/<int:user_id>', ListCartItemsView.as_view()),
    path('cart/add-to-cart/', AddToCartView.as_view()),
    path('cart/<int:cart_item_id>', UpdateCartItemsView.as_view()),
    path('order/place-order/', CreateOrderView.as_view()),
    path('order/cancel-order/<int:order_id>', CancelOrderView.as_view()),
    path('order/all/', ListOrdersView.as_view())
]
