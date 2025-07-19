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
    
    
    
@admin.register(TeacherInfo)
class TeacherInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'department', 'designation')
    

@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    
    
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'phone_number', 'address')
    search_fields = ('user__username', 'name')
    list_filter = ('created_at',)

@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_name', 'item_description', 'item_price')
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_amount', 'order_date')
    
    
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'balance')
    
    
admin.site.register(Payment)


@admin.register(Companyname)
class CompanynameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('created_at',)


@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order', 'amount', 'created_at')
    
    
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'designation']
    
@admin.register(EmployeeAttendace)
class EmployeeAttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'status']
    
    
@admin.register(EmployeeSalary)
class EmployeeSalaryAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'salary']