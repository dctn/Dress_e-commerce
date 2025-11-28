from .cart import Cart
from core.models import VariantProduct
def get_cart(request):
    cart = Cart(request)
    total = 0
    for item,details in cart.session['cart'].items():
        product_details = VariantProduct.objects.get(variant_id=item)
        product_price = product_details.get_price()
        # product_price = product_details.discount_price if product_details.is_discount else product_details.price
        total += (details['qty'] * product_price)

    return {'cart': cart.all_products(),"total": total}