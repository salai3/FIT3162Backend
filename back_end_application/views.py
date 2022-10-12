import re
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Batch, BatchStatus, Customer, CustomerOrder, CustomerOrderContents, CustomerOrderStatus, Product, Supplier, SupplierProduct, Stock
from .serializers import BatchStatusSerializer, OrderSerializer, OrderStatusSerializer, ProductSerializer, BatchSerializer, OrderContentSerializer, StockSerializer, SupplierProductSerializer
from rest_framework import serializers, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import time
from uuid import UUID
# Create your views here.

def home (request):
    return HttpResponse("Test")
  
@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_product': '/',
        'Search by ID': '/?product=product_id',
        'Add': '/create',
        'Update': '/update/pk'
    }
  
    return Response(api_urls)

# View methods for products
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_products(request):
    product = ProductSerializer(data=request.data)
  
    # validating for already existing data
    if Product.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
  
    if product.is_valid():
        product.save()
        return Response(product.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_low_on_stock(request):
    # checking for the parameters from the URL
    stock = Product.objects.all().order_by('stockAmount')[:5]

    # if there is something in items else raise error
    if stock:
        return JsonResponse(data=list(stock.values()), safe=False)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_stock(request):
    stock = StockSerializer(data=request.data)
    # validating for already existing data
    if Stock.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
    if stock.is_valid():
        stock.save()
        return Response(stock.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_stock(request):
    # checking for the parameters from the URL
    cust = request.data["customerID"]
    if request.query_params:
        stock = Stock.objects.filter(customerID = cust)
    else:
        stock = Stock.objects.all()
  
    # if there is something in items else raise error
    if stock:
        return JsonResponse(data=list(stock.values()), safe=False)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_stock (request):
    amount = request.data["update_amount"]
    cust = request.data["customer"]
    product = request.data["product"]
    stock = Stock.objects.get(customerID = cust, productID = product)
    stock.amount += amount
    stock.save()
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_products(request):
    
    # checking for the parameters from the URL
    if request.query_params:
        prod_id = request.query_params.get('productID')
        products = Product.objects.filter(productID = prod_id)
    else:
        products = Product.objects.all()
  
    # if there is something in items else raise error
    if products:
        return JsonResponse(data=list(products.values()), safe=False)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_products(request):
    prodID = request.data["productID"]
    product = Product.objects.get(productID = prodID)
    try:
        name = request.data["name"]    
    except KeyError as e:
        name = None
    try:
        size = request.data["size"]    
    except KeyError as e:
        size = None
    try:
        price = request.data["price"]    
    except KeyError as e:
        price = None
    try:
        currentStock = request.data["currentStock"]    
    except KeyError as e:
        currentStock = None

    if name != None:
        product.name = name
    
    if size != None:
        product.size = size
    
    if price != None:
        product.price = price

    if currentStock != None:
        product.currentStock = currentStock
    
    product.save()

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_product(request):
    try:
        prodID = request.data["productID"]    
    except KeyError as e:
        prodID = None
    # checking for the parameters from the URL
    if prodID != None:
        try:
            product_to_delete = Product.objects.get(productID = prodID)
            product_to_delete.delete()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_200_OK)

# View Methods for Batch
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_batch(request):
    batch = BatchSerializer(data=request.data)

    # validating for already existing data
    if Batch.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
  
    if batch.is_valid():
        batch.save()
        return Response(batch.data)
    else:
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_batch(request):
    
    # checking for the parameters from the URL
    if request.query_params:
        batch = Batch.objects.filter(**request.query_param.dict())
    else:
        batch = Batch.objects.all()
  
    # if there is something in items else raise error
    if batch:
        return JsonResponse(data=list(batch.values()), safe=False)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_batch(request):
    batID = request.data["batchID"]
    batch = Batch.objects.get(batchID = batID)
    try:
        product = request.data["product"]    
    except KeyError as e:
        product = None
    try:
        dateReceived = request.data["dateReceived"]    
    except KeyError as e:
        dateReceived = None
    try:
        expiryDate = request.data["expiryDate"]    
    except KeyError as e:
        expiryDate = None
    try:
        quantity = request.data["quantity"]    
    except KeyError as e:
        quantity = None
    try:
        stat = request.data["status"]    
    except KeyError as e:
        stat = None
    if product != None:
        batch.product = product
    
    if dateReceived != None:
        batch.dateReceived = dateReceived
    
    if expiryDate != None:
        batch.expiryDate = expiryDate

    if quantity != None:
        batch.quantity = quantity

    if stat != None:
        batch.status = stat
    
    batch.save()

    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_batch(request):
    try:
        batID = request.data["batchID"]    
    except KeyError as e:
        batID = None
    # checking for the parameters from the URL
    if batID != None:
        try:
            batch_to_delete = Batch.objects.get(batchID = batID)
            batch_to_delete.delete()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_200_OK)

