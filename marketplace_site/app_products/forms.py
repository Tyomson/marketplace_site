from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Profile, Marketplace, Products


class ExtendedRegisterForm(UserCreationForm):
    first_name = forms.CharField(min_length=3, required=False, help_text=_('Имя'))
    last_name = forms.CharField(min_length=3, required=False, help_text=_('Фамилия'))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')


class AddProduct(forms.Form):
    product_name = forms.CharField(min_length=3, help_text=_('название товара'))
    stocks = forms.IntegerField(min_value=1, help_text=_('количество товара на складе'))
    price = forms.FloatField(min_value=1.0, help_text=_('цена товара'))


class BalanceReplenishment(forms.Form):
    balance = forms.FloatField(required=False, help_text=_('сумма пополнения'))

    # class Meta:
    #     model = Profile
    #     fields = ('first_name', 'last_name', 'balance')


class ShoppingCartForm(forms.Form):
    # pk = forms.IntegerField(show_hidden_initial=False, required=False, widget=forms.HiddenInput)
    number = forms.FloatField(show_hidden_initial=False, label=_('Выберите количество товара'), required=False)

    # class Meta:
    #     model = Products
    #     fields = ('number',)


class BuyShoppingCartForm(forms.Form):
    accept = forms.BooleanField(label=_('Подтверждение покупки'), required=False)
