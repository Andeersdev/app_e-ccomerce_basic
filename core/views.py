from core.user.models import User
from core.user.forms import UserForm
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, TemplateView
from .forms import CustomAutheticationForm
from django.urls import reverse_lazy
from core.product.models import Product
from core.category.models import Category
from core.subcategory.models import Subcategory


class LoginView(LoginView):
    form_class = CustomAutheticationForm
    template_name = 'auth/login.html'
    success_url = reverse_lazy('dash:index')


class RegisterView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['categories'] = Category.objects.all()
        return context
