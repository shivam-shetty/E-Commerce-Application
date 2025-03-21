from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = PhoneNumberField(blank=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    cost = models.FloatField()
    digital = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id =  models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.transaction_id
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null = True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name},{self.order.transaction_id}" #We put foreign key like this. The self.product.name specifies that we want the product name only
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null = True, blank = True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.TextField(max_length=500, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    pin_code = models.CharField(max_length=100, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address