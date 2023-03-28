from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from rest_framework import permissions
from rest_framework.parsers import FormParser, MultiPartParser

# lets us explicitly set upload path and filename


def upload_to(instance, filename):
    return "images/{filename}".format(filename=filename)


class Categories(MPTTModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)
    image_url = models.ImageField(upload_to=upload_to, blank=True, null=False)
    is_active = models.BooleanField(default=False)

    class MPTTMeta:
        order_insertion_by = ["slug"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255)
    image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    is_active = models.BooleanField(default=False)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    categories = TreeForeignKey(
        "categories", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name


class ProductLine(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=50)
    sku = models.CharField(max_length=100)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_line"
    )
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.sku)
