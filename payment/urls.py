from django.urls import path
from . import views
urlpatterns = [
    path("payment/<order_id>/",views.payment_page,name="payment_page"),
    path("update_address/<shipping_address_id>/",views.update_shipping_address,name="update_address"),
    path("process_order/<order_id>/",views.process_order,name="process_order"),
    path("payment_verify/",views.payment_verify,name="payment_verify"),
]