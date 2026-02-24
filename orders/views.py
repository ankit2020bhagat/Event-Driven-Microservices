from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from yaml import serialize

from .models import Order
import logging

from orders.kafka_producer import OrderProducer
from orders.serializers import OrderSerializer

logger = logging.getLogger(__name__)


# Create your views here.
@api_view(['POSt'])
def create_order(request):
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        order = serializer.save()
        order_data = {
            'order_id': order.order_id,
            'customer_name': order.customer_name,
            'customer_email': order.customer_email,
            'product_name': order.product_name,
            'quantity': order.quantity,
            'price': order.price,
            'status': order.status
        }
        producer = OrderProducer
        kafka_success = producer.send_offer(order_data)
        producer.close()

        if kafka_success:
            return Response({
                'message': 'Order created successfully and send for processing',
                'order': serializer.data
            }, status=status.HTTP_201_CREATED)

        else:
            return Response({
                'message': 'Order created but failed to queue for processing',
                'order': serializer.data,
            }, status=status.HTTP_400_BAD_REQUEST)

    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
def get_order(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id)
        serialzer = OrderSerializer(order)
        return Response(serialzer.data)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders)

    return Response(serializer.errors)
