from .models import Product
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Cart

def cart(request):
    return {'cart': Cart.objects.filter(user_id=request.user.id)}

class ProductListView(generic.ListView):
    model = Product
    ordering = ['-date_modified']
    paginate_by = 2

class ProductDetailView(generic.DetailView):
    model = Product

class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Product
    fields = ['name', 'description', 'price', 'category', 'quantity', 'image']

    def test_func(self):
        return self.request.user.has_perm('store.add_product')

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Product
    fields = ['name', 'description', 'price', 'category', 'quantity', 'image']

    def test_func(self):
        return self.request.user.has_perm('store.change_product')

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Product
    success_url = '/'

    def test_func(self):
        return self.request.user.has_perm('store.delete_product')

    