from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from . import forms
from shop import models
from django.shortcuts import get_object_or_404
import json
from payment.forms import ShippingForm
from payment.models import ShippingAddress, Order, OrderItem
from cart.cart import Cart


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            current_user = models.Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.my_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)

                for key, value in converted_cart.items():
                    product = models.Product.objects.get(id=key)
                    cart.db_add(product=product, qty=value['qty'], update=True)

            messages.success(request, 'با موفقیت وارد شدید!')
            return redirect('home')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور نادرست است!')
            return render(request, "accounts/login.html")

    return render(request, "accounts/login.html")


def logout_user(request):
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید!')
    return redirect("home")


def register_user(request):
    form = forms.RegisterForm()
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'با موفقیت ثبت نام شدید!')
            return redirect('update_profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect('register')
    else:
        form = forms.RegisterForm()

    return render(request, "accounts/register.html", {'form': form})


def update_user(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        form = forms.UpdateForm(request.POST or None, instance=user)

        if form.is_valid():
            form.save()
            login(request, user)
            messages.success(request, 'ویرایش با موفقیت انجام شدید!')
            return redirect("home")

        return render(request, "accounts/update.html", {'form': form})
    else:
        messages.error(request, 'برای ویرایش پروفایل، باید وارد شوید!')
        return redirect("login")


def update_password(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)

        if request.method == 'POST':
            form = forms.UpdatePasswordForm(user, request.POST)

            if form.is_valid():
                form.save()
                login(request, user)
                messages.success(request, 'ویرایش با موفقیت انجام شدید!')
                return redirect("update")
            else:
                for error in form.errors.values():
                    messages.error(request, error)
                return redirect("update_password")
        else:
            form = forms.UpdatePasswordForm(user)
            return render(request, "accounts/update_password.html", {'form': form})
    else:
        messages.error(request, 'برای ویرایش رمزعبور، باید وارد شوید!')
        return redirect("login")


def update_profile(request):
    profile = get_object_or_404(models.Profile, user=request.user)
    profile, created = models.Profile.objects.get_or_create(user=request.user)
    shipping_user, created = ShippingAddress.objects.get_or_create(
        user=request.user)

    if request.method == 'POST':
        form = forms.UpdateUserProfile(request.POST, instance=profile)
        shipping_form = ShippingForm(request.POST, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, 'پروفایل با موفقیت به‌روزرسانی شد!')
            return redirect('home')
    else:
        form = forms.UpdateUserProfile(instance=profile)
        shipping_form = ShippingForm(instance=shipping_user)

    return render(request, 'accounts/update_profile.html', {'form': form, 'shipping_form': shipping_form})


def orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
        return render(request, 'accounts/orders.html', {'orders': orders})

    else:
        messages.success(request, 'دسترسی به اسن صفخه امکان پذیر نیست!')
        return redirect('login')


def order_detail(request, pk):
    if request.user.is_authenticated:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)

        return render(request, 'accounts/order_detail.html', {'order': order, 'items': items})

    else:
        messages.success(request, 'دسترسی به اسن صفخه امکان پذیر نیست!')
        return redirect('login')
