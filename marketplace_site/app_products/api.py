from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, \
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from .models import Products, Marketplace
from .serializers import ProductSerializer, MarketplaceSerializer


class StandardResultsSetPagination(PageNumberPagination):
    """Класс пагинации с настройками"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductListApi(ListModelMixin, CreateModelMixin, GenericAPIView):
    """Представление для получения списка товаров и добавление нового товара"""
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'product_name', 'stocks', 'price']

    def get(self, request):
        return self.list(request)

    def post(self, request, format=None):
        return self.create(request)


class ProductDetailApi(UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    """Представление для получения детальной информации об товаре,
     а так же для его редактирования и удаления"""
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class MarketplaceListApi(ListModelMixin, CreateModelMixin, GenericAPIView):
    """Представление для получения списка магазинов и добавление новых магазинов"""
    queryset = Marketplace.objects.all()
    serializer_class = MarketplaceSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['name']

    def get(self, request):
        return self.list(request)

    def post(self, request, format=None):
        return self.create(request)


class MarketplaceDetailApi(UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    """Представление для получения детальной информации о магазине,
     а так же для её редактирования и удаления"""
    queryset = Marketplace.objects.all()
    serializer_class = MarketplaceSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
