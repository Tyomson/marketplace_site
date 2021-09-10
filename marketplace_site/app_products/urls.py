from django.urls import path
from .views import RegisterView, AnotherLogoutView, AnotherLoginView, ProductsView, ProductsDetailView, \
    CreateProduct, AccountView, BalanceEdit, ShoppingCartView, MarketplaceView
from .api import ProductListApi, ProductDetailApi, MarketplaceListApi, MarketplaceDetailApi

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', AnotherLoginView.as_view(), name='login'),
    path('logout/', AnotherLogoutView.as_view(), name='logout'),
    path('products_list/', ProductsView.as_view(), name='products'),
    path('products/<int:pk>', ProductsDetailView.as_view(), name='products-detail'),
    path('marketplace/<int:pk>', MarketplaceView.as_view(), name='marketplace-detail'),
    path('create_new_products/', CreateProduct.as_view(), name='create_new_products'),
    path('account/', AccountView.as_view(), name='account'),
    path('balance_replenishment/', BalanceEdit.as_view(), name='balance-replenishment'),
    path('shopping_cart/', ShoppingCartView.as_view(), name='shopping-cart'),
    path('product_api/', ProductListApi.as_view(), name='product_list_api'),
    path('marketplace_api/', MarketplaceListApi.as_view(), name='marketplace_list_api'),
    path('product_api/<int:pk>', ProductDetailApi.as_view(), name='product_detail_api'),
    path('marketplace_api/<int:pk>', MarketplaceDetailApi.as_view(), name='marketplace_detail_api'),
]