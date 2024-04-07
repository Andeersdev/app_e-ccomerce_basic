from core.user.models import User
from core.user.forms import UserForm
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, TemplateView, View
from .forms import CustomAutheticationForm
from django.urls import reverse_lazy
from core.product.models import Product
from core.category.models import Category
from core.subcategory.models import Subcategory
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.conf import settings


class LoginView(LoginView):
    form_class = CustomAutheticationForm
    template_name = 'auth/login.html'
    success_url = reverse_lazy('dash:index')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy(settings.LOGOUT_REDIRECT_URL))


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

        search = self.request.GET.get('search', '')
        filter_ = self.request.GET.get('filter', '')
        if search:
            products = Product.objects.filter(name__icontains=search)
        elif filter_:
            products = Product.objects.filter(subcategory__name=filter_)
        else:
            products = Product.objects.all()
        context['products'] = products
        context['categories'] = Category.objects.all()
        return context
