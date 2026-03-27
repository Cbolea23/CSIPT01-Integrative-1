from django.db import models

# Create your models here.
class Customer(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.full_name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.name

class Order(models.Model):
    order_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE) 
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return self.order_number