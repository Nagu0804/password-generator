from django.shortcuts import render
from .models import GeneratedPassword
import random

def user_update_or_create(request, model, defaults):
    if request.user.is_authenticated:
        model.objects.create(
            user=request.user,
            **defaults
        )

def home(request):
    return render(request, 'generator/home.html')

def generate(request):
    context = {
        'weak_range': range(6, 16),
        'strong_range': range(16, 129),
        'unbelievable_range': [256, 512, 1024, 2048],
    }
    return render(request, 'generator/generate.html', context)

def password(request):
    lower_case_letters = list('abcdefghijklmnopqrstuvwxyz')
    upper_case_letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    numbers = list('0123456789')
    symbols = list('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')

    length = int(request.GET.get('length', 16))
    purpose = str(request.GET.get('purpose', ''))
    available_chars = lower_case_letters

    if request.GET.get('uppercase'):
        available_chars += upper_case_letters

    if request.GET.get('numbers'):
        available_chars += numbers

    if request.GET.get('symbols'):
        available_chars += symbols
    
    generated_password = ''.join(random.choice(available_chars) for _ in range(length))

    user_update_or_create(
        request,
        GeneratedPassword,
        {
            'password': generated_password,
            'purpose': purpose
        }
    )

    return render(request, 'generator/password.html', {'password': generated_password})

def password_details(request):
    saved_passwords = GeneratedPassword.objects.filter(user=request.user)
    return render(request, 'generator/password_details.html', {'saved_passwords': saved_passwords})
