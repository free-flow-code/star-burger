from django.http import JsonResponse
from django.templatetags.static import static
from .models import Product, Order, OrderProducts
import json


from .models import Product


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


def register_order(request):
    try:
        order_details = json.loads(request.body.decode())
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

        return JsonResponse(order_details)

    except ValueError:
        return JsonResponse({
            'error': 'ValueError',
        })
