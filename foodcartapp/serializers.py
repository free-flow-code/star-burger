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

    def create(self, validated_data):
        products = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        for order_product in products:
            OrderProducts.objects.create(order=order, **order_product, price=order_product['product'].price)
        return order

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
