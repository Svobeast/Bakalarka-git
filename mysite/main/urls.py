from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("pocasiP", views.pocasiP, name="pocasiP"),
    #path("nbl", views.nbl, name="nbl"),
    path("AkPocasi", views.AkPocasi, name="AkPocasi")
]