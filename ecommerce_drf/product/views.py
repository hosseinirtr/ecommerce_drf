from rest_framework import viewsets
from rest_framework.response import Response

from .models import Brand, Categories, Product
from .serializers import BrandSerializer, CategoriesSerializer, ProductSerializer

# Create your views here.


class CategoryViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all categories
    """

    queryset = Categories.objects.all()

    def list(self, req):
        serializers = CategoriesSerializer(self.queryset, many=True)
        return Response(serializers.data)


class BrandViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all categories
    """

    queryset = Brand.objects.all()

    def list(self, req):
        serializers = BrandSerializer(self.queryset, many=True)
        return Response(serializers.data)


class ProductViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all Product
    """

    queryset = Product.objects.all()

    def list(self, req):
        serializers = ProductSerializer(self.queryset, many=True)
        return Response(serializers.data)
