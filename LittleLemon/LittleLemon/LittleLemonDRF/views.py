# LittleLemonAPI/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import Group
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer

# Custom permission classes
class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='manager').exists()

class IsDeliveryCrew(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='delivery-crew').exists()

# Menu Items Endpoints
@api_view(['GET'])
def menu_item_list(request):
    if request.user.groups.filter(name='manager').exists():
        menu_items = MenuItem.objects.all()
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data)
    elif request.user.groups.filter(name='delivery-crew').exists():
        menu_items = MenuItem.objects.all()
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data)
    else:
        return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def menu_item_detail(request, pk):
    try:
        menu_item = MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.user.groups.filter(name='manager').exists() or request.user.groups.filter(name='delivery-crew').exists():
        serializer = MenuItemSerializer(menu_item)
        return Response(serializer.data)
    else:
        return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
@permission_classes([IsManager])
def create_menu_item(request):
    serializer = MenuItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsManager])
def update_menu_item(request, pk):
    try:
        menu_item = MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MenuItemSerializer(menu_item, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsManager])
def delete_menu_item(request, pk):
    try:
        menu_item = MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    menu_item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# User Group Management Endpoints
@api_view(['GET'])
@permission_classes([IsManager])
def manager_list(request):
    managers = User.objects.filter(groups__name='manager')
    serializer = UserSerializer(managers, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsManager])
def assign_manager(request):
    user_id = request.data.get('user_id')
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    manager_group = Group.objects.get(name='manager')
    user.groups.add(manager_group)
    return Response({'detail': 'User assigned as manager'}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsManager])
def remove_manager(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    manager_group = Group.objects.get(name='manager')
    user.groups.remove(manager_group)
    return Response({'detail': 'User removed from manager group'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsManager])
def delivery_crew_list(request):
    delivery_crew = User.objects.filter(groups__name='delivery-crew')
    serializer = UserSerializer(delivery_crew, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsManager])
def assign_delivery_crew(request):
    user_id = request.data.get('user_id')
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    delivery_crew_group = Group.objects.get(name='delivery-crew')
    user.groups.add(delivery_crew_group)
    return Response({'detail': 'User assigned as delivery crew'}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsManager])
def remove_delivery_crew(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    delivery_crew_group = Group.objects.get(name='delivery-crew')
    user.groups.remove(delivery_crew_group)
    return Response({'detail': 'User removed from delivery crew group'}, status=status.HTTP_200_OK)

# Cart Management Endpoints
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def cart_list(request):
    cart_items = Cart.objects.filter(user=request.user)
    serializer = CartSerializer(cart_items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_to_cart(request):
    serializer = CartSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def clear_cart(request):
    Cart.objects.filter(user=request.user).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Order Management Endpoints
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def order_list(request):
    if request.user.groups.filter(name='manager').exists():
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        return Response({'detail': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        order = serializer.save(user=request.user)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price
            )
        cart_items.delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.user.groups.filter(name='manager').exists() or order.user == request.user:
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsManager])
def update_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderSerializer(order, data=request.data, partial=True)
    if serializer.is_valid():
        order = serializer.save()
        if 'delivery_crew' in request.data:
            order.delivery_crew = User.objects.get(pk=request.data['delivery_crew'])
        if 'status' in request.data:
            order.status = request.data['status']
        order.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsManager])
def delete_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    order.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsDeliveryCrew])
def delivery_crew_orders(request):
    orders = Order.objects.filter(delivery_crew=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsDeliveryCrew])
def update_order_status(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if order.delivery_crew != request.user:
        return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

    status = request.data.get('status')
    if status in [0, 1]:
        order.status = status
        order.save()
        return Response(OrderSerializer(order).data)
    return Response({'detail': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
