from django.contrib import admin

from .models import Corso, Iscrizione


class IscrizioneInline(admin.TabularInline):
    model = Iscrizione
    extra = 0
    readonly_fields = ["data_iscrizione"]


@admin.register(Corso)
class CorsoAdmin(admin.ModelAdmin):
    list_display = ["titolo", "docente", "data_inizio", "durata", "stato", "posti_liberi"]
    list_filter = ["stato", "data_inizio"]
    search_fields = ["titolo", "docente", "descrizione"]
    list_editable = ["stato"]
    date_hierarchy = "data_inizio"
    inlines = [IscrizioneInline]


@admin.register(Iscrizione)
class IscrizioneAdmin(admin.ModelAdmin):
    list_display = ["utente", "corso", "data_iscrizione"]
    list_filter = ["corso"]
    search_fields = ["utente__username", "corso__titolo"]