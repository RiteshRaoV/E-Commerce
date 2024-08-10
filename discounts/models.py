import random
import string
from django.db import models

from shop.models import Product, Store
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator
from datetime import date

# Create your models here.


class ProductDiscount(models.Model):
    DISCOUNT_TYPES = [
        ("percentage", "Percentage"),
        ("fixed", "Fixed Amount"),
    ]

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="discounts"
    )
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.discount_type} - {self.amount} for {self.product}"


class StoreDiscount(models.Model):
    DISCOUNT_TYPES = [
        ("percentage", "Percentage"),
        ("fixed", "Fixed Amount"),
    ]

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="discounts")
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.discount_type} - {self.amount} for {self.store}"


class Coupon(models.Model):
    DISCOUNT_TYPES = [
        ("percentage", "Percentage"),
        ("fixed", "Fixed Amount"),
        ("free_shipping", "Free Shipping"),
    ]

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=25, unique=True, blank=True)
    description = models.TextField(max_length=200, blank=True)
    discount_type = models.CharField(
        max_length=20, choices=DISCOUNT_TYPES, default="percentage"
    )
    discount_value = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    min_purchase_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=0
    )
    start_date = models.DateField(default=timezone.now)
    expiry_date = models.DateField()
    coupon_count = models.IntegerField(default=0)
    per_user_limit = models.IntegerField(default=1)
    is_valid = models.BooleanField(default=True)  # Changed default to True
    applicable_products = models.ManyToManyField(
        Product, blank=True, related_name="applicable_coupons"
    )
    excluded_products = models.ManyToManyField(
        Product, blank=True, related_name="excluded_coupons"
    )

    def __str__(self):
        return self.code or "No Code"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        super().save(*args, **kwargs)

    def generate_code(self):
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def is_active(self):
        today = timezone.now().date()
        return self.is_valid and self.start_date <= today <= self.expiry_date

    def apply_discount(self, total_amount):
        if not self.is_active():
            return total_amount

        if self.discount_type == "percentage":
            discount = (self.discount_value / 100) * total_amount
        elif self.discount_type == "fixed":
            discount = self.discount_value
        elif self.discount_type == "free_shipping":
            return 0
        else:
            discount = 0

        return max(total_amount - discount, 0)

    def has_user_used(self, user):
        return CouponUsage.objects.filter(coupon=self, user=user).exists()


class CouponUsage(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("coupon", "user")

    def __str__(self):
        return f"{self.coupon.code} used by {self.user.username}"
