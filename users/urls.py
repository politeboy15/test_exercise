from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signin_view, name='signin'),
    path('signout/', views.signout_view, name='signout'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
    path('', views.home_view, name='home'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
]
