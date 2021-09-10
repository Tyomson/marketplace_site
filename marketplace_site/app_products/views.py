from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.db.models import ExpressionWrapper, F, FloatField
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic, View
from django.utils.translation import gettext_lazy as _
from .models import Marketplace, Products, Profile, ShoppingCart
from .forms import ExtendedRegisterForm, BalanceReplenishment, \
    ShoppingCartForm, BuyShoppingCartForm, AddProduct


class ProductsView(generic.ListView):
    """Представление для отображения списка всех товаров"""
    model = Products
    template_name = 'products_list.html'
    context_object_name = 'products_list'
    queryset = Products.objects.all()


class ProductsDetailView(generic.DetailView):
    """Представление для детального отображения товара"""
    model = Products
    queryset = Products.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProductsDetailView, self).get_context_data(**kwargs)
        context['form'] = ShoppingCartForm()
        return context

    def post(self, request, pk, *args, **kwargs):
        shop_form = ShoppingCartForm(request.POST)
        if shop_form.is_valid():
            with transaction.atomic():
                number = shop_form.cleaned_data['number']
                shop_id = request.POST['shop_id']
                product = Products.objects.get(id=shop_id)
                user = User.objects.get(username=request.user.username)
                ShoppingCart.objects.create(user=user, product_id=product, product_quantity=number)
        return HttpResponseRedirect(f'/products/products/{pk}')


class MarketplaceView(View):
    """Представление для детального отображения магазина"""

    def get(self, request, pk):
        shop = Marketplace.objects.filter(id=pk)
        return render(request, 'app_products/marketplace_detail.html', {'shop': shop})


class RegisterView(View):
    """Представление для регистрации нового пользователя"""
    def get(self, request):
        form = ExtendedRegisterForm()
        return render(request, 'app_products/register.html', {'form': form})

    def post(self, request):
        form = ExtendedRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
            )
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/products/products_list/')
        return render(request, 'app_products/register.html', {'form': form})


class CreateProduct(View):
    """Представление для добавления нового товара"""
    def get(self, request):
        create_product_form = AddProduct()
        context = {'create_product_form': create_product_form}
        return render(request, 'app_products/create_new_products.html', context=context)

    def post(self, request):
        create_product_form = AddProduct(request.POST)
        if create_product_form.is_valid():
            product_name = create_product_form.cleaned_data.get('product_name')
            stocks = create_product_form.cleaned_data.get('stocks')
            price = create_product_form.cleaned_data.get('price')
            Products.objects.create(product_name=product_name, stocks=stocks, price=price)
            return HttpResponseRedirect('/products/products_list/')

        return render(request, 'app_products/create_new_products.html',
                      context={
                          'create_product_form': create_product_form
                      }
                      )


class AnotherLoginView(LoginView):
    """Представление для Login"""
    template_name = 'app_products/login.html'


class AnotherLogoutView(LogoutView):
    """Представление для Logout"""
    template_name = 'app_products/logout.html'
    next_page = '/products/products_list/'


class AccountView(View):
    """Представление для отображения информации пользователя"""
    def get(self, request):
        information_users = request.user
        return render(request, 'app_products/account.html', {'account': information_users})


class BalanceEdit(View):
    """Представление для пополнения баланса пользователя"""
    def get(self, request):
        # user = User.objects.get(username=request.user)
        balance_form = BalanceReplenishment()
        return render(request, 'app_products/balance_replenishment.html',
                      context={'balance_form': balance_form})

    def post(self, request):
        balance_form = BalanceReplenishment(request.POST)
        if balance_form.is_valid():
            balance = balance_form.cleaned_data.get('balance')
            user_balance = Profile.objects.get(user=request.user).balance
            Profile.objects.filter(user=request.user).update(balance=user_balance + balance)
        return HttpResponseRedirect(f'/products/account/')


class ShoppingCartView(View):
    """Представление для отображения корзины пользователя"""
    def get(self, request):
        # shopping_form = BuyShoppingCartForm()
        shopping_cart = ShoppingCart.objects.filter(user=request.user).annotate(
            cart_summ=ExpressionWrapper(
                F('product_quantity')*F('product_id__price'), output_field=FloatField()
            )
        )
        return render(request, 'app_products/shopping_cart.html',
                      context={
                          'shopping_cart': shopping_cart,
                          # 'shopping_form': shopping_form,
                      }
                      )

    def post(self, request):
        shopping_form = BuyShoppingCartForm(request.POST)
        if shopping_form.is_valid():
            with transaction.atomic():
                goods = request.POST
                for item in goods:
                    if item[0:6] != 'accept':
                        continue
                    product_id = item[6:7]
                    cart = ShoppingCart.objects.get(user=request.user, id=product_id)
                    profile = Profile.objects.get(user=request.user)
                    product = Products.objects.get(id=product_id)
                    # удаление остатков
                    if product.stocks < cart.product_quantity:
                        return HttpResponse(f'<h1>{_("Товар отсутствует на складе")}!</h1>')
                    Products.objects.filter(id=product_id).update(stocks=product.stocks - cart.product_quantity)
                    # удаление денег с баланса и добавление к потраченным деньгам
                    if profile.balance < (product.price * cart.product_quantity):
                        return HttpResponse(f'<h1>{_("Недостаточно средств")}!</h1>')
                    Profile.objects.filter(user=request.user).update(
                        balance=profile.balance - (product.price * cart.product_quantity),
                        money_spent=profile.money_spent + (product.price * cart.product_quantity))
                    # смена статуса
                    if profile.status == 'Базовый' and profile.money_spent >= 100.0:
                        Profile.objects.filter(user=request.user).update(status='Средний')
                    elif profile.status == 'Средний' and profile.money_spent >= 1000.0:
                        Profile.objects.filter(user=request.user).update(status='Максимальный')
                    cart.delete()

        return HttpResponseRedirect(f'/products/shopping_cart/')
