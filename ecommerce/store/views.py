from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Product, OrderItem, Customer  # Import Customer model
import json

def store(request):
    customer = getattr(request.user, 'customer', None)
    if customer:
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.order_items.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order["get_cart_items"]

    products = Product.objects.all()
    context = {"products": products, "cartItems": cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    customer = getattr(request.user, 'customer', None)
    if customer:
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.order_items.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order["get_cart_items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    customer = getattr(request.user, 'customer', None)
    if customer:
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.order_items.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, 'store/checkout.html', context)

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('store')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'store/login.html')

def sign_up(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        terms_accepted = request.POST.get('terms') == 'on'

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('sign_up')

        if not terms_accepted:
            messages.error(request, 'You must agree to the terms and conditions.')
            return redirect('sign_up')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('sign_up')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('sign_up')

        user = User.objects.create_user(username=username, email=email, password=password)
        name_parts = fullname.split(maxsplit=1)
        user.first_name = name_parts[0]
        user.last_name = name_parts[1] if len(name_parts) > 1 else ''
        user.save()

        # ✅ Fixing indentation issue
        customer, created = Customer.objects.get_or_create(
            user=user,
            defaults={"name": fullname, "email": email}
        )

        auth_login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('store')

    return render(request, 'store/sign_up.html')


def updateItem(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

    try:
        data = json.loads(request.body)
        productId = data.get('productId')
        action = data.get('action')

        customer = getattr(request.user, 'customer', None)
        if not customer:
            return JsonResponse({'error': 'Customer not found'}, status=400)

        product = get_object_or_404(Product, id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity += 1
        elif action == 'remove':
            orderItem.quantity -= 1

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

        return JsonResponse({'message': 'Item was updated successfully'}, safe=False)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    images = product.product_images.all()
    description = product.product_details.first() if hasattr(product, 'product_details') else None
    context = {"description": description, "product": product, "images": images}
    return render(request, "store/product_detail.html", context)