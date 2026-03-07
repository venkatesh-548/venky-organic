from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.views import get_cart
from .models import Order, OrderItem
from .forms import OrderCreateForm

@login_required
def checkout(request):
    cart = get_cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
            # Clear cart
            cart.items.all().delete()
            return render(request, 'orders/created.html', {'order': order})
    else:
        form = OrderCreateForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'address': request.user.address,
        })
    return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})

@login_required
def order_list(request):
    orders = request.user.orders.all()
    return render(request, 'orders/order_list.html', {'orders': orders})
