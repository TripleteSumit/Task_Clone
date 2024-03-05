from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .models import Customer, Order, Product, OrderItem, Review
from django.db.models import Value
from django.db.models.functions import Concat
from .serializer import Customer_Serializer, ProductSerializer, ReviewSerializer, OrderSerializer

# the below implmentation is function bases views but django provies class based views. Let's do that.

'''
@api_view(['GET', 'POST'])
def customer_list(request):
    if request.method == 'GET':
        queryset = Customer.objects.annotate(full_name=Concat(
            'first_name', Value(' '), 'last_name')).all().order_by('id')
        serializer = Customer_Serializer(queryset, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = Customer_Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def customer_details(request, id):
    customer = Customer.objects.annotate(full_name=Concat(
        'first_name', Value(' '), 'last_name')).get(pk=id)
    if request.method == 'GET':
        serializer = Customer_Serializer(customer)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = Customer_Serializer(customer, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(request.data)
    elif request.method == 'DELETE':
        if customer.order_set.count() > 0:
            return response.Response({'error': 'customer can not be deleted because customer has some orders and it is associated with orders table'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        customer.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
'''

# class based views
#  import a APIViews class from package rest_framework.views

'''
class CustomerList(APIView):
    def get(self, request):
        queryset = Customer.objects.annotate(full_name=Concat(
            'first_name', Value(' '), 'last_name')).all().order_by('id')
        serializer = Customer_Serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        deseializer = Customer_Serializer(data=request.data)
        deseializer.is_valid(raise_exception=True)
        deseializer.save()
        return Response(deseializer.data, status=status.HTTP_201_CREATED)


class CustomerDetails(APIView):
    def get(self, request, id):
        customer = Customer.objects.annotate(full_name=Concat(
            'first_name', Value(' '), 'last_name')).get(pk=id)
        serializer = Customer_Serializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        customer = Customer.objects.annotate(full_name=Concat(
            'first_name', Value(' '), 'last_name')).get(pk=id)
        serializer = Customer_Serializer(customer, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        customer = Customer.objects.annotate(full_name=Concat(
            'first_name', Value(' '), 'last_name')).get(pk=id)
        if customer.order_set.count() > 0:
            return Response({'error': 'customer can not be deleted because customer has some orders and it is associated with orders table'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''

# class based generic view which allows us to write less code becuse the code that we write is very repetative in nature. so django provide us for better approch

'''
class CustomerList(ListCreateAPIView):
    queryset = Customer.objects.annotate(full_name=Concat(
        'first_name', Value(' '), 'last_name')).all().order_by('id')
    serializer_class = Customer_Serializer


class CustomerDetails(RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.annotate(full_name=Concat(
        'first_name', Value(' '), 'last_name')).all()
    serializer_class = Customer_Serializer

    def delete(self, request, pk):
        customer = Customer.objects.annotate(full_name=Concat(
            'first_name', Value(' '), 'last_name')).get(pk=pk)
        if customer.order_set.count() > 0:
            return Response({'error': 'customer can not be deleted because customer has some orders and it is associated with orders table'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''

# ViewSet in Django
# as most of our code in repetative in nature look the above two function customer list and customer Details
# most of the code is same with few differences
# in this scenario viewset comes into the pictures it combines both the code in a single class let's look

# RetrieveUpdateDestroyAPIView()


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.annotate(full_name=Concat(
        'first_name', Value(' '), 'last_name')).all().order_by('id')
    serializer_class = Customer_Serializer

    def destroy(self, request, *args, **kwargs):
        if Order.objects.filter(customer_id=kwargs['pk']).count() > 0:
            return Response({'error': 'customer can not be deleted because customer has some orders and it is associated with orders table'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    # def delete(self, request, pk):
    #     customer = Customer.objects.annotate(full_name=Concat(
    #         'first_name', Value(' '), 'last_name')).get(pk=pk)
    #     customer.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# by applying the above implementation our application is broken because we don't have any CustomerList or CustomerDetails class. We have only one class that is CustomerViewSet. For that reason we have to register this class in a router


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer

    def destroy(self, request, *args, **kwargs):

        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'product is associated with orderitem.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # if you want to set a customer filter filed then you have to create a class which inherites for filterset class. you can serch on google and learn form that.
    filterset_fields = ['customer_id', 'payment_status']
    search_fields = ['placed_at']
    ordering_fields = ['customer']
    pagination_class = PageNumberPagination

    # def get_queryset(self):
    #     queryset = Order.objects.all()
    #     customer_id = self.request.query_params.get('customer_id')
    #     if customer_id is not None:
    #         queryset = queryset.filter(customer_id=customer_id)

    # return queryset








class FilterSet(ModelViewSet):
    pass 
