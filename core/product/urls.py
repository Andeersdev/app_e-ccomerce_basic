from django.urls import path
from .views import ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView

app_name = 'product'

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete')
]
