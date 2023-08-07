from django.http import JsonResponse
from django.templatetags.static import static
from .models import Product, Order, OrderProducts
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import phonenumbers


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


def check_valid_data(order_details: dict):
    keys = [
        "products",
        "firstname",
        "lastname",
        "phonenumber",
        "address"
    ]
    error_message = ''

    for key in keys:
        if key not in order_details.keys():
            error_message = f"{key} key not presented."
            return {"detail": error_message}
        elif not order_details[key]:
            error_message = f"{key} value cannot be empty."
            return {"detail": error_message}

    if not isinstance(order_details['products'], list):
        error_message = "products value is not a valid list."
        return {"detail": error_message}
    for product in order_details['products']:
        if not Product.objects.filter(pk=product["product"]).exists():
            return {"detail": f"invalid primary key {product['product']}"}

    for key in keys[1:]:
        if not isinstance(order_details[key], str):
            error_message = f"{key} value is not a valid string."
            return {"detail": error_message}

    phone = phonenumbers.parse(order_details["phonenumber"], None)
    if not phonenumbers.is_valid_number(phone):
        return {"detail": "not a valid phone number"}


@api_view(['POST'])
def register_order(request):
    try:
        order_details = request.data
        wrong_data = check_valid_data(order_details)
        if wrong_data:
            return Response(wrong_data, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        order_object = Order.objects.create(
            first_name=order_details['firstname'],
            last_name=order_details['lastname'],
            address=order_details['address'],
            phone=order_details['phonenumber']
        )

        for product in order_details['products']:
            order_products_object = OrderProducts.objects.create(
                order=order_object,
                product=Product.objects.get(pk=product['product']),
                quantity=product['quantity']
            )

        return Response(order_details)

    except ValueError:
        return Response({
            'error': 'ValueError',
        })
