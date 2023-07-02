from rest_framework import serializers

from .models import Brand, Categories, Product, ProductLine


class CategoriesSerializer(serializers.ModelSerializer):
    Category_name = serializers.CharField

    class Meta:
        model = Categories
        # fields = "__all__"
        fields = ["name", "image_url", "slug"]


class BrandSerializer(serializers.ModelSerializer):
    creator_id = serializers.ReadOnlyField(source="creator.id")
    image_url = serializers.ImageField(required=False)

    class Meta:
        model = Brand
        exclude = ["id"]


class ProductLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLine
        exclude = ["id"]


class ProductSerializer(serializers.ModelSerializer):
    # Note: mapping data
    brand_name = serializers.CharField(source="brand.name")
    # todo: return list of category because it's categories :)
    categories_name = serializers.CharField(source="categories.name")
    # categories = CategoriesSerializer()
    product_line = ProductLineSerializer(many=True)

    class Meta:
        model = Product
        # exclude = "id"
        fields = (
            "name",
            "slug",
            "description",
            "brand_name",
            "categories_name",
            "product_line",
        )
