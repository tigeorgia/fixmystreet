from django.dispatch import Signal

user_confirmed = Signal(providing_args=['user'])
