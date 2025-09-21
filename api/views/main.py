from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers.main import CategorySerializer, ProductSerializer
from apps.main.models import Category, Product


class CategoryApiView(APIView):

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailApiView(APIView):

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        if not pk:
            return Response({"detail": "Method PUT not allowed without pk"}, status=status.HTTP_400_BAD_REQUEST)

        instance = Category.objects.get(pk=pk)
        serializer = CategorySerializer(instance, request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not pk:
            return Response({"detail": "Method DELETE not allowed without pk"}, status=status.HTTP_400_BAD_REQUEST)
        product = Category.objects.get(id=pk)

        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductApiView(APIView):

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailApiView(APIView):

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        if not pk:
            return Response({"detail": "Method PUT not allowed without pk"}, status=status.HTTP_400_BAD_REQUEST)
        instance = Product.objects.get(pk=pk)
        serializer = ProductSerializer(instance, )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not pk:
            return Response({"detail": "Method DELETE not allowed without pk"}, status=status.HTTP_400_BAD_REQUEST)
        product = Product.objects.get(id=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
