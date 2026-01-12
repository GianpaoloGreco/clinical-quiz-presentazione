#!/usr/bin/env python3
"""
Clinical Quiz - Generatore Diagrammi di Flusso
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Configurazione colori
COLORS = {
    'start_end': '#2E7D32',      # Verde scuro
    'process': '#1976D2',         # Blu
    'decision': '#F57C00',        # Arancione
    'io': '#7B1FA2',              # Viola
    'connector': '#424242',       # Grigio scuro
    'background': '#FAFAFA',      # Grigio chiaro
    'text': '#212121',            # Nero
    'text_light': '#FFFFFF',      # Bianco
    'arrow': '#616161',           # Grigio
    'highlight': '#E53935',       # Rosso
    'success': '#43A047',         # Verde
}

def draw_rounded_box(ax, x, y, width, height, color, text, text_color='white', fontsize=9):
    """Disegna un box arrotondato con testo"""
    box = FancyBboxPatch((x - width/2, y - height/2), width, height,
                         boxstyle="round,pad=0.02,rounding_size=0.1",
                         facecolor=color, edgecolor='none', linewidth=0)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize,
            color=text_color, fontweight='bold', wrap=True)

def draw_diamond(ax, x, y, size, color, text, text_color='white', fontsize=8):
    """Disegna un rombo (decisione) con testo"""
    diamond = plt.Polygon([(x, y + size/2), (x + size/2, y),
                           (x, y - size/2), (x - size/2, y)],
                          facecolor=color, edgecolor='none')
    ax.add_patch(diamond)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize,
            color=text_color, fontweight='bold', wrap=True)

def draw_arrow(ax, start, end, color='#616161'):
    """Disegna una freccia"""
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5))

def draw_arrow_curved(ax, start, end, color='#616161', connectionstyle="arc3,rad=0.3"):
    """Disegna una freccia curva"""
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5,
                               connectionstyle=connectionstyle))

def create_admin_flow():
    """Crea il diagramma del flusso Admin"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 16))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 16)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor(COLORS['background'])
    fig.patch.set_facecolor(COLORS['background'])

    # Titolo
    ax.text(7, 15.5, 'FLUSSO ADMIN', ha='center', va='center',
            fontsize=16, fontweight='bold', color=COLORS['text'])
    ax.text(7, 15, 'Clinical Quiz Platform', ha='center', va='center',
            fontsize=10, color=COLORS['arrow'])

    # START
    draw_rounded_box(ax, 7, 14, 2.5, 0.6, COLORS['start_end'], 'START', fontsize=10)

    # Login
    draw_rounded_box(ax, 7, 12.8, 3, 0.7, COLORS['io'], 'Accesso URL\n/admin')
    draw_arrow(ax, (7, 13.7), (7, 13.15))

    # Form Login
    draw_rounded_box(ax, 7, 11.6, 3.5, 0.7, COLORS['process'], 'Inserimento\nCredenziali')
    draw_arrow(ax, (7, 12.45), (7, 11.95))

    # Validazione
    draw_diamond(ax, 7, 10.3, 1.2, COLORS['decision'], 'Valide?')
    draw_arrow(ax, (7, 11.25), (7, 10.9))

    # Errore
    draw_rounded_box(ax, 10, 10.3, 2.5, 0.6, COLORS['highlight'], 'Errore Login')
    draw_arrow(ax, (7.6, 10.3), (8.75, 10.3))
    ax.text(8.2, 10.5, 'NO', fontsize=8, color=COLORS['arrow'])
    draw_arrow_curved(ax, (10, 10.6), (7, 12.45), connectionstyle="arc3,rad=-0.3")

    # Dashboard
    draw_rounded_box(ax, 7, 8.8, 3.5, 0.8, COLORS['success'], 'DASHBOARD\nADMIN')
    draw_arrow(ax, (7, 9.7), (7, 9.2))
    ax.text(7.2, 9.5, 'SI', fontsize=8, color=COLORS['arrow'])

    # Tre opzioni
    draw_rounded_box(ax, 2.5, 7, 2.8, 0.7, COLORS['process'], 'Gestione\nUtenti')
    draw_rounded_box(ax, 7, 7, 2.8, 0.7, COLORS['process'], 'Visualizza\nEventi')
    draw_rounded_box(ax, 11.5, 7, 2.8, 0.7, COLORS['process'], 'Report\nAggregati')

    draw_arrow(ax, (5.5, 8.4), (2.5, 7.35))
    draw_arrow(ax, (7, 8.4), (7, 7.35))
    draw_arrow(ax, (8.5, 8.4), (11.5, 7.35))

    # Sotto-opzioni Gestione Utenti
    draw_rounded_box(ax, 1, 5.5, 2.2, 0.6, COLORS['io'], 'Crea\nCreator')
    draw_rounded_box(ax, 2.5, 5.5, 2.2, 0.6, COLORS['io'], 'Modifica\nCreator')
    draw_rounded_box(ax, 4, 5.5, 2.2, 0.6, COLORS['io'], 'Disattiva\nCreator')

    draw_arrow(ax, (1.8, 6.65), (1, 5.8))
    draw_arrow(ax, (2.5, 6.65), (2.5, 5.8))
    draw_arrow(ax, (3.2, 6.65), (4, 5.8))

    # Sotto-opzioni Eventi
    draw_rounded_box(ax, 6, 5.5, 2.2, 0.6, COLORS['io'], 'Lista\nEventi')
    draw_rounded_box(ax, 8, 5.5, 2.2, 0.6, COLORS['io'], 'Dettaglio\nEvento')

    draw_arrow(ax, (6.5, 6.65), (6, 5.8))
    draw_arrow(ax, (7.5, 6.65), (8, 5.8))

    # Sotto-opzioni Report
    draw_rounded_box(ax, 10.5, 5.5, 2.2, 0.6, COLORS['io'], 'Statistiche\nGlobali')
    draw_rounded_box(ax, 12.5, 5.5, 2.2, 0.6, COLORS['io'], 'Export\nDati')

    draw_arrow(ax, (11, 6.65), (10.5, 5.8))
    draw_arrow(ax, (12, 6.65), (12.5, 5.8))

    # Flusso Crea Creator dettagliato
    ax.text(2.5, 4.6, 'Dettaglio: Crea Creator', ha='center', fontsize=9,
            fontweight='bold', color=COLORS['text'])

    draw_rounded_box(ax, 2.5, 4, 2.5, 0.5, COLORS['process'], 'Form Dati')
    draw_arrow(ax, (1, 5.2), (2.5, 4.25))

    draw_diamond(ax, 2.5, 3, 1, COLORS['decision'], 'Validi?')
    draw_arrow(ax, (2.5, 3.75), (2.5, 3.5))

    draw_rounded_box(ax, 2.5, 2, 2.5, 0.5, COLORS['success'], 'Account Creato')
    draw_arrow(ax, (2.5, 2.5), (2.5, 2.25))
    ax.text(2.7, 2.7, 'SI', fontsize=8, color=COLORS['arrow'])

    draw_rounded_box(ax, 5, 3, 2, 0.5, COLORS['highlight'], 'Errore')
    draw_arrow(ax, (3, 3), (4, 3))
    ax.text(3.3, 3.15, 'NO', fontsize=8, color=COLORS['arrow'])

    # Legenda
    ax.text(10, 4.2, 'LEGENDA', ha='center', fontsize=10, fontweight='bold', color=COLORS['text'])
    draw_rounded_box(ax, 9, 3.5, 1.5, 0.4, COLORS['start_end'], 'Start/End', fontsize=7)
    draw_rounded_box(ax, 11, 3.5, 1.5, 0.4, COLORS['process'], 'Processo', fontsize=7)
    draw_rounded_box(ax, 9, 2.8, 1.5, 0.4, COLORS['io'], 'Input/Output', fontsize=7)
    draw_diamond(ax, 11, 2.8, 0.5, COLORS['decision'], '?', fontsize=7)
    ax.text(11.5, 2.8, 'Decisione', fontsize=7, color=COLORS['text'])

    # END
    draw_rounded_box(ax, 7, 1, 2.5, 0.6, COLORS['start_end'], 'END', fontsize=10)

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/flow_admin.svg',
                format='svg', bbox_inches='tight', facecolor=COLORS['background'])
    plt.close()
    print("✓ Flow Admin generato (SVG)")


