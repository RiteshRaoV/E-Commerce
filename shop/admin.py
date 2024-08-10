from django.contrib import admin

from shop.models import Cart, CartItem, CustomUser, Order, OrderItem, Product, ProductImage, Store, StoreProduct

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(ProductImage)

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Store)
admin.site.register(StoreProduct)
