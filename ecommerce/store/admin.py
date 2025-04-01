from django.contrib import admin
from .models import* #.models means the models.py in this directory

# Register your models here.
class ImagesInLine(admin.TabularInline):
    model=ProductImages
    extra=1
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={"slug":("name",)}
    inlines=[ImagesInLine]
    fields = ['name', 'cost', 'digital', 'image', 'description', 'slug']

admin.site.register(Customer) #We add the model name, hence have written it in capital
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(ProductDetails)