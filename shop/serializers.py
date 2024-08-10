from datetime import date
from rest_framework import serializers

from shop.models import (
    CartItem,
    Order,
    OrderItem,
    Product,
    ProductImage,
    Store,
    StoreProduct,
)


def get_discounted_price(product):
    price = product.price

    product_discounts = product.discounts.filter(
        is_active=True, start_date__lte=date.today(), end_date__gte=date.today()
    )
    for discount in product_discounts:
        if discount.discount_type == "percentage":
            price -= price * (discount.amount / 100)
        elif discount.discount_type == "fixed":
            price -= discount.amount

    price = max(price, 0)
    store_products = product.store_products.all()
    store_discounts = []
    if store_products.exists():
        store = store_products[0].store
        store_discounts = store.discounts.filter(
            is_active=True, start_date__lte=date.today(), end_date__gte=date.today()
        )

    for discount in store_discounts:
        if discount.discount_type == "percentage":
            price -= price * (discount.amount / 100)
        elif discount.discount_type == "fixed":
            price -= discount.amount

    return max(price, 0)


class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source="brand.name", read_only=True)
    category = serializers.CharField(source="category.name", read_only=True)
    seller = serializers.CharField(source="seller.first_name", read_only=True)
    discounted_price = serializers.SerializerMethodField()
    product_images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "seller",
            "title",
            "description",
            "price",
            "discounted_price",
            "stock",
            "brand",
            "category",
            "thumbnail",
            "product_images",
        ]

    def get_discounted_price(self, obj):
        return get_discounted_price(obj)

    def get_product_images(self, obj):
        request = self.context.get("request")
        data = ProductImage.objects.filter(product=obj)
        images = []
        for image in data:
            if image.product_image:
                image_url = request.build_absolute_uri(
                    image.product_image.url
                )
                images.append(image_url)
        return images


class UploadProductImagesSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all())
    images = serializers.ListField(
        child=serializers.ImageField(max_length=100000), write_only=True
    )


class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ["seller"]


class UpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ["id"]


class CartItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"


class CartItemsListSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ["product", "quantity"]


class CartItemsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        exclude = ["id"]


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "user",
            "order_items",
            "total_amount",
            "status",
            "created_at",
            "updated_at",
        ]

    def get_order_items(self, obj):
        return OrderItemSerializer(OrderItem.objects.filter(order=obj), many=True).data


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        exclude = ["owner"]


class StoreProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = StoreProduct
        fields = ["store", "product"]


class StoreProductListSerializer(serializers.Serializer):
    store = serializers.PrimaryKeyRelatedField(queryset=Store.objects.all())
    products = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=True
    )

    def validate(self, data):
        if len(data["products"]) != len(set(data["products"])):
            raise serializers.ValidationError(
                "Duplicate products are not allowed.")
        return data

    def create(self, validated_data):
        store = validated_data["store"]
        products = validated_data["products"]

        existing_store_products = StoreProduct.objects.filter(
            store=store, product__in=products
        )
        existing_products = set(
            existing_store_products.values_list("product_id", flat=True)
        )

        new_products = [
            StoreProduct(store=store, product=product)
            for product in products
            if product.id not in existing_products
        ]

        StoreProduct.objects.bulk_create(new_products)

        return validated_data

class CreateOrderSerializer(serializers.Serializer):
    coupon_code = serializers.CharField(required=False, allow_blank=True)
