from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "corsi"

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="corsi:lista"), name="home"),
    path("corsi/", views.CorsoListView.as_view(), name="lista"),
    path("corsi/<int:pk>/", views.CorsoDetailView.as_view(), name="dettaglio"),
]