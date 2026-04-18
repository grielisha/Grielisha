from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment, Order
from accounts.models import ActivityLog

@receiver(post_save, sender=Payment)
def log_payment_activity(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            user=instance.order.user,
            action='purchase',
            description=f"Payment initiated for Order #{instance.order.id}. Method: {instance.payment_method}. Amount: KES {instance.amount}"
        )
    elif instance.status == 'verified':
        ActivityLog.objects.create(
            user=instance.order.user,
            action='purchase',
            description=f"Payment VERIFIED for Order #{instance.order.id}. M-Pesa/Ref: {instance.transaction_code}"
        )

@receiver(post_save, sender=Order)
def log_order_status_change(sender, instance, created, **kwargs):
    if not created:
        ActivityLog.objects.create(
            user=instance.user,
            action='purchase',
            description=f"Order #{instance.id} status updated to: {instance.status}"
        )
