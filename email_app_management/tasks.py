from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from .models import *

@shared_task
def delete_old_payment_history():
    threshold = timezone.now() - timedelta(minutes=2)
    deleted_count, _ = PaymentHistory.objects.filter(created_at__lt=threshold).delete()
    return f"Deleted {deleted_count} old PaymentHistory records."





@shared_task
def send_unpaid_order_reminders():
    unpaid_orders = Order.objects.filter(payment_type='unpaid', customer__user__email__isnull=False)

    for order in unpaid_orders:
        customer = order.customer
        user_email = customer.user.email
        total = order.total_amount

        send_mail(
            subject='🧾 Payment Reminder for Your Order',
            message=(
                f"Dear {customer.name},\n\n"
                f"You have a pending payment of {total} for order #{order.id}.\n"
                f"Please complete your payment as soon as possible to avoid order cancellation.\n\n"
                f"Thank you!"
            ),
            from_email='noreply@example.com',
            recipient_list=[user_email],
            fail_silently=False,
        )

    return f"Sent reminders for {unpaid_orders.count()} unpaid orders."