from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('generate/', generate, name="generate"),
    path('password/', password, name="password"),
    path('password_details/', password_details, name="password_details"),
]