from django.db.models import fields
from rest_framework import serializers
from .models import BatchStatus, Customer, CustomerOrder, CustomerOrderContents, CustomerOrderStatus, Product, Batch, Stock, Supplier, SupplierProduct
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('productID', 'name','stockAmount','pendingStock')

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('first_name','last_name','email', 'phone', 'shipping_address')

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ('batchID', 'product', 'dateReceived', 'expiryDate','quantity','status')

class BatchStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchStatus
        fields = ('batchStatusID','status')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerOrder
        fields = ('customerOrderID', 'customerID','customerOrderStatus','dateCreated','lastUpdated')

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerOrderStatus
        fields = ('updateID', 'updateType')

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ('stockID', 'productID', 'customerID','amount')

class OrderContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerOrderContents
        fields = ('customerOrderContentsID', 'customerOrderID','supplierID','product','quantity')

class SupplierProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierProduct
        fields = ('supplierProductID' ,'supplierID','product','price','currentStock')

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('name','address', 'phone')

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    customer = CustomerSerializer(required = False)
    supplier = SupplierSerializer(required = False)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name','customer','supplier')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        print (validated_data)
        try:
            customer = validated_data.pop('customer')
        except KeyError as e:
            customer = None
        try:
            supplier = validated_data.pop('supplier')
        except KeyError as e:
            supplier = None
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        if customer != None:
            customer = Customer.objects.create(
                user = user,
                first_name = validated_data['first_name'],
                email = validated_data['email'],
                last_name = validated_data['last_name'],
                phone = customer['phone'],
                shipping_address = customer['shipping_address']
            )
            customer.save()
        else:
            supplier = Supplier.objects.create(
                supplierID = user,
                name = supplier['name'],
                address = supplier['address'],
                phone = supplier['phone']
            )
            supplier.save()
        user.save()
        return user