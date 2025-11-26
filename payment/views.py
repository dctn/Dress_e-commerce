from django.shortcuts import render, redirect
from django.conf import settings
from payment.forms import ShippingAdressForm
from payment.models import Order, ShippingAddress


# Create your views here.
def update_shipping_address(request, shipping_address_id):
    address = ShippingAddress.objects.get(pk=shipping_address_id)
    if request.method == "POST":
        form = ShippingAdressForm(request.POST, instance=address)
        if form.is_valid():
            shipping_address = form.save()
            order = Order.objects.get(shipping_address=shipping_address.pk)
            return redirect("payment_page",order.pk)
    else:
        form = ShippingAdressForm(instance=address)
    return render(request, "checkout.html", {"form": form})


def payment_page(request, order_id):
    order = Order.objects.get(order_id=order_id)

    context = {
        "order": order,
    }
    return render(request, "checkout-payment.html", context)


# def process_order(request):
    







