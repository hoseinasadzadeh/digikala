from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from .forms import ShippingForm
from .models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from shop.models import Product, Profile
from django.contrib.auth.models import User
import requests
from dotenv import load_dotenv
import os
import uuid
from django.http import HttpResponse, HttpResponseRedirect


load_dotenv()
ZARINPAL_MERCHANT = os.getenv('ZARINPAL_MERCHANT')
ZARINPAL_API = 'https://payment.zarinpal.com/pg/v4/payment/request.json'
ZARINPAL_VERIFY = 'https://api.zarinpal.com/pg/v4/payment/verify.json'


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    qty = cart.get_quants()
    total = cart.get_total_price()
    return render(request, 'payment/checkout.html', {'cart_products': cart_products, 'qty': qty, 'total': total})


def shipping(request):
    cart = Cart(request)
    total = cart.get_total_price()

    if request.method == 'POST':
        if request.user.is_authenticated:
            shipping_user, created = ShippingAddress.objects.get_or_create(
                user=request.user)
            shipping_form = ShippingForm(request.POST, instance=shipping_user)
        else:
            shipping_form = ShippingForm(request.POST)

        if shipping_form.is_valid():
            shipping_instance = shipping_form.save(commit=False)
            if request.user.is_authenticated:
                shipping_instance.user = request.user
            shipping_instance.save()
            return redirect('payment:confirm')
    else:
        if request.user.is_authenticated:
            shipping_user = ShippingAddress.objects.filter(
                user=request.user).first()
            if shipping_user:
                shipping_form = ShippingForm(instance=shipping_user)
            else:
                shipping_form = ShippingForm()
        else:
            shipping_form = ShippingForm()

    return render(request, 'payment/shipping.html', {
        'total': total,
        'shipping_form': shipping_form,
    })


def confirm_order(request):

    if request.POST:
        cart = Cart(request)
        total = cart.get_total_price()

        user_shipping = request.POST
        request.session['user_shipping'] = user_shipping

        return render(request, 'payment/confirm_order.html', {'total': total, 'shipping_info': user_shipping})

    else:
        messages.error(request, 'دسترسی به این صفحه مجاز نمیباشد!')
        return redirect('home')


def proccess_order(request):
    if request.method == 'POST':
        try:
            cart = Cart(request)
            cart_products = cart.get_products()
            qty = cart.get_quants()
            total = cart.get_total_price()

            user_shipping = request.session.get('user_shipping')
            if not user_shipping:
                raise ValueError("اطلاعات ارسال یافت نشد")

            order_uuid = str(uuid.uuid4())

            if request.user.is_authenticated:
                order = Order(
                    uuid=order_uuid,
                    user=request.user,
                    fullName=user_shipping['shipping_fullName'],
                    email=user_shipping['shipping_email'],
                    shipping_address=f"{user_shipping['shipping_country']} - {user_shipping['shipping_city']}",
                    amount=total,
                    status='pending'
                )
            else:
                order = Order(
                    uuid=order_uuid,
                    fullName=user_shipping['shipping_fullName'],
                    email=user_shipping['shipping_email'],
                    shipping_address=f"{user_shipping['shipping_country']} - {user_shipping['shipping_city']}",
                    amount=total,
                    status='pending'
                )
            order.save()

            for product in cart_products:
                product_list = get_object_or_404(Product, id=product.id)
                price = product.sale_price if product.is_sale else product.product_price

                if str(product.id) in qty:
                    OrderItem.objects.create(
                        order=order,
                        product=product_list,
                        price=price,
                        quantity=qty[str(product.id)]['qty'],
                        user=order.user if request.user.is_authenticated else None
                    )

            if request.user.is_authenticated:
                Profile.objects.filter(user=request.user).update(my_cart='')
            cart.clear()

            CALLBACK_URL = f"http://127.0.0.1:8000/payment/verify/?uuid={order.uuid}"
            payload = {
                "merchant_id": ZARINPAL_MERCHANT,
                "amount": int(total),
                "currency": "IRT",
                "callback_url": CALLBACK_URL,
                "description": f"سفارش شماره {order.id}",
            }

            headers = {
                "accept": "application/json",
                "content-type": "application/json"
            }

            response = requests.post(
                ZARINPAL_API,
                json=payload,
                headers=headers
            )
            data = response.json()

            if data['data']['code'] == 100:
                pay_url = f"https://www.zarinpal.com/pg/StartPay/{data['data']['authority']}"
                return render(request, 'payment/redirecting.html', {'pay_url': pay_url})
            else:
                messages.error(request, "خطا در ایجاد تراکنش")

        except Exception as e:
            messages.error(request, str(e))
            return redirect('cart_summary')

    messages.error(request, 'دسترسی به این صفحه مجاز نمیباشد!')
    return redirect('home')


def verify_payment(request):
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')
    order_uuid = request.GET.get('uuid')

    try:
        order = Order.objects.get(uuid=order_uuid)

        if status == 'OK':
            payload = {
                "merchant_id": ZARINPAL_MERCHANT,
                "amount": int(order.amount),
                "authority": authority
            }

            headers = {
                "accept": "application/json",
                "content-type": "application/json"
            }

            response = requests.post(
                ZARINPAL_VERIFY,
                json=payload,
                headers=headers
            )

            data = response.json()

            if data['data']['code'] in [100, 101]:
                order.status = 'processing'
                order.save()
                return render(request, 'payment/payment_success.html', {
                    'message': "پرداخت با موفقیت انجام شد",
                    'ref_id': data['data']['ref_id'],
                    'order': order
                })
            else:
                order.status = 'failed'
                order.save()
                return render(request, 'payment/payment_failed.html', {
                    'message': "خطایی در پرداخت رخ داد",
                    'order': order
                })
        else:
            order.status = 'cancelled'
            order.save()
            return render(request, 'payment/payment_failed.html', {
                'message': 'پرداخت توسط کاربر لغو شد.',
            })

    except Order.DoesNotExist:
        messages.error(request, 'سفارش یافت نشد.')
        return redirect('home')
