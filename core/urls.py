from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name="index"),
    path("products/",views.products,name="products"),
    path("products/<str:filter>/", views.products, name="products_filter_tag"),
    path("products_details/<id>/", views.product_details, name="product_details"),
    path("cancel_refund/", views.cancel_refund, name="cancel_refund"),
    path("terms_and_conditions/", views.terms_and_conditions, name="terms_and_conditions"),
    path("shipping_policy/", views.shipping_policy, name="shipping_policy"),
    path("privacy_policy/", views.privacy_policy, name="privacy_policy"),
    path("contact/", views.contact, name="contact"),
]