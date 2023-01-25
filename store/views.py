from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Collection, Product


def main(request):
    return render(request, 'store/main.html')


def collection_list(request, slug):
    collection = get_object_or_404(Collection, slug=slug)
    products = Product.objects.filter(collection=collection)
    return render(request, 'store/collection_list.html', {'collection': collection, 'products': products})


class CollectionCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Collection
    fields = ['image', 'name', 'slug', 'description', 'season']

    def test_func(self):
        return self.request.user.has_perm('store.add_collection')


class ProductListView(generic.ListView):
    model = Product
    ordering = ['-date_modified']
    paginate_by = 9


class ProductDetailView(generic.DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Product
    fields = ['name', 'description', 'price', 'collection', 'quantity', 'image', 'slug']
    fields = [
        'collection',
        'name',
        'slug',
        'description',
        'price',
        'quantity',
        'sex',
        'size',
        'sale',
        'new',
        'image',
    ]


    def test_func(self):
        return self.request.user.has_perm('store.add_product')


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Product
    fields = ['name', 'description', 'price', 'collection', 'quantity', 'image']

    def test_func(self):
        return self.request.user.has_perm('store.change_product')


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Product
    success_url = '/'

    def test_func(self):
        return self.request.user.has_perm('store.delete_product')
