from django.contrib import admin

from shop.models import Brand, Cart, CartItem, Category, CustomUser, Order, OrderItem, Product, Store, StoreProduct

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Store)
admin.site.register(StoreProduct)
