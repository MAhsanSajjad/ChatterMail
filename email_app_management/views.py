from django.shortcuts import render
from django.http import HttpResponse
from email_app_management.models import *
from email_app_management.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework.generics import ListAPIView
from .pagination import StandardResultSetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail

# Create your views here.

class CustomerCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Allow any user to access this view

    def post(self, request):
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')

        if not email or not phone_number:
            return Response({
                'success': False,
                'response': {'message': 'Email and phone number are required.'}
            }, status=status.HTTP_400_BAD_REQUEST)

        if CustomerDetails.objects.filter(email=email).exists():
            return Response({
                'success': False,
                'response': {'message': 'Email already exists.'}
            }, status=status.HTTP_400_BAD_REQUEST)

        if CustomerDetails.objects.filter(phone_number=phone_number).exists():
            return Response({
                'success': False,
                'response': {'message': 'Phone number already exists.'}
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomerDetailSerializer(data=request.data)
        if serializer.is_valid():
            # Manually inject user into serializer's validated_data
            serializer.save(user=request.user)
            return Response({
                'success': True,
                'response': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'success': False,
            'response': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({
                'success': False,
                'response': {'message': 'Username and password are required.'}
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'success': True,
                'response': {
                    'token': token.key,
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'response': {'message': 'Invalid username or password.'}
            }, status=status.HTTP_401_UNAUTHORIZED)




import threading
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# Email sending logic (runs in thread)
def send_document_email(to_email, subject, body, document_path, document_name):
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=[to_email],
    )
    if document_path:
        email.attach_file(document_path)  # Removed filename and mimetype
    email.send()


class SendDocumentToCustomerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        customer_id = request.data.get("customer_id")
        document_id = request.data.get("document_id")

        if not customer_id or not document_id:
            return Response({
                "success": False,
                "response": {"message": "Customer ID and Document ID are required."}
            }, status=status.HTTP_400_BAD_REQUEST)

        customer = CustomerDetails.objects.filter(id=customer_id).first()
        if not customer:
            return Response({
                "success": False,
                "response": {"message": "Customer not found."}
            }, status=status.HTTP_404_NOT_FOUND)

        document = Documents.objects.filter(id=document_id, customer=customer).first()
        if not document:
            return Response({
                "success": False,
                "response": {"message": "Document not found for this customer."}
            }, status=status.HTTP_404_NOT_FOUND)

        subject = "Your Requested Document"
        message = f"Hello {customer.user.username},\n\nPlease find the attached document."

        # Send email in background
        threading.Thread(
            target=send_document_email,
            args=(customer.email, subject, message, document.document.path, document.document.name)
        ).start()

        return Response({
            "success": True,
            "response": {"message": f"Document is being sent to {customer.email}."}
        }, status=status.HTTP_200_OK)




class ImportantDocument(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        document = request.FILES.get('document')

        if not document:
            return Response({
                'success': False,
                'response': {'message': 'Document is required.'}
            }, status=status.HTTP_400_BAD_REQUEST)

        customer = CustomerDetails.objects.filter(user=request.user).first()
        if not customer:
            return Response({
                'success': False,
                'response': {'message': 'Customer profile not found.'}
            }, status=status.HTTP_404_NOT_FOUND)

        Documents.objects.create(customer=customer, document=document)

        return Response({
            'success': True,
            'response': {'message': 'Document uploaded successfully.'}
        }, status=status.HTTP_201_CREATED)
        
        
        
        
class UniversityAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get('name')
        location = request.data.get('location')

        if not name:
            return Response({
                'success': False,
                'response': {'message': 'University name is required.'}
            }, status=status.HTTP_400_BAD_REQUEST)

        customer = CustomerDetails.objects.filter(user=request.user).first()
        if not customer:
            return Response({
                'success': False,
                'response': {'message': 'Customer profile not found.'}
            }, status=status.HTTP_404_NOT_FOUND)

        university, created = University.objects.get_or_create(customer=customer, defaults={'name': name, 'location': location})

        if not created:
            return Response({
                'success': False,
                'response': {'message': 'University already exists for this customer.'}
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'success': True,
            'response': {'message': 'University created successfully.', 'university_id': university.id}
        }, status=status.HTTP_201_CREATED)
        
        
class CreateTeacherAPIView(APIView):
    def post(self, request):
        name = request.data.get('name')
        department = request.data.get('department')
        designation = request.data.get('designation')

        if not name or not department or not designation:
            return Response(
                {
                    "success": False,
                    "response": {
                        "message": "All fields are required!"
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )



        serializer = TeacherInfoSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    {
                        "success": True,
                        "response": serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {
                        "success": False,
                        "response": {
                            "message": str(e)
                        }
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            {
                "success": False,
                "response": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class TeacherListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = TeacherInfoListSerializer
    pagination_class = StandardResultSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']
    filterset_fields = ['name']

    def get(self, request, *args, **kwargs):
        teacher_id = self.kwargs.get('id')
        if teacher_id:
            teacher = TeacherInfo.objects.filter(id=teacher_id).first()
            if not teacher:
                return Response({"success": False, "message": "Teacher not found"}, status=404)
            serializer = self.get_serializer(teacher)
            return Response({"success": True, "data": serializer.data}, status=200)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return TeacherInfo.objects.all()
    

class PublicCustomerCreateAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny] 

    def post(self, request):
        name = request.data.get('name')
        phone_number = request.data.get('phone_number')
        address = request.data.get('address')
        username = request.data.get('username')
        password = request.data.get('password')

        # Validate required fields
        if not name or not phone_number:
            return Response({
                'success': False,
                'response': {'message': 'name and phone_number are required!'}
            }, status=400)

        if not username or not password:
            return Response({
                'success': False,
                'response': {'message': 'username and password are required!'}
            }, status=400)

        # Check for duplicate username
        if User.objects.filter(username=username).exists():
            return Response({
                'success': False,
                'response': {'message': 'Username already exists!'}
            }, status=400)

        # Create user
        user = User.objects.create_user(username=username, password=password)
        wallet, created = Wallet.objects.get_or_create(user=user)

        # Create customer linked to user
        customer = Customer.objects.create(
            user=user,
            name=name,
            phone_number=phone_number,
            address=address
        )

        serializer = CustomerSerializer(customer)
        return Response({'success': True, 'response': serializer.data}, status=201)
    
    
    
class ItemsAPIView(APIView):
    def post(self, request):
        items = Items.objects.create(
            item_name = request.data.get('item_name'),
            item_description = request.data.get('item_description'),
            item_price = request.data.get('item_price')
            
        )
        serializer = ItemsSerializer(items)
        return Response({
            'success': True,
            'response': serializer.data
        }, status=status.HTTP_201_CREATED)
        
        
class OrderAPIView(APIView):
    def post(self, request):
        customer_id = request.data.get('customer_id')
        item_ids = request.data.get('item_ids', [])

        if not customer_id or not item_ids:
            return Response({
                'success': False,
                'response': {'message': 'Customer ID and item IDs are required.'}
            }, status=status.HTTP_400_BAD_REQUEST)

        customer = Customer.objects.filter(id=customer_id).first()
        if not customer:
            return Response({
                'success': False,
                'response': {'message': 'Customer not found.'}
            }, status=status.HTTP_404_NOT_FOUND)

        items = Items.objects.filter(id__in=item_ids)
        if not items.exists():
            return Response({
                'success': False,
                'response': {'message': 'No valid items found.'}
            }, status=status.HTTP_404_NOT_FOUND)

        order = Order.objects.create(customer=customer)
        order.items.set(items)  # Set ManyToMany field
        order.save()

        serializer = OrderSerializer(order)
        return Response({
            'success': True,
            'response': serializer.data
        }, status=status.HTTP_201_CREATED)
        
        


class CreatePaymentAPIView(APIView):
    def post(self, request):
        customer_id = request.data.get('customer_id')
        order_id = request.data.get('order_id')

        if not customer_id or not order_id:
            return Response({
                "success": False,
                "message": "customer_id and order_id are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        customer = Customer.objects.filter(id=customer_id).first()
        if not customer:
            return Response({
                "success": False,
                "message": "Customer not found."
            }, status=status.HTTP_404_NOT_FOUND)

        order = Order.objects.filter(id=order_id, customer=customer).first()
        if not order:
            return Response({
                "success": False,
                "message": "Order not found for this customer."
            }, status=status.HTTP_404_NOT_FOUND)

        if order.payment_type == 'paid':
            return Response({
                "success": False,
                "message": "Payment already completed for this order."
            }, status=status.HTTP_400_BAD_REQUEST)

        if order.total_amount is None:
            return Response({
                "success": False,
                "message": "Order has no total amount yet."
            }, status=status.HTTP_400_BAD_REQUEST)

        wallet = Wallet.objects.filter(user=customer.user).first()
        if not wallet:
            return Response({
                "success": False,
                "message": "Wallet not found for this customer."
            }, status=status.HTTP_404_NOT_FOUND)

        if wallet.balance < order.total_amount:
            return Response({
                "success": False,
                "message": "Insufficient wallet balance."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Deduct the amount
        wallet.balance -= order.total_amount
        wallet.save()

        # Mark the order as paid
        order.payment_type = 'paid'
        order.save(update_fields=['payment_type'])

        # Create the payment record
        payment = Payment.objects.create(customer=customer, order=order)

        # ✅ Create the payment history record
        PaymentHistory.objects.create(
            customer=customer,
            order=order,
            amount=order.total_amount
        )

        return Response({
            "success": True,
            "message": f"Payment successful. Amount {order.total_amount} deducted from wallet.",
            "wallet_balance": wallet.balance
        }, status=status.HTTP_201_CREATED)





class CheckPaymentStatusAPIView(APIView):
    def post(self, request):
        customer_id = request.data.get('customer_id')
        order_id = request.data.get('order_id')

        if not customer_id or not order_id:
            return Response({
                'success': False,
                'message': 'customer_id and order_id are required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        customer = Customer.objects.filter(id=customer_id).first()
        if not customer:
            return Response({
                'success': False,
                'message': 'Customer not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        order = Order.objects.filter(id=order_id, customer=customer).first()
        if not order:
            return Response({
                'success': False,
                'message': 'Order not found for this customer.'
            }, status=status.HTTP_404_NOT_FOUND)

        # ✅ Option 1: Check Payment record
        payment_exists = Payment.objects.filter(customer=customer, order=order).exists()

        # ✅ Option 2: You can also check order.payment_type == 'paid'

        return Response({
            'success': True,
            'paid': payment_exists,
            'payment_type': order.payment_type,
            'total_amount': order.total_amount
        }, status=status.HTTP_200_OK)
        
        
        
class EmployeeSalaryAPIView(APIView):
    def post(self, request, id):
        salary = request.data.get('salary')

        if salary is None:
            return Response({
                'success': False,
                'response': {'message': 'Salary is required!'}
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            salary = float(salary)
        except ValueError:
            return Response({
                'success': False,
                'response': {'message': 'Invalid salary format!'}
            }, status=status.HTTP_400_BAD_REQUEST)

        employee = Employee.objects.filter(id=id).first()
        if not employee:
            return Response({
                'success': False,
                'response': {'message': 'Employee not found!'}
            }, status=status.HTTP_404_NOT_FOUND)

        EmployeeSalary.objects.create(employee=employee, salary=salary)

        return Response({
            'success': True,
            'response': {'message': 'Salary added successfully.'}
        }, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        salary = EmployeeSalary.objects.filter(id=id).first()
        salary.delete()
        return Response({'success':True, 'response': {'message': 'salary deleted successfully!'}}, status=status.HTTP_200_OK)
    
    
    
class EmployeeAPIView(APIView):
    def post(self, request):
        name = request.data.get('name')
        if name is None:
            return Response({'success': False, 'response': {'message': 'Name is required!'}}, status=status.HTTP_400_BAD_REQUEST)
        if Employee.objects.filter(name=name).exists():
            return Response({'suceess':False, 'response': {'message': 'This name is already taken!'}}, status=status.HTTP_400_BAD_REQUEST)
        # Create serializer instance with data
        serializer = EmployeeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()  # This creates and saves the Employee object
            return Response({'success': True, 'response': {'message': 'Employee created successfully!'}}, status=status.HTTP_201_CREATED)
        else:
            return Response({'success': False, 'response': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class EmployeeUpdateAPIView(APIView):
    def patch(self, request, id):
        employee = Employee.objects.filter(id=id).filter()
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':True, 'response': {'message': 'Employee data updated Successfully!'}}, status=status.HTTP_200_OK)
        else:
            return Response({'success':False, 'response': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
