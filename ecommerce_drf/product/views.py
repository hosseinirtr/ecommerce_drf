from django.db import connection
from drf_spectacular.utils import extend_schema
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import SqlLexer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from sqlparse import format

from .models import Brand, Categories, Product
from .serializers import BrandSerializer, CategoriesSerializer, ProductSerializer

# Create your views here.


class handle_404(APIException):
    status_code = 404
    default_detail = "Item not found"
    default_code = "ITEM_NOT_FOUND"


class CategoryViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all categories
    """

    serializer_class = CategoriesSerializer
    queryset = Categories.objects.all()

    @extend_schema(responses=CategoriesSerializer)
    def list(self, req):
        serializers = CategoriesSerializer(self.queryset, many=True)
        return Response(serializers.data)


class BrandViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all Brands
    """

    serializer_class = BrandSerializer
    queryset = Brand.objects.all()

    @extend_schema(responses=BrandSerializer)
    def list(self, req):
        serializers = BrandSerializer(self.queryset, many=True)
        return Response(serializers.data)


class ProductViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all Product
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = "slug"

    def retrieve(self, req, slug=None):
        serializer = ProductSerializer(
            self.queryset.filter(slug=slug).select_related("categories", "brand"),
            many=True,
        )
        data = Response(serializer.data)

        if serializer.data:
            return data
        raise handle_404

    @extend_schema(responses=ProductSerializer)
    def list(self, req):
        serializers = ProductSerializer(self.queryset, many=True)
        return Response(serializers.data)

    @action(
        methods=["get"],
        detail=False,
        url_path=r"category/(?P<category>\w+)/all",
        url_name="all",
    )
    def list_product_by_category(self, req, category=None):
        """
        An Endpoint to return Products by categories
        """
        serializer = ProductSerializer(
            self.queryset.filter(categories__name=category), many=True
        )
        return Response(serializer.data)
