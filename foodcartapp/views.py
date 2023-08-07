from django.http import JsonResponse
from django.templatetags.static import static
from .models import Product, Order, OrderProducts
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ModelSerializer


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


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    order_object = Order.objects.create(
        firstname=serializer.validated_data['firstname'],
        lastname=serializer.validated_data['lastname'],
        address=serializer.validated_data['address'],
        phonenumber=serializer.validated_data['phonenumber']
    )
    print(serializer.validated_data['products'])
    products = serializer.validated_data['products']
    order_products = [OrderProducts(order=order_object, **fields) for fields in products]
    OrderProducts.objects.bulk_create(order_products)

    return Response(OrderSerializer(instance=order_object).data, status=status.HTTP_201_CREATED)
