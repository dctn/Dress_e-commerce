from django.shortcuts import render
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.
def index(request):
    return render(request, 'index.html')


def products(request,filter=None,category=None):

    all_products = VariantProduct.objects.all()
    search = request.GET.get('search')
    if search:
        all_products = all_products.filter(Q(base_product__name__icontains =search) |
                                           Q(base_product__desp__icontains=search) |
                                           Q(tag__name__icontains =search) |
                                           Q(color__name__icontains = search)).distinct()


    if filter:
        all_products = VariantProduct.objects.filter(tag__name=filter)

    paginator = Paginator(all_products, 9)
    page = request.GET.get('page')
    all_products = paginator.get_page(page)
    context = {
        'all_products': all_products,
    }
    return render(request,"category.html",context)

def product_details(request,id):
    product = VariantProduct.objects.get(variant_id=id)

    related_base_product = VariantProduct.objects.filter(base_product=product.base_product)
    # if related_base_product.count() < 4:
    #     related_base_product = VariantProduct.objects.filter(Q(tag__name=product.tag.name)|
    #                                                          Q(color__name =product.color.name))

    context = {
        'product': product,
        'related_base_product': related_base_product,
    }
    return render(request,"product_details.html",context)