from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("Aknbl", views.Aknbl, name="Aknbl"),
    path("AkPocasi", views.AkPocasi, name="AkPocasi"),
    path("HisNbl", views.HisNbl, name="HisNbl" ),
    path("zlato", views.zlato, name = "zlato")
]