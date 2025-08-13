from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=255)
    tag = models.CharField(max_length=255, default='none')

    def __str__(self):
        return self.name


class Customer(models.Model):
    fisrt_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11)
    email = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=128)

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    def __str__(self):
        return f"{self.fisrt_name} {self.last_name}"


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=25, blank=False)
    address1 = models.CharField(max_length=255, blank=False)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    zipcode = models.CharField(max_length=25)
    country = models.CharField(max_length=25, default='IRAN')
    my_cart = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        Profile.objects.create(user=instance)


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_describtion = models.CharField(
        max_length=255, default="", blank=True, null=True
    )
    product_price = models.DecimalField(
        default=0, max_digits=18, decimal_places=0)
    product_category = models.ForeignKey(
        Category, on_delete=models.PROTECT, default=1)
    product_image = models.ImageField(upload_to="upload/product/")
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(
        default=0, max_digits=18, decimal_places=0)
    quantity = models.PositiveIntegerField(default=0)
    star = models.IntegerField(default=0, validators=[
                               MaxValueValidator(5), MinValueValidator(0)])

    def __str__(self):
        return self.product_name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer_name = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    address = models.CharField(default="", blank=False)
    phone_number = models.CharField(max_length=11, blank=True)
    order_date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product
