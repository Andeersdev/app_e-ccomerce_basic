
from django.contrib import admin
from django.urls import path, include
from .views import LoginView, RegisterView, HomeView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('dashboard/', include('core.dashboard.urls')),
    path('user/', include('core.user.urls')),
    path('category/', include('core.category.urls')),
    path('subcategory/', include('core.subcategory.urls')),
    path('product/', include('core.product.urls')),
    path('cart/', include('core.cart.urls')),
    path('order/', include('core.orders.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
