from core.models import VariantProduct

class Cart:
    def __init__(self,request):
        self.session = request.session

        cart = self.session.get('cart')
        if "cart" not in request.session:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add_product(self,product,size,color,qty):
        product = str(product)
        if product not in self.cart:
            self.cart[product] = {
                'size': size,
                'color': color,
                'qty': qty,
            }
        else:
            self.cart[product]['qty'] += qty

        self.session.modified = True

    def all_products(self):
        items = []
        for product_id,details in self.cart.items():
            product = VariantProduct.objects.get(variant_id=product_id)
            product_price = product.get_price()
            # product_price = product.discount_price if product.is_discount else product.price
            items.append({
                'product': product,
                'size': details['size'],
                'color': details['color'],
                'qty': details['qty'],
                'product_price': product_price,
            })
        return items


    def __len__(self):
        total_qty = 0
        for product in self.cart.values():
            total_qty += product['qty']

        return total_qty

    def remove_product(self,product):
        product = str(product)
        if product in self.cart:
            del self.cart[product]
            self.session.modified = True
        return None
