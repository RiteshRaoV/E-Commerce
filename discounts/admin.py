from django.contrib import admin

from discounts.models import Coupon, CouponUsage, ProductDiscount, StoreDiscount

# Register your models here.
admin.site.register(Coupon)
admin.site.register(ProductDiscount)
admin.site.register(StoreDiscount)
admin.site.register(CouponUsage)