from django.shortcuts import render
from .models import Stock
from django.views import generic

class StockListView(generic.ListView):
    model = Stock

def home(request):
    return render(request, 'store/main.html')
