from django.urls import path
from . import views

urlpatterns = [
        #Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('login/', views.login, name = "login"),
    path('sign_up/', views.sign_up, name="sign_up"),
    path('update_item/', views.updateItem, name = "update_item"),
    path('product_detail', views.product_detail, name = "product_detail"),
]