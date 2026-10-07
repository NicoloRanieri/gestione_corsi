from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CorsoForm
from .models import Corso, Iscrizione

from django.db.models import Q


class CorsoListView(ListView):
    model = Corso
    context_object_name = "corsi"


class CorsoDetailView(DetailView):
    model = Corso

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["iscrizione"] = Iscrizione.objects.filter(
                corso=self.object, utente=self.request.user
            ).first()
        return context


@login_required
@require_POST
def iscriviti(request, pk):
    corso = get_object_or_404(Corso, pk=pk)

    if Iscrizione.objects.filter(corso=corso, utente=request.user).exists():
        messages.warning(request, "Sei già iscritto a questo corso.")
        return redirect(corso)

    iscrizione = Iscrizione(corso=corso, utente=request.user)
    try:
        iscrizione.full_clean()
    except ValidationError as errore:
        for messaggio in errore.messages:
            messages.error(request, messaggio)
        return redirect(corso)

    iscrizione.save()
    messages.success(request, f'Iscrizione al corso "{corso.titolo}" completata!')
    return redirect(corso)


@login_required
@require_POST
def annulla_iscrizione(request, pk):
    iscrizione = get_object_or_404(Iscrizione, pk=pk, utente=request.user)

    if iscrizione.corso.stato != Corso.Stato.PROGRAMMATO:
        messages.error(request, "Puoi annullare solo l'iscrizione a corsi non ancora iniziati.")
    else:
        titolo = iscrizione.corso.titolo
        iscrizione.delete()
        messages.success(request, f'Iscrizione al corso "{titolo}" annullata.')

    return redirect("corsi:mie_iscrizioni")


class MieIscrizioniView(LoginRequiredMixin, ListView):
    template_name = "corsi/mie_iscrizioni.html"
    context_object_name = "iscrizioni"

    def get_queryset(self):
        return Iscrizione.objects.filter(utente=self.request.user).select_related("corso")

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class CorsoCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = Corso
    form_class = CorsoForm
    success_message = 'Il corso "%(titolo)s" è stato creato.'


class CorsoUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Corso
    form_class = CorsoForm
    success_message = 'Il corso "%(titolo)s" è stato aggiornato.'


class CorsoDeleteView(StaffRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Corso
    success_url = reverse_lazy("corsi:lista")

    def get_success_message(self, cleaned_data):
        return f'Il corso "{self.object.titolo}" è stato eliminato.'

class CorsoListView(ListView):
    model = Corso
    context_object_name = "corsi"

    def get_queryset(self):
        queryset = super().get_queryset()
        self.q = self.request.GET.get("q", "").strip()
        self.stato = self.request.GET.get("stato", "")

        if self.q:
            queryset = queryset.filter(
                Q(titolo__icontains=self.q)
                | Q(docente__icontains=self.q)
                | Q(descrizione__icontains=self.q)
            )

        if self.stato in Corso.Stato.values:
            queryset = queryset.filter(stato=self.stato)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.q
        context["stato_selezionato"] = self.stato
        context["stati"] = Corso.Stato.choices
        context["filtri_attivi"] = bool(self.q or self.stato in Corso.Stato.values)
        return context