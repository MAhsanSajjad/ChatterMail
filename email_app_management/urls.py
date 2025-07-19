from django.urls import path
from . import views
urlpatterns = [
    path("CreateCustomer/", views.CustomerCreateAPIView.as_view(), name="create_customer"),
    path('Login/', views.LoginAPIView.as_view(), name='login'),
    path('SendEmail/', views.SendDocumentToCustomerAPIView.as_view(), name='send_email_to_customer'),
    path('ImportantDocuments/', views.ImportantDocument.as_view(), name='important_documents'),
    path('UniversityDetails/', views.UniversityAPIView.as_view(), name='university_details'),
    path('CreateTeacher/', views.CreateTeacherAPIView.as_view()),
    path('TeacherList/', views.TeacherListAPIView.as_view()),
    path('TeacherList/<int:id>/', views.TeacherListAPIView.as_view()),
    # path('CreateC/', views.CustomersAPIView.as_view),
    path('public-create-customer/', views.PublicCustomerCreateAPIView.as_view()),
    path('items/', views.ItemsAPIView.as_view()),
    path('orders/', views.OrderAPIView.as_view()),
    path('payment/', views.CreatePaymentAPIView.as_view()),
    path('check-payment-status/', views.CheckPaymentStatusAPIView.as_view()),
    path('salary/<int:id>/', views.EmployeeSalaryAPIView.as_view())




    
]