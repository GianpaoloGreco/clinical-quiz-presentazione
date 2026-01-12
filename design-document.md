# Clinical Quiz - Documento di Design Tecnico

## 1. Panoramica del Progetto

**Clinical Quiz** è una web application pensata per l'utilizzo durante congressi ed eventi medici. Permette agli organizzatori di creare quiz interattivi e formativi, accessibili ai partecipanti tramite QR code e/o codice stanza.

Il sistema integra un'intelligenza artificiale (GPT-4 Mini) che fornisce feedback educativi sulle risposte degli utenti, impersonando un medico chirurgo professionista.

---

## 2. Pre-Produzione: User Flow Descrittivi

Questa sezione descrive in dettaglio i percorsi utente (user flow) per ogni tipologia di utilizzatore della piattaforma. I flussi sono organizzati per ruolo e scenario d'uso.

---

### 2.1 User Flow: Admin della Piattaforma

#### UF-A01: Primo Accesso e Login Admin

**Attore:** Amministratore della piattaforma
**Precondizione:** L'admin possiede credenziali valide
**Obiettivo:** Accedere al pannello di amministrazione

1. L'admin accede alla URL dedicata del backoffice (es. `/admin`)
2. Il sistema mostra la schermata di login con campi username e password
3. L'admin inserisce le proprie credenziali
4. Il sistema valida le credenziali
   - **Se valide:** reindirizza alla Dashboard Admin
   - **Se non valide:** mostra messaggio di errore e permette un nuovo tentativo
5. La sessione viene creata e l'admin visualizza la dashboard principale

**Postcondizione:** L'admin è autenticato e può operare nel sistema

---

#### UF-A02: Creazione di un Nuovo Account Creator

**Attore:** Amministratore della piattaforma
**Precondizione:** L'admin è autenticato nel sistema
**Obiettivo:** Creare un account per un nuovo organizzatore di eventi

1. Dalla Dashboard, l'admin seleziona la sezione "Gestione Utenti"
2. Il sistema mostra la lista dei Creator esistenti con stato (attivo/disattivo)
3. L'admin clicca sul pulsante "Nuovo Creator"
4. Il sistema presenta un form con i campi richiesti:
   - Username (obbligatorio, univoco)
   - Password temporanea (obbligatorio)
   - Email (obbligatorio)
   - Nome completo (obbligatorio)
   - Note interne (opzionale)
5. L'admin compila i campi e conferma
6. Il sistema valida i dati inseriti
   - **Se username già esistente:** mostra errore specifico
   - **Se email non valida:** mostra errore di formato
   - **Se dati validi:** crea l'account
7. Il sistema genera le credenziali e le mostra all'admin
8. L'admin può copiare le credenziali o inviarle via email al Creator

**Postcondizione:** Il nuovo Creator può accedere con le credenziali fornite

---

#### UF-A03: Visualizzazione Report Aggregati

**Attore:** Amministratore della piattaforma
**Precondizione:** L'admin è autenticato; esistono quiz completati nel sistema
**Obiettivo:** Consultare statistiche globali della piattaforma

1. Dalla Dashboard, l'admin seleziona la sezione "Report"
2. Il sistema mostra una panoramica con:
   - Numero totale di Creator attivi
   - Numero totale di quiz creati
   - Numero totale di partecipazioni
   - Grafico andamento partecipazioni nel tempo
3. L'admin può filtrare per:
   - Intervallo di date
   - Specifico Creator
   - Stato del quiz (attivo/concluso)
4. L'admin può selezionare un singolo evento per vedere il dettaglio
5. L'admin può esportare i dati in formato CSV o PDF
6. Il sistema genera il file e avvia il download

**Postcondizione:** L'admin ha consultato e/o esportato i dati aggregati

---

#### UF-A04: Disattivazione Account Creator

**Attore:** Amministratore della piattaforma
**Precondizione:** L'admin è autenticato; esiste almeno un Creator attivo
**Obiettivo:** Disattivare un account Creator (senza eliminarlo)

1. Dalla sezione "Gestione Utenti", l'admin visualizza la lista Creator
2. L'admin individua il Creator da disattivare
3. L'admin clicca sull'azione "Disattiva"
4. Il sistema chiede conferma con un messaggio: "Confermi la disattivazione? Il Creator non potrà più accedere ma i suoi quiz rimarranno nel sistema"
5. L'admin conferma
6. Il sistema imposta lo stato del Creator come "disattivo"
7. I quiz esistenti del Creator rimangono accessibili ai partecipanti
8. Il Creator non può più effettuare login

