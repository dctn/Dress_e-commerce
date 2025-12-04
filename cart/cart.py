from core.models import VariantProduct

class Cart:
    def __init__(self,request):
        self.session = request.session

        cart = self.session.get('cart')
        if "cart" not in request.session:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add_product(self,product,size,color,qty,is_stitched):
        product = str(product)

        if product not in self.cart:
            self.cart[product] = []

        for item in self.cart[product]:
            if item['size'] == size and item['color'] == color and item['is_stitched'] == is_stitched:
                item['qty'] += qty
                self.session.modified = True
                return

        self.cart[product].append({
            'size': size,
            'color': color,
            'qty': qty,
            'is_stitched': is_stitched,
        })
        self.session.modified = True

    def all_products(self):
        items = []
        for product_id,details in self.cart.items():
            product = VariantProduct.objects.get(variant_id=product_id)
            product_price = product.get_price()
            for detail in details:
                items.append({
                    'product': product,
                    'size': detail['size'],
                    'color': detail['color'],
                    'qty': detail['qty'],
                    'product_price': product_price,
                    'is_stitched': detail['is_stitched'],
                })
        return items

    def total_amount(self):
        total = 0
        for item in self.all_products():
            if item['is_stitched'] == "1":
                total += (item['product_price'] * item['qty']) + 1000
            else:
                total += item['product_price'] * item['qty']
        return total

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

    def clear(self):
        self.cart = {}
        self.session['cart'] = {}
        self.session.modified = True

