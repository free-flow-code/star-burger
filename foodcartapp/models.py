import requests.exceptions
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from geopy import distance
from coords.models import Place


class OrderQuerySet(models.QuerySet):

    def add_total_cost(self):
        return (self.annotate(
            total_cost=models.Sum(models.F("product__price") * models.F("product__quantity"))
        ).order_by("-status", "registered_at", "id"))

    def fetch_restaurants(self):
        distances = {}
        for order in self:
            if not order.restaurant and order.status == "UN":
                order_restaurants = []
                distances[f"{order.pk}"] = {}

                for product in order.products.all():
                    product_items = RestaurantMenuItem.objects \
                        .filter(product=product, availability=True) \
                        .prefetch_related('restaurant') \
                        .order_by('product') \

                    for item in product_items:
                        order_restaurants.append(item.restaurant.pk)
                        distances[f"{order.pk}"][f"{item.restaurant.pk}"] = "%.2f" % distance.distance(
                            Place.objects.get_coordinates(order.address),
                            Place.objects.get_coordinates(item.restaurant.address)
                        ).km

                order.restaurants.set(order_restaurants)

            else:
                order_object = Order.objects.get(pk=order.pk)
                order_object.status = "RS"
                order_object.save(update_fields=["status"])

        return self, distances


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class Order(models.Model):
    class Status(models.TextChoices):
        UNPROCESSED = "UN", _("Необработанный")
        RESTAURANT = "RS", _("Передан в ресторан")
        DELIVERY = "DL", _("Доставляется")
        COMPLETED = "OK", _("Выполнен")

    class PaymentMethod(models.TextChoices):
        CASH = "CH", _("Наличными")
        TRANSFER = "TF", _("Переводом")

    status = models.CharField(
        verbose_name="статус",
        max_length=2,
        choices=Status.choices,
        default=Status.UNPROCESSED,
        db_index=True
    )
    payment_method = models.CharField(
        verbose_name="способ оплаты",
        max_length=2,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH,
        db_index=True
    )
    products = models.ManyToManyField(
        Product,
        verbose_name="товары",
        related_name="orders",
        through="OrderProducts"
    )
    firstname = models.CharField(
        verbose_name="имя",
        max_length=80,
        null=False
    )
    lastname = models.CharField(
        verbose_name="фамилия",
        max_length=80,
        null=False
    )
    address = models.CharField(
        verbose_name="адрес доставки",
        max_length=500,
        null=False
    )
    phonenumber = PhoneNumberField(
        verbose_name="телефон",
        max_length=20,
        db_index=True
    )
    restaurant = models.ForeignKey(
        Restaurant,
        verbose_name="готовит ресторан",
        related_name="orders",
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    restaurants = models.ManyToManyField(
        Restaurant,
        verbose_name="рестораны, которые могут приготовить"
    )
    comment = models.TextField(
        blank=True,
        verbose_name="комментарий"
    )
    registered_at = models.DateTimeField(
        verbose_name="зарегистрирован",
        default=timezone.now,
        db_index=True
    )
    called_at = models.DateTimeField(
        verbose_name="дата звонка",
        blank=True,
        null=True
    )
    delivered_at = models.DateTimeField(
        verbose_name="дата доставки",
        blank=True,
        null=True
    )
    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы"

    def __str__(self):
        return f"{self.firstname} {self.lastname} - {self.address}"


class OrderProducts(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name="заказ",
        related_name="product",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name="товар",
        related_name="order",
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        verbose_name="количество",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(99)
        ]
    )
    price = models.DecimalField(
        verbose_name="цена",
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = "элемент заказа"
        verbose_name_plural = "элементы заказа"
