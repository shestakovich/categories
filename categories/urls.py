from django.contrib import admin
from django.urls import path

from main.views import CategoryCreateView, CategoryDetailView, CategoriesListView

urlpatterns = [
    path('categories/', CategoryCreateView.as_view()),
    path('categories/<int:pk>/', CategoryDetailView.as_view()),
    path('categories/all/', CategoriesListView.as_view()),
]
