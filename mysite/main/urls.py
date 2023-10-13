from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("pocasiP", views.pocasiP, name="pocasiP"),
    path("Aknbl", views.Aknbl, name="Aknbl"),
    path("AkPocasi", views.AkPocasi, name="AkPocasi")
]