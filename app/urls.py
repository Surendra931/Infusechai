# app/urls.py
from django.urls import path
from . import views  # Ensure there's no circular import

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='user_login'),
    path('about/', views.about, name='about'), 
    path('logout/', views.user_logout, name='user_logout'),
    path('products/', views.products, name='products'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('confirm-order/', views.confirm_order, name='confirm_order'),
    path('order-details/<int:order_id>/', views.order_details, name='order_details'),
    path('previous-orders/', views.previous_orders, name='previous_orders'),
    path('user-profile/', views.user_profile, name='user_profile'),  
]
