from django.urls import path
from .views import CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView

app_name = 'category'

urlpatterns = [
    path('', CategoryListView.as_view(), name='index'),
    path('create/', CategoryCreateView.as_view(), name='create'),
    path('update/<int:pk>', CategoryUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', CategoryDeleteView.as_view(), name='delete')
]
