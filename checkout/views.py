from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51QJCWrJ0NE1ts5c23BY0NHC7A0HrpA80JpXP8mGzkbnbsIZEGlAEJ4LdqmjIogKHPX30iFmA4M412UNuvqC1qUk500rmXdra4e',
        'client_secret': 'sk_test_51QJCWrJ0NE1ts5c2LjBn8ekb7RCqw7VIK9pxupmyNn5g6CXPvKX1huCX4NxJNUq8DW2bF1alHOgpoPWBeyTa4wHH00xMMUym9h',
    }

    return render(request, template, context)