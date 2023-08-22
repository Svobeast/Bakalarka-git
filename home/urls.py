from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home_view"),
    path("vysledek", views.vysledek, name="vysledek"),
    path("znovu", views.home_view, name = "znovu"),
]