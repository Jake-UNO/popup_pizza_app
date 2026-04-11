from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Category, Product
from .forms import ProductForm
from cart.forms import CartAddProductForm
from cart.cart import Cart


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    cart = Cart(request)

    return render(
        request,
        'shop/product/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products,
            'cart': cart
        }
    )


def product_detail(request, id):
    product = get_object_or_404(Product, id=id, available=True)

    cart = Cart(request)
    cartquantity = 0

    for item in cart:
        cartproduct = get_object_or_404(Product, id=item['product'].id)
        if product == cartproduct:
            cartquantity = item['quantity']
            break

    if 10 - cartquantity > 0:
        choices = [(i, str(i)) for i in range(1, 11)]
    else:
        choices = [(1, 0)]

    cart_product_form = CartAddProductForm(my_choices=choices)

    return render(
        request,
        'shop/product/detail.html',
        {
            'product': product,
            'cart_product_form': cart_product_form,
            'cart': cart
        }
    )


@staff_member_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect('shop:product_detail', id=product.id)
    else:
        form = ProductForm()

    cart = Cart(request)

    return render(
        request,
        'shop/product/create.html',
        {
            'form': form,
            'cart': cart
        }
    )


@staff_member_required
def product_update(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('shop:product_detail', id=product.id)
    else:
        form = ProductForm(instance=product)

    cart = Cart(request)

    return render(
        request,
        'shop/product/update.html',
        {
            'form': form,
            'product': product,
            'cart': cart
        }
    )


@staff_member_required
def product_delete(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        product.delete()
        return redirect('shop:product_list')

    cart = Cart(request)

    return render(
        request,
        'shop/product/delete.html',
        {
            'product': product,
            'cart': cart
        }
    )