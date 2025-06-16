from rest_framework import serializers
from email_app_management.models import CustomerDetails
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
        