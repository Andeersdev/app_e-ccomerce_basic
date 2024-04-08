from django.urls import path
from .views import create_order, capture_order, cancel_order, save_order, pay_order, view_order, OrderListView

app_name = 'order'

urlpatterns = [
    path('', OrderListView.as_view(), name='index'),
    path('create/', create_order, name='create'),
    path('save_order/', save_order, name='save'),
    path('capture/', capture_order, name='capture'),
    path('pay/', pay_order, name='pay'),
    path('cancel/', cancel_order, name='cancel'),
    path('view/<int:id>/', view_order, name='pdf')
]
