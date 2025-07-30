from django.urls import path
from . import views

urlpatterns = [
    # Старые URL для веб-интерфейса
    path('signin/', views.signin_view, name='signin'),
    path('signout/', views.signout_view, name='signout'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    
    # Новые API URL для JWT
    path('api/signin/', views.signin_api, name='signin_api'),
    path('api/signup/', views.signup_api, name='signup_api'),
    path('api/profile/', views.profile_api, name='profile_api'),
    path('api/delete/', views.delete_user_api, name='delete_user_api'),
    
    path('', views.home_view, name='home'),
]
