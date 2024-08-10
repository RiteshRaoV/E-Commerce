from rest_framework import generics
from discounts.models import Coupon, CouponUsage
from drf_yasg.utils import swagger_auto_schema
from shop.models import (
    CartItem,
    Order,
    OrderItem,
    Product,
    ProductImage,
    Store,
    StoreProduct,
)
from shop.serializers import (
    AddProductSerializer,
    CartItemsDetailsSerializer,
    CartItemsListSerializer,
    CartItemsSerializer,
    OrderSerializer,
    ProductSerializer,
    StoreProductListSerializer,
    StoreProductSerializer,
    StoreSerializer,
    UpdateProductSerializer,
)
from rest_framework import status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import permission_classes
from .permissions import IsSeller
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from .serializers import (
    CreateOrderSerializer,
    UploadProductImagesSerializer,
    get_discounted_price,
)

User = get_user_model()


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = "page_size"
    max_page_size = 1000


class ListAllProducts(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


@permission_classes([IsAuthenticated, IsSeller])
class AddProductView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = AddProductSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        seller = self.request.user
        user = get_object_or_404(User, pk=seller)

        if user.is_seller:  # type: ignore
            serializer.save()
        else:
            raise PermissionDenied("Unauthorized")


# @permission_classes([IsAuthenticated, IsSeller])


class UploadProductImagesView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Handle file uploads

    def post(self, request, *args, **kwargs):
        serializer = UploadProductImagesSerializer(data=request.data)

        if serializer.is_valid():
            product = serializer.validated_data["product"]
            images = serializer.validated_data["images"]

            for image in images:
                ProductImage.objects.create(product=product, image=image)

            return Response(
                {"message": "Images uploaded successfully"},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated, IsSeller])
class UpdateProductDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UpdateProductSerializer

    def get_object(self):
        product_id = self.kwargs.get("product_id")
        try:
            return Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise NotFound("Product does not exist")

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProductSerializer(instance)
        return Response(serializer.data)


class ListSellersProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        seller_id = self.kwargs.get("seller_id")
        if seller_id:
            return Product.objects.filter(seller__id=seller_id)
        return Product.objects.none()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class AddToCartView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemsSerializer

    def perform_create(self, serializer):
        cart = serializer.validated_data["cart"]
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]
        if product.stock <= quantity:
            raise NotFound("product is not available in the requested quantity")
        existing_item = CartItem.objects.filter(cart=cart, product=product).first()

        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
        else:
            serializer.save()


class UpdateCartItemsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemsDetailsSerializer

    def get_object(self):
        cart_item_id = self.kwargs.get("cart_item_id")
        try:
            return CartItem.objects.get(pk=cart_item_id)
        except CartItem.DoesNotExist:
            raise NotFound("Item does not exist")


class ListCartItemsView(generics.ListAPIView):
    serializer_class = CartItemsListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        if user_id:
            return CartItem.objects.filter(cart__user__id=user_id)
        return CartItem.objects.none()


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    @swagger_auto_schema(request_body=CreateOrderSerializer)
    def post(self, request, *args, **kwargs):
        user = self.request.user
        cart_items = CartItem.objects.filter(cart__user=user)

        if not cart_items.exists():
            return Response(
                {"message": "No items in the cart"}, status=status.HTTP_204_NO_CONTENT
            )

        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        coupon_code = serializer.validated_data.get("coupon_code", None)

        coupon = None
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                if not coupon.is_active() or coupon.has_user_used(user):
                    return Response(
                        {"message": "Invalid or expired coupon"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except Coupon.DoesNotExist:
                return Response(
                    {"message": "Coupon does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        total_price = sum(
            get_discounted_price(item.product) * item.quantity for item in cart_items
        )
        actual_amount = sum(item.product.price * item.quantity for item in cart_items)

        if coupon:
            total_price = coupon.apply_discount(total_price)
            
        savings = actual_amount - total_price

        order = Order.objects.create(
            user=user,
            coupon=coupon if coupon else None,
            total_amount=actual_amount,
            final_discounted_amount=total_price,
            savings=savings,
        )

        for item in cart_items:
            discounted_price = get_discounted_price(item.product)

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=discounted_price,
            )

            product = Product.objects.get(pk=item.product.pk)
            product.stock -= item.quantity
            product.save()

        if coupon:
            CouponUsage.objects.create(coupon=coupon, user=user)

        cart_items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


@permission_classes([IsAuthenticated])
class CancelOrderView(APIView):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs.get("order_id")

        try:
            order = Order.objects.get(pk=order_id)

            if order.status == "Cancelled":
                return Response(
                    {"message": "Order already cancelled"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            order_items = OrderItem.objects.filter(order=order)
            for item in order_items:
                product = item.product
                product.stock += item.quantity
                product.save()

            if order.coupon:
                try:
                    coupon_usage = CouponUsage.objects.get(
                        coupon=order.coupon, user=order.user
                    )
                    coupon_usage.delete()

                    coupon = Coupon.objects.get(pk=order.coupon.pk)
                    coupon.coupon_count += 1
                    coupon.save()
                except CouponUsage.DoesNotExist:
                    pass

            order.status = "Cancelled"
            order.save()

            return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response(
                {"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )


@permission_classes([IsAuthenticated])
class ListOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


@permission_classes([IsAuthenticated, IsSeller])
class CreateStoreView(generics.CreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@permission_classes([IsAuthenticated, IsSeller])
class AddProductsToStoreView(generics.CreateAPIView):
    queryset = StoreProduct.objects.all()
    serializer_class = StoreProductListSerializer


class ListStoreProductsView(generics.ListAPIView):
    queryset = StoreProduct.objects.all()
    serializer_class = StoreProductSerializer

    def get_queryset(self):
        store_id = self.kwargs.get("store_id")
        return StoreProduct.objects.filter(store=store_id)
