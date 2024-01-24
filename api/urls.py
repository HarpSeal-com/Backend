from django.urls import path
from . import views

urlpatterns = [
    path('getProduct', views.main, name="main-api"),
]