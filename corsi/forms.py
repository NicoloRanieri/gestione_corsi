from django import forms
from django.utils import timezone

from .models import Corso


class CorsoForm(forms.ModelForm):

    class Meta:
        model = Corso
        fields = [
            "titolo",
            "descrizione",
            "docente",
            "data_inizio",
            "durata",
            "stato",
            "posti_massimi",
        ]
        labels = {
            "data_inizio": "Data di inizio",
        }
        widgets = {
            "descrizione": forms.Textarea(attrs={"rows": 5}),
            "data_inizio": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            if isinstance(campo.widget, forms.Select):
                campo.widget.attrs["class"] = "form-select"
            else:
                campo.widget.attrs["class"] = "form-control"

    def clean_posti_massimi(self):
        posti = self.cleaned_data["posti_massimi"]
        if self.instance.pk:
            iscritti = self.instance.iscrizioni.count()
            if posti < iscritti:
                raise forms.ValidationError(
                    f"Il corso ha già {iscritti} iscritti: i posti non possono essere meno di {iscritti}."
                )
        return posti

    def clean(self):
        cleaned_data = super().clean()
        stato = cleaned_data.get("stato")
        data_inizio = cleaned_data.get("data_inizio")

        if stato and data_inizio:
            oggi = timezone.localdate()
            if stato == Corso.Stato.PROGRAMMATO and data_inizio < oggi:
                self.add_error(
                    "data_inizio",
                    "Un corso programmato non può avere una data di inizio già passata.",
                )
            if stato in (Corso.Stato.IN_CORSO, Corso.Stato.CONCLUSO) and data_inizio > oggi:
                self.add_error(
                    "data_inizio",
                    "Un corso in corso o concluso non può avere una data di inizio futura.",
                )

        return cleaned_data