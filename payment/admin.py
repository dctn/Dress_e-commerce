from django.contrib import admin

from payment.models import *

# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "total", "status", "created_at")
    search_fields = ("payment_id",)  # Enables search by payment ID
    list_filter = ("status", "created_at")  # Optional: filters in sidebar

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("variant_product", "is_fixed_price", "price_at_purchase", "quantity")

    def variant_product(self, obj):
        return obj.variant_id.base_product.name

    variant_product.short_description = "Product"

admin.site.register(ShippingAddress)
