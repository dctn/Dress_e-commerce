from .cart import Cart
from core.models import VariantProduct
def get_cart(request):
    cart = Cart(request)


    return {'cart': cart.all_products(),"total": cart.total_amount()}