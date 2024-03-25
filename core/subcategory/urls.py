from django.urls import path
from .views import SubCategoryListView, SubCategoryCreateView, SubCategoryUpdateView, SubCategoryDeleteView

app_name = 'subcategory'

urlpatterns = [
    path('', SubCategoryListView.as_view(), name='index'),
    path('create/', SubCategoryCreateView.as_view(), name='create'),
    path('update/<int:pk>', SubCategoryUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', SubCategoryDeleteView.as_view(), name='delete')
]
