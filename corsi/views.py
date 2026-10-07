from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView

from .models import Corso, Iscrizione


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