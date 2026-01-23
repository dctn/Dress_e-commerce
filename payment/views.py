import os
import uuid

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from core.models import Color
from payment.forms import ShippingAdressForm
from payment.models import Order, ShippingAddress, OrderItem
from cart.cart import Cart

from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.models.customer_details import CustomerDetails
from cashfree_pg.models.order_meta import OrderMeta

from django.db import transaction
from dotenv import load_dotenv
load_dotenv()

Cashfree.XClientId = settings.CASHFREE_CLIENT_ID
Cashfree.XClientSecret = settings.CASHFREE_CLIENT_SECRET
Cashfree.XEnvironment =  Cashfree.SANDBOX

if os.environ.get("ENVIRONMENT") == "production":
    Cashfree.XClientId = settings.PROD_CASHFREE_CLIENT_ID
    Cashfree.XClientSecret = settings.PROD_CASHFREE_CLIENT_SECRET
    Cashfree.XEnvironment = Cashfree.PRODUCTION

# Create your views here.
def update_shipping_address(request, shipping_address_id):
    address = ShippingAddress.objects.get(pk=shipping_address_id)
    if request.method == "POST":
        form = ShippingAdressForm(request.POST, instance=address)
        if form.is_valid():
            shipping_address = form.save()
            order = Order.objects.get(shipping_address=shipping_address.pk)
            return redirect("payment_page", order.pk)
    else:
        form = ShippingAdressForm(instance=address)
    return render(request, "checkout.html", {"form": form})


def payment_page(request, order_id):
    order = Order.objects.get(order_id=order_id)
    env = os.environ.get("ENVIRONMENT")
    if env == "production":
        env_ = 'production'
    else:
        env_ = 'sandbox'

    context = {
        "order": order,
        "env": env_,
    }
    return render(request, "checkout-payment.html", context)


x_api_version = "2023-08-01"


def process_order(request, order_id):
    cart = Cart(request)
    order = Order.objects.get(order_id=order_id)

    all_products = cart.all_products()
    total_amount = int(cart.total_amount()) + 100  # add delivery charge


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
            is_fixed_price=is_fixed_price,
            product_name=item['product'].base_product.name,
            is_stitched=item['is_stitched'],
        )

    if os.environ.get("ENVIRONMENT") == "production":
        callback_url = OrderMeta(
            return_url=request.build_absolute_uri(reverse(settings.RAZOR_PAY_CALLBACK_URL))+ "?order_id={order_id}".replace("http://",
                                                                                                    "https://")
        )
    else:
        callback_url = OrderMeta(return_url=request.build_absolute_uri(reverse(settings.RAZOR_PAY_CALLBACK_URL))+ "?order_id={order_id}")

    customer = CustomerDetails(
        customer_id=f"user_{request.user.username}",
        customer_name=request.user.username,
        customer_phone=order.shipping_address.phone_number,
        customer_email=request.user.email
    )

    cashfree_order_id = str(uuid.uuid4())

    data = CreateOrderRequest(
        order_id=cashfree_order_id,
        order_amount=float(total_amount),  # RUPEES
        order_currency="INR",
        customer_details=customer,
        order_meta=callback_url,
    )

    response = Cashfree().PGCreateOrder(
        x_api_version,
        data,
        None,
        None
    )

    order.razorpay_order_id = response.data.payment_session_id
    order.total = total_amount
    order.save()


    return JsonResponse({
        "payment_session_id": response.data.payment_session_id
    })

@csrf_exempt
def payment_verify(request):
    cashfree_order_id = request.GET.get("order_id")

    # 1️⃣ Validate request
    if not cashfree_order_id:
        return render(
            request,
            "payment_verify.html",
            {
                "status": "Invalid request",
                "is_success": False,
            }
        )

    # 2️⃣ Fetch order from DB
    try:
        order = Order.objects.get(order_id=cashfree_order_id)
    except Order.DoesNotExist:
        return render(
            request,
            "payment_verify.html",
            {
                "status": "Order not found",
                "is_success": False,
            }
        )

    # 3️⃣ Fetch order status from Cashfree
    response = Cashfree().PGFetchOrder(
        x_api_version,
        cashfree_order_id,
        None
    )

    print("Cashfree Response:", response.data)

    # 4️⃣ HARD BLOCK — payment not completed
    if response.data.order_status != "PAID":
        return render(
            request,
            "payment_verify.html",
            {
                "status": "Payment not completed",
                "payment_status": response.data.order_status,
                "order_id": cashfree_order_id,
                "is_success": False,
            }
        )

    # 5️⃣ Prevent duplicate processing
    if order.is_paid:
        return render(
            request,
            "payment_verify.html",
            {
                "status": "Payment already verified",
                "order_id": cashfree_order_id,
                "is_success": True,
            }
        )

    # 6️⃣ Atomic transaction (CRITICAL)
    with transaction.atomic():

        order.is_paid = True
        order.payment_gateway_order_id = response.data.order_id
        order.save()

        order_items = OrderItem.objects.select_for_update().filter(order_id=order)

        for item in order_items:
            product = item.variant_id
            qty = item.quantity

            product.sale = (product.sale or 0) + qty
            product.stock -= qty
            product.save()

    # 7️⃣ Clear cart safely (UX only)
    Cart(request).clear()

    # 8️⃣ Success response
    return render(
        request,
        "payment_verify.html",
        {
            "status": "Payment Verified Successfully",
            "order_id": cashfree_order_id,
            "is_success": True,
        }
    )


@login_required
def order_page(request):
    orders = Order.objects.filter(user=request.user, is_paid=True)
    context = {
        "orders": orders,
    }
    return render(request, "order_details.html", context)


def admin_order(request):
    if request.user.is_superuser:
        status_filter = request.GET.get('status')
        if status_filter in ["pending", "packed", "shipped", "delivered"]:
            orders = Order.objects.filter(status=status_filter,is_paid=True).order_by('-created_at')
        else:
            orders = Order.objects.filter(is_paid=True).order_by('-created_at')

        context = {
            "orders": orders,
        }

        return render(request, "admin_order.html",context)
    else:
        messages.error(request, "You are not authorized to view this page.")
        return redirect("index")

def update_order_status(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)

    # Change status in steps
    order = get_object_or_404(Order, order_id=order_id)

    # Change status step by step
    if order.status == "pending":
        order.status = "packed"
    elif order.status == "packed":
        order.status = "shipped"
    elif order.status == "shipped":
        order.status = "delivered"
    # if already delivered, do nothing

    order.save()
    return redirect('admin_order')