def create_creator_flow():
    """Crea il diagramma del flusso Creator"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 20))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 20)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor(COLORS['background'])
    fig.patch.set_facecolor(COLORS['background'])

    # Titolo
    ax.text(8, 19.5, 'FLUSSO CREATOR', ha='center', va='center',
            fontsize=16, fontweight='bold', color=COLORS['text'])
    ax.text(8, 19, 'Organizzatore Evento', ha='center', va='center',
            fontsize=10, color=COLORS['arrow'])

    # START
    draw_rounded_box(ax, 8, 18, 2.5, 0.6, COLORS['start_end'], 'START', fontsize=10)

    # Login
    draw_rounded_box(ax, 8, 16.8, 3, 0.7, COLORS['io'], 'Login con\nCredenziali')
    draw_arrow(ax, (8, 17.7), (8, 17.15))

    # Dashboard
    draw_rounded_box(ax, 8, 15.5, 3.5, 0.8, COLORS['success'], 'DASHBOARD\nCREATOR')
    draw_arrow(ax, (8, 16.45), (8, 15.9))

    # Opzioni principali
    draw_rounded_box(ax, 3, 13.8, 2.8, 0.7, COLORS['process'], 'Crea\nQuiz')
    draw_rounded_box(ax, 8, 13.8, 2.8, 0.7, COLORS['process'], 'Gestisci\nQuiz')
    draw_rounded_box(ax, 13, 13.8, 2.8, 0.7, COLORS['process'], 'Report')

    draw_arrow(ax, (6, 15.1), (3, 14.15))
    draw_arrow(ax, (8, 15.1), (8, 14.15))
    draw_arrow(ax, (10, 15.1), (13, 14.15))

    # === WIZARD CREAZIONE QUIZ ===
    ax.text(3, 12.8, 'WIZARD CREAZIONE QUIZ', ha='center', fontsize=9,
            fontweight='bold', color=COLORS['text'])

    # Step 1
    draw_rounded_box(ax, 3, 12, 3, 0.6, COLORS['process'], 'Step 1: Info Base')
    draw_arrow(ax, (3, 13.45), (3, 12.3))
    ax.text(0.5, 12, '• Titolo\n• Descrizione\n• Data evento', fontsize=7,
            va='center', color=COLORS['text'])

    # Step 2
    draw_rounded_box(ax, 3, 10.8, 3, 0.6, COLORS['process'], 'Step 2: Grafica')
    draw_arrow(ax, (3, 11.7), (3, 11.1))
    ax.text(0.5, 10.8, '• Logo\n• 3 Colori', fontsize=7,
            va='center', color=COLORS['text'])

    # Step 3
    draw_rounded_box(ax, 3, 9.6, 3, 0.6, COLORS['process'], 'Step 3: Privacy')
    draw_arrow(ax, (3, 10.5), (3, 9.9))
    ax.text(0.5, 9.6, '• Campi richiesti\n• GDPR', fontsize=7,
            va='center', color=COLORS['text'])

    # Step 4
    draw_rounded_box(ax, 3, 8.4, 3, 0.6, COLORS['process'], 'Step 4: Import')
    draw_arrow(ax, (3, 9.3), (3, 8.7))
    ax.text(0.5, 8.4, '• Link Google Form\n• Domande', fontsize=7,
            va='center', color=COLORS['text'])

    # Step 5
    draw_rounded_box(ax, 3, 7.2, 3, 0.6, COLORS['process'], 'Step 5: Classifica')
    draw_arrow(ax, (3, 8.1), (3, 7.5))
    ax.text(0.5, 7.2, '• Visualizzazione\n• Top N', fontsize=7,
            va='center', color=COLORS['text'])

    # Decisione Salva
    draw_diamond(ax, 3, 5.8, 1.2, COLORS['decision'], 'Azione?')
    draw_arrow(ax, (3, 6.9), (3, 6.4))

    # Bozza
    draw_rounded_box(ax, 1, 4.5, 2, 0.5, COLORS['io'], 'Salva\nBozza')
    draw_arrow(ax, (2.4, 5.8), (1, 4.75))
    ax.text(1.5, 5.3, 'Bozza', fontsize=7, color=COLORS['arrow'])

    # Pubblica
    draw_rounded_box(ax, 5, 4.5, 2, 0.5, COLORS['success'], 'Pubblica')
    draw_arrow(ax, (3.6, 5.8), (5, 4.75))
    ax.text(4.2, 5.3, 'Pubblica', fontsize=7, color=COLORS['arrow'])

    # Genera QR
    draw_rounded_box(ax, 5, 3.3, 2.5, 0.5, COLORS['process'], 'Genera QR\n+ Codice')
    draw_arrow(ax, (5, 4.25), (5, 3.55))

    # === GESTISCI QUIZ ===
    ax.text(8, 12.8, 'GESTIONE QUIZ', ha='center', fontsize=9,
            fontweight='bold', color=COLORS['text'])

    draw_rounded_box(ax, 8, 12, 2.5, 0.5, COLORS['io'], 'Modifica')
    draw_rounded_box(ax, 8, 11, 2.5, 0.5, COLORS['io'], 'QR Code')
    draw_rounded_box(ax, 8, 10, 2.5, 0.5, COLORS['io'], 'Codice Stanza')

    draw_arrow(ax, (8, 13.45), (8, 12.25))
    draw_arrow(ax, (8, 11.75), (8, 11.25))
    draw_arrow(ax, (8, 10.75), (8, 10.25))

    # Monitor Live
    draw_rounded_box(ax, 8, 8.5, 3, 0.7, COLORS['process'], 'Monitor\nLive')
    draw_arrow(ax, (8, 9.75), (8, 8.85))

    ax.text(10.5, 8.5, '• Partecipanti attivi\n• Quiz completati\n• Classifica live',
            fontsize=7, va='center', color=COLORS['text'])

    # === REPORT ===
    ax.text(13, 12.8, 'REPORT', ha='center', fontsize=9,
            fontweight='bold', color=COLORS['text'])

    draw_rounded_box(ax, 13, 12, 2.8, 0.5, COLORS['io'], 'Riepilogo')
    draw_arrow(ax, (13, 13.45), (13, 12.25))

    ax.text(15, 12, '• Totale partecipanti\n• Punteggio medio\n• Statistiche',
            fontsize=7, va='center', color=COLORS['text'])

    draw_diamond(ax, 13, 10.5, 1.2, COLORS['decision'], 'Export?')
    draw_arrow(ax, (13, 11.75), (13, 11.1))

    draw_rounded_box(ax, 11, 9, 1.8, 0.5, COLORS['io'], 'CSV')
    draw_rounded_box(ax, 13, 9, 1.8, 0.5, COLORS['io'], 'PDF')
    draw_rounded_box(ax, 15, 9, 1.8, 0.5, COLORS['io'], 'Email')

    draw_arrow(ax, (12.4, 10.5), (11, 9.25))
    draw_arrow(ax, (13, 9.9), (13, 9.25))
    draw_arrow(ax, (13.6, 10.5), (15, 9.25))

    # END
    draw_rounded_box(ax, 8, 1.5, 2.5, 0.6, COLORS['start_end'], 'END', fontsize=10)

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/flow_creator.svg',
                format='svg', bbox_inches='tight', facecolor=COLORS['background'])
    plt.close()
    print("✓ Flow Creator generato (SVG)")


def create_participant_flow():
    """Crea il diagramma del flusso Partecipante"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 22))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 22)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor(COLORS['background'])
    fig.patch.set_facecolor(COLORS['background'])

    # Titolo
    ax.text(7, 21.5, 'FLUSSO PARTECIPANTE', ha='center', va='center',
            fontsize=16, fontweight='bold', color=COLORS['text'])
    ax.text(7, 21, 'Utente Finale', ha='center', va='center',
            fontsize=10, color=COLORS['arrow'])

    # START
    draw_rounded_box(ax, 7, 20, 2.5, 0.6, COLORS['start_end'], 'START', fontsize=10)

    # Accesso
    draw_diamond(ax, 7, 18.5, 1.5, COLORS['decision'], 'Accesso?')
    draw_arrow(ax, (7, 19.7), (7, 19.25))

    draw_rounded_box(ax, 4, 17.3, 2.5, 0.6, COLORS['io'], 'Scansiona\nQR Code')
    draw_rounded_box(ax, 10, 17.3, 2.5, 0.6, COLORS['io'], 'Inserisci\nCodice')

    draw_arrow(ax, (6.25, 18.5), (4, 17.6))
    draw_arrow(ax, (7.75, 18.5), (10, 17.6))
    ax.text(5, 18.3, 'QR', fontsize=8, color=COLORS['arrow'])
    ax.text(8.5, 18.3, 'Codice', fontsize=8, color=COLORS['arrow'])

    # Validazione codice
    draw_diamond(ax, 10, 16, 1.2, COLORS['decision'], 'Valido?')
    draw_arrow(ax, (10, 17), (10, 16.6))

    draw_rounded_box(ax, 12.5, 16, 2, 0.5, COLORS['highlight'], 'Errore')
    draw_arrow(ax, (10.6, 16), (11.5, 16))
    ax.text(10.9, 16.2, 'NO', fontsize=8, color=COLORS['arrow'])

    # Schermata benvenuto
    draw_rounded_box(ax, 7, 14.5, 3.5, 0.8, COLORS['process'], 'Schermata\nBenvenuto')
    draw_arrow(ax, (4, 17), (7, 14.9))
    draw_arrow(ax, (10, 15.4), (7, 14.9))
    ax.text(9.5, 15.6, 'SI', fontsize=8, color=COLORS['arrow'])

    # Form dati
    draw_rounded_box(ax, 7, 13.2, 3, 0.6, COLORS['io'], 'Inserimento Dati\n(Nome/Email)')
    draw_arrow(ax, (7, 14.1), (7, 13.5))

    # GDPR
    draw_diamond(ax, 7, 11.8, 1.2, COLORS['decision'], 'GDPR?')
    draw_arrow(ax, (7, 12.9), (7, 12.4))

    draw_rounded_box(ax, 10, 11.8, 2.5, 0.5, COLORS['io'], 'Consenso\nObbligatorio')
    draw_arrow(ax, (7.6, 11.8), (8.75, 11.8))
    ax.text(8, 12, 'Attivo', fontsize=8, color=COLORS['arrow'])

    # Avvia Quiz
    draw_rounded_box(ax, 7, 10.3, 3, 0.7, COLORS['success'], 'AVVIA QUIZ')
    draw_arrow(ax, (7, 11.2), (7, 10.65))
    draw_arrow(ax, (10, 11.55), (7, 10.65))

    # Loop domande
    ax.add_patch(FancyBboxPatch((2.5, 4), 9, 5.5, boxstyle="round,pad=0.02,rounding_size=0.2",
                                facecolor='#E3F2FD', edgecolor=COLORS['process'], linewidth=2))
    ax.text(7, 9.2, 'LOOP DOMANDE', ha='center', fontsize=10, fontweight='bold', color=COLORS['process'])

    # Mostra domanda
    draw_rounded_box(ax, 7, 8.3, 3.5, 0.6, COLORS['process'], 'Mostra Domanda\n+ Media + Timer')
    draw_arrow(ax, (7, 9.95), (7, 8.6))

    # Selezione risposta
    draw_rounded_box(ax, 7, 7.2, 3, 0.5, COLORS['io'], 'Seleziona Risposta')
    draw_arrow(ax, (7, 8), (7, 7.45))

    # Verifica
    draw_diamond(ax, 7, 6, 1.3, COLORS['decision'], 'Corretta?')
    draw_arrow(ax, (7, 6.95), (7, 6.65))

    # Risposta corretta
    draw_rounded_box(ax, 4, 5, 2.5, 0.6, COLORS['success'], 'Feedback\nPositivo')
    draw_arrow(ax, (6.35, 6), (4, 5.3))
    ax.text(5, 5.8, 'SI', fontsize=8, color=COLORS['arrow'])

    draw_rounded_box(ax, 4, 4.2, 2, 0.4, COLORS['success'], '+Punti')
    draw_arrow(ax, (4, 4.7), (4, 4.4))

    # Risposta errata
    draw_rounded_box(ax, 10, 5, 2.5, 0.6, COLORS['highlight'], 'Feedback AI\nEducativo')
    draw_arrow(ax, (7.65, 6), (10, 5.3))
    ax.text(8.5, 5.8, 'NO', fontsize=8, color=COLORS['arrow'])

    draw_rounded_box(ax, 10, 4.2, 2, 0.4, COLORS['highlight'], '-Punti')
    draw_arrow(ax, (10, 4.7), (10, 4.4))

    # Prossima domanda
    draw_diamond(ax, 7, 3, 1.3, COLORS['decision'], 'Altre\ndomande?')
    draw_arrow(ax, (4, 3.95), (7, 3.65))
    draw_arrow(ax, (10, 3.95), (7, 3.65))

    # Loop back
    draw_arrow_curved(ax, (6.35, 3), (5, 8.3), connectionstyle="arc3,rad=0.5")
    ax.text(3.5, 5.5, 'SI', fontsize=8, color=COLORS['arrow'])

    # Fine quiz
    draw_rounded_box(ax, 7, 1.8, 3.5, 0.8, COLORS['process'], 'RISULTATI\nFINALI')
    draw_arrow(ax, (7.65, 3), (7, 2.2))
    ax.text(7.8, 2.7, 'NO', fontsize=8, color=COLORS['arrow'])

    ax.text(11, 1.8, '• Punteggio totale\n• % Successo\n• Feedback AI finale\n• Badge',
            fontsize=7, va='center', color=COLORS['text'])

    # Classifica
    draw_rounded_box(ax, 7, 0.6, 3, 0.6, COLORS['io'], 'Visualizza\nClassifica')
    draw_arrow(ax, (7, 1.4), (7, 0.9))

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/flow_participant.svg',
                format='svg', bbox_inches='tight', facecolor=COLORS['background'])
    plt.close()
    print("✓ Flow Partecipante generato (SVG)")


