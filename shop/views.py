from django.shortcuts import render, get_object_or_404
from shop.models import Category, Product

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    if request.headers.get('HX-Request'):
        # Для HTMX-запросов возвращаем только список продуктов
        return render(request, 'shop/product_list.html', {'products': products})
    else:
        # Для обычных запросов возвращаем полную страницу
        return render(request, 'shop/catalog.html', {
            'category': category,
            'categories': categories,
            'products': products
        })

def product_detail(request, id, slug):
    product = get_object_or_404(
        Product.objects.select_related('category', 'brand').prefetch_related('images'),
        id=id,
        slug=slug,
        is_available=True
    )
    similar_products = Product.objects.filter(category=product.category,is_available=True).exclude(id=product.id).select_related('brand').order_by('?')[:4]
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'similar_products': similar_products
    })

