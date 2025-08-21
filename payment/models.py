from django.db import models
from django.contrib.auth.models import User
from shop.models import Product
from django_jalali.db import models as jmodels
import jdatetime
import uuid


class ShippingAddress(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=False)
    shipping_fullName = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_phone = models.CharField(max_length=25, blank=True)
    shipping_address1 = models.CharField(max_length=255, blank=True)
    shipping_address2 = models.CharField(max_length=255, null=True)
    shipping_city = models.CharField(max_length=25)
    shipping_state = models.CharField(max_length=25, blank=True, null=True)
    shipping_zipcode = models.CharField(max_length=25, blank=True, null=True)
    shipping_country = models.CharField(max_length=25, default='IRAN')

    def __str__(self):
        return f'Shipping Address for {self.user}'


class Order(models.Model):

    STATUS = [
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('processing', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل داده شده'),
        ('cancelled', 'لغو شده'),
        ('failed', 'پرداخت ناموفق'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=False)
    fullName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    shipping_address = models.CharField(max_length=250, blank=True)
    amount = models.DecimalField(decimal_places=0, max_digits=12)
    status = models.CharField(max_length=50, choices=STATUS, default='pending')
    date_ordered = jmodels.jDateTimeField(auto_now_add=True)
    last_update = jmodels.jDateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def __str__(self):
        return f'Order #{self.id} - {self.status}'

    def save(self, *args, **kwargs):
        if self.pk:
            old_status = Order.objects.get(id=self.pk).status

            if old_status != self.status:
                self.last_date = jdatetime.datetime.now()

        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True, blank=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=False)

    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(decimal_places=0, max_digits=12)

    def __str__(self):
        return f'Order Item #{self.id} for {self.user}'
