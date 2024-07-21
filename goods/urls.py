from itertools import product
from django.urls import path

from goods import views

app_name = 'goods'

urlpatterns = [
    path('<slug:category_slug>/', views.catalog, name = 'index'),
    path('<slug:category_slug>/<int:page>/', views.catalog, name = 'index'), 
    # url-маршрутизация для отображения страницы по целому значению 
    path('product/<slug:product_slug>/', views.product, name = 'product'),
]