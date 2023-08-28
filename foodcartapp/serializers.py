from rest_framework.serializers import ModelSerializer
from .models import Order, OrderProducts


class OrderProductsSerializer(ModelSerializer):
    class Meta:
        model = OrderProducts
        fields = [
            "product",
            "quantity"
        ]


class OrderSerializer(ModelSerializer):
    products = OrderProductsSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "products",
            "firstname",
            "lastname",
            "phonenumber",
            "address"
        ]
