from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(CustomerDetails)
class CustomerDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email', 'phone_number', 'address', 'created_at')
    search_fields = ('user__username', 'email')
    list_filter = ('created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    


@admin.register(Documents)
class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'document')
    
@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'name', 'location')
    search_fields = ('name', 'location')
    list_filter = ('created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer')