from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import ListView
from .models import Vegetable, CartItem, Order
from decimal import Decimal
from django.db.models import Sum, F
from .models import OrderItem, Vegetable
from django.contrib.admin.views.decorators import staff_member_required

def home(request):
    return render(request, 'cart/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('vegetable_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class VegetableListView(ListView):
    model = Vegetable
    template_name = 'cart/vegetable_list.html'
    context_object_name = 'vegetables'

@login_required
def add_to_cart(request, veg_id):
    veg = get_object_or_404(Vegetable, id=veg_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, vegetable=veg)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    messages.success(request, f'{veg.name} added to cart.')
    return redirect('cart')

@login_required
def update_quantity(request, veg_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item = get_object_or_404(CartItem, user=request.user, vegetable_id=veg_id)
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart')

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.subtotal() for item in cart_items)
    return render(request, 'cart/cart.html', {
        'cart_items': cart_items, 
        'total': total
    })

@login_required
def remove_from_cart(request, veg_id):
    cart_item = get_object_or_404(CartItem, user=request.user, vegetable_id=veg_id)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')
    
    total = sum(item.subtotal() for item in cart_items)
    
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            total_amount=total
        )
        # Add items to order
        for item in cart_items:
            order.items.create(
                vegetable=item.vegetable,
                quantity=item.quantity,
                price=item.vegetable.price
            )
        # Clear cart
        cart_items.delete()
        messages.success(request, 'Order placed successfully!')
        return redirect('order_confirmation', order_id=order.id)
    
    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'cart/order_confirmation.html', {'order': order})

@staff_member_required
def vegetable_order_summary(request):
    order_items = OrderItem.objects.values(
        'order__id',
        'order__date_ordered',
        'vegetable__name',
        'quantity',
        'order__complete'
    ).annotate(
        order_id=F('order__id'),
        date_ordered=F('order__date_ordered'),
        vegetable_name=F('vegetable__name'),
        complete=F('order__complete')
    ).order_by('-order__date_ordered')

    return render(request, 'cart/vegetable_summary.html', {
        'orders': order_items
    })

@staff_member_required
def complete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.complete = True
    order.save()
    messages.success(request, f'Order #{order.id} marked as complete')
    return redirect('vegetable_summary')
