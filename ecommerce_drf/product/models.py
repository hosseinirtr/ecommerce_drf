from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from rest_framework import permissions
from rest_framework.parsers import FormParser, MultiPartParser

# lets us explicitly set upload path and filename


def upload_to(instance, filename):
    return "images/{filename}".format(filename=filename)


class Categories(MPTTModel):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)
    image_url = models.ImageField(upload_to=upload_to, blank=True, null=False)

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)

    categories = TreeForeignKey(
        "categories", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name
