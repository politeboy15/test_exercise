from django.urls import path
from . import views

urlpatterns = [
    path('ads/<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('ads/<int:ad_id>/trade/', views.trade_view, name='trade_view'),
]
