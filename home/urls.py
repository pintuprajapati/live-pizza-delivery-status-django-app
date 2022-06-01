from django.urls import path
from .views import *
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('<order_id>/', order, name='order'),
    path('api/order', order_pizza, name='order_pizza'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

