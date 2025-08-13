from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from django.utils.translation import gettext_lazy as _
from shop import models


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label="", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "نام خود را وارد کنید"}))
    last_name = forms.CharField(
        label="", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "نام خانوادگی خود را وارد کنید"}))
    email = forms.EmailField(
        label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "ایمیل خود را وارد کنید"}))
    username = forms.CharField(
        label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "نام کاربری خود را وارد کنید"}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'name': 'password',
        'type': "password",
        'placeholder': 'رمز بالای ۸ کاراکتر وارد کنید'
    }))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'name': 'password',
        'type': "password",
        'placeholder': 'رمز خود را مجددا وارد کنید'
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'username', 'password1', 'password2')


class UpdateForm(UserChangeForm):
    password = None
    first_name = forms.CharField(
        label="", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "نام خود را وارد کنید"}))
    last_name = forms.CharField(
        label="", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "نام خانوادگی خود را وارد کنید"}))
    email = forms.EmailField(
        label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "ایمیل خود را وارد کنید"}))
    username = forms.CharField(
        label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "نام کاربری خود را وارد کنید"}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email','username')



class UpdatePasswordForm(SetPasswordForm):
    password = None
    error_messages = {
        'password_incorrect': _("رمز عبور فعلی نادرست است."),
        'password_mismatch': _("رمزهای عبور جدید با هم مطابقت ندارند."),
        'password_too_short': _("رمز عبور جدید باید حداقل %(min_length)d کاراکتر باشد."),
        'password_common': _("رمز عبور جدید بسیار ساده و قابل پیش‌بینی است."),
    }
    new_password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'name': 'password',
        'type': "password",
        'placeholder': 'رمز بالای ۸ کاراکتر وارد کنید'
    }))
    new_password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'name': 'password',
        'type': "password",
        'placeholder': 'رمز خود را مجددا وارد کنید'
    }))
    
    class Meta:
        model = User
        fields = ('new_password1', 'new_password2')


class UpdateUserProfile(forms.ModelForm):
    
    phone = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'name': 'phone',
        'type': "text",
        'placeholder': 'موبایل خود را وارد کنید'
    }))
    address1 = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'name': 'address1',
        'type': "text",
        'placeholder': 'آدرس منزل خود را وارد کنید'
    }))
    address2 = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'name': 'address2',
        'type': "text",
        'placeholder': 'آدرس محل کار خود را وارد کنید'
    }))
    city = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'name': 'city',
        'type': "text",
        'placeholder': 'شهر خود را وارد کنید'
    }))
    state = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'name': 'state',
        'type': "text",
        'placeholder': 'منطقه خود را وارد کنید'
    }))
    zipcode = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'name': 'zipcode',
        'type': "text",
        'placeholder': 'کدپستی خود را وارد کنید'
    }))
    country = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'name': 'country',
        'type': "text",
        'placeholder': 'کشور خود را وارد کنید'
    }))
    
    
    class Meta:
        model =models.Profile
        fields = ('phone', 'address1', 'address2',
                  'city', 'state', 'zipcode', 'country')