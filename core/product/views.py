from django.shortcuts import render
from .models import Product
from core.subcategory.models import Subcategory
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import ProductForm
from django.urls import reverse_lazy
from django.http import JsonResponse


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'product/list.html'


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product/detail.html'

    def get_object(self, queryset=None):
        # Obtén el nombre del producto de la URL
        product_name = self.kwargs.get('name')
        # Busca el producto por su nombre
        return Product.objects.get(name=product_name)


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('product:index')

    def post(self, request):
        data = request.POST
        name = data['name']
        description = data['description']
        price = data['price']
        if 'image' in request.FILES:
            image = request.FILES['image']
        else:
            image = None
        subcategory_id = data['subcategory']
        subcategory = Subcategory.objects.get(id=subcategory_id)
        try:
            product = Product.objects.create(
                name=name, description=description, price=price, image=image, subcategory=subcategory)
            response = 'Product is created successfull'
        except Exception as e:
            response = str(e)
        return JsonResponse({'response': response}, status=200)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/edit.html'
    success_url = reverse_lazy('product:index')

    def form_valid(self, form):
        product_id = self.kwargs['pk']
        name = form.cleaned_data['name']
        description = form.cleaned_data['description']
        price = form.cleaned_data['price']

        if form.cleaned_data['image']:
            image = form.cleaned_data['image']

        subcategory = form.cleaned_data['subcategory']
        try:
            product = Product.objects.get(id=product_id)
            product.name = name
            product.description = description
            product.price = price
            product.image = image
            product.subcategory = subcategory
            product.save()
            response = 'Product is updated successfull'
        except Exception as e:
            response = str(e)
        return JsonResponse({'response': 'response'}, status=200)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('product:index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return JsonResponse({'message': 'Objeto eliminado exitosamente'}, status=200)
