from .models import Cart,Product
from customer.models import Customer
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('full_name',)
    

class CartSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    product = ProductSerializer()
    class Meta:
        model = Cart
        fields = ['id', 'customer', 'product', 'quantity',]

