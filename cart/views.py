from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override']
        )
    return redirect('cart:cart_detail')
@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')
def cart_detail(request):
    cart = Cart(request)
    # Добавляем форму для каждого товара в корзине
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'override': True
            }
        )
    return render(request, 'cart/detail.html', {'cart': cart})  #
def cart_update(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] = quantity
            request.session['cart'] = cart
            request.session.modified = True
    
    return redirect('cart:cart_detail')
from django.shortcuts import redirect

def cart_clear(request):
    """Очистка всей корзины"""
    if 'cart' in request.session:
        del request.session['cart']
        request.session.modified = True
    return redirect('cart:cart_detail')
