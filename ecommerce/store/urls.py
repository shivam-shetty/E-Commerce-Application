from django.urls import path
from . import views

urlpatterns = [
        #Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('login/', views.user_login, name = "login"),
    path('sign_up/', views.sign_up, name="sign_up"),
    path('update_item/', views.updateItem, name = "update_item"),
    path('products/<slug:slug>', views.product_detail, name = "product_detail"),
]