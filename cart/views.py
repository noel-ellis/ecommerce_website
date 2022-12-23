from django.shortcuts import render
from django.urls import reverse

# Create your views here.
def cart_summary(request):
    return render(request, 'store/cart/summary.html')