from django.shortcuts import render
from .models import Subcategory
from core.category.models import Category
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import SubCategoryForm
from django.urls import reverse_lazy
from django.http import JsonResponse


class SubCategoryListView(ListView):
    model = Subcategory
    context_object_name = 'subcategories'
    template_name = 'subcategory/list.html'


class SubCategoryCreateView(CreateView):
    model = Subcategory
    form_class = SubCategoryForm
    template_name = 'subcategory/create.html'
    success_url = reverse_lazy('subcategory:index')

    def post(self, request):
        data = request.POST
        name = data['name']
        category_id = data['category']
        category = Category.objects.get(id=category_id)
        try:
            category = Subcategory.objects.create(
                name=name, category=category)
            response = 'SubCategory is created successfull'
        except Exception as e:
            response = str(e)
        return JsonResponse({'response': response}, status=200)


class SubCategoryUpdateView(UpdateView):
    model = Subcategory
    form_class = SubCategoryForm
    template_name = 'subcategory/edit.html'
    success_url = reverse_lazy('subcategory:index')


class SubCategoryDeleteView(DeleteView):
    model = Subcategory
    success_url = reverse_lazy('subcategory:index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return JsonResponse({'message': 'Objeto eliminado exitosamente'}, status=200)
