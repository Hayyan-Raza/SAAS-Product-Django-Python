from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('home/', views.logout_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('generate/', views.generate_resume, name='generate_resume'),
    path('', views.home, name='home'),

]
