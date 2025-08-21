from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("shipping/", views.shipping, name="shipping"),
    path("confirm/", views.confirm_order, name="confirm"),
    path("proccess/", views.proccess_order, name="proccess"),
    path('verify/', views.verify_payment, name='verify_payment'),
]
