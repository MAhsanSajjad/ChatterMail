from django.urls import path
from . import views
urlpatterns = [
    path("CreateCustomer/", views.CustomerCreateAPIView.as_view(), name="create_customer"),
    path('Login/', views.LoginAPIView.as_view(), name='login'),
    path('SendEmail/', views.SendDocumentToCustomerAPIView.as_view(), name='send_email_to_customer'),
    path('ImportantDocuments/', views.ImportantDocument.as_view(), name='important_documents'),
    path('UniversityDetails/', views.UniversityAPIView.as_view(), name='university_details'),
    
]