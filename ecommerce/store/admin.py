from django.contrib import admin
from .models import* #.models means the models.py in this directory

# Register your models here.
admin.site.register(Customer) #We add the model name, hence have written it in capital
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)