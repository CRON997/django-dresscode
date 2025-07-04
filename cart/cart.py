from main.models import Product
from shop import settings


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, size=None, quantity=1, override_quantity=False):
        product_id = str(product.id)

        # Создаем словарь для размера (если размер есть)
        size_data = None
        if size:
            size_data = {
                'id': size.id,
                'name': size.name,
                'type': size.__class__.__name__  # 'ShoesSize' или 'ClothingSize'
            }

        # Создаем уникальный ключ для товара с размером
        cart_key = f"{product_id}_{size.id}" if size else product_id

        if cart_key not in self.cart:
            self.cart[cart_key] = {
                'product_id': product.id,
                'quantity': 0,
                'price': float(product.price),
                'size': size_data
            }

        if override_quantity:
            self.cart[cart_key]['quantity'] = quantity
        else:
            self.cart[cart_key]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product, size=None):
        product_id = str(product.id)
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
        """
        Итерируемся по товарам в корзине и получаем товары из базы данных
        """
        product_ids = [item['product_id'] for item in self.cart.values()]
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for item in cart.values():
            product = next((p for p in products if p.id == item['product_id']), None)
            if product:
                item['product'] = product
                item['total_price'] = item['price'] * item['quantity']

                # Получаем объект размера если он есть
                if item['size']:
                    size_type = item['size']['type']
                    size_id = item['size']['id']

                    if size_type == 'ShoesSize':
                        from main.models import ShoesSize  # импортируйте вашу модель
                        try:
                            item['size_object'] = ShoesSize.objects.get(id=size_id)
                        except ShoesSize.DoesNotExist:
                            item['size_object'] = None
                    elif size_type == 'ClothingSize':
                        from main.models import ClothingSize  # импортируйте вашу модель
                        try:
                            item['size_object'] = ClothingSize.objects.get(id=size_id)
                        except ClothingSize.DoesNotExist:
                            item['size_object'] = None
                else:
                    item['size_object'] = None

                yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
