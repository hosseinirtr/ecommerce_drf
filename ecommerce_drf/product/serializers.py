from rest_framework import serializers

from .models import Brand, Categories, Product


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        # fields = "__all__"
        fields = ["name", "image_url", "title"]


class BrandSerializer(serializers.ModelSerializer):
    creator_id = serializers.ReadOnlyField(source="creator.id")
    image_url = serializers.ImageField(required=False)

    class Meta:
        model = Brand
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    categories = CategoriesSerializer()

    class Meta:
        model = Product
        fields = "__all__"
