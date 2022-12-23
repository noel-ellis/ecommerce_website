from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Cart, Category, Product


def cart(request):
    return {'cart': Cart.objects.filter(user_id=request.user.id)}


def categories(request):
    return {'categories': Category.objects.all()}


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/category_list.html', {'category': category, 'products': products})


class ProductListView(generic.ListView):
    model = Product
    ordering = ['-date_modified']
    paginate_by = 9


class ProductDetailView(generic.DetailView):
    model = Product


class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Category
    fields = ['name', 'slug']

    def test_func(self):
        return self.request.user.has_perm('store.add_category')


class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Product
    fields = ['name', 'description', 'price', 'category', 'quantity', 'image', 'slug']

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
