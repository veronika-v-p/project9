from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('materials/', views.MaterialListCreateView.as_view(), name="materials"), 
    path('registr', views.registr, name="registr"),
    path('loginn/', views.loginn, name="loginn"),

]
