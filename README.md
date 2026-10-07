# Gestione Corsi

Web application Django per la gestione di corsi e iscrizioni. Gli utenti possono consultare il catalogo dei corsi, cercarli e filtrarli, iscriversi e gestire le proprie iscrizioni; lo staff può creare, modificare ed eliminare i corsi sia dal sito sia dal pannello di amministrazione.

## Requisiti

- Python 3.12 o superiore
- pip

Tutte le altre dipendenze sono elencate in `requirements.txt`.

## Installazione

1. Clonare la repository ed entrare nella cartella del progetto:

   ```bash
   git clone https://github.com/NicoloRanieri/gestione_corsi
   cd gestione_corsi
   ```

2. Creare e attivare un ambiente virtuale.

   Su Windows:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   Su macOS/Linux:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Installare le dipendenze:

   ```bash
   pip install -r requirements.txt
   ```

4. Applicare le migrazioni (il database `db.sqlite3` con i dati di esempio è già incluso):

   ```bash
   python manage.py migrate
   ```

## Avvio

```bash
python manage.py runserver
```

L'applicazione è raggiungibile all'indirizzo http://127.0.0.1:8000/ e il pannello di amministrazione all'indirizzo http://127.0.0.1:8000/admin/.

## Utenti di prova

Il database incluso contiene i seguenti account:

| Username | Password | Ruolo |
|---|---|---|
| nicolo | `1234` | Superutente (accesso all'Admin e gestione dei corsi) |
| mario | `Prova1234!` | Utente normale |
| giulia | `Prova1234!` | Utente normale |
| luca | `Prova1234!` | Utente normale |


## Funzionalità

**Autenticazione.** Login e logout tramite il sistema di autenticazione integrato di Django. La barra di navigazione cambia in base all'utente: chi non è autenticato vede il pulsante di accesso, gli utenti autenticati vedono le proprie iscrizioni e il pulsante di uscita, lo staff vede anche il collegamento all'Admin.

**Catalogo dei corsi.** Lista dei corsi con titolo, docente, data di inizio, durata e stato (Programmato, In corso, Concluso, Annullato), e pagina di dettaglio con descrizione completa e posti disponibili.

**Ricerca e filtri.** Nella lista dei corsi è possibile cercare per titolo, docente o descrizione e filtrare per stato. I due criteri si possono combinare e i parametri restano nell'indirizzo della pagina, così una ricerca può essere salvata o condivisa.

**Iscrizioni.** Un utente autenticato può iscriversi a un corso dalla pagina di dettaglio. L'iscrizione è consentita solo se il corso è nello stato "Programmato", se ci sono posti liberi e se l'utente non è già iscritto.

**Le mie iscrizioni.** Pagina riservata agli utenti autenticati con l'elenco delle proprie iscrizioni. Un'iscrizione può essere annullata finché il corso non è iniziato.

**Gestione dei corsi (CRUD).** Gli utenti staff possono creare, modificare ed eliminare i corsi direttamente dal sito tramite un ModelForm. Prima dell'eliminazione viene mostrata una pagina di conferma, con un avviso se il corso ha iscritti. Gli altri utenti non vedono i relativi pulsanti e ricevono un errore 403 se provano ad accedere a queste pagine.

**Pannello Admin.** Corsi e iscrizioni sono gestibili dall'Admin di Django, personalizzato con colonne, filtri laterali, ricerca, modifica rapida dello stato dalla lista e visualizzazione delle iscrizioni all'interno della pagina di ciascun corso.

**Validazioni personalizzate.**

- Nel model `Iscrizione` non è possibile iscriversi a un corso che non è programmato o che è al completo. Essendo nel model, la regola vale sia per il sito sia per l'Admin.
- Nel form `CorsoForm` i posti di un corso non possono essere ridotti sotto il numero di iscritti già presenti.
- Nel form `CorsoForm` un corso programmato non può avere una data di inizio passata, e un corso in corso o concluso non può avere una data di inizio futura.
- A livello di database, un vincolo `UniqueConstraint` impedisce che lo stesso utente si iscriva due volte allo stesso corso.

## Struttura del progetto

```
gestione_corsi/
├── config/                  # impostazioni e URL principali del progetto
├── corsi/                   # app principale
│   ├── admin.py             # configurazione del pannello Admin
│   ├── forms.py             # CorsoForm con le validazioni personalizzate
│   ├── models.py            # model Corso e Iscrizione
│   ├── urls.py              # URL dell'app
│   ├── views.py             # view per lista, dettaglio, CRUD e iscrizioni
│   └── templates/corsi/     # template dell'app
├── templates/
│   ├── base.html            # layout comune con la barra di navigazione
│   └── registration/
│       └── login.html       # pagina di login
├── db.sqlite3               # database con i dati di esempio
├── manage.py
└── requirements.txt
```

## Principali indirizzi

| URL | Pagina | Accesso |
|---|---|---|
| `/corsi/` | Lista dei corsi con ricerca e filtri | Tutti |
| `/corsi/<id>/` | Dettaglio di un corso | Tutti |
| `/corsi/nuovo/` | Creazione di un corso | Staff |
| `/corsi/<id>/modifica/` | Modifica di un corso | Staff |
| `/corsi/<id>/elimina/` | Eliminazione di un corso | Staff |
| `/iscrizioni/` | Le mie iscrizioni | Utenti autenticati |
| `/accounts/login/` | Login | Tutti |
| `/admin/` | Pannello di amministrazione | Staff |