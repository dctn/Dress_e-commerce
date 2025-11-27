from django.db import models
import uuid
from datetime import timedelta
from django.utils import timezone
# Create your models here.
class Tag(models.Model):
    tag_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,unique=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class BaseProduct(models.Model):
    base_product_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True,unique=True)
    name = models.CharField(max_length=100)
    desp = models.TextField()


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Color(models.Model):
    color_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,unique=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class VariantProduct(models.Model):
    variant_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True,unique=True)
    base_product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE,related_name='variants')
    color = models.ForeignKey(Color, on_delete=models.CASCADE,related_name='variants')
    tag = models.ManyToManyField(Tag,related_name='variants')
    image_1 = models.ImageField(upload_to='product_images/')
    image_2 = models.ImageField(blank=True, null=True, upload_to='product_images/')
    image_3 = models.ImageField(blank=True, null=True, upload_to='product_images/')
    image_4 = models.ImageField(blank=True, null=True, upload_to='product_images/')


    price = models.FloatField(blank=True, null=True)
    stock = models.IntegerField()
    sale = models.IntegerField(blank=True, null=True, editable=False,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_discount = models.BooleanField(default=False)
    discount_price = models.FloatField(blank=True, null=True)

    price_per_inches = models.FloatField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_price(self,):
        if self.price and self.is_discount:
            return self.discount_price
        elif self.price and not self.is_discount:
            return self.price
        if self.price_per_inches:
            return self.price_per_inches
        return 0

    @property
    def is_new(self,):
        return self.created_at >= timezone.now() - timedelta(days=7)

