from django.db import models
from django.contrib.auth.models import User
from utils_app.models import BaseModelWithCreatedInfo
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