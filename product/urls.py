
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from main.views import MainView
from product.views import ProductDetailAPI, ProductDetailView

app_name = 'products'

urlpatterns = [
    path('<int:product_id>/', ProductDetailAPI.as_view(), name='list'),
    path('detail/', ProductDetailView.as_view(), name='list'),
]
