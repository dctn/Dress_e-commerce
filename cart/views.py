from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from .cart import Cart
from django.http import JsonResponse
from payment.forms import ShippingAdressForm
from payment.models import Order
# Create your views here.
def add_cart(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        qty = int(request.POST.get("qty"))
        product_id = request.POST.get("product_id")
        size = request.POST.get("product_size")
        color = request.POST.get("product_color")
        cart.add_product(product=product_id,
                         size=size,
                         color=color,
                         qty=qty)
        return JsonResponse({"message": "success"})
    return None

def remove_cart(request,product_id):
    cart = Cart(request)
    cart.remove_product(product=product_id)
    referer = request.META.get('HTTP_REFERER', '/')

    return redirect(referer)

def cart_view(request):
    return render(request, "cart.html")

def checkout(request):
    if request.method == "POST":
        form = ShippingAdressForm(request.POST)

        if form.is_valid():
            # Save the shipping address first
            shipping_address = form.save(commit=False)
            shipping_address.save()   # ✔ NOW it is in database

            # Create the order with the saved instance
            order = Order.objects.create(
                user=request.user,
                shipping_address=shipping_address
            )

            # Redirect to payment page WITH order_id
            return redirect("payment_page", order.pk)

    else:
        form = ShippingAdressForm()

    return render(request, "checkout.html", {"form": form})

