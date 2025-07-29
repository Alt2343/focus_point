from cart.cart import Cart
from django.shortcuts import render
from .forms import OrderCreateForm
from .models import OrderItem
# Create your views here.

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            order.total = cart.get_total_price()
            order.discount = cart.get_discount_total()
            order.final_total = cart.get_total_price_with_discount()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            cart.clear()
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
        return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})   
