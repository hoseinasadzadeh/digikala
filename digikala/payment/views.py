from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from .forms import ShippingForm
from .models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from shop.models import Product, Profile
from django.contrib.auth.models import User


def success(request):
    return render(request, 'payment/payment_success.html', {})


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
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_products()
        qty = cart.get_quants()
        total = cart.get_total_price()

        user_shipping = request.session.get('user_shipping')

        full_name = user_shipping['shipping_fullName']
        email = user_shipping['shipping_email']
        shipping_address = f'{user_shipping['shipping_country']} - {user_shipping['shipping_city']} - {user_shipping['shipping_state']} - {user_shipping['shipping_address2']} - {user_shipping['shipping_address1']}'

        if request.user.is_authenticated:
            user = request.user
            order = Order(user=user, fullName=full_name, email=email,
                          shipping_address=shipping_address, amount=total,)
            order.save()

            for product in cart_products:
                product_list = get_object_or_404(Product, id=product.id)

                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.product_price

                for key, value in qty.items():
                    if int(key) == product.id:
                        new_item = OrderItem(
                            order=order, product=product_list, price=price, quantity=value['qty'], user=user)
                        new_item.save()
            cart.clear()

            current_user = Profile.objects.filter(user__id=request.user.id)
            current_user.update(my_cart='')

            messages.success(request, 'سفارش با موفقیت ثبت شد!')
            return redirect('home')
        else:
            order = Order(fullName=full_name, email=email,
                          shipping_address=shipping_address, amount=total,)
            order.save()
            for product in cart_products:
                product_list = get_object_or_404(Product, id=product.id)

                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.product_price

                for key, value in qty.items():
                    if int(key) == product.id:
                        new_item = OrderItem(
                            order=order, product=product_list, price=price, quantity=value['qty'])
                        new_item.save()

            cart.clear()
            messages.success(request, 'سفارش با موفقیت ثبت شد!')
            return redirect('home')

    else:
        messages.error(request, 'دسترسی به این صفحه مجاز نمیباشد!')
        return redirect('home')


def success(request):
    return render(request, 'payment/payment_success.html')
