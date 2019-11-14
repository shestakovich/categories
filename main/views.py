from django.shortcuts import render
from rest_framework import generics

from main.models import Category
from main.serializers import CategoryDetailSerializer, CategoryCreateSerializer, SubCategoryDetail


class CategoryCreateView(generics.CreateAPIView):
    serializer_class = CategoryCreateSerializer


class CategoryDetailView(generics.RetrieveAPIView):
    serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()


class CategoriesListView(generics.ListAPIView):
    serializer_class = SubCategoryDetail
    queryset = Category.objects.all()
