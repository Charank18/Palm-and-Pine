# LittleLemonAPI/urls.py

from django.urls import path
from .views import (
    menu_item_list, menu_item_detail, create_menu_item, update_menu_item, delete_menu_item,
    manager_list, assign_manager, remove_manager, delivery_crew_list, assign_delivery_crew, remove_delivery_crew,
    cart_list, add_to_cart, clear_cart,
    order_list, create_order, order_detail, update_order, delete_order, delivery_crew_orders, update_order_status
)

urlpatterns = [
    path('menu-items/', menu_item_list, name='menu-item-list'),
    path('menu-items/<int:pk>/', menu_item_detail, name='menu-item-detail'),
    path('menu-items/create/', create_menu_item, name='create-menu-item'),
    path('menu-items/<int:pk>/update/', update_menu_item, name='update-menu-item'),
    path('menu-items/<int:pk>/delete/', delete_menu_item, name='delete-menu-item'),
    
    path('groups/manager/users/', manager_list, name='manager-list'),
    path('groups/manager/users/assign/', assign_manager, name='assign-manager'),
    path('groups/manager/users/<int:user_id>/remove/', remove_manager, name='remove-manager'),
    
    path('groups/delivery-crew/users/', delivery_crew_list, name='delivery-crew-list'),
    path('groups/delivery-crew/users/assign/', assign_delivery_crew, name='assign-delivery-crew'),
    path('groups/delivery-crew/users/<int:user_id>/remove/', remove_delivery_crew, name='remove-delivery-crew'),
    
    path('cart/menu-items/', cart_list, name='cart-list'),
    path('cart/menu-items/add/', add_to_cart, name='add-to-cart'),
    path('cart/menu-items/clear/', clear_cart, name='clear-cart'),
    
    path('orders/', order_list, name='order-list'),
    path('orders/create/', create_order, name='create-order'),
    path('orders/<int:pk>/', order_detail, name='order-detail'),
    path('orders/<int:pk>/update/', update_order, name='update-order'),
    path('orders/<int:pk>/delete/', delete_order, name='delete-order'),
    path('orders/delivery-crew/', delivery_crew_orders, name='delivery-crew-orders'),
    path('orders/<int:pk>/status/', update_order_status, name='update-order-status'),
]
