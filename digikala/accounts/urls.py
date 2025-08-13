from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("update/", views.update_user, name="update"),
    path("update_password/", views.update_password, name="update_password"),
    path("update_profile/", views.update_profile, name="update_profile"),
    path("orders/", views.orders, name="orders"),
    path("order_detail/<int:pk>", views.order_detail, name="order_detail"),
]
