from django.shortcuts import render, get_object_or_404
from cart.cart import Cart
from shop.models import Product
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    qty = cart.get_quants()
    total = cart.get_total_price()

    return render(request, 'cart/cart_summary.html', {'cart_products': cart_products, 'qty': qty, 'total': total})


@require_POST
def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')
        product = get_object_or_404(Product, id=product_id)
        if product.is_sale:
            last_price = product.sale_price
        else:
            last_price = product.product_price
        cart.add(product=product, qty=product_qty)
        cart_quantity = cart.__len__()
        return JsonResponse({
            'product_name': product.product_name,
            'product_price': last_price,
            'cart_quantity': cart_quantity,
            'success': True
        })


@require_POST
def cart_delete(request):
    cart = Cart(request)
    product_id = request.POST.get('product_id')

    if product_id in cart.cart:
        del cart.cart[product_id]
        cart.save()

    return JsonResponse({
        'success': True,
        'total_price': cart.get_total_price(),
        'cart_count': len(cart)

    })


@require_POST
def cart_update(request):
    cart = Cart(request)
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 0))

    if quantity < 1:
        if product_id in cart.cart:
            del cart.cart[product_id]
    else:
        cart.cart[product_id]['qty'] = quantity

    cart.save()

    return JsonResponse({
        'success': True,
        'total_price': cart.get_total_price(),
        'cart_count': cart.__len__(),
        'item_total': cart.cart[product_id]['qty'] * cart.cart[product_id]['price']
    })
