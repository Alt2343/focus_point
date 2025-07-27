from decimal import  Decimal
from django.conf import settings
from shop.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохранить пустую корзину в сеансе
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
    def save(self):
        self.session.modified = True
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in  products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield  item
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
    def get_discount_total(self):
        """Возвращает общую сумму скидки"""
        total_discount = Decimal('0')
        for item in self:
            product = item['product']
            if hasattr(product, 'discount') and product.discount > 0:
                discount_amount = item['price'] * (Decimal(product.discount) / Decimal('100'))
                total_discount += discount_amount * item['quantity']
        return total_discount.quantize(Decimal('0'))
    
    def get_total_price_with_discount(self):
        """Возвращает итоговую сумму с учётом скидок"""
        return self.get_total_price() - self.get_discount_total()