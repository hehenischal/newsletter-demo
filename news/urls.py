from django.urls import path
from .views import *

urlpatterns = [
    path('', register_receipient, name='register_receipient'),
    path('send/', send_newsletter, name='send_newsletter'),
]