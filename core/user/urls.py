from django.urls import path
from .views import UserListView, UserDeleteView

app_name = 'user'

urlpatterns = [
    path('', UserListView.as_view(), name='index'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name="delete")
]
