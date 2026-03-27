from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-customer/', views.add_customer, name='add_customer'),
    path('add-product/', views.add_product, name='add_product'),
    path('add-order/', views.add_order, name='add_order'),
    
    path('api/customers/', views.CustomerListAPI.as_view(), name='api_customer_list'),
    path('api/products/', views.ProductListAPI.as_view(), name='api_product_list'),
    path('api/orders/', views.OrderListAPI.as_view(), name='api_order_list'),
    path('api/orders/<int:pk>/', views.OrderDetailAPI.as_view(), name='api_order_detail'),
]