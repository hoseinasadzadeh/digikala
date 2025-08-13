from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    
    shipping_fullName = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'name': 'phone',
        'type': "text",
        'placeholder': 'نام خود را وارد کنید'
    }))
    shipping_email = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'name': 'phone',
        'type': "text",
        'placeholder': 'ایمیل خود را وارد کنید'
    }))
    shipping_phone = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'name': 'phone',
        'type': "text",
        'placeholder': 'موبایل خود را وارد کنید'
    }))
    shipping_address1 = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'name': 'address1',
        'type': "text",
        'placeholder': 'آدرس منزل خود را وارد کنید'
    }))
    shipping_address2 = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'name': 'address2',
        'type': "text",
        'placeholder': 'آدرس محل کار خود را وارد کنید'
    }))
    shipping_city = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'name': 'city',
        'type': "text",
        'placeholder': 'شهر خود را وارد کنید'
    }))
    shipping_state = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'name': 'state',
        'type': "text",
        'placeholder': 'منطقه خود را وارد کنید'
    }))
    shipping_zipcode = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'name': 'zipcode',
        'type': "text",
        'placeholder': 'کدپستی خود را وارد کنید'
    }))
    shipping_country = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'name': 'country',
        'type': "text",
        'placeholder': 'کشور خود را وارد کنید'
    }))
    
    class Meta:
        model = ShippingAddress
        fields = [
			'shipping_fullName',
			'shipping_email',
			'shipping_phone',
			'shipping_address1',
			'shipping_address2',
			'shipping_city',
			'shipping_state',
			'shipping_zipcode',
			'shipping_country',
		]
        exclude = ['user',]