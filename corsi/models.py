from django.conf import settings
from django.db import models


class Corso(models.Model):

    class Stato(models.TextChoices):
        PROGRAMMATO = "programmato", "Programmato"
        IN_CORSO = "in_corso", "In corso"
        CONCLUSO = "concluso", "Concluso"
        ANNULLATO = "annullato", "Annullato"

    titolo = models.CharField(max_length=200)
    descrizione = models.TextField()
    docente = models.CharField(max_length=100)
    data_inizio = models.DateField()
    durata = models.PositiveIntegerField(help_text="Durata in ore")
    stato = models.CharField(
        max_length=20,
        choices=Stato.choices,
        default=Stato.PROGRAMMATO,
    )
    posti_massimi = models.PositiveIntegerField(default=20)

    class Meta:
        ordering = ["data_inizio"]
        verbose_name = "corso"
        verbose_name_plural = "corsi"

    def __str__(self):
        return self.titolo

    def posti_liberi(self):
        return self.posti_massimi - self.iscrizioni.count()


class Iscrizione(models.Model):
    utente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="iscrizioni",
    )
    corso = models.ForeignKey(
        Corso,
        on_delete=models.CASCADE,
        related_name="iscrizioni",
    )
    data_iscrizione = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_iscrizione"]
        verbose_name = "iscrizione"
        verbose_name_plural = "iscrizioni"
        constraints = [
            models.UniqueConstraint(
                fields=["utente", "corso"],
                name="iscrizione_unica",
            )
        ]

    def __str__(self):
        return f"{self.utente} - {self.corso}"