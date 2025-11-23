from django.urls import path
from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path('product/<slug:slug>/', views.Product_Detail, name='product'),
  path("cart/", views.cart, name="cart"),
  path('cart/add/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
  path('cart/remove/<int:item_id>/', views.remove_from_cart, name="remove_from_cart"),
  path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
  path('success/', views.success_view, name='success'),
  path('cancel/', views.cancel_view, name='cancel'),
]