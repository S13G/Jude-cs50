from django import views
from django.urls import path
from .views import index, register,login, logout
app_name = 'accounts'

urlpatterns = [
    path('',index, name="home"),
    # path('###',save_reg,name="save"),
    path('register',register, name="register"),
    path('login',login, name="login"),
    path('logout',logout, name="logout"),
]