from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path("user/login/", LoginView.as_view(template_name='users/login.html'), name="login"),
    path("user/logout", views.LogoutView, name='logout'),
    path('user/register', views.register, name='register')
]
