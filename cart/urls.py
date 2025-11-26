from django.urls import path
from . import views
urlpatterns = [
    path('add_cart/', views.add_cart, name='add_cart'),
    path('remove_cart/<product_id>/', views.remove_cart, name='remove_cart'),
    path("cart/",views.cart_view,name="cart"),
    path("checkout/", views.checkout, name="checkout"),
]