# View methods for Batch Status
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_batch_status(request):
    batch = BatchStatusSerializer(data=request.data)
    # validating for already existing data
    if BatchStatus.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
  
    if batch.is_valid():
        batch.save()
        return Response(batch.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_batch_status(request):
    # checking for the parameters from the URL
    if request.query_params:
        batch = BatchStatus.objects.filter(**request.query_param.dict())
    else:
        batch = BatchStatus.objects.all()
  
    # if there is something in items else raise error
    if batch:
        return JsonResponse(data=list(batch.values()), safe=False)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# View methods for Customer Order
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_order(request):
    order = OrderSerializer(data=request.data)
    exists = False
    # validating for already existing data
    if CustomerOrder.objects.filter(**request.data).exists():
        exists = True
    if exists == True:
        return Response(status=status.HTTP_200_OK,data="Data already exists")
  
    if order.is_valid():
        order.save()
        return Response(order.data)
    else:
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_order(request):
    try:
        custID = request.data["customerID"]    
    except KeyError as e:
        custID = None
    # checking for the parameters from the URL
    if custID != None:
        order = CustomerOrder.objects.filter(customerID = custID)
    else:
        order = CustomerOrder.objects.all()
  
    # if there is something in items else raise error
    if order:
        return JsonResponse(data=list(order.values()), safe=False)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_order(request):
    ordID = request.data["customerOrderID"]
    try:
        uuid_obj = UUID(ordID, version=4)
    except ValueError:
        return Response(status=status.HTTP_200_OK,data = request.data["date"] +"  ")
    order = CustomerOrder.objects.get(customerOrderID = ordID)
    try:
        customerID = request.data["customerID"]    
    except KeyError as e:
        customerID = None
    try:
        date = request.data["date"]    
    except KeyError as e:
        date = None
    if customerID != None:
        order.customerID = customerID
    
    if date != None:
        order.date = date
    order.save()
    return Response(status=status.HTTP_200_OK,data = "Order Successfully Updated")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_order(request):
    try:
        ordID = request.data["customerOrderID"]    
    except KeyError as e:
        ordID = None
    try:
        uuid_obj = UUID(ordID, version=4)
    except ValueError:
        return Response(status=status.HTTP_200_OK,data = "Order Does Not Exist. Please check your entered value.")
    # checking for the parameters from the URL
    if ordID != None:
        try:
            order_to_delete = CustomerOrder.objects.get(customerOrderID = ordID)
            order_to_delete.delete()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_200_OK)

#View method for Customer Order Contents
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_order_content(request):
    quantity = request.data["quantity"] 
    if quantity == 0:
        print (quantity)
        return Response(status=status.HTTP_200_OK,data = "Quantity cannot be 0")
    elif quantity < 0:
        return Response(status=status.HTTP_200_OK,data = "Quantity cannot be negative")
    else:
        pass
    order_content = OrderContentSerializer(data=request.data)
    # validating for already existing data
    if CustomerOrderContents.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
  
    if order_content.is_valid():
        order_content.save()
        return Response(order_content.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_order_content(request):
    try:
        orderID = request.data["orderID"]    
    except KeyError as e:
        orderID = None
    # checking for the parameters from the URL
    if orderID != None:
        order_content = CustomerOrderContents.objects.filter(customerOrderID = orderID)
    else:
        order_content = CustomerOrderContents.objects.all()
  
    # if there is something in items else raise error
    if order_content:
        return JsonResponse(data=list(order_content.values()), safe=False)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_order_content(request):
    ordContentID = request.data["customerOrderContentsID"]
    ordContent = CustomerOrderContents.objects.get(customerOrderContentsID = ordContentID)
    try:
        customerOrderID = request.data["customerOrderID"]    
    except KeyError as e:
        customerOrderID = None
    try:
        product = request.data["product"]    
    except KeyError as e:
        product = None
    try:
        quantity = request.data["quantity"] 
        if quantity == 0:
            return Response(status=status.HTTP_200_OK,data = "Quantity cannot be 0")
        elif quantity < 0:
            return Response(status=status.HTTP_200_OK,data = "Quantity cannot be negative")
        else:
            pass   
    except KeyError as e:
        quantity = None

    if customerOrderID != None:
        ordContent.customerOrderID = customerOrderID
    
    if product != None:
        ordContent.product = product

    if quantity != None:
        ordContent.quantity = quantity
    
    ordContent.save()
    return Response(status=status.HTTP_200_OK, data = "Order Content Successfully Updated")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_order_content(request):
    try:
        ordContentID = request.data["customerOrderContentsID"]    
    except KeyError as e:
        ordContentID = None
    # checking for the parameters from the URL
    if ordContentID != None:
        try:
            order_content_to_delete = CustomerOrderContents.objects.get(customerOrderContentsID = ordContentID)
            order_content_to_delete.delete()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_200_OK,data = "Order Content Successfully Deleted")