def create_system_flow():
    """Crea il diagramma del flusso Sistema (AI + Import)"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor(COLORS['background'])
    fig.patch.set_facecolor(COLORS['background'])

    # Titolo
    ax.text(8, 11.5, 'FLUSSI SISTEMA AUTOMATICI', ha='center', va='center',
            fontsize=16, fontweight='bold', color=COLORS['text'])

    # === IMPORTAZIONE GOOGLE FORM ===
    ax.text(4, 10.5, 'IMPORTAZIONE GOOGLE FORM', ha='center', fontsize=11,
            fontweight='bold', color=COLORS['process'])

    draw_rounded_box(ax, 4, 9.5, 3, 0.6, COLORS['io'], 'Link Google Form')

    draw_rounded_box(ax, 4, 8.3, 3, 0.6, COLORS['process'], 'Valida Formato')
    draw_arrow(ax, (4, 9.2), (4, 8.6))

    draw_rounded_box(ax, 4, 7.1, 3, 0.6, COLORS['process'], 'Fetch Dati')
    draw_arrow(ax, (4, 8), (4, 7.4))

    draw_rounded_box(ax, 4, 5.9, 3, 0.6, COLORS['process'], 'Estrai Struttura')
    draw_arrow(ax, (4, 6.8), (4, 6.2))

    ax.text(0.5, 5.9, '• Domande\n• Risposte\n• Difficoltà\n• Media URL',
            fontsize=7, va='center', color=COLORS['text'])

    draw_diamond(ax, 4, 4.5, 1.2, COLORS['decision'], 'Validi?')
    draw_arrow(ax, (4, 5.6), (4, 5.1))

    draw_rounded_box(ax, 1.5, 4.5, 2, 0.5, COLORS['highlight'], 'Errore')
    draw_arrow(ax, (3.4, 4.5), (2.5, 4.5))
    ax.text(2.8, 4.7, 'NO', fontsize=8, color=COLORS['arrow'])

    draw_rounded_box(ax, 4, 3.2, 3, 0.6, COLORS['process'], 'Crea Entità DB')
    draw_arrow(ax, (4, 3.9), (4, 3.5))
    ax.text(4.3, 4.1, 'SI', fontsize=8, color=COLORS['arrow'])

    draw_rounded_box(ax, 4, 2, 3, 0.6, COLORS['process'], 'Ordina per\nDifficoltà')
    draw_arrow(ax, (4, 2.9), (4, 2.3))

    draw_rounded_box(ax, 4, 0.8, 3, 0.6, COLORS['success'], 'Import\nCompletato')
    draw_arrow(ax, (4, 1.7), (4, 1.1))

    # === GENERAZIONE FEEDBACK AI ===
    ax.text(12, 10.5, 'GENERAZIONE FEEDBACK AI', ha='center', fontsize=11,
            fontweight='bold', color=COLORS['process'])

    draw_rounded_box(ax, 12, 9.5, 3, 0.6, COLORS['io'], 'Risposta Utente')

    draw_rounded_box(ax, 12, 8.3, 3, 0.6, COLORS['process'], 'Prepara Prompt')
    draw_arrow(ax, (12, 9.2), (12, 8.6))

    ax.text(14.5, 8.3, '• Domanda\n• Risposta data\n• Risposta corretta\n• Contesto medico',
            fontsize=7, va='center', color=COLORS['text'])

    draw_rounded_box(ax, 12, 7.1, 3.2, 0.6, COLORS['process'], 'Chiama GPT-4 Mini')
    draw_arrow(ax, (12, 8), (12, 7.4))

    ax.text(14.5, 7.1, 'Max 500-600 token\nTemp: 0.7',
            fontsize=7, va='center', color=COLORS['text'])

    draw_diamond(ax, 12, 5.7, 1.2, COLORS['decision'], 'OK?')
    draw_arrow(ax, (12, 6.8), (12, 6.3))

    draw_rounded_box(ax, 14.5, 5.7, 2, 0.5, COLORS['io'], 'Fallback')
    draw_arrow(ax, (12.6, 5.7), (13.5, 5.7))
    ax.text(13, 5.9, 'Errore', fontsize=8, color=COLORS['arrow'])

    draw_rounded_box(ax, 12, 4.3, 3, 0.6, COLORS['process'], 'Salva Feedback')
    draw_arrow(ax, (12, 5.1), (12, 4.6))
    ax.text(12.3, 4.9, 'OK', fontsize=8, color=COLORS['arrow'])
    draw_arrow(ax, (14.5, 5.45), (12, 4.6))

    draw_rounded_box(ax, 12, 3, 3, 0.6, COLORS['io'], 'Mostra a Utente')
    draw_arrow(ax, (12, 4), (12, 3.3))

    draw_rounded_box(ax, 12, 1.7, 3, 0.6, COLORS['success'], 'Feedback\nCompletato')
    draw_arrow(ax, (12, 2.7), (12, 2))

    # Linea divisoria
    ax.axvline(x=8, ymin=0.08, ymax=0.85, color=COLORS['arrow'], linestyle='--', linewidth=1)

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/flow_system.svg',
                format='svg', bbox_inches='tight', facecolor=COLORS['background'])
    plt.close()
    print("✓ Flow Sistema generato (SVG)")


def create_overview_flow():
    """Crea un diagramma panoramico dell'intero sistema"""
    fig, ax = plt.subplots(1, 1, figsize=(18, 14))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 14)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor(COLORS['background'])
    fig.patch.set_facecolor(COLORS['background'])

    # Titolo
    ax.text(9, 13.5, 'CLINICAL QUIZ - PANORAMICA SISTEMA', ha='center', va='center',
            fontsize=18, fontweight='bold', color=COLORS['text'])
    ax.text(9, 13, 'Architettura e Flussi Principali', ha='center', va='center',
            fontsize=11, color=COLORS['arrow'])

    # === ADMIN ===
    ax.add_patch(FancyBboxPatch((0.5, 8.5), 5, 3.5, boxstyle="round,pad=0.02,rounding_size=0.2",
                                facecolor='#E8F5E9', edgecolor=COLORS['start_end'], linewidth=2))
    ax.text(3, 11.7, 'ADMIN', ha='center', fontsize=12, fontweight='bold', color=COLORS['start_end'])

    draw_rounded_box(ax, 3, 10.8, 2.5, 0.5, COLORS['start_end'], 'Backoffice', fontsize=9)
    draw_rounded_box(ax, 1.8, 9.8, 2, 0.4, COLORS['process'], 'Gestione\nCreator', fontsize=7)
    draw_rounded_box(ax, 4.2, 9.8, 2, 0.4, COLORS['process'], 'Report\nGlobali', fontsize=7)

    draw_arrow(ax, (2.5, 10.55), (1.8, 10))
    draw_arrow(ax, (3.5, 10.55), (4.2, 10))

    # === CREATOR ===
    ax.add_patch(FancyBboxPatch((6.5, 8.5), 5, 3.5, boxstyle="round,pad=0.02,rounding_size=0.2",
                                facecolor='#E3F2FD', edgecolor=COLORS['process'], linewidth=2))
    ax.text(9, 11.7, 'CREATOR', ha='center', fontsize=12, fontweight='bold', color=COLORS['process'])

    draw_rounded_box(ax, 9, 10.8, 2.5, 0.5, COLORS['process'], 'Dashboard', fontsize=9)
    draw_rounded_box(ax, 7.5, 9.8, 1.8, 0.4, COLORS['io'], 'Crea Quiz', fontsize=7)
    draw_rounded_box(ax, 9, 9.8, 1.8, 0.4, COLORS['io'], 'Monitor', fontsize=7)
    draw_rounded_box(ax, 10.5, 9.8, 1.8, 0.4, COLORS['io'], 'Report', fontsize=7)

    draw_arrow(ax, (8.5, 10.55), (7.5, 10))
    draw_arrow(ax, (9, 10.55), (9, 10))
    draw_arrow(ax, (9.5, 10.55), (10.5, 10))

    # Freccia Admin -> Creator
    draw_arrow(ax, (5.5, 10.5), (6.5, 10.5))
    ax.text(6, 10.7, 'crea', fontsize=8, color=COLORS['arrow'])

    # === QUIZ ===
    ax.add_patch(FancyBboxPatch((6.5, 4.5), 5, 3, boxstyle="round,pad=0.02,rounding_size=0.2",
                                facecolor='#FFF3E0', edgecolor=COLORS['decision'], linewidth=2))
    ax.text(9, 7.2, 'QUIZ', ha='center', fontsize=12, fontweight='bold', color=COLORS['decision'])

    draw_rounded_box(ax, 7.5, 6.3, 1.8, 0.4, COLORS['decision'], 'Domande', fontsize=7)
    draw_rounded_box(ax, 9, 6.3, 1.8, 0.4, COLORS['decision'], 'Timer', fontsize=7)
    draw_rounded_box(ax, 10.5, 6.3, 1.8, 0.4, COLORS['decision'], 'Punteggi', fontsize=7)
    draw_rounded_box(ax, 9, 5.3, 2.5, 0.5, COLORS['decision'], 'QR + Codice', fontsize=8)

    # Freccia Creator -> Quiz
    draw_arrow(ax, (9, 9.55), (9, 7.5))
    ax.text(9.2, 8.5, 'pubblica', fontsize=8, color=COLORS['arrow'])

    # === PARTECIPANTE ===
    ax.add_patch(FancyBboxPatch((12.5, 8.5), 5, 3.5, boxstyle="round,pad=0.02,rounding_size=0.2",
                                facecolor='#F3E5F5', edgecolor='#7B1FA2', linewidth=2))
    ax.text(15, 11.7, 'PARTECIPANTE', ha='center', fontsize=12, fontweight='bold', color='#7B1FA2')

    draw_rounded_box(ax, 15, 10.8, 2.5, 0.5, '#7B1FA2', 'Mobile', fontsize=9)
    draw_rounded_box(ax, 13.8, 9.8, 1.8, 0.4, COLORS['io'], 'Scansiona', fontsize=7)
    draw_rounded_box(ax, 15, 9.8, 1.8, 0.4, COLORS['io'], 'Risponde', fontsize=7)
    draw_rounded_box(ax, 16.2, 9.8, 1.8, 0.4, COLORS['io'], 'Classifica', fontsize=7)

    draw_arrow(ax, (14.5, 10.55), (13.8, 10))
    draw_arrow(ax, (15, 10.55), (15, 10))
    draw_arrow(ax, (15.5, 10.55), (16.2, 10))

    # Freccia Quiz -> Partecipante
    draw_arrow(ax, (11.5, 6), (15, 9.55))
    ax.text(13, 8, 'accede', fontsize=8, color=COLORS['arrow'])

    # === AI ===
    ax.add_patch(FancyBboxPatch((12.5, 4.5), 5, 3, boxstyle="round,pad=0.02,rounding_size=0.2",
                                facecolor='#FFEBEE', edgecolor=COLORS['highlight'], linewidth=2))
    ax.text(15, 7.2, 'AI (GPT-4 Mini)', ha='center', fontsize=12, fontweight='bold', color=COLORS['highlight'])

    draw_rounded_box(ax, 15, 6.3, 3, 0.5, COLORS['highlight'], 'Feedback Educativo', fontsize=8)
    draw_rounded_box(ax, 15, 5.3, 3, 0.5, COLORS['highlight'], 'Persona: Chirurgo', fontsize=8)

    # Freccia Partecipante <-> AI
    draw_arrow(ax, (15, 9.55), (15, 7.5))
    ax.text(15.2, 8.5, 'richiede\nfeedback', fontsize=7, color=COLORS['arrow'])

    # === GOOGLE FORM ===
    ax.add_patch(FancyBboxPatch((0.5, 4.5), 5, 3, boxstyle="round,pad=0.02,rounding_size=0.2",
                                facecolor='#E0F7FA', edgecolor='#00ACC1', linewidth=2))
    ax.text(3, 7.2, 'GOOGLE FORM', ha='center', fontsize=12, fontweight='bold', color='#00ACC1')

    draw_rounded_box(ax, 3, 6.3, 3, 0.5, '#00ACC1', 'Domande + Risposte', fontsize=8)
    draw_rounded_box(ax, 3, 5.3, 3, 0.5, '#00ACC1', 'Media (YouTube)', fontsize=8)

    # Freccia Google Form -> Quiz
    draw_arrow(ax, (5.5, 6), (6.5, 6))
    ax.text(6, 6.2, 'importa', fontsize=8, color=COLORS['arrow'])

    # === DATABASE ===
    ax.add_patch(FancyBboxPatch((6.5, 1), 5, 2.5, boxstyle="round,pad=0.02,rounding_size=0.2",
                                facecolor='#ECEFF1', edgecolor='#546E7A', linewidth=2))
    ax.text(9, 3.2, 'DATABASE', ha='center', fontsize=12, fontweight='bold', color='#546E7A')

    draw_rounded_box(ax, 7.5, 2.3, 1.5, 0.4, '#546E7A', 'Users', fontsize=7)
    draw_rounded_box(ax, 9, 2.3, 1.5, 0.4, '#546E7A', 'Quiz', fontsize=7)
    draw_rounded_box(ax, 10.5, 2.3, 1.5, 0.4, '#546E7A', 'Results', fontsize=7)

    # Frecce al Database
    draw_arrow(ax, (9, 4.5), (9, 3.5))
    draw_arrow(ax, (3, 4.5), (7.5, 3.5))
    draw_arrow(ax, (15, 4.5), (10.5, 3.5))

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/flow_overview.svg',
                format='svg', bbox_inches='tight', facecolor=COLORS['background'])
    plt.close()
    print("✓ Flow Overview generato (SVG)")


if __name__ == '__main__':
    print("\n📊 Generazione diagrammi di flusso Clinical Quiz\n")
    print("-" * 50)

    create_admin_flow()
    create_creator_flow()
    create_participant_flow()
    create_system_flow()
    create_overview_flow()

    print("-" * 50)
    print("\n✅ Tutti i diagrammi generati nella cartella output/\n")
