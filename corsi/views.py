from django.views.generic import DetailView, ListView

from .models import Corso


class CorsoListView(ListView):
    model = Corso
    context_object_name = "corsi"


class CorsoDetailView(DetailView):
    model = Corso