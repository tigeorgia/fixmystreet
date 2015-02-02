from django.dispatch import receiver
from datetime import datetime
from .models import Report
from .signals import councillor_notified

@receiver(councillor_notified, sender=Report)
def update_report(sender, report, councillor, **kwargs):
    """
    Update report instance with sent_at and email_sent_to fields.
    """
    report.sent_at = datetime.now()
    report.email_sent_to = councillor.email
    report.save()