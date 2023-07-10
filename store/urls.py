# from django.contrib import admin
# from django.urls import path,include

from django.contrib import admin
from django.urls import path
from store import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="updateItem"),
    path('process_order/', views.processOrder, name="process_order"),
    path('sign_up/', views.SignupPage, name="sign_up"),
    path('log_in/', views.LoginPage, name="log_in"),
    path('logout/', views.LogoutPage, name="logout")
]

