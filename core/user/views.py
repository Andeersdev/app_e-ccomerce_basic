from django.shortcuts import render
from .models import User
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse


class UserListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'user/list.html'


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('user:index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return JsonResponse({'message': 'Objeto eliminado exitosamente'}, status=200)
