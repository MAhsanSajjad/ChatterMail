from django.db import models
from django.contrib.auth.models import User
from utils_app.models import BaseModelWithCreatedInfo
from email_app_management.constants import *
# Create your models here.


class CustomerDetails(BaseModelWithCreatedInfo):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}"




class Documents(BaseModelWithCreatedInfo):
    customer = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents/')
    
    def __str__(self):
        return f"Document for {self.customer.user.username}"
    
    
    
class University(BaseModelWithCreatedInfo):
    customer = models.OneToOneField(CustomerDetails, on_delete=models.CASCADE, unique=True)
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
    
    
class TeacherInfo(BaseModelWithCreatedInfo):
    name = models.CharField(max_length=255, null=True, blank=True)
    department = models.ForeignKey('email_app_management.Department', on_delete=models.CASCADE, null=True, blank=True)
    designation = models.ForeignKey('email_app_management.Designation', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    
class Department(BaseModelWithCreatedInfo):
    name = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.name
class Designation(BaseModelWithCreatedInfo):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class Companyname(BaseModelWithCreatedInfo):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
class Customer(BaseModelWithCreatedInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Companyname, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Items(BaseModelWithCreatedInfo):
    item_name = models.CharField(max_length=255, null=True, blank=True)
    item_description = models.TextField(null=True, blank=True)
    item_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.item_name

from decimal import Decimal

class Order(BaseModelWithCreatedInfo):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    items = models.ManyToManyField(Items, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=255, choices=PAYMENT_CHOICES)

    def __str__(self):
        return f"Order {self.id} for {self.customer.name if self.customer else 'Unknown Customer'}"
    

    def save(self, *args, **kwargs):
        # Initial save to generate ID (required for ManyToMany to work)
        is_new = self._state.adding
        super().save(*args, **kwargs)

        if is_new:
            return  # Skip total calculation until items are set

        # Calculate total based on item_price
        total = Decimal('0.00')
        for item in self.items.all():
            total += item.item_price or Decimal('0.00')

        self.total_amount = total

        # Save total amount only if it changed
        super().save(update_fields=['total_amount'])
    
    
class Wallet(BaseModelWithCreatedInfo):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    
class Payment(BaseModelWithCreatedInfo):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.customer.name} order for {self.order.total_amount}"
    
    
class PaymentHistory(BaseModelWithCreatedInfo):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment of {self.amount} for {self.order.id} by {self.customer.name}"
    
    
    
class Employee(BaseModelWithCreatedInfo):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=100, choices=DESIGNATION_CHOICES, default='staff')
    def __str__(self):
        return self.name
    
class EmployeeAttendace(BaseModelWithCreatedInfo):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=ATTENDANCE_CHOICES, default='present')

    def __str__(self):
        return f"{self.employee.name} - {self.date} - {self.status}"
    
class EmployeeSalary(BaseModelWithCreatedInfo):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True)
    salary = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    
    def __str__(self):
        return self.employee.name