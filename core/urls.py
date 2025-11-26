from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name="index"),
    path("products/",views.products,name="products"),
    path("products/<str:filter>/", views.products, name="products_filter_tag"),
    path("products_details/<id>/", views.product_details, name="product_details"),
]