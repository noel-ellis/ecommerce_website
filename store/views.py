from .models import Stock
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class StockListView(generic.ListView):
    model = Stock

class StockDetailView(generic.DetailView):
    model = Stock

class StockCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Stock

    fields = ['name', 'description', 'price', 'category', 'quantity', 'image']

    def test_func(self):
        return self.request.user.has_perm('store.add_stock')

class StockUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Stock
    fields = ['name', 'description', 'price', 'category', 'quantity', 'image']

    def test_func(self):
        return self.request.user.has_perm('store.change_stock')

class StockDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Stock
    success_url = '/'

    def test_func(self):
        return self.request.user.has_perm('store.delete_stock')

    