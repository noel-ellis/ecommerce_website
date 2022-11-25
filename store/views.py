from django.shortcuts import render
from .models import Users, Stock
from django.views import generic

class UsersListView(generic.ListView):
    model = Users

class StockListView(generic.ListView):
    model = Stock

def home(request):
    return render(request, 'store/main.html')
