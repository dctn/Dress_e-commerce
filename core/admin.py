from django.contrib import admin
from django import forms
from core.models import VariantProduct, BaseProduct, Color, Tag


class VariantProductAdminForm(forms.ModelForm):
    class Meta:
        model = VariantProduct
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        price_per_inch = cleaned_data.get('price_per_inches')

        if price and price_per_inch:
            raise forms.ValidationError(
                "❌ Choose ONLY ONE pricing method: Fixed Price OR Price Per Inch."
            )

        if not price and not price_per_inch:
            raise forms.ValidationError(
                "❌ You must enter at least one pricing method."
            )

        return cleaned_data


@admin.register(VariantProduct)
class VariantProductAdmin(admin.ModelAdmin):
    form = VariantProductAdminForm  # 👈 IMPORTANT
    list_display = ("base_product", "color_name", "price_value", "is_discount", "discount_price","price_per_inches")

    def color_name(self, obj):
        return obj.color.name

    color_name.short_description = "Color"

    def price_value(self, obj):
        return obj.price

    price_value.short_description = "Price"

    def discount_price(self, obj):
        return obj.discount_price

    discount_price.short_description = "Discount"

    def is_discount(self, obj):
        return obj.is_discount

    is_discount.boolean = True

    def price_per_inches(self, obj):
        return obj.price_per_inches
    price_per_inches.short_description = "Price per Inches"


admin.site.register(BaseProduct)
admin.site.register(Color)
admin.site.register(Tag)