#View methods for custom user types
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_customers(request):
    # checking for the parameters from the URL
    if request.query_params:
        customer = Customer.objects.filter(**request.query_param.dict())
    else:
        customer = Customer.objects.all()

    # if there is something in items else raise error
    if customer:
        return JsonResponse(data=list(customer.values()), safe=False)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_suppliers(request):
    # checking for the parameters from the URL
    if request.query_params:
        supplier = Supplier.objects.filter(**request.query_param.dict())
    else:
        supplier = Supplier.objects.all()

    # if there is something in items else raise error
    if supplier:
        return JsonResponse(data=list(supplier.values()), safe=False)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

#View methods for supplier 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_supplier_product(request):
    supprod = SupplierProductSerializer(data=request.data)
    # validating for already existing data
    if SupplierProduct.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
  
    if supprod.is_valid():
        supprod.save()
        return Response(supprod.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_supplier_product_by_product(request,product_id):
    # checking for the parameters from the URL
    if product_id != None:
        supprod = SupplierProduct.objects.filter(product = product_id)
    else:
        supprod = SupplierProduct.objects.all()
    # if there is something in items else raise error
    if supprod:
        return JsonResponse(data=list(supprod.values()), safe=False)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_supplier_product_by_supplier(request,supplier_id):
    # checking for the parameters from the URL
    if supplier_id != None:
        supprod = SupplierProduct.objects.filter(supplierID = supplier_id)
    else:
        supprod = SupplierProduct.objects.all()
    # if there is something in items else raise error
    if supprod:
        return JsonResponse(data=list(supprod.values()), safe=False)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def calculate_eta_for_supplier(request,product_id):
    # checking for the parameters from the URL
    done = CustomerOrderStatus.objects.filter(updateType = "Completed").values('updateID')
    completedID = done[0].get('updateID')
    query = CustomerOrder.objects.filter(customerOrderStatus = completedID)
    temp = query.values_list('customerOrderID',flat=True)
    order_content_lst = CustomerOrderContents.objects.filter(customerOrderID__in = temp, product = product_id).values('customerOrderID','supplierID')
    result_list = [0 for _ in range(len(Supplier.objects.all())+7)]
    for i in range (len(order_content_lst)):
        order_id = order_content_lst[i].get('customerOrderID')
        supplier_id = order_content_lst[i].get('supplierID')
        days_taken = query.get(customerOrderID = order_id).date_diff
        if result_list[supplier_id] == 0:
            result_list[supplier_id] = ([supplier_id,product_id,days_taken,1])
        else:
            result_list[supplier_id] = ([supplier_id,product_id,(result_list[supplier_id][2] + days_taken/(result_list[supplier_id][3] + 1)),result_list[supplier_id][3] + 1])
    # if there is something in items else raise error
    if result_list:
        return JsonResponse(data=list(filter(lambda a: a != 0, result_list)), safe=False)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_order_status(request):
    order_content = CustomerOrderStatus.objects.all()
    # if there is something in items else raise error
    if order_content:
        return JsonResponse(data=list(order_content.values()), safe=False)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_order_status(request):
    ord_stat = OrderStatusSerializer(data=request.data)
    # validating for already existing data
    if CustomerOrderStatus.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
  
    if ord_stat.is_valid():
        ord_stat.save()
        return Response(ord_stat.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)