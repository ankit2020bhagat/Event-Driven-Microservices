from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id', 'order_id', 'customer_name', 'customer_email', 'product_name', 'quantity', 'price', 'total_amount'
            , 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'order_id', 'total_amount', 'status', 'created_at', 'updated_at']
