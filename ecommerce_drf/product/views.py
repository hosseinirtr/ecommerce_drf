from django.shortcuts import render
from rest_framework import response, viewsets

from .models import Category
from .serializers import CategorySerializer

# Create your views here.


def home(req):
    return render(req, "index.html")


class CategoryViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all categories
    """

    queryset = Category.objects.all()

    def list(self, req):
        serializers = CategorySerializer(self.queryset, many=True)
        print(serializers.data)
        print(serializers)
        return response(serializers.data)
