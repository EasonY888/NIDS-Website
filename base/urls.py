from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name="home"),
    path('register/', views.Register, name="register"),
    path('login/', views.LoginUser, name="login"),
    path('logout/', views.LogoutUser, name="logout"),
]