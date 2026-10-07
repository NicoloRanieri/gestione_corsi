from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "corsi"

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="corsi:lista"), name="home"),
    path("corsi/", views.CorsoListView.as_view(), name="lista"),
    path("corsi/<int:pk>/", views.CorsoDetailView.as_view(), name="dettaglio"),

    path("corsi/<int:pk>/iscriviti/", views.iscriviti, name="iscriviti"),
    path("iscrizioni/", views.MieIscrizioniView.as_view(), name="mie_iscrizioni"),
    path("iscrizioni/<int:pk>/annulla/", views.annulla_iscrizione, name="annulla_iscrizione"),
]