from django.contrib.auth.models import User
from django.db import models
import uuid

from core.models import *
# Create your models here.

# Address Choices
STATE_CHOICES = [
    ("KA", "Karnataka"),
    ("TN", "Tamil Nadu"),
    ("MH", "Maharashtra"),
    ("TS", "Telangana"),
]

DISTRICT_CHOICES = [
        ("Chennai", "Chennai"),
        ("Coimbatore", "Coimbatore"),
        ("Madurai", "Madurai"),
        ("Tiruchirappalli", "Tiruchirappalli"),
        ("Salem", "Salem"),
        ("Tirunelveli", "Tirunelveli"),
        ("Erode", "Erode"),
        ("Vellore", "Vellore"),
        ("Thoothukudi", "Thoothukudi"),
        ("Dindigul", "Dindigul"),
        ("Thanjavur", "Thanjavur"),
        ("Kancheepuram", "Kancheepuram"),
        ("Virudhunagar", "Virudhunagar"),
        ("Karur", "Karur"),
        ("Krishnagiri", "Krishnagiri"),
        ("Namakkal", "Namakkal"),
        ("Ramanathapuram", "Ramanathapuram"),
        ("Kanyakumari", "Kanyakumari"),
    ]

class ShippingAddress(models.Model):
    shipping_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=10)
    street_address = models.CharField(max_length=255)
    district = models.CharField(max_length=100,choices=DISTRICT_CHOICES,default="Chennai")
    landmark = models.CharField(max_length=100,)
    state = models.CharField(max_length=100,choices=STATE_CHOICES,default="TN")
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class OrderItem(models.Model):
    order_item_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True,primary_key=True)
    variant_id = models.ForeignKey(VariantProduct, on_delete=models.SET_NULL, null=True)
    order_id = models.ForeignKey("Order", on_delete=models.SET_NULL, null=True)
    is_fixed_price = models.BooleanField(default=False)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=100)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)



class Order(models.Model):
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True,primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_items = models.ManyToManyField(VariantProduct, through=OrderItem,blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=255, null=True, blank=True)
    signature_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.payment_id}"