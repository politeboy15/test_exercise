from django.urls import path
from . import views

urlpatterns = [
    path('create_ad/', views.create_ad, name='create_ad'),
    path('<uuid:ad_id>/', views.ad_detail_view, name='ad_detail'),
    path('<uuid:ad_id>/trade/', views.trade_view, name='trade'),
    path('<uuid:ad_id>/trade_page/', views.trade_page_view, name='trade_page'),
    path('<uuid:ad_id>/edit/', views.ad_edit, name='ad_edit'),
    path('<uuid:ad_id>/delete/', views.ad_delete, name='ad_delete'),
]
