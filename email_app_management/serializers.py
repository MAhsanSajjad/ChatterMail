from rest_framework import serializers
from email_app_management.models import *
from django.contrib.auth.models import User

class CustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetails
        fields = ['id', 'email', 'phone_number', 'address', 'created_at']
        
        
        
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetails
        fields = ['id', 'document', 'created_at']
        


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetails
        fields = ['id', 'name', 'location', 'created_at']
        
        
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']
        
class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ['id', 'name']
        
class TeacherInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeacherInfo
        fields = ['id', 'name', 'department', 'designation']

  
class TeacherInfoListSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()
    designation = serializers.SerializerMethodField()

    class Meta:
        model = TeacherInfo
        fields = ['id', 'name', 'department', 'designation', 'designation']
        
    def get_department(self, instance):
        return instance.department.name if instance.department else None
    
    def get_designation(self, instance):
        return instance.designation.name if instance.designation else None
    
    
# class CustomerSerializer(serializers.ModelSerializer):
#     email = serializers.SerializerMethodField()

#     class Meta:
#         model = Customer
#         fields = ['id', 'name', 'email', 'phone_number', 'address']

#     def get_email(self, obj):
#         return obj.user.email if obj.user else None


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ['id', 'item_name', 'item_description', 'item_price']
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'items', 'total_amount', 'order_date']
        
        
        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone_number', 'address']


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'designation']