from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework import generics, mixins, filters
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission

from .models import Customer, Product, Order
from .forms import CustomerForm, ProductForm, OrderForm
from .serializers import CustomerSerializer, ProductSerializer, OrderSerializer

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Administrator').exists()

def home(request):
    return render(request, 'ordering/index.html')

@login_required
@user_passes_test(is_manager)
def add_customer(request):
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('add_customer')
    return render(request, 'ordering/form.html', {'form': form, 'title': 'Add Customer'})

@login_required
@user_passes_test(is_manager)
def add_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('add_product')
    return render(request, 'ordering/form.html', {'form': form, 'title': 'Add Product'})

@login_required
@user_passes_test(is_manager)
def add_order(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('add_order')
    return render(request, 'ordering/form.html', {'form': form, 'title': 'Add Order'})

class CustomerListAPI(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdministrator]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class CustomerDetailAPI(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdministrator]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ProductListAPI(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdministrator]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class ProductDetailAPI(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdministrator]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class OrderListAPI(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdministrator]
    filter_backends = [filters.SearchFilter]
    search_fields = ['product_name__name', 'order_number']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class OrderDetailAPI(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdministrator]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)