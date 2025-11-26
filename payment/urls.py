from django.urls import path
from . import views
urlpatterns = [
    path("payment/<order_id>/",views.payment_page,name="payment_page"),
    path("update_address/<shipping_address_id>/",views.update_shipping_address,name="update_address"),
]