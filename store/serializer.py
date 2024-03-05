from rest_framework import serializers
from .models import Customer, Product, Review, Order


class Customer_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'full_name', 'email', 'phone']

    full_name = serializers.CharField(max_length=255, required=False)

    def create(self, validated_data):
        full_name = validated_data.pop('full_name', None)

        if full_name is None:
            raise serializers.ValidationError(
                "Full name is required to create you account")

        customer_name = full_name.split()

        if len(customer_name) >= 2:
            validated_data['first_name'] = customer_name[0]
            validated_data['last_name'] = ''.join(customer_name[1:])
        else:
            validated_data['first_name'] = customer_name[0]
            validated_data['last_name'] = ''

        return super().create(validated_data)

    def update(self, instance, validated_data):
        full_name = validated_data.pop('full_name', None)

        if full_name is None:
            raise serializers.ValidationError("Full name can not be empty")

        customer_name = full_name.split()
        instance.first_name = customer_name[0]
        instance.last_name = ''.join(customer_name[1:])
        return super().update(instance, validated_data)

    #  product serializer


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'unit_price',
                  'inventory', 'collection']


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'placed_at', 'payment_status', 'customer']
