from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.shopPage, name="shop"),
    path("product/<int:pk>", views.product, name="product"),
    path("category/<str:cat>", views.category, name="category"),
    path("category/", views.category_summary, name="category_summary"),
    path("search/", views.search, name="search"),
]
