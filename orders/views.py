from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import OrderItem, Order, Product
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import send_mail


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(
        request,
        'admin/orders/order/detail.html',
        {'order': order}
    )


def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()

            pickup = order.pickup_slot
            pickup.current_orders += 1
            pickup.save()

            ordered_items = []
            total_quantity = 0
            total_price = 0

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

                line_total = item['price'] * item['quantity']

                ordered_items.append(
                    f"- {item['product']} x {item['quantity']} @ ${item['price']} each = ${line_total:.2f}"
                )

                total_quantity += item['quantity']
                total_price += line_total

            items_text = "\n".join(ordered_items)

            send_mail(
                subject=f'Popup Pizza Order Confirmation #{order.id}',
                message=(
                    f"Thank you for your order, {order.first_name}.\n\n"
                    f"Your order number is {order.id}.\n"
                    f"Pickup slot: {order.pickup_slot}\n"
                    f"Total pizzas/items: {total_quantity}\n"
                    f"Total price: ${total_price:.2f}\n\n"
                    f"Items ordered:\n"
                    f"{items_text}\n\n"
                    f"We appreciate your order."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.email],
                fail_silently=False,
            )

            cart.clear()
            request.session['order_id'] = order.id

            return render(request, 'orders/order/created.html', {'order_id': order.id})
    else:
        form = OrderCreateForm()

    return render(
        request,
        'orders/order/create.html',
        {'cart': cart, 'form': form}
    )