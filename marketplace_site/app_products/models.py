from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    balance = models.FloatField(default=0, verbose_name=_('баланс'))
    status = models.CharField(default='Базовый', max_length=100, verbose_name=_('статус'))
    money_spent = models.FloatField(default=0, verbose_name=_('денег потраченных пользователем'))

    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')


class Marketplace(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name=_('название'))

    class Meta:
        verbose_name = _('магазин')
        verbose_name_plural = _('магазины')

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.ManyToManyField(Marketplace, default=None, null=True,
                                  related_name='products', verbose_name=_('магазин'))
    product_name = models.CharField(max_length=1000, db_index=True, verbose_name=_('название'))
    stocks = models.PositiveIntegerField(default=0, verbose_name=_('остатки товара'))
    price = models.FloatField(default=0, verbose_name=_('цена за одну штуку товара'))

    class Meta:
        verbose_name = _('товар')
        verbose_name_plural = _('товары')


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE,
                             related_name='cart_user', verbose_name=_('пользователь'))
    product_id = models.ForeignKey(Products, default=None, null=True, on_delete=models.CASCADE,
                                   related_name='shopping_cart', verbose_name=_('товар'))
    product_quantity = models.PositiveIntegerField(verbose_name=_('количество товара'))
