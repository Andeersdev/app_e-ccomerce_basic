from django.shortcuts import render
from .models import Category
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import CategoryForm
from django.urls import reverse_lazy
from django.http import JsonResponse


class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'category/list.html'


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/create.html'
    success_url = reverse_lazy('category:index')

    def post(self, request):
        data = request.POST
        name = data['name']
        description = data['description']
        try:
            category = Category.objects.create(
                name=name, description=description)
            response = 'Category is created successfull'
        except Exception as e:
            response = str(e)
        return JsonResponse({'response': response}, status=200)


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/edit.html'
    success_url = reverse_lazy('category:index')


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('category:index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return JsonResponse({'message': 'Objeto eliminado exitosamente'}, status=200)