**Postcondizione:** Il Creator è disattivato; i dati storici sono preservati

---

### 2.2 User Flow: Creator (Organizzatore Evento)

#### UF-C01: Primo Accesso Creator

**Attore:** Creator dell'evento
**Precondizione:** Il Creator ha ricevuto le credenziali dall'Admin
**Obiettivo:** Accedere al proprio pannello di gestione

1. Il Creator accede alla URL della piattaforma
2. Il sistema mostra la schermata di login
3. Il Creator inserisce username e password forniti dall'Admin
4. Il sistema valida le credenziali
   - **Se primo accesso:** suggerisce il cambio password (opzionale)
   - **Se credenziali errate:** mostra errore
5. Il Creator accede alla propria Dashboard personale
6. La Dashboard mostra:
   - Lista dei propri quiz (vuota se primo accesso)
   - Pulsante "Crea Nuovo Quiz"
   - Accesso ai Report dei propri eventi

**Postcondizione:** Il Creator è autenticato e può gestire i propri quiz

---

#### UF-C02: Creazione di un Nuovo Quiz

**Attore:** Creator dell'evento
**Precondizione:** Il Creator è autenticato
**Obiettivo:** Creare un nuovo quiz per un evento medico

1. Dalla Dashboard, il Creator clicca "Crea Nuovo Quiz"
2. Il sistema presenta un wizard di creazione suddiviso in step

**Step 1 - Informazioni Base:**
3. Il Creator inserisce:
   - Titolo del quiz (obbligatorio)
   - Descrizione (obbligatorio)
   - Data evento (opzionale)
4. Il Creator prosegue al passo successivo

**Step 2 - Personalizzazione Grafica:**
5. Il Creator può caricare:
   - Logo dell'evento (PNG/JPG)
   - Selezionare 3 colori (primario, secondario, accento) tramite color picker
6. Il sistema mostra un'anteprima della personalizzazione
7. Il Creator prosegue o torna indietro per modificare

**Step 3 - Configurazione Privacy:**
8. Il Creator definisce quali dati richiedere ai partecipanti:
   - Nome (checkbox)
   - Cognome (checkbox)
   - Email (checkbox)
9. Il Creator attiva/disattiva il consenso GDPR obbligatorio
10. Il Creator prosegue

**Step 4 - Importazione Domande:**
11. Il Creator inserisce il link al Google Form contenente le domande
12. Il sistema importa i dati dal form:
    - Testo domande
    - Risposte (corretta + errate)
    - Livello di difficoltà
    - Link a media (YouTube)
13. Il sistema mostra un riepilogo delle domande importate
14. Il Creator può riordinare le domande o rimuoverne alcune

**Step 5 - Configurazione Classifica:**
15. Il Creator definisce:
    - Visualizzazione nomi: completo o solo iniziali
    - Numero di posizioni visibili: Top 10 / Top 20 / Tutti
16. Il Creator salva come bozza o pubblica direttamente

**Postcondizione:** Il quiz è creato (in bozza o pubblicato)

---

#### UF-C03: Pubblicazione Quiz e Generazione Codici Accesso

**Attore:** Creator dell'evento
**Precondizione:** Esiste un quiz in stato "bozza"
**Obiettivo:** Rendere il quiz accessibile ai partecipanti

1. Dalla lista quiz, il Creator seleziona un quiz in bozza
2. Il Creator clicca "Pubblica"
3. Il sistema chiede conferma: "Una volta pubblicato, il quiz sarà accessibile. Confermi?"
4. Il Creator conferma
5. Il sistema:
   - Cambia lo stato del quiz in "pubblicato"
   - Genera automaticamente un codice stanza univoco (es. "EVT-2024-ABC")
   - Genera un QR code che punta all'URL del quiz
6. Il sistema mostra al Creator:
   - Il codice stanza da comunicare verbalmente
   - Il QR code scaricabile (PNG ad alta risoluzione)
   - L'URL diretto al quiz
7. Il Creator può scaricare il QR code o copiare il codice stanza

**Postcondizione:** Il quiz è attivo e i partecipanti possono accedervi

---

#### UF-C04: Monitoraggio Risultati in Tempo Reale

**Attore:** Creator dell'evento
**Precondizione:** Il quiz è pubblicato; almeno un partecipante ha iniziato
**Obiettivo:** Visualizzare l'andamento del quiz durante l'evento

1. Dalla Dashboard, il Creator seleziona il quiz attivo
2. Il Creator accede alla sezione "Monitor Live"
3. Il sistema mostra in tempo reale:
   - Numero di partecipanti attivi in quel momento
   - Numero di quiz completati
   - Punteggio medio corrente
   - Classifica aggiornata live
4. La pagina si aggiorna automaticamente ogni 5 secondi
5. Il Creator può visualizzare:
   - Grafico a barre con % risposte corrette per domanda
   - Lista partecipanti con stato (in corso/completato)
6. Il Creator può proiettare la classifica su schermo esterno (modalità presentazione)

**Postcondizione:** Il Creator ha visibilità real-time sull'andamento

---

#### UF-C05: Export Report Finale

**Attore:** Creator dell'evento
**Precondizione:** Il quiz è concluso; esistono partecipazioni registrate
**Obiettivo:** Scaricare il report completo dell'evento

1. Dalla lista quiz, il Creator seleziona il quiz concluso
2. Il Creator accede alla sezione "Report"
3. Il sistema mostra il riepilogo finale:
   - Totale partecipanti
   - Punteggio medio, minimo e massimo
   - Tempo medio di completamento
   - Domanda con più errori
   - Domanda con più risposte corrette
4. Il Creator seleziona il formato di export:
   - **CSV:** dati grezzi per elaborazione esterna
   - **PDF:** report formattato con grafici
   - **Email:** invio diretto a un indirizzo specificato
5. Il Creator clicca "Esporta"
6. Il sistema genera il file e avvia il download (o invia l'email)

**Postcondizione:** Il Creator possiede il report dell'evento

---

### 2.3 User Flow: Partecipante (Utente Finale)

#### UF-P01: Accesso al Quiz tramite QR Code

**Attore:** Partecipante all'evento
**Precondizione:** Il quiz è pubblicato e attivo
**Obiettivo:** Iniziare il quiz formativo

1. Il partecipante inquadra il QR code mostrato durante l'evento
2. Il dispositivo apre il browser all'URL del quiz
3. Il sistema mostra la schermata di benvenuto con:
   - Logo e colori personalizzati dell'evento
   - Titolo e descrizione del quiz
   - Pulsante "Inizia"
4. Il partecipante clicca "Inizia"
5. Il sistema mostra il form di inserimento dati (secondo configurazione):
   - Nome (se richiesto)
   - Cognome (se richiesto)
   - Email (se richiesta)
6. Se il GDPR è attivo, viene mostrato il checkbox di consenso obbligatorio
7. Il partecipante compila i campi e accetta le condizioni
8. Il partecipante clicca "Avvia Quiz"
9. Il sistema registra il partecipante e avvia il quiz

**Postcondizione:** Il partecipante è registrato e il quiz inizia

---

#### UF-P02: Accesso al Quiz tramite Codice Stanza

**Attore:** Partecipante all'evento
**Precondizione:** Il partecipante conosce il codice stanza comunicato dall'organizzatore
**Obiettivo:** Accedere al quiz senza QR code

1. Il partecipante accede alla homepage della piattaforma
2. Il sistema mostra un campo "Inserisci codice stanza"
3. Il partecipante digita il codice (es. "EVT-2024-ABC")
4. Il partecipante clicca "Accedi"
5. Il sistema valida il codice:
   - **Se valido:** reindirizza alla schermata di benvenuto del quiz
   - **Se non valido:** mostra errore "Codice non trovato"
   - **Se quiz non attivo:** mostra messaggio "Il quiz non è ancora disponibile"
6. Da qui il flusso prosegue come UF-P01 dal punto 4

**Postcondizione:** Il partecipante accede al quiz

---

#### UF-P03: Svolgimento del Quiz - Risposta Corretta

**Attore:** Partecipante
**Precondizione:** Il partecipante ha avviato il quiz
**Obiettivo:** Rispondere correttamente a una domanda

1. Il sistema mostra la domanda corrente con:
   - Numero domanda / totale (es. "3/15")
   - Testo della domanda
   - Eventuale immagine o video allegato
   - Le opzioni di risposta (minimo 3)
   - Timer countdown (se configurato)
2. Il partecipante legge la domanda e valuta le opzioni
3. Il partecipante seleziona la risposta che ritiene corretta
4. Il partecipante clicca "Conferma"
5. Il sistema verifica la risposta
6. **Risposta corretta:** il sistema mostra:
   - Feedback visivo positivo (es. bordo verde, icona check)
   - Breve messaggio di conferma dell'AI: "Corretto! [breve spiegazione]"
   - Punti guadagnati (es. "+10 punti")
   - Punteggio totale aggiornato
7. Dopo 2-3 secondi, il sistema passa automaticamente alla domanda successiva

**Postcondizione:** Il punteggio è incrementato; il partecipante procede

---

#### UF-P04: Svolgimento del Quiz - Risposta Errata

**Attore:** Partecipante
**Precondizione:** Il partecipante ha avviato il quiz
**Obiettivo:** Comprendere l'errore grazie al feedback AI

1. Il partecipante visualizza la domanda (come UF-P03, punti 1-4)
2. Il partecipante seleziona una risposta e conferma
3. Il sistema verifica la risposta
4. **Risposta errata:** il sistema mostra:
   - Feedback visivo negativo (es. bordo rosso, icona X)
   - La risposta corretta evidenziata
   - Feedback educativo dell'AI (500-600 token max):
     - Spiegazione del perché la risposta scelta è errata
     - Razionale scientifico della risposta corretta
     - Tono professionale da medico chirurgo
   - Punti persi (es. "-5 punti")
   - Punteggio totale aggiornato
5. Il partecipante legge il feedback formativo
6. Il partecipante clicca "Prosegui" per passare alla domanda successiva

**Postcondizione:** Il partecipante ha appreso dall'errore; procede con il quiz

---

#### UF-P05: Scadenza Timer senza Risposta

**Attore:** Partecipante
**Precondizione:** La domanda ha un timer attivo; il tempo è scaduto
**Obiettivo:** Gestire la mancata risposta

1. Il partecipante visualizza la domanda con timer attivo
2. Il timer raggiunge lo zero prima della selezione
3. Il sistema:
   - Blocca la possibilità di rispondere
   - Considera la domanda come "non risposta" (equivalente a errata)
   - Mostra messaggio: "Tempo scaduto!"
   - Mostra la risposta corretta
   - Fornisce feedback AI abbreviato
   - Applica la penalità punti
4. Il sistema passa automaticamente alla domanda successiva

**Postcondizione:** La domanda è registrata come errata; il quiz prosegue

---

#### UF-P06: Completamento Quiz e Visualizzazione Risultati

**Attore:** Partecipante
**Precondizione:** Il partecipante ha risposto a tutte le domande
**Obiettivo:** Visualizzare il risultato finale

1. Dopo l'ultima domanda, il sistema mostra la schermata "Quiz Completato"
2. Il sistema elabora e mostra:
   - Punteggio finale totale
   - Numero risposte corrette / totale domande
   - Percentuale di successo
   - Feedback finale personalizzato dell'AI basato sulla performance:
     - **Ottimo (>80%):** messaggio di congratulazioni
     - **Buono (60-80%):** messaggio di incoraggiamento
     - **Da migliorare (<60%):** messaggio motivazionale con suggerimenti
3. Se configurato, il sistema mostra un badge di completamento
4. Il sistema mostra due pulsanti:
   - "Vedi Classifica"
   - "Chiudi"
5. Il partecipante può scegliere di vedere la classifica

**Postcondizione:** Il quiz è completato; i dati sono salvati

---

#### UF-P07: Consultazione Classifica Pubblica

**Attore:** Partecipante o visitatore dell'evento
**Precondizione:** Il quiz ha almeno un partecipante che ha completato
**Obiettivo:** Visualizzare la classifica dei partecipanti

1. L'utente accede alla classifica tramite:
   - Pulsante "Vedi Classifica" dopo il quiz
   - QR code/codice stanza + selezione "Classifica"
2. Il sistema mostra la classifica con:
   - Posizione in classifica
   - Nome/nickname (secondo privacy configurata)
   - Punteggio
3. La propria posizione (se partecipante) è evidenziata
4. La classifica si aggiorna in tempo reale
5. L'utente può:
   - Scorrere la lista (se visibile oltre il top N)
   - Tornare alla home del quiz
   - Condividere il proprio risultato (opzionale)

**Postcondizione:** L'utente ha consultato la classifica

---

### 2.4 User Flow: Sistema (Automatici)

#### UF-S01: Importazione Domande da Google Form

**Attore:** Sistema automatico
**Trigger:** Il Creator inserisce un link Google Form valido
**Obiettivo:** Popolare il quiz con le domande dal form

1. Il Creator incolla il link al Google Form
2. Il sistema valida il formato del link
3. Il sistema effettua una richiesta al Google Form/Sheet collegato
4. Il sistema estrae i dati strutturati:
   - Per ogni riga: testo domanda, risposta corretta, risposte errate, difficoltà, link media
5. Il sistema valida i dati:
   - **Se mancano campi obbligatori:** segnala errore specifico
   - **Se link media non valido:** segnala warning (procede comunque)
6. Il sistema crea le entità Domanda e Risposta nel database
7. Il sistema ordina le domande per difficoltà (facili prima, difficili dopo)
8. Il sistema conferma l'importazione al Creator

**Postcondizione:** Le domande sono importate e pronte per il quiz

---

#### UF-S02: Generazione Feedback AI

**Attore:** Sistema automatico
**Trigger:** Il partecipante conferma una risposta
**Obiettivo:** Generare feedback educativo tramite GPT-4 Mini

1. Il sistema riceve la risposta del partecipante
2. Il sistema prepara il prompt per l'AI includendo:
   - Testo della domanda
   - Risposta selezionata
   - Risposta corretta
   - Contesto: "Rispondi come un medico chirurgo professionista"
3. Il sistema invia la richiesta a GPT-4 Mini con:
   - Max tokens: 500-600
   - Temperature: 0.7 (bilanciato)
4. L'AI genera la risposta
5. Il sistema riceve e valida la risposta:
   - **Se risposta vuota o errore:** usa fallback predefinito
   - **Se risposta valida:** procede
6. Il sistema salva il feedback nel record della risposta utente
7. Il sistema mostra il feedback al partecipante

**Postcondizione:** Il feedback è generato, salvato e mostrato

---

## 3. Architettura dei Ruoli

### 3.1 Admin della Piattaforma
- Accesso globale a tutte le funzionalità
- Gestione utenti (creazione account Creator)
- Visualizzazione di tutti gli eventi
- Accesso ai report aggregati
- Attivazione account Creator tramite credenziali (username/password)

### 3.2 Creator dell'Evento
- Cliente che acquista il servizio per un evento specifico
- Accesso a pannello personale dedicato
- Creazione e gestione quiz tramite form
- Monitoraggio risultati in tempo reale
- Accesso ai report del proprio evento

### 3.3 Utente Finale (Partecipante)
- Nessuna registrazione richiesta
- Accesso tramite QR code o codice stanza
- Inserimento dati minimi (nome, cognome, email - configurabile)
- Consenso GDPR (opzionale, configurabile dall'organizzatore)

---

## 4. Struttura del Quiz

### 4.1 Configurazione Base
| Campo | Descrizione | Obbligatorio |
|-------|-------------|--------------|
| Titolo | Nome del quiz | Si |
| Descrizione | Descrizione del quiz | Si |
| Logo | Logo personalizzato | No |
| Colori | 3 colori per personalizzazione grafica | No |

### 4.2 Struttura Domande
Ogni domanda (snodo decisionale) contiene:

| Elemento | Descrizione | Obbligatorio |
|----------|-------------|--------------|
| Testo domanda | Il quesito da porre | Si |
| Risposta corretta | Una sola risposta corretta | Si |
| Risposte errate | Minimo 2 risposte errate | Si |
| Livello difficoltà | Facile/Medio/Difficile | Si |
| Immagine/Video | Contenuto multimediale | No |
| Timer | Tempo limite per rispondere | No |

### 4.3 Sistema di Difficoltà Progressiva
- Le domande sono organizzate in insiemi di difficoltà crescente
- Vengono proposte prima le domande facili, poi quelle difficili
- Più una domanda è complessa, maggiore è il punteggio (positivo o negativo)
- Il percorso si adatta al livello di conoscenza del partecipante

---

## 5. Flusso dell'Applicazione

### 5.1 Flusso Admin

```
[Login Admin]
     |
     v
[Dashboard Admin]
     |
     +---> [Gestione Utenti]
     |         |
     |         +---> Crea Creator
     |         +---> Modifica Creator
     |         +---> Disattiva Creator
     |
     +---> [Visualizza Eventi]
     |         |
     |         +---> Lista tutti gli eventi
     |         +---> Dettaglio evento
     |
     +---> [Report Aggregati]
               |
               +---> Statistiche globali
               +---> Export dati
```

### 5.2 Flusso Creator

```
[Login Creator]
     |
     v
[Dashboard Creator]
     |
     +---> [Crea Quiz]
     |         |
     |         +---> Definisci titolo/descrizione
     |         +---> Aggiungi domande
     |         +---> Configura difficoltà
     |         +---> Aggiungi media (opzionale)
     |         +---> Configura timer (opzionale)
     |         +---> Personalizza grafica
     |         +---> Salva bozza / Pubblica
     |
     +---> [Gestisci Quiz]
     |         |
     |         +---> Modifica quiz
     |         +---> Genera QR code
     |         +---> Genera codice stanza
     |
     +---> [Report]
               |
               +---> Visualizza risultati
               +---> Export (CSV/PDF/Email)
```

### 5.3 Flusso Utente Finale

```
[Scansione QR / Inserimento Codice]
     |
     v
[Inserimento Dati Personali]
(nome, cognome, email - secondo config)
     |
     v
[Accettazione GDPR] (se attivo)
     |
     v
[Inizio Quiz]
     |
     v
+------------------+
|   LOOP DOMANDE   |
+------------------+
     |
     v
[Visualizza Domanda + Media]
     |
     v
[Timer attivo] (se configurato)
     |
     v
[Selezione Risposta]
     |
     +---> [Risposta CORRETTA]
     |         |
     |         +---> Conferma visiva
     |         +---> Assegnazione punti (+)
     |         +---> Prossima domanda
     |
     +---> [Risposta ERRATA]
               |
               +---> Feedback AI (spiegazione)
               +---> Sottrazione punti (-)
               +---> Prossima domanda
     |
     v
[Fine Quiz]
     |
     v
[Schermata Risultati]
     |
     +---> Punteggio totale
     +---> Feedback finale AI
     +---> Badge completamento (opzionale)
     +---> Accesso classifica
```

---

## 6. Integrazione AI

### 6.1 Configurazione
- **Modello**: GPT-4 Mini
- **Token limit**: 500-600 token per risposta
- **Persona**: Medico chirurgo professionista

### 6.2 Comportamento AI
| Scenario | Risposta AI |
|----------|-------------|
| Risposta corretta | Conferma breve |
| Risposta errata | Spiegazione dettagliata del perché la risposta non è corretta |

### 6.3 Stile Comunicativo
- Spiegazioni scientifiche ma accessibili
- Tono professionale da medico
- Focus sull'apprendimento

---

## 7. Sistema Punteggio

### 7.1 Calcolo Punti
```
Punti = Base * Moltiplicatore_Difficoltà

Dove:
- Base = punti per risposta corretta/errata
- Moltiplicatore:
  - Facile: x1
  - Medio: x2
  - Difficile: x3
```

### 7.2 Regole
- Risposta corretta: punti aggiunti
- Risposta errata: punti sottratti
- Il punteggio finale può essere negativo

---

## 8. Classifica Pubblica

### 8.1 Accesso
- Accessibile dallo stesso QR code del quiz
- Nessun login richiesto
- Visualizzabile da tutti i presenti all'evento

### 8.2 Configurazione
| Opzione | Descrizione |
|---------|-------------|
| Visualizzazione nome | Nome completo o nickname |
| Numero classificati | Solo top N o lista completa |
| Aggiornamento | Tempo reale |

### 8.3 Funzionalità
- Mostra nomi/nickname e punteggi
- Aggiornamento in tempo reale
- Elemento ludico per incentivare partecipazione

---

## 9. Sistema Report

### 9.1 Metriche Disponibili
| Metrica | Descrizione |
|---------|-------------|
| Numero partecipanti | Totale utenti che hanno completato |
| Punteggi medi | Media punteggi per quiz |
| Andamento risposte | Statistiche per singola domanda |
| Risultati individuali | Dettaglio per partecipante |

### 9.2 Export
- **CSV**: Dati grezzi per analisi
- **PDF**: Report formattato
- **Email**: Invio diretto report

### 9.3 Temporalità
- Monitoraggio in tempo reale
- Report finale post-evento

---

## 10. Gestione Contenuti (Google Form)

### 10.1 Flusso Importazione
```
[Google Form]
     |
     +---> Domande
     +---> Risposte
     +---> Difficoltà
     +---> Link media (YouTube privato)
     |
     v
[Sistema importazione]
     |
     v
[Generazione Quiz in piattaforma]
```

### 10.2 Vantaggi
- Nessuna dashboard interna complessa
- Modifica rapida: aggiorna form e rigenera
- Gestione media tramite link YouTube privati

---

## 11. Personalizzazione Grafica

### 11.1 Elementi Personalizzabili
| Elemento | Tipo |
|----------|------|
| Logo | Immagine (PNG/JPG) |
| Colore primario | HEX/RGB |
| Colore secondario | HEX/RGB |
| Colore accento | HEX/RGB |

---

## 12. Requisiti Tecnici

### 12.1 Performance
- Scalabilità: supporto per centinaia di accessi simultanei
- Responsività: ottimizzato per mobile (QR code)

### 12.2 Hosting
- Cloud hosting (AWS, Render, o simili)
- Scalabilità automatica

### 12.3 Costi Variabili
| Voce | Descrizione |
|------|-------------|
| Hosting | Costo server mensile |
| AI Tokens | Costo per utilizzo GPT-4 Mini |

---

## 13. Funzionalità Future (Roadmap)

| Priorità | Funzionalità |
|----------|--------------|
| Alta | Salvataggio modelli di quiz |
| Media | Supporto multilingua (IT/EN) |

---

## 14. Diagramma Entità

```
+------------------+
|      ADMIN       |
+------------------+
| - id             |
| - username       |
| - password       |
| - email          |
+------------------+
        |
        | gestisce
        v
+------------------+
|     CREATOR      |
+------------------+
| - id             |
| - username       |
| - password       |
| - email          |
| - attivo         |
+------------------+
        |
        | crea
        v
+------------------+
|      QUIZ        |
+------------------+
| - id             |
| - titolo         |
| - descrizione    |
| - stato (bozza/  |
|   pubblicato)    |
| - qr_code        |
| - codice_stanza  |
| - logo           |
| - colori[]       |
| - gdpr_attivo    |
| - campi_richiesti|
+------------------+
        |
        | contiene
        v
+------------------+
|     DOMANDA      |
+------------------+
| - id             |
| - testo          |
| - difficolta     |
| - punti          |
| - timer          |
| - media_url      |
| - ordine         |
+------------------+
        |
        | ha
        v
+------------------+
|     RISPOSTA     |
+------------------+
| - id             |
| - testo          |
| - corretta       |
+------------------+

+------------------+
|   PARTECIPANTE   |
+------------------+
| - id             |
| - nome           |
| - cognome        |
| - email          |
| - quiz_id        |
| - punteggio      |
| - completato     |
| - timestamp      |
+------------------+

+------------------+
| RISPOSTA_UTENTE  |
+------------------+
| - id             |
| - partecipante_id|
| - domanda_id     |
| - risposta_id    |
| - corretta       |
| - tempo_risposta |
| - feedback_ai    |
+------------------+
```

---

## 15. API Endpoints (Bozza)

### Auth
- `POST /api/auth/login` - Login Admin/Creator
- `POST /api/auth/logout` - Logout

### Admin
- `GET /api/admin/creators` - Lista Creator
- `POST /api/admin/creators` - Crea Creator
- `PUT /api/admin/creators/:id` - Modifica Creator
- `DELETE /api/admin/creators/:id` - Disattiva Creator
- `GET /api/admin/reports` - Report aggregati

### Creator
- `GET /api/quiz` - Lista quiz
- `POST /api/quiz` - Crea quiz
- `PUT /api/quiz/:id` - Modifica quiz
- `DELETE /api/quiz/:id` - Elimina quiz
- `POST /api/quiz/:id/publish` - Pubblica quiz
- `GET /api/quiz/:id/qrcode` - Genera QR
- `GET /api/quiz/:id/report` - Report quiz

### Pubblico
- `GET /api/public/quiz/:code` - Accesso quiz via codice
- `POST /api/public/quiz/:id/start` - Inizia quiz
- `POST /api/public/quiz/:id/answer` - Invia risposta
- `GET /api/public/quiz/:id/leaderboard` - Classifica

### AI
- `POST /api/ai/feedback` - Genera feedback AI

---

*Documento generato per il progetto Clinical Quiz by SVP*
