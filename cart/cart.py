from shop.models import Product, Profile
import json


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault('session_key', {})
        self.request = request

    def add(self, product, qty=0, update=False):
        product_id = str(product.id)

        if product.is_sale:
            last_price = product.sale_price
        else:
            last_price = product.product_price

        if product_id not in self.cart or update:
            self.cart[product_id] = {
                'qty': int(qty),
                'price': float(last_price)
            }
        else:
            self.cart[product_id]['qty'] += int(qty)

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(
                user__id=self.request.user.id)
            db_cart = json.dumps(self.cart)
            current_user.update(my_cart=str(db_cart))

    def db_add(self, product, qty=0, update=False):
        product_id = str(product.id)
        product = Product.objects.get(id=product_id)

        if product.is_sale:
            last_price = product.sale_price
        else:
            last_price = product.product_price
        if product_id not in self.cart or update:
            self.cart[product_id] = {
                'qty': int(qty),
                'price': float(last_price)
            }
        else:
            self.cart[product_id]['qty'] += int(qty)

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.get(user__id=self.request.user.id)
            db_cart = json.dumps(self.cart)
            current_user.my_cart = db_cart
            current_user.save()

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def get_products(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quants(self):
        qty = self.cart
        return qty

    def get_total_price(self):
        return sum(
            item['price'] * item['qty']
            for item in self.cart.values()
        )

    def save(self):
        self.session['session_key'] = self.cart
        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.get(user__id=self.request.user.id)
            db_cart = json.dumps(self.cart)
            current_user.my_cart = db_cart
            current_user.save()

    def clear(self):
        if 'session_key' in self.session:
            del self.session['session_key']
            self.session.modified = True

        self.cart = {}
