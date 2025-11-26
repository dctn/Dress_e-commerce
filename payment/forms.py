from django import forms
from django.core.exceptions import ValidationError
import re
from payment.models import ShippingAddress


class ShippingAdressForm(forms.ModelForm    ):
    class Meta:
        model = ShippingAddress
        fields = "__all__"
        exclude = ["shipping_id"]

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "9156565500",}),
            "street_address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Street & House No"}),
            "landmark": forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
            "district": forms.Select(attrs={"class": "form-select"}),
            "state": forms.Select(attrs={"class": "form-select"}),
            "postal_code": forms.TextInput(attrs={"class": "form-control"}),
        }

        # Phone number validation

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        if not re.fullmatch(r"\d{10}", phone):
            raise ValidationError("Phone number must be 10 digits")
        return phone

        # ZIP Code validation

    def clean_postal_code(self):
        zipcode = self.cleaned_data.get("postal_code")
        if not re.fullmatch(r"\d{6}", zipcode):
            raise ValidationError("Postal Code must be 6 digits.")
        return zipcode
