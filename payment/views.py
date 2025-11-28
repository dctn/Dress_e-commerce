import os

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from core.models import Color
from payment.forms import ShippingAdressForm
from payment.models import Order, ShippingAddress, OrderItem
import razorpay
from cart.cart import Cart
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


def process_order(request,order_id):
    cart = Cart(request)
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))
    order = Order.objects.get(pk=order_id)

    all_products = cart.all_products()
    total_amount = cart.total_amount()


    data = {
        "amount": int(total_amount)*100,
        "currency": "INR",
        "payment_capture": "1"
    }

    razorpay_order = client.order.create(data)



    for item in all_products:
        if item["product"].price:
            is_fixed_price = True
        elif item["product"].price_per_inches:
            is_fixed_price = False
        OrderItem.objects.create(
            order_id=order,
            variant_id=item['product'],
            quantity=item['qty'],
            price_at_purchase=item['product_price'],
            size=item['size'],
            color=Color.objects.get(name=item['color']),
            is_fixed_price=is_fixed_price
        )

    if os.environ.get("ENVIRONMENT") == "production":
        callback_url = request.build_absolute_uri(reverse(settings.RAZOR_PAY_CALLBACK_URL)).replace("http://",
                                                                                                    "https://")
    else:
        callback_url = request.build_absolute_uri(reverse(settings.RAZOR_PAY_CALLBACK_URL))

    order.razorpay_order_id = razorpay_order["id"]
    order.total = total_amount
    order.save()
    print(callback_url)
    return JsonResponse({
        "order_id": razorpay_order["id"],
        "razorpay_key_id": settings.RAZORPAY_KEY,
        "product_name": request.user.username,
        "amount": razorpay_order["amount"],
        "callback_url": callback_url,
    })

@csrf_exempt
def payment_verify(request):

    if "razorpay_signature" in request.POST:
        cart = Cart(request)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY,settings.RAZORPAY_SECRET))

        order_id = request.POST.get("razorpay_order_id")
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        razorpay_signature  = request.POST.get("razorpay_signature")

        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            })

            # Payment verified successfully
            order = Order.objects.get(razorpay_order_id=order_id)
            order.is_paid = True
            order.payment_id = razorpay_payment_id
            order.signature_id  = razorpay_signature
            order.save()

            items = OrderItem.objects.filter(order_id=order)

            for order_item in items:
                product = order_item.variant_id
                for item in cart.all_products():
                    if item["product"] == product:
                        product_sold = item["qty"]

                if product.sale is None:
                    product.sale = 0

                product.sale += product_sold
                product.save()


            cart.clear()


            return render(request,"payment_verify.html",{"status": "Payment Verified Successfully","order_id":order_id})
            # return redirect("confirm_order",order_id)
        except razorpay.errors.SignatureVerificationError:

            return render(request,"payment_verify.html",{"status":"Payment verification failed"})

    return render(request,"payment_verify.html",{"status":"Invalid Request"})





