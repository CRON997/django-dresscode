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

    def add(self, product, size=None, quantity=1):
        product_id = str(product.id)

        # Fix: Consistent key generation using size.id
        cart_key = f"{product_id}_{size.id}" if size else product_id

        if cart_key not in self.cart:
            self.cart[cart_key] = {
                'product_id': product.id,
                'quantity': 0,
                'price': float(product.price),
                'size_id': size.id if size else None,  # Store size_id instead of size name
                'size_name': size.name if size else None,  # Store size name separately
            }

        self.cart[cart_key]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product, size):
        product_id = str(product.id)

        # Fix: Use size.id for consistent key generation
        cart_key = f"{product_id}_{size.id}" if size else product_id

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
        products_dict = {product.id: product for product in products}

        # Get all unique size IDs from cart items
        size_ids = [item['size_id'] for item in self.cart.values() if item.get('size_id')]
        sizes = {}
        if size_ids:
            from apps.main.models import Size
            size_objects = Size.objects.filter(id__in=size_ids)
            sizes = {size.id: size for size in size_objects}

        for cart_key, cart_item in self.cart.items():
            product_id = cart_item['product_id']

            if product_id in products_dict:
                cart_item = cart_item.copy()
                cart_item['product'] = products_dict[product_id]
                cart_item['total_price'] = Decimal(str(cart_item['price'])) * cart_item['quantity']
                cart_item['cart_key'] = cart_key

                # Add size object if exists
                size_id = cart_item.get('size_id')
                if size_id and size_id in sizes:
                    cart_item['size'] = sizes[size_id]

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
            return (Decimal(self.coupon.discount) / Decimal(100)) * Decimal(self.get_total_price())
        return Decimal(0)

    def get_total_price_after_discount(self):
        return Decimal(self.get_total_price()) - self.get_discount()
