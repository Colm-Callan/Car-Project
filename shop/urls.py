from django.urls import path
from . import views
from .views import (
    CarCreateView,
    CarDetailView,
    CarListView, 
    CarDeleteView,
    add_comment,
    )

app_name = 'shop'

urlpatterns = [
    path('', views.prod_list,name = 'all_products'),
    path('<uuid:category_id>/', views.prod_list, name = 'products_by_category'),
    path('<uuid:category_id>/<uuid:product_id>/', views.product_detail, name = 'product_detail'),
    path('newcomment/<int:pk>/', add_comment, name='add_comment'),
    path('new/', CarCreateView.as_view(), name='car_create'),
    path('<int:pk>/delete/',CarDeleteView.as_view(), name = 'car_delete'),
    path('<int:pk>/', CarDetailView.as_view(), name='car_detail'),
]
