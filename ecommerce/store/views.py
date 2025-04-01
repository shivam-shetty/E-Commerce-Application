from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Product, OrderItem
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
import json

# Create your views here.
def store(request):
     if request.user.is_authenticated:
          customer = request.user.customer
          order,created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.order_items.all()
          cartItems = order.get_cart_items
     else:
          items = []
          order = {"get_cart_total":0, "get_cart_items":0}
          cartItems = order["get_cart_items"]
     products = Product.objects.all()
     context = {"products":products, "cartItems":cartItems}
     return render(request, 'store/store.html', context)

def cart(request):
     if request.user.is_authenticated:
          customer = request.user.customer
          order,created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.order_items.all()
          cartItems = order.get_cart_items
     else:
          items = []
          order = {"get_cart_total":0, "get_cart_items":0}
          cartItems = order["get_cart_items"]
     context = {"items":items, "order":order, "cartItems":cartItems}
     return render(request, 'store/cart.html', context)

def checkout(request):
     if request.user.is_authenticated:
          customer = request.user.customer
          order,created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.order_items.all()
          cartItems = order.get_cart_items

     else:
          items = []
          order = {"get_cart_total":0, "get_cart_items":0, "shipping":False}
          cartItems = order["get_cart_items"]
     context = {"items":items, "order":order, "cartItems":cartItems}
     return render(request, 'store/checkout.html', context)

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')  # Redirect to store page after login
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'store/login.html')  # Ensure this template exists

def sign_up(request):
    if request.method == 'POST':
        # Retrieve form data
        fullname = request.POST['fullname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        terms_accepted = request.POST.get('terms', False)

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('sign_up')

        # Check if user agrees to the terms
        if not terms_accepted:
            messages.error(request, 'You must agree to the terms and conditions.')
            return redirect('sign_up')

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('sign_up')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('sign_up')

        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = fullname
        user.save()

        # Log the user in automatically
        login(request, user)

        # Redirect to a success page or home
        messages.success(request, 'Account created successfully!')
        return redirect('store')  # Redirect to the store or homepage after successful sign-up

    return render(request, 'store/sign_up.html')

def updateItem(request):
     data=json.loads(request.body)
     productId=data['productId']
     action=data['action']
     print('action',action)
     print('Product',productId)
     customer=request.user.customer
     product=Product.objects.get(id=productId)
     order,created=Order.objects.get_or_create(customer=customer, complete=False)
     orderItem,created=OrderItem.objects.get_or_create(order=order, product=product)
     if action=='add':
          orderItem.quantity+=1
     elif action=='remove':
          orderItem.quantity-=1
     orderItem.save()
     if orderItem.quantity<=0:
          orderItem.delete()
     return JsonResponse('item was added',safe=False)

def product_detail(request):
     return render (request, "store/product_detail.html")