from django.dispatch import Signal

# Sent when councillor is notified about the report.
councillor_notified = Signal(providing_args=['report', 'councillor'])