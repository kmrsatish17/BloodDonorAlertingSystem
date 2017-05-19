from django.shortcuts import redirect
from django.urls import reverse


def redirect_home(request):
    return redirect(reverse('loginsignup:home'))
