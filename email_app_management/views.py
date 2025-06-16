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