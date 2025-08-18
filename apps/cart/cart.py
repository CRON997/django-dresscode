from decimal import Decimal

from apps.main.models import Product
from shop import settings
from apps.coupons.models import Coupon


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, size, quantity=1, override_quantity=False):
        product_id = str(product.id)
        size_name = str(size)

        cart_key = f"{product_id}_{size.id}"

        if cart_key not in self.cart:
            self.cart[cart_key] = {
                'product_id': product.id,
                'quantity': 0,
                'price': float(product.price),
                'size': size_name
            }

        if override_quantity:
            self.cart[cart_key]['quantity'] = quantity
        else:
            self.cart[cart_key]['quantity'] += quantity

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product, size):
        product_id = str(product.id)
        size_name = str(size)
        cart_key = f"{product_id}_{size.id}"

        if cart_key in self.cart:
            del self.cart[cart_key]
            self.save()

    def get_total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.cart.values())

    def get_total_items(self):
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def __iter__(self):
        product_ids = [item['product_id'] for item in self.cart.values()]
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            for cart_key, cart_item in cart.items():
                if cart_item['product_id'] == str(product.id):
                    cart_item['product'] = product
                    cart_item['total_price'] = Decimal(cart_item['price']) * cart_item['quantity']
                    yield cart_item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
            return None

    def get_discount(self):
        if self.coupon:
            return (Decimal(self.coupon.discount / Decimal(100)) * Decimal(self.get_total_price()))
        return Decimal(0)

    def get_total_price_after_discount(self):
        return Decimal(self.get_total_price()) - self.get_discount()
