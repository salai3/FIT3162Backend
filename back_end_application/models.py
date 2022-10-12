from pyexpat import model
from tkinter import CASCADE
from django.db import models
import phone_field.models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class Product (models.Model):
    productID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=False, default='')
    stockAmount = models.IntegerField(default=0)
    pendingStock = models.IntegerField(default=0)
    def __str__(self) -> str:
        return "%s %s" % (self.productID ,self.name,self.stockAmount,self.pendingStock)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    first_name = models.CharField(max_length=100, blank=False, default='')
    last_name = models.CharField(max_length=100, blank=False, default='')
    email = models.EmailField(('email address'), unique=True)
    phone = models.IntegerField(default=0)
    shipping_address = models.CharField(max_length=300, blank=False, default='')

    def __str__(self) -> str:
        return "%s %s" % (self.user,self.first_name, self.last_name, self.email, self.phone, self.shipping_address)

class Stock (models.Model):
    stockID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    productID = models.ForeignKey(Product,on_delete=models.CASCADE)
    customerID = models.ForeignKey(Customer,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=5)
    def __str__(self) -> str:
        return "%s %s" % (self.stockID ,self.productID, self.customerID, self.amount)

class CustomerOrderStatus (models.Model):
    updateID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    updateType = models.CharField(max_length=512)
    
class CustomerOrder(models.Model):
    customerOrderID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customerID = models.ForeignKey(Customer,on_delete=models.CASCADE)
    customerOrderStatus = models.ForeignKey(CustomerOrderStatus,on_delete=models.CASCADE)
    dateCreated = models.DateTimeField()
    lastUpdated = models.DateTimeField()

    @property
    def date_diff(self):
        return (self.lastUpdated - self.dateCreated).days

    def __str__(self) -> str:
        return "%s %s" % (self.customerOrderID, self.customerID, self.customerOrderStatus, self.dateCreated, self.lastUpdated)

class BatchStatus (models.Model):
    batchStatusID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=100, blank=False, default='')

class Batch (models.Model):
    batchID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    dateReceived = models.DateTimeField()
    expiryDate = models.DateTimeField()
    quantity = models.IntegerField()
    status = models.ForeignKey(BatchStatus,on_delete=models.CASCADE)

#Supplier table start
class Supplier (models.Model):
    supplierID = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    name = models.CharField(max_length=100, blank=False)
    address = models.CharField(max_length=200)
    phone = models.IntegerField(default=0)

class CustomerOrderContents (models.Model):
    customerOrderContentsID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customerOrderID = models.ForeignKey(CustomerOrder,on_delete=models.CASCADE)
    supplierID = models.ForeignKey(Supplier,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return "%s %s" % (self.customerOrderContentsID,self.customerOrderID, self.supplierID, self.product, self.quantity)

class SupplierProduct (models.Model):
    supplierProductID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    supplierID = models.ForeignKey(Supplier,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=5)
    currentStock = models.IntegerField(default=0)

# First run at these tables, untested.
class SupplyOrder (models.Model):
    supplyOrderID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    supplierID = models.ForeignKey(Supplier,on_delete=models.CASCADE)
    invoiceNumber = models.CharField(max_length=12, blank=False, default='000000000000')
    date = models.DateTimeField()

class SupplyOrderStatus (models.Model):
    UPDATE_CHOICES = [
        ('DLY', 'Delayed'),
        ('DVD', 'Delivered'),
        ('SNT', 'Sent'),
        ('CNC', 'Cancelled'),
        ('OTH', 'Other'),
    ]
    updateID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    supplyOrderID = models.ForeignKey(SupplyOrder,on_delete=models.CASCADE)
    updateType = models.CharField(max_length=512, choices=UPDATE_CHOICES)
    updateContents = models.CharField(max_length=512)






    



