from django.urls import path

from shop.views import AddProductView, AddProductsToStoreView, AddToCartView, CancelOrderView, CreateOrderView, CreateStoreView, ListAllProducts, ListCartItemsView, ListOrdersView, ListSellersProductsView, ListStoreProductsView, UpdateCartItemsView, UpdateProductDetailsView


urlpatterns = [
    path('store/create/', CreateStoreView.as_view()),
    path('store/add-product/', AddProductsToStoreView.as_view()),
    path('store/products/<int:store_id>', ListStoreProductsView.as_view()),
    path('products/', ListAllProducts.as_view()),
    path('seller/products/<int:seller_id>', ListSellersProductsView.as_view()),
    path('product/add/', AddProductView.as_view()),
    path('product/update/<int:product_id>',
         UpdateProductDetailsView.as_view()),
    path('cart/items/<int:user_id>', ListCartItemsView.as_view()),
    path('cart/add-to-cart/', AddToCartView.as_view()),
    path('cart/<int:cart_item_id>', UpdateCartItemsView.as_view()),
    path('place-order/', CreateOrderView.as_view()),
    path('cancel-order/<int:order_id>', CancelOrderView.as_view()),
    path('orders/', ListOrdersView.as_view())
]
