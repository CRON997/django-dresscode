from io import BytesIO
from celery import shared_task
import weasyprint
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from apps.orders.models import Order
import logging

logger = logging.getLogger(__name__)


def payment_completed(order_id):
    try:
        order = get_object_or_404(Order, id=order_id)

        subject = f'Dresscode shop - Invoice no {order.order_number}'
        message = 'Please find your order invoice attached.'
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [order.email]
        )

        html = render_to_string('orders/pdf.html', {'order': order})
        out = BytesIO()
        weasyprint.HTML(string=html).write_pdf(out)

        email.attach(
            f'order_{order.order_number}.pdf',
            out.getvalue(),
            'application/pdf'
        )

        email.send()

        return True, f"Invoice sent successfully for order {order.order_number}"

    except Exception as e:
        return False, f"Error sending invoice: {str(e)}"
