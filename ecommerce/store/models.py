from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from tinymce.models import HTMLField
from django.template.defaultfilters import slugify

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
    image = models.ImageField(null=True, blank=True, upload_to="product_images")
    slug = models.SlugField(default="", unique=True, null=True)
    description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs): #Arguments -> touple form || keyword arguments -> dict form
        if not self.slug:
            self.slug=slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name="order")
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id =  models.CharField(max_length=200, null=True)

    @property
    def get_cart_total(self):
        orderitems = self.order_items.all()
        total=sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.order_items.all()
        total=sum([item.quantity for item in orderitems])
        return total
    
    @property
    def shipping(self):
        shipping=False
        orderitems = self.order_items.all()
        for i in orderitems:
            if i.product.digital==False:
                shipping=True
        return shipping

    def __str__(self):
        return self.transaction_id
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="order_items")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name="order_items")
    quantity = models.IntegerField(default=0, null = True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.cost*self.quantity
        return total

    def __str__(self):
        return f"{self.product.name},{self.order.transaction_id}" #We put foreign key like this. The self.product.name specifies that we want the product name only
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null = True, blank = True, related_name="shipping_address")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name="shipping_address")
    address = models.TextField(max_length=500, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    pin_code = models.CharField(max_length=100, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
class ProductDetails(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="product_details")
    description = HTMLField()

    def __str__(self):
        return
    # multiple images

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="product_images")
    details = models.ForeignKey(ProductDetails, on_delete=models.SET_NULL, null = True, related_name="product_images")
    image = models.ImageField(upload_to="product_images")
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        images = list(self.product.product_images.order_by("id"))
        image_index = images.index(self)+1
        return f"photo {image_index} of {self.product.name}"