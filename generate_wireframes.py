#!/usr/bin/env python3
"""
Clinical Quiz - Generatore Wireframe SVG
Wireframe UI per tutte le schermate della piattaforma
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
import numpy as np

# Configurazione colori wireframe
COLORS = {
    'bg': '#FFFFFF',
    'frame': '#E0E0E0',
    'primary': '#1976D2',
    'secondary': '#757575',
    'text': '#212121',
    'text_light': '#9E9E9E',
    'input_bg': '#F5F5F5',
    'success': '#4CAF50',
    'error': '#F44336',
    'warning': '#FF9800',
    'card': '#FAFAFA',
    'border': '#BDBDBD',
}

def draw_phone_frame(ax, title=""):
    """Disegna cornice smartphone"""
    # Phone outline
    phone = FancyBboxPatch((0.5, 0.5), 9, 18, boxstyle="round,pad=0,rounding_size=0.5",
                           facecolor=COLORS['bg'], edgecolor=COLORS['text'], linewidth=2)
    ax.add_patch(phone)
    # Status bar
    ax.add_patch(Rectangle((0.5, 17.5), 9, 1, facecolor=COLORS['frame'], edgecolor='none'))
    ax.text(5, 18, '9:41', ha='center', va='center', fontsize=8, color=COLORS['text'])
    # Title bar
    if title:
        ax.add_patch(Rectangle((0.5, 16.5), 9, 1, facecolor=COLORS['primary'], edgecolor='none'))
        ax.text(5, 17, title, ha='center', va='center', fontsize=10, fontweight='bold', color='white')

def draw_desktop_frame(ax, title="", width=16, height=10):
    """Disegna cornice desktop/browser"""
    # Browser window
    browser = FancyBboxPatch((0.5, 0.5), width, height, boxstyle="round,pad=0,rounding_size=0.2",
                             facecolor=COLORS['bg'], edgecolor=COLORS['border'], linewidth=2)
    ax.add_patch(browser)
    # Title bar
    ax.add_patch(Rectangle((0.5, height-0.3), width, 0.8, facecolor=COLORS['frame'], edgecolor='none'))
    # Browser dots
    ax.add_patch(Circle((1.2, height+0.1), 0.15, facecolor='#FF5F56', edgecolor='none'))
    ax.add_patch(Circle((1.7, height+0.1), 0.15, facecolor='#FFBD2E', edgecolor='none'))
    ax.add_patch(Circle((2.2, height+0.1), 0.15, facecolor='#27CA3F', edgecolor='none'))
    # URL bar
    ax.add_patch(FancyBboxPatch((3, height-0.15), 10, 0.5, boxstyle="round,pad=0,rounding_size=0.1",
                                facecolor='white', edgecolor=COLORS['border'], linewidth=1))
    ax.text(8, height+0.1, 'clinicalquiz.app/' + title.lower().replace(' ', '-'),
            ha='center', va='center', fontsize=7, color=COLORS['text_light'])

def draw_button(ax, x, y, width, height, text, color=None, text_color='white'):
    """Disegna un pulsante"""
    if color is None:
        color = COLORS['primary']
    btn = FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0,rounding_size=0.1",
                         facecolor=color, edgecolor='none')
    ax.add_patch(btn)
    ax.text(x + width/2, y + height/2, text, ha='center', va='center',
            fontsize=8, fontweight='bold', color=text_color)

def draw_input(ax, x, y, width, height, placeholder="", label=""):
    """Disegna un campo input"""
    if label:
        ax.text(x, y + height + 0.15, label, ha='left', va='bottom', fontsize=7, color=COLORS['text'])
    inp = FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0,rounding_size=0.05",
                         facecolor=COLORS['input_bg'], edgecolor=COLORS['border'], linewidth=1)
    ax.add_patch(inp)
    if placeholder:
        ax.text(x + 0.2, y + height/2, placeholder, ha='left', va='center',
                fontsize=7, color=COLORS['text_light'])

def draw_card(ax, x, y, width, height):
    """Disegna una card"""
    card = FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0,rounding_size=0.1",
                          facecolor=COLORS['card'], edgecolor=COLORS['border'], linewidth=1)
    ax.add_patch(card)

def draw_icon_placeholder(ax, x, y, size=0.5):
    """Disegna placeholder per icona"""
    ax.add_patch(Circle((x, y), size, facecolor=COLORS['frame'], edgecolor=COLORS['border']))

def draw_image_placeholder(ax, x, y, width, height, text="IMG"):
    """Disegna placeholder per immagine"""
    ax.add_patch(Rectangle((x, y), width, height, facecolor=COLORS['frame'], edgecolor=COLORS['border']))
    ax.plot([x, x+width], [y, y+height], color=COLORS['border'], linewidth=1)
    ax.plot([x+width, x], [y, y+height], color=COLORS['border'], linewidth=1)
    ax.text(x+width/2, y+height/2, text, ha='center', va='center', fontsize=8, color=COLORS['text_light'])

def draw_sidebar(ax, items, active_index=0, x=0.5, y=0.5, width=3, height=9):
    """Disegna sidebar navigazione"""
    ax.add_patch(Rectangle((x, y), width, height, facecolor=COLORS['primary'], edgecolor='none'))
    item_height = 0.8
    start_y = y + height - 1.5
    for i, item in enumerate(items):
        if i == active_index:
            ax.add_patch(Rectangle((x, start_y - i*item_height - 0.1), width, item_height,
                                   facecolor=(1, 1, 1, 0.2), edgecolor='none'))
        ax.text(x + 0.5, start_y - i*item_height + 0.3, item, ha='left', va='center',
                fontsize=8, color='white')

def draw_table_header(ax, x, y, width, columns):
    """Disegna header tabella"""
    col_width = width / len(columns)
    ax.add_patch(Rectangle((x, y), width, 0.6, facecolor=COLORS['frame'], edgecolor=COLORS['border']))
    for i, col in enumerate(columns):
        ax.text(x + i*col_width + col_width/2, y + 0.3, col, ha='center', va='center',
                fontsize=7, fontweight='bold', color=COLORS['text'])

def draw_table_row(ax, x, y, width, values, columns):
    """Disegna riga tabella"""
    col_width = width / len(columns)
    ax.add_patch(Rectangle((x, y), width, 0.5, facecolor='white', edgecolor=COLORS['border'], linewidth=0.5))
    for i, val in enumerate(values):
        ax.text(x + i*col_width + col_width/2, y + 0.25, val, ha='center', va='center',
                fontsize=6, color=COLORS['text'])


# ============================================
# WIREFRAME ADMIN
# ============================================

def create_wireframe_login():
    """Wireframe: Pagina Login"""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 17)
    ax.set_ylim(0, 11)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg'])

    draw_desktop_frame(ax, "Login", width=16, height=10)

    # Logo placeholder
    draw_image_placeholder(ax, 6.5, 7, 4, 1.5, "LOGO")

    # Login card
    draw_card(ax, 5, 2, 7, 4.5)
    ax.text(8.5, 6, 'Accedi alla piattaforma', ha='center', fontsize=10, fontweight='bold', color=COLORS['text'])

    # Form fields
    draw_input(ax, 5.5, 4.8, 6, 0.6, "Username", "Username")
    draw_input(ax, 5.5, 3.5, 6, 0.6, "••••••••", "Password")

    # Login button
    draw_button(ax, 5.5, 2.3, 6, 0.7, "ACCEDI")

    ax.text(8.5, 13, 'WIREFRAME: LOGIN', ha='center', fontsize=12, fontweight='bold', color=COLORS['text'])

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/wireframe_login.svg',
                format='svg', bbox_inches='tight')
    plt.close()
    print("✓ wireframe_login.svg")


def create_wireframe_admin_dashboard():
    """Wireframe: Dashboard Admin"""
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 17)
    ax.set_ylim(0, 11)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg'])

    draw_desktop_frame(ax, "Admin Dashboard", width=16, height=10)

    # Sidebar
    draw_sidebar(ax, ['Dashboard', 'Gestione Utenti', 'Eventi', 'Report'], active_index=0,
                 x=0.5, y=0.5, width=3, height=9.2)

    # Header
    ax.text(10, 9, 'Dashboard Admin', ha='center', fontsize=12, fontweight='bold', color=COLORS['text'])

    # Stats cards
    stats = [('Creator Attivi', '24'), ('Quiz Totali', '156'), ('Partecipazioni', '3.2K')]
    for i, (label, value) in enumerate(stats):
        draw_card(ax, 4 + i*4, 6.5, 3.5, 2)
        ax.text(5.75 + i*4, 8, value, ha='center', fontsize=14, fontweight='bold', color=COLORS['primary'])
        ax.text(5.75 + i*4, 7.2, label, ha='center', fontsize=8, color=COLORS['text_light'])

    # Recent activity
    draw_card(ax, 4, 1, 11.5, 5)
    ax.text(4.5, 5.5, 'Attività Recente', ha='left', fontsize=9, fontweight='bold', color=COLORS['text'])

    columns = ['Data', 'Creator', 'Evento', 'Partecipanti']
    draw_table_header(ax, 4.2, 4.5, 11, columns)
    rows = [
        ('04/01', 'Dr. Rossi', 'Congresso Cardiologia', '145'),
        ('03/01', 'Dr. Bianchi', 'Workshop Chirurgia', '89'),
        ('02/01', 'Dr. Verdi', 'Corso ECM', '234'),
    ]
    for i, row in enumerate(rows):
        draw_table_row(ax, 4.2, 3.9 - i*0.6, 11, row, columns)

    ax.text(8.5, 13, 'WIREFRAME: ADMIN DASHBOARD', ha='center', fontsize=12, fontweight='bold', color=COLORS['text'])

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/wireframe_admin_dashboard.svg',
                format='svg', bbox_inches='tight')
    plt.close()
    print("✓ wireframe_admin_dashboard.svg")


def create_wireframe_admin_users():
    """Wireframe: Gestione Utenti Admin"""
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 17)
    ax.set_ylim(0, 11)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg'])

    draw_desktop_frame(ax, "Gestione Utenti", width=16, height=10)

    # Sidebar
    draw_sidebar(ax, ['Dashboard', 'Gestione Utenti', 'Eventi', 'Report'], active_index=1,
                 x=0.5, y=0.5, width=3, height=9.2)

    # Header with button
    ax.text(6, 9, 'Gestione Creator', ha='left', fontsize=12, fontweight='bold', color=COLORS['text'])
    draw_button(ax, 13, 8.7, 2.5, 0.6, '+ Nuovo Creator', color=COLORS['success'])

    # Search bar
    draw_input(ax, 4, 7.8, 5, 0.5, "Cerca creator...")

    # Users table
    columns = ['Nome', 'Email', 'Quiz', 'Stato', 'Azioni']
    draw_table_header(ax, 4, 7, 11.5, columns)

    users = [
        ('Dr. Mario Rossi', 'm.rossi@email.it', '12', '● Attivo', '✏️ 🗑️'),
        ('Dr. Anna Bianchi', 'a.bianchi@email.it', '8', '● Attivo', '✏️ 🗑️'),
        ('Dr. Luigi Verdi', 'l.verdi@email.it', '5', '○ Inattivo', '✏️ 🗑️'),
        ('Dr. Sara Neri', 's.neri@email.it', '15', '● Attivo', '✏️ 🗑️'),
    ]
    for i, user in enumerate(users):
        draw_table_row(ax, 4, 6.3 - i*0.6, 11.5, user, columns)

    # Pagination
    ax.text(9.75, 3.5, '< 1 2 3 ... 10 >', ha='center', fontsize=8, color=COLORS['text_light'])

    ax.text(8.5, 13, 'WIREFRAME: GESTIONE UTENTI', ha='center', fontsize=12, fontweight='bold', color=COLORS['text'])

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/wireframe_admin_users.svg',
                format='svg', bbox_inches='tight')
    plt.close()
    print("✓ wireframe_admin_users.svg")


def create_wireframe_admin_create_user():
    """Wireframe: Form Creazione Creator"""
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 17)
    ax.set_ylim(0, 11)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg'])

    draw_desktop_frame(ax, "Nuovo Creator", width=16, height=10)

    # Sidebar
    draw_sidebar(ax, ['Dashboard', 'Gestione Utenti', 'Eventi', 'Report'], active_index=1,
                 x=0.5, y=0.5, width=3, height=9.2)

    # Form card
    draw_card(ax, 4.5, 1, 10.5, 8.5)
    ax.text(9.75, 9, 'Nuovo Account Creator', ha='center', fontsize=11, fontweight='bold', color=COLORS['text'])

    # Form fields
    draw_input(ax, 5, 7.5, 4.5, 0.55, "Mario Rossi", "Nome Completo *")
    draw_input(ax, 10, 7.5, 4.5, 0.55, "m.rossi", "Username *")

    draw_input(ax, 5, 6, 4.5, 0.55, "mario.rossi@email.it", "Email *")
    draw_input(ax, 10, 6, 4.5, 0.55, "••••••••", "Password *")

    draw_input(ax, 5, 4.5, 9.5, 0.55, "Note opzionali...", "Note Interne")

    # Checkbox
    ax.add_patch(Rectangle((5, 3.5), 0.3, 0.3, facecolor='white', edgecolor=COLORS['border']))
    ax.text(5.5, 3.65, 'Invia credenziali via email', fontsize=8, color=COLORS['text'])

    # Buttons
    draw_button(ax, 10, 1.8, 2, 0.6, 'Annulla', color=COLORS['secondary'])
    draw_button(ax, 12.5, 1.8, 2, 0.6, 'Crea', color=COLORS['success'])

    ax.text(8.5, 13, 'WIREFRAME: CREA CREATOR', ha='center', fontsize=12, fontweight='bold', color=COLORS['text'])

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/wireframe_admin_create_user.svg',
                format='svg', bbox_inches='tight')
    plt.close()
    print("✓ wireframe_admin_create_user.svg")


def create_wireframe_admin_reports():
    """Wireframe: Report Aggregati Admin"""
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 17)
    ax.set_ylim(0, 11)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg'])

    draw_desktop_frame(ax, "Report", width=16, height=10)

    # Sidebar
    draw_sidebar(ax, ['Dashboard', 'Gestione Utenti', 'Eventi', 'Report'], active_index=3,
                 x=0.5, y=0.5, width=3, height=9.2)

    # Header
    ax.text(6, 9, 'Report Aggregati', ha='left', fontsize=12, fontweight='bold', color=COLORS['text'])

    # Filters
    draw_input(ax, 4, 8.2, 2.5, 0.5, "Da: 01/01/2024")
    draw_input(ax, 7, 8.2, 2.5, 0.5, "A: 04/01/2024")
    draw_button(ax, 10, 8.2, 1.5, 0.5, 'Filtra', color=COLORS['secondary'])
    draw_button(ax, 14, 8.2, 1.5, 0.5, 'Export', color=COLORS['success'])

    # Chart placeholder
    draw_card(ax, 4, 4.5, 7, 3.2)
    ax.text(7.5, 7.3, 'Partecipazioni nel Tempo', ha='center', fontsize=9, fontweight='bold', color=COLORS['text'])
    # Fake chart bars
    for i in range(6):
        h = 0.5 + np.random.random() * 1.5
        ax.add_patch(Rectangle((4.5 + i*1, 5), 0.6, h, facecolor=COLORS['primary'], edgecolor='none'))

    # Pie chart placeholder
    draw_card(ax, 11.5, 4.5, 4, 3.2)
    ax.text(13.5, 7.3, 'Quiz per Categoria', ha='center', fontsize=9, fontweight='bold', color=COLORS['text'])
    ax.add_patch(Circle((13.5, 5.8), 0.9, facecolor=COLORS['primary'], edgecolor='none'))
    ax.add_patch(mpatches.Wedge((13.5, 5.8), 0.9, 0, 120, facecolor=COLORS['success'], edgecolor='none'))
    ax.add_patch(mpatches.Wedge((13.5, 5.8), 0.9, 120, 200, facecolor=COLORS['warning'], edgecolor='none'))

    # Stats row
    stats = [('Media Punteggio', '78%'), ('Completamento', '92%'), ('Tempo Medio', '8:45')]
    for i, (label, value) in enumerate(stats):
        draw_card(ax, 4 + i*3.8, 1.2, 3.5, 2.8)
        ax.text(5.75 + i*3.8, 3.2, value, ha='center', fontsize=12, fontweight='bold', color=COLORS['primary'])
        ax.text(5.75 + i*3.8, 2.2, label, ha='center', fontsize=8, color=COLORS['text_light'])

    ax.text(8.5, 13, 'WIREFRAME: REPORT ADMIN', ha='center', fontsize=12, fontweight='bold', color=COLORS['text'])

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/wireframe_admin_reports.svg',
                format='svg', bbox_inches='tight')
    plt.close()
    print("✓ wireframe_admin_reports.svg")


# ============================================
# WIREFRAME CREATOR
# ============================================

def create_wireframe_creator_dashboard():
    """Wireframe: Dashboard Creator"""
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 17)
    ax.set_ylim(0, 11)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg'])

    draw_desktop_frame(ax, "Creator Dashboard", width=16, height=10)

    # Sidebar
    draw_sidebar(ax, ['Dashboard', 'I Miei Quiz', 'Crea Quiz', 'Report'], active_index=0,
                 x=0.5, y=0.5, width=3, height=9.2)

    # Header
    ax.text(6, 9, 'Benvenuto, Dr. Rossi', ha='left', fontsize=12, fontweight='bold', color=COLORS['text'])
    draw_button(ax, 13, 8.7, 2.5, 0.6, '+ Nuovo Quiz', color=COLORS['success'])

    # Stats
    stats = [('Quiz Attivi', '3'), ('Partecipanti Totali', '456'), ('Media Punteggio', '82%')]
    for i, (label, value) in enumerate(stats):
        draw_card(ax, 4 + i*4, 6.5, 3.5, 2)
        ax.text(5.75 + i*4, 8, value, ha='center', fontsize=14, fontweight='bold', color=COLORS['primary'])
        ax.text(5.75 + i*4, 7.2, label, ha='center', fontsize=8, color=COLORS['text_light'])

    # My quizzes
    ax.text(4.5, 5.8, 'I Miei Quiz', ha='left', fontsize=10, fontweight='bold', color=COLORS['text'])

    quizzes = [
        ('Congresso Cardiologia 2024', '● Attivo', '145 partecipanti'),
        ('Workshop Chirurgia Mini-invasiva', '● Attivo', '89 partecipanti'),
        ('ECM Medicina Interna', '○ Bozza', '- partecipanti'),
    ]
    for i, (title, status, parts) in enumerate(quizzes):
        draw_card(ax, 4, 4.5 - i*1.3, 11.5, 1.1)
        ax.text(4.5, 5 - i*1.3, title, ha='left', fontsize=9, fontweight='bold', color=COLORS['text'])
        ax.text(4.5, 4.6 - i*1.3, f'{status}  •  {parts}', ha='left', fontsize=7, color=COLORS['text_light'])
        draw_button(ax, 13.5, 4.6 - i*1.3, 1.5, 0.5, 'Apri', color=COLORS['secondary'])

    ax.text(8.5, 13, 'WIREFRAME: CREATOR DASHBOARD', ha='center', fontsize=12, fontweight='bold', color=COLORS['text'])

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/wireframe_creator_dashboard.svg',
                format='svg', bbox_inches='tight')
    plt.close()
    print("✓ wireframe_creator_dashboard.svg")


def create_wireframe_wizard_step1():
    """Wireframe: Wizard Quiz - Step 1 Info Base"""
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 17)
    ax.set_ylim(0, 11)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg'])

    draw_desktop_frame(ax, "Crea Quiz", width=16, height=10)

    # Progress steps
    steps = ['Info Base', 'Grafica', 'Privacy', 'Import', 'Classifica']
    for i, step in enumerate(steps):
        color = COLORS['primary'] if i == 0 else COLORS['frame']
        ax.add_patch(Circle((3 + i*2.8, 9.2), 0.25, facecolor=color, edgecolor='none'))
        ax.text(3 + i*2.8, 9.2, str(i+1), ha='center', va='center', fontsize=7,
                color='white' if i == 0 else COLORS['text_light'])
        ax.text(3 + i*2.8, 8.7, step, ha='center', fontsize=7,
                color=COLORS['text'] if i == 0 else COLORS['text_light'])
        if i < 4:
            ax.plot([3.3 + i*2.8, 5.5 + i*2.8], [9.2, 9.2], color=COLORS['frame'], linewidth=1)

    # Form card
    draw_card(ax, 2, 1.5, 13, 6.5)
    ax.text(8.5, 7.5, 'Step 1: Informazioni Base', ha='center', fontsize=11, fontweight='bold', color=COLORS['text'])

    draw_input(ax, 2.5, 6, 12, 0.6, "Es: Congresso Cardiologia 2024", "Titolo Quiz *")
    draw_input(ax, 2.5, 4.3, 12, 1.2, "Descrizione del quiz e istruzioni per i partecipanti...", "Descrizione *")
    draw_input(ax, 2.5, 2.5, 5.5, 0.6, "04/01/2024", "Data Evento")
    draw_input(ax, 8.5, 2.5, 5.5, 0.6, "Centro Congressi Roma", "Luogo (opzionale)")

    # Buttons
    draw_button(ax, 11, 0.7, 2, 0.6, 'Annulla', color=COLORS['secondary'])
    draw_button(ax, 13.5, 0.7, 2, 0.6, 'Avanti →', color=COLORS['primary'])

    ax.text(8.5, 13, 'WIREFRAME: WIZARD STEP 1 - INFO BASE', ha='center', fontsize=12, fontweight='bold', color=COLORS['text'])

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/wireframe_wizard_step1.svg',
                format='svg', bbox_inches='tight')
    plt.close()
    print("✓ wireframe_wizard_step1.svg")


def create_wireframe_wizard_step2():
    """Wireframe: Wizard Quiz - Step 2 Grafica"""
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 17)
    ax.set_ylim(0, 11)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg'])

    draw_desktop_frame(ax, "Crea Quiz", width=16, height=10)

    # Progress steps
    steps = ['Info Base', 'Grafica', 'Privacy', 'Import', 'Classifica']
    for i, step in enumerate(steps):
        color = COLORS['primary'] if i <= 1 else COLORS['frame']
        ax.add_patch(Circle((3 + i*2.8, 9.2), 0.25, facecolor=color, edgecolor='none'))
        ax.text(3 + i*2.8, 9.2, str(i+1), ha='center', va='center', fontsize=7,
                color='white' if i <= 1 else COLORS['text_light'])
        ax.text(3 + i*2.8, 8.7, step, ha='center', fontsize=7,
                color=COLORS['text'] if i <= 1 else COLORS['text_light'])
        if i < 4:
            ax.plot([3.3 + i*2.8, 5.5 + i*2.8], [9.2, 9.2],
                   color=COLORS['primary'] if i < 1 else COLORS['frame'], linewidth=1)

    # Form card
    draw_card(ax, 2, 1.5, 13, 6.5)
    ax.text(8.5, 7.5, 'Step 2: Personalizzazione Grafica', ha='center', fontsize=11, fontweight='bold', color=COLORS['text'])

    # Logo upload
    ax.text(2.5, 6.5, 'Logo Evento', ha='left', fontsize=8, color=COLORS['text'])
    draw_image_placeholder(ax, 2.5, 4.8, 3, 1.5, "Carica Logo")
    draw_button(ax, 2.5, 4.2, 3, 0.5, 'Seleziona File', color=COLORS['secondary'])

    # Color pickers
    ax.text(7, 6.5, 'Colori Personalizzati', ha='left', fontsize=8, color=COLORS['text'])
    colors_labels = ['Primario', 'Secondario', 'Accento']
    sample_colors = ['#1976D2', '#424242', '#FF9800']
    for i, (label, col) in enumerate(zip(colors_labels, sample_colors)):
        ax.add_patch(Rectangle((7, 5.5 - i*0.8), 0.6, 0.6, facecolor=col, edgecolor=COLORS['border']))
        ax.text(7.8, 5.8 - i*0.8, label, ha='left', va='center', fontsize=7, color=COLORS['text'])
        draw_input(ax, 10, 5.5 - i*0.8, 2.5, 0.5, col)

    # Preview
    ax.text(2.5, 3.8, 'Anteprima', ha='left', fontsize=8, color=COLORS['text'])
    draw_card(ax, 2.5, 2, 4, 1.5)
    ax.add_patch(Rectangle((2.6, 3.1), 3.8, 0.3, facecolor='#1976D2', edgecolor='none'))
    ax.text(4.5, 2.6, 'Quiz Preview', ha='center', fontsize=7, color=COLORS['text_light'])

    # Buttons
    draw_button(ax, 9, 0.7, 2, 0.6, '← Indietro', color=COLORS['secondary'])
    draw_button(ax, 11.5, 0.7, 2, 0.6, 'Avanti →', color=COLORS['primary'])

    ax.text(8.5, 13, 'WIREFRAME: WIZARD STEP 2 - GRAFICA', ha='center', fontsize=12, fontweight='bold', color=COLORS['text'])

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/wireframe_wizard_step2.svg',
                format='svg', bbox_inches='tight')
    plt.close()
    print("✓ wireframe_wizard_step2.svg")


def create_wireframe_wizard_step3():
    """Wireframe: Wizard Quiz - Step 3 Privacy"""
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 17)
    ax.set_ylim(0, 11)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg'])

    draw_desktop_frame(ax, "Crea Quiz", width=16, height=10)

    # Progress steps
    steps = ['Info Base', 'Grafica', 'Privacy', 'Import', 'Classifica']
    for i, step in enumerate(steps):
        color = COLORS['primary'] if i <= 2 else COLORS['frame']
        ax.add_patch(Circle((3 + i*2.8, 9.2), 0.25, facecolor=color, edgecolor='none'))
        ax.text(3 + i*2.8, 9.2, str(i+1), ha='center', va='center', fontsize=7,
                color='white' if i <= 2 else COLORS['text_light'])
        ax.text(3 + i*2.8, 8.7, step, ha='center', fontsize=7,
                color=COLORS['text'] if i <= 2 else COLORS['text_light'])
        if i < 4:
            ax.plot([3.3 + i*2.8, 5.5 + i*2.8], [9.2, 9.2],
                   color=COLORS['primary'] if i < 2 else COLORS['frame'], linewidth=1)

    # Form card
    draw_card(ax, 2, 1.5, 13, 6.5)
    ax.text(8.5, 7.5, 'Step 3: Configurazione Privacy', ha='center', fontsize=11, fontweight='bold', color=COLORS['text'])

    # Checkboxes for required fields
    ax.text(2.5, 6.5, 'Dati richiesti ai partecipanti:', ha='left', fontsize=9, fontweight='bold', color=COLORS['text'])

    fields = [('Nome', True), ('Cognome', True), ('Email', True), ('Telefono', False)]
    for i, (field, checked) in enumerate(fields):
        ax.add_patch(Rectangle((2.5 + (i%2)*5, 5.5 - (i//2)*0.8), 0.35, 0.35,
                               facecolor=COLORS['primary'] if checked else 'white', edgecolor=COLORS['border']))
        if checked:
            ax.text(2.67 + (i%2)*5, 5.67 - (i//2)*0.8, '✓', ha='center', va='center', fontsize=8, color='white')
        ax.text(3 + (i%2)*5, 5.67 - (i//2)*0.8, field, ha='left', va='center', fontsize=8, color=COLORS['text'])

    # GDPR toggle
    ax.text(2.5, 4.2, 'Consenso GDPR:', ha='left', fontsize=9, fontweight='bold', color=COLORS['text'])
    ax.add_patch(FancyBboxPatch((2.5, 3.5), 1.2, 0.5, boxstyle="round,pad=0,rounding_size=0.25",
                                facecolor=COLORS['success'], edgecolor='none'))
    ax.add_patch(Circle((3.4, 3.75), 0.2, facecolor='white', edgecolor='none'))
    ax.text(4, 3.75, 'Attivo - I partecipanti dovranno accettare i termini',
            ha='left', va='center', fontsize=7, color=COLORS['text'])

    # Privacy text
    ax.text(2.5, 2.8, 'Testo consenso (opzionale):', ha='left', fontsize=8, color=COLORS['text'])
    draw_input(ax, 2.5, 1.8, 12, 0.8, "Acconsento al trattamento dei miei dati personali...")

    # Buttons
    draw_button(ax, 9, 0.7, 2, 0.6, '← Indietro', color=COLORS['secondary'])
    draw_button(ax, 11.5, 0.7, 2, 0.6, 'Avanti →', color=COLORS['primary'])

    ax.text(8.5, 13, 'WIREFRAME: WIZARD STEP 3 - PRIVACY', ha='center', fontsize=12, fontweight='bold', color=COLORS['text'])

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/wireframe_wizard_step3.svg',
                format='svg', bbox_inches='tight')
    plt.close()
    print("✓ wireframe_wizard_step3.svg")


def create_wireframe_wizard_step4():
    """Wireframe: Wizard Quiz - Step 4 Import"""
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 17)
    ax.set_ylim(0, 11)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg'])

    draw_desktop_frame(ax, "Crea Quiz", width=16, height=10)

    # Progress steps
    steps = ['Info Base', 'Grafica', 'Privacy', 'Import', 'Classifica']
    for i, step in enumerate(steps):
        color = COLORS['primary'] if i <= 3 else COLORS['frame']
        ax.add_patch(Circle((3 + i*2.8, 9.2), 0.25, facecolor=color, edgecolor='none'))
        ax.text(3 + i*2.8, 9.2, str(i+1), ha='center', va='center', fontsize=7,
                color='white' if i <= 3 else COLORS['text_light'])
        ax.text(3 + i*2.8, 8.7, step, ha='center', fontsize=7,
                color=COLORS['text'] if i <= 3 else COLORS['text_light'])
        if i < 4:
            ax.plot([3.3 + i*2.8, 5.5 + i*2.8], [9.2, 9.2],
                   color=COLORS['primary'] if i < 3 else COLORS['frame'], linewidth=1)

    # Form card
    draw_card(ax, 2, 1.5, 13, 6.5)
    ax.text(8.5, 7.5, 'Step 4: Importa Domande', ha='center', fontsize=11, fontweight='bold', color=COLORS['text'])

    # Google Form link
    ax.text(2.5, 6.5, 'Link Google Form:', ha='left', fontsize=9, fontweight='bold', color=COLORS['text'])
    draw_input(ax, 2.5, 5.7, 9, 0.6, "https://docs.google.com/forms/d/...")
    draw_button(ax, 12, 5.7, 2.5, 0.6, 'Importa', color=COLORS['primary'])

    # Imported questions preview
    ax.text(2.5, 4.8, 'Domande importate: 15', ha='left', fontsize=9, color=COLORS['success'])

    columns = ['#', 'Domanda', 'Difficoltà', 'Media']
    draw_table_header(ax, 2.5, 4.2, 12, columns)
    questions = [
        ('1', 'Qual è il trattamento di prima linea...', 'Facile', '—'),
        ('2', 'In caso di fibrillazione atriale...', 'Media', '🖼️'),
        ('3', 'Quale farmaco è controindicato...', 'Difficile', '—'),
    ]
    for i, q in enumerate(questions):
        draw_table_row(ax, 2.5, 3.6 - i*0.55, 12, q, columns)

    # Buttons
    draw_button(ax, 9, 0.7, 2, 0.6, '← Indietro', color=COLORS['secondary'])
    draw_button(ax, 11.5, 0.7, 2, 0.6, 'Avanti →', color=COLORS['primary'])

    ax.text(8.5, 13, 'WIREFRAME: WIZARD STEP 4 - IMPORT', ha='center', fontsize=12, fontweight='bold', color=COLORS['text'])

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/wireframe_wizard_step4.svg',
                format='svg', bbox_inches='tight')
    plt.close()
    print("✓ wireframe_wizard_step4.svg")


def create_wireframe_wizard_step5():
    """Wireframe: Wizard Quiz - Step 5 Classifica"""
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 17)
    ax.set_ylim(0, 11)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg'])

    draw_desktop_frame(ax, "Crea Quiz", width=16, height=10)

    # Progress steps - all complete
    steps = ['Info Base', 'Grafica', 'Privacy', 'Import', 'Classifica']
    for i, step in enumerate(steps):
        ax.add_patch(Circle((3 + i*2.8, 9.2), 0.25, facecolor=COLORS['primary'], edgecolor='none'))
        ax.text(3 + i*2.8, 9.2, str(i+1), ha='center', va='center', fontsize=7, color='white')
        ax.text(3 + i*2.8, 8.7, step, ha='center', fontsize=7, color=COLORS['text'])
        if i < 4:
            ax.plot([3.3 + i*2.8, 5.5 + i*2.8], [9.2, 9.2], color=COLORS['primary'], linewidth=1)

    # Form card
    draw_card(ax, 2, 1.5, 13, 6.5)
    ax.text(8.5, 7.5, 'Step 5: Configurazione Classifica', ha='center', fontsize=11, fontweight='bold', color=COLORS['text'])

    # Display name options
    ax.text(2.5, 6.5, 'Visualizzazione nomi:', ha='left', fontsize=9, fontweight='bold', color=COLORS['text'])
    # Radio buttons
    ax.add_patch(Circle((2.7, 5.9), 0.15, facecolor=COLORS['primary'], edgecolor=COLORS['border']))
    ax.text(3, 5.9, 'Nome completo (Mario Rossi)', ha='left', va='center', fontsize=8, color=COLORS['text'])
    ax.add_patch(Circle((2.7, 5.4), 0.15, facecolor='white', edgecolor=COLORS['border']))
    ax.text(3, 5.4, 'Solo iniziali (M.R.)', ha='left', va='center', fontsize=8, color=COLORS['text'])
    ax.add_patch(Circle((2.7, 4.9), 0.15, facecolor='white', edgecolor=COLORS['border']))
    ax.text(3, 4.9, 'Nickname personalizzato', ha='left', va='center', fontsize=8, color=COLORS['text'])

    # Top N options
    ax.text(8, 6.5, 'Posizioni visibili:', ha='left', fontsize=9, fontweight='bold', color=COLORS['text'])
    ax.add_patch(Circle((8.2, 5.9), 0.15, facecolor='white', edgecolor=COLORS['border']))
    ax.text(8.5, 5.9, 'Top 10', ha='left', va='center', fontsize=8, color=COLORS['text'])
    ax.add_patch(Circle((8.2, 5.4), 0.15, facecolor=COLORS['primary'], edgecolor=COLORS['border']))
    ax.text(8.5, 5.4, 'Top 20', ha='left', va='center', fontsize=8, color=COLORS['text'])
    ax.add_patch(Circle((8.2, 4.9), 0.15, facecolor='white', edgecolor=COLORS['border']))
    ax.text(8.5, 4.9, 'Tutti', ha='left', va='center', fontsize=8, color=COLORS['text'])

    # Summary
    ax.text(2.5, 4, 'Riepilogo Quiz:', ha='left', fontsize=9, fontweight='bold', color=COLORS['text'])
    summary = ['Titolo: Congresso Cardiologia 2024', '15 domande importate', 'GDPR attivo', 'Top 20 in classifica']
    for i, line in enumerate(summary):
        ax.text(2.7, 3.5 - i*0.4, f'• {line}', ha='left', fontsize=7, color=COLORS['text_light'])

    # Buttons
    draw_button(ax, 7, 0.7, 2.5, 0.6, '← Indietro', color=COLORS['secondary'])
    draw_button(ax, 10, 0.7, 2.5, 0.6, 'Salva Bozza', color=COLORS['warning'])
    draw_button(ax, 13, 0.7, 2.5, 0.6, 'Pubblica', color=COLORS['success'])

    ax.text(8.5, 13, 'WIREFRAME: WIZARD STEP 5 - CLASSIFICA', ha='center', fontsize=12, fontweight='bold', color=COLORS['text'])

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/wireframe_wizard_step5.svg',
                format='svg', bbox_inches='tight')
    plt.close()
    print("✓ wireframe_wizard_step5.svg")


def create_wireframe_qr_code():
    """Wireframe: QR Code e Codice Stanza"""
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 17)
    ax.set_ylim(0, 11)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg'])

    draw_desktop_frame(ax, "Quiz Pubblicato", width=16, height=10)

    # Success message
    ax.add_patch(FancyBboxPatch((3, 7.5), 11, 1.5, boxstyle="round,pad=0,rounding_size=0.1",
                                facecolor='#E8F5E9', edgecolor=COLORS['success'], linewidth=1))
    ax.text(8.5, 8.3, '✓ Quiz pubblicato con successo!', ha='center', fontsize=11, fontweight='bold', color=COLORS['success'])
    ax.text(8.5, 7.8, 'Condividi il QR code o il codice stanza con i partecipanti', ha='center', fontsize=8, color=COLORS['text'])

    # QR Code section
    draw_card(ax, 2.5, 2, 5, 5)
    ax.text(5, 6.5, 'QR Code', ha='center', fontsize=10, fontweight='bold', color=COLORS['text'])
    # QR placeholder
    ax.add_patch(Rectangle((3.5, 3), 3, 3, facecolor=COLORS['frame'], edgecolor=COLORS['border']))
    ax.text(5, 4.5, 'QR', ha='center', fontsize=16, color=COLORS['text_light'])
    draw_button(ax, 3, 2.3, 4, 0.5, '⬇ Scarica PNG', color=COLORS['primary'])

    # Room code section
    draw_card(ax, 8.5, 2, 6, 5)
    ax.text(11.5, 6.5, 'Codice Stanza', ha='center', fontsize=10, fontweight='bold', color=COLORS['text'])
    ax.add_patch(FancyBboxPatch((9, 4.5), 5, 1.2, boxstyle="round,pad=0,rounding_size=0.1",
                                facecolor=COLORS['input_bg'], edgecolor=COLORS['border'], linewidth=2))
    ax.text(11.5, 5.1, 'EVT-2024-ABC', ha='center', fontsize=14, fontweight='bold', color=COLORS['text'])

    ax.text(11.5, 3.8, 'URL diretto:', ha='center', fontsize=8, color=COLORS['text_light'])
    ax.text(11.5, 3.4, 'clinicalquiz.app/q/EVT-2024-ABC', ha='center', fontsize=7, color=COLORS['primary'])

    draw_button(ax, 9.5, 2.3, 4, 0.5, '📋 Copia Link', color=COLORS['secondary'])

    ax.text(8.5, 13, 'WIREFRAME: QR CODE & CODICE STANZA', ha='center', fontsize=12, fontweight='bold', color=COLORS['text'])

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/wireframe_qr_code.svg',
                format='svg', bbox_inches='tight')
    plt.close()
    print("✓ wireframe_qr_code.svg")


def create_wireframe_monitor_live():
    """Wireframe: Monitor Live"""
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 17)
    ax.set_ylim(0, 11)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg'])

    draw_desktop_frame(ax, "Monitor Live", width=16, height=10)

    # Header with live indicator
    ax.text(4, 9, 'Congresso Cardiologia 2024', ha='left', fontsize=11, fontweight='bold', color=COLORS['text'])
    ax.add_patch(Circle((14.5, 9), 0.15, facecolor=COLORS['error'], edgecolor='none'))
    ax.text(15, 9, 'LIVE', ha='left', fontsize=8, fontweight='bold', color=COLORS['error'])

    # Stats row
    stats = [('Attivi Ora', '23', COLORS['success']), ('Completati', '122', COLORS['primary']),
             ('Media Punti', '78%', COLORS['warning'])]
    for i, (label, value, color) in enumerate(stats):
        draw_card(ax, 1 + i*5, 6.8, 4.5, 1.8)
        ax.text(3.25 + i*5, 8.1, value, ha='center', fontsize=14, fontweight='bold', color=color)
        ax.text(3.25 + i*5, 7.4, label, ha='center', fontsize=8, color=COLORS['text_light'])

    # Leaderboard
    draw_card(ax, 1, 1.2, 7, 5.2)
    ax.text(4.5, 6, 'Classifica Live', ha='center', fontsize=10, fontweight='bold', color=COLORS['text'])

    leaders = [('🥇 Mario R.', '156 pts'), ('🥈 Anna B.', '142 pts'), ('🥉 Luigi V.', '138 pts'),
               ('4. Sara N.', '125 pts'), ('5. Paolo M.', '118 pts')]
    for i, (name, score) in enumerate(leaders):
        ax.text(1.5, 5.3 - i*0.7, name, ha='left', fontsize=8, color=COLORS['text'])
        ax.text(7.5, 5.3 - i*0.7, score, ha='right', fontsize=8, fontweight='bold', color=COLORS['primary'])

    # Question stats
    draw_card(ax, 8.5, 1.2, 7, 5.2)
    ax.text(12, 6, 'Risposte per Domanda', ha='center', fontsize=10, fontweight='bold', color=COLORS['text'])

    # Bar chart
    questions = ['D1', 'D2', 'D3', 'D4', 'D5']
    percentages = [92, 78, 65, 88, 71]
    for i, (q, p) in enumerate(zip(questions, percentages)):
        ax.text(9, 5.2 - i*0.8, q, ha='left', fontsize=7, color=COLORS['text'])
        ax.add_patch(Rectangle((9.5, 5 - i*0.8), p/25, 0.4, facecolor=COLORS['success'], edgecolor='none'))
        ax.text(9.6 + p/25, 5.2 - i*0.8, f'{p}%', ha='left', fontsize=7, color=COLORS['text'])

    # Fullscreen button
    draw_button(ax, 12, 0.5, 3, 0.5, '⛶ Modalità Presentazione', color=COLORS['secondary'])

    ax.text(8.5, 13, 'WIREFRAME: MONITOR LIVE', ha='center', fontsize=12, fontweight='bold', color=COLORS['text'])

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/wireframe_monitor_live.svg',
                format='svg', bbox_inches='tight')
    plt.close()
    print("✓ wireframe_monitor_live.svg")


# ============================================
# WIREFRAME PARTECIPANTE (MOBILE)
# ============================================

def create_wireframe_mobile_landing():
    """Wireframe Mobile: Landing Page"""
    fig, ax = plt.subplots(figsize=(6, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 19)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg'])

    draw_phone_frame(ax, "Clinical Quiz")

    # Logo
    draw_image_placeholder(ax, 3, 12, 4, 2, "LOGO")

    # Welcome text
    ax.text(5, 11, 'Benvenuto!', ha='center', fontsize=12, fontweight='bold', color=COLORS['text'])
    ax.text(5, 10.4, 'Inserisci il codice stanza\nper accedere al quiz', ha='center', fontsize=8, color=COLORS['text_light'])

    # Code input
    draw_input(ax, 1.5, 8.5, 7, 1, "EVT-2024-ABC", "Codice Stanza")

    # OR divider
    ax.plot([1.5, 4], [7.5, 7.5], color=COLORS['frame'], linewidth=1)
    ax.text(5, 7.5, 'oppure', ha='center', fontsize=8, color=COLORS['text_light'])
    ax.plot([6, 8.5], [7.5, 7.5], color=COLORS['frame'], linewidth=1)

    # QR button
    draw_button(ax, 1.5, 6, 7, 1, '📷 Scansiona QR Code', color=COLORS['secondary'])

    # Enter button
    draw_button(ax, 1.5, 4, 7, 1, 'ACCEDI', color=COLORS['primary'])

    ax.text(5, 20.5, 'WIREFRAME: MOBILE LANDING', ha='center', fontsize=10, fontweight='bold', color=COLORS['text'])

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/wireframe_mobile_landing.svg',
                format='svg', bbox_inches='tight')
    plt.close()
    print("✓ wireframe_mobile_landing.svg")


def create_wireframe_mobile_welcome():
    """Wireframe Mobile: Schermata Benvenuto"""
    fig, ax = plt.subplots(figsize=(6, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 19)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg'])

    draw_phone_frame(ax, "Quiz")

    # Event logo
    draw_image_placeholder(ax, 2.5, 12.5, 5, 2, "LOGO EVENTO")

    # Title
    ax.text(5, 11.5, 'Congresso Cardiologia', ha='center', fontsize=11, fontweight='bold', color=COLORS['text'])
    ax.text(5, 11, '2024', ha='center', fontsize=11, fontweight='bold', color=COLORS['text'])

    # Description
    ax.text(5, 9.8, 'Quiz formativo interattivo\nsulla cardiologia moderna.\n\n15 domande • ~10 minuti',
            ha='center', fontsize=8, color=COLORS['text_light'])

    # Info card
    draw_card(ax, 1, 6, 8, 2.5)
    ax.text(5, 8, 'Informazioni', ha='center', fontsize=9, fontweight='bold', color=COLORS['text'])
    ax.text(1.5, 7.3, '• Rispondi alle domande', ha='left', fontsize=7, color=COLORS['text_light'])
    ax.text(1.5, 6.8, '• Ricevi feedback educativo', ha='left', fontsize=7, color=COLORS['text_light'])
    ax.text(1.5, 6.3, '• Scala la classifica!', ha='left', fontsize=7, color=COLORS['text_light'])

    # Start button
    draw_button(ax, 1.5, 4, 7, 1.2, 'INIZIA', color=COLORS['success'])

    ax.text(5, 20.5, 'WIREFRAME: MOBILE WELCOME', ha='center', fontsize=10, fontweight='bold', color=COLORS['text'])

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/wireframe_mobile_welcome.svg',
                format='svg', bbox_inches='tight')
    plt.close()
    print("✓ wireframe_mobile_welcome.svg")


def create_wireframe_mobile_registration():
    """Wireframe Mobile: Form Registrazione + GDPR"""
    fig, ax = plt.subplots(figsize=(6, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 19)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg'])

    draw_phone_frame(ax, "Registrazione")

    ax.text(5, 14.5, 'Inserisci i tuoi dati', ha='center', fontsize=11, fontweight='bold', color=COLORS['text'])

    # Form fields
    draw_input(ax, 1, 12.5, 8, 0.8, "Mario", "Nome *")
    draw_input(ax, 1, 10.8, 8, 0.8, "Rossi", "Cognome *")
    draw_input(ax, 1, 9.1, 8, 0.8, "mario.rossi@email.it", "Email *")

    # GDPR
    draw_card(ax, 1, 5.5, 8, 3)
    ax.text(5, 8, 'Consenso Privacy', ha='center', fontsize=9, fontweight='bold', color=COLORS['text'])
    ax.text(5, 7.2, 'Acconsento al trattamento dei\nmiei dati personali secondo\nla normativa GDPR vigente.',
            ha='center', fontsize=7, color=COLORS['text_light'])

    # Checkbox
    ax.add_patch(Rectangle((1.5, 5.8), 0.4, 0.4, facecolor=COLORS['primary'], edgecolor=COLORS['border']))
    ax.text(1.7, 6, '✓', ha='center', va='center', fontsize=9, color='white')
    ax.text(2.1, 6, 'Accetto i termini e condizioni *', ha='left', va='center', fontsize=7, color=COLORS['text'])

    # Continue button
    draw_button(ax, 1.5, 3.5, 7, 1, 'CONTINUA', color=COLORS['primary'])

    ax.text(5, 20.5, 'WIREFRAME: MOBILE REGISTRATION', ha='center', fontsize=10, fontweight='bold', color=COLORS['text'])

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/wireframe_mobile_registration.svg',
                format='svg', bbox_inches='tight')
    plt.close()
    print("✓ wireframe_mobile_registration.svg")


def create_wireframe_mobile_question():
    """Wireframe Mobile: Domanda Quiz"""
    fig, ax = plt.subplots(figsize=(6, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 19)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg'])

    draw_phone_frame(ax, "Domanda 3/15")

    # Progress bar
    ax.add_patch(Rectangle((1, 15.5), 8, 0.3, facecolor=COLORS['frame'], edgecolor='none'))
    ax.add_patch(Rectangle((1, 15.5), 1.6, 0.3, facecolor=COLORS['primary'], edgecolor='none'))

    # Timer
    ax.add_patch(Circle((8, 14.5), 0.6, facecolor='white', edgecolor=COLORS['warning'], linewidth=2))
    ax.text(8, 14.5, '45', ha='center', va='center', fontsize=9, fontweight='bold', color=COLORS['warning'])

    # Points
    ax.text(2, 14.5, '🏆 24 pts', ha='left', fontsize=9, color=COLORS['text'])

    # Question
    draw_card(ax, 0.8, 10.5, 8.4, 3.2)
    ax.text(5, 13.2, 'Qual è il trattamento di prima\nlinea per la fibrillazione\natriale parossistica?',
            ha='center', fontsize=9, fontweight='bold', color=COLORS['text'])

    # Image placeholder (optional)
    draw_image_placeholder(ax, 3, 10.8, 4, 1.5, "IMG")

    # Answer options
    options = ['A) Beta-bloccanti', 'B) ACE inibitori', 'C) Anticoagulanti', 'D) Calcio antagonisti']
    for i, opt in enumerate(options):
        draw_card(ax, 0.8, 8.5 - i*1.5, 8.4, 1.2)
        ax.add_patch(Circle((1.6, 8.1 - i*1.5), 0.25, facecolor='white', edgecolor=COLORS['primary'], linewidth=1.5))
        ax.text(2.2, 8.1 - i*1.5, opt, ha='left', va='center', fontsize=8, color=COLORS['text'])

    # Confirm button
    draw_button(ax, 1.5, 1.5, 7, 1, 'CONFERMA', color=COLORS['primary'])

    ax.text(5, 20.5, 'WIREFRAME: MOBILE QUESTION', ha='center', fontsize=10, fontweight='bold', color=COLORS['text'])

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/wireframe_mobile_question.svg',
                format='svg', bbox_inches='tight')
    plt.close()
    print("✓ wireframe_mobile_question.svg")


def create_wireframe_mobile_correct():
    """Wireframe Mobile: Risposta Corretta"""
    fig, ax = plt.subplots(figsize=(6, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 19)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg'])

    draw_phone_frame(ax, "Domanda 3/15")

    # Progress bar
    ax.add_patch(Rectangle((1, 15.5), 8, 0.3, facecolor=COLORS['frame'], edgecolor='none'))
    ax.add_patch(Rectangle((1, 15.5), 1.6, 0.3, facecolor=COLORS['primary'], edgecolor='none'))

    # Success icon
    ax.add_patch(Circle((5, 13.5), 1.2, facecolor=COLORS['success'], edgecolor='none'))
    ax.text(5, 13.5, '✓', ha='center', va='center', fontsize=24, color='white')

    # Message
    ax.text(5, 11.5, 'Corretto!', ha='center', fontsize=14, fontweight='bold', color=COLORS['success'])
    ax.text(5, 10.8, '+10 punti', ha='center', fontsize=10, color=COLORS['success'])

    # AI Feedback
    draw_card(ax, 0.8, 5.5, 8.4, 4.5)
    ax.text(5, 9.5, 'Feedback', ha='center', fontsize=9, fontweight='bold', color=COLORS['text'])
    ax.text(5, 8, 'Esatto! I beta-bloccanti sono\neffettivamente il trattamento di\nprima linea per il controllo\ndella frequenza nella FA\nparossistica, grazie alla loro\ncapacità di ridurre la risposta\nventricolare.',
            ha='center', fontsize=7, color=COLORS['text_light'])

    # Points display
    ax.text(5, 4.5, 'Punteggio attuale: 34 pts', ha='center', fontsize=9, fontweight='bold', color=COLORS['text'])

    # Continue button
    draw_button(ax, 1.5, 2, 7, 1, 'PROSSIMA DOMANDA →', color=COLORS['primary'])

    ax.text(5, 20.5, 'WIREFRAME: MOBILE CORRECT', ha='center', fontsize=10, fontweight='bold', color=COLORS['text'])

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/wireframe_mobile_correct.svg',
                format='svg', bbox_inches='tight')
    plt.close()
    print("✓ wireframe_mobile_correct.svg")


def create_wireframe_mobile_wrong():
    """Wireframe Mobile: Risposta Errata con Feedback AI"""
    fig, ax = plt.subplots(figsize=(6, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 19)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg'])

    draw_phone_frame(ax, "Domanda 3/15")

    # Progress bar
    ax.add_patch(Rectangle((1, 15.5), 8, 0.3, facecolor=COLORS['frame'], edgecolor='none'))
    ax.add_patch(Rectangle((1, 15.5), 1.6, 0.3, facecolor=COLORS['primary'], edgecolor='none'))

    # Error icon
    ax.add_patch(Circle((5, 13.5), 1.2, facecolor=COLORS['error'], edgecolor='none'))
    ax.text(5, 13.5, '✗', ha='center', va='center', fontsize=24, color='white')

    # Message
    ax.text(5, 11.5, 'Non corretto', ha='center', fontsize=14, fontweight='bold', color=COLORS['error'])
    ax.text(5, 10.8, '-5 punti', ha='center', fontsize=10, color=COLORS['error'])

    # Correct answer
    ax.text(5, 10, 'Risposta corretta: A) Beta-bloccanti', ha='center', fontsize=8,
            fontweight='bold', color=COLORS['success'])

    # AI Feedback (longer)
    draw_card(ax, 0.8, 4, 8.4, 5.5)
    ax.text(5, 9, '🤖 Feedback del Dr. AI', ha='center', fontsize=9, fontweight='bold', color=COLORS['text'])
    ax.text(5, 7.2, 'Gli ACE inibitori, sebbene utili\nnel trattamento dello scompenso\ncardiaco, non sono indicati come\nprima linea per la FA.\n\nI beta-bloccanti sono preferiti\nperché agiscono direttamente\nsul nodo AV, rallentando la\nconduzione e controllando\nla frequenza ventricolare.',
            ha='center', fontsize=6.5, color=COLORS['text_light'])

    # Points display
    ax.text(5, 3, 'Punteggio attuale: 19 pts', ha='center', fontsize=9, fontweight='bold', color=COLORS['text'])

    # Continue button
    draw_button(ax, 1.5, 1.2, 7, 1, 'PROSEGUI →', color=COLORS['primary'])

    ax.text(5, 20.5, 'WIREFRAME: MOBILE WRONG + AI', ha='center', fontsize=10, fontweight='bold', color=COLORS['text'])

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/wireframe_mobile_wrong.svg',
                format='svg', bbox_inches='tight')
    plt.close()
    print("✓ wireframe_mobile_wrong.svg")


def create_wireframe_mobile_results():
    """Wireframe Mobile: Risultati Finali"""
    fig, ax = plt.subplots(figsize=(6, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 19)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg'])

    draw_phone_frame(ax, "Risultati")

    # Congrats
    ax.text(5, 14.5, '🎉', ha='center', fontsize=24)
    ax.text(5, 13.5, 'Quiz Completato!', ha='center', fontsize=12, fontweight='bold', color=COLORS['text'])

    # Score card
    draw_card(ax, 1.5, 10, 7, 3)
    ax.add_patch(Circle((5, 11.8), 1, facecolor=COLORS['primary'], edgecolor='none'))
    ax.text(5, 11.8, '78', ha='center', va='center', fontsize=14, fontweight='bold', color='white')
    ax.text(5, 10.5, 'punti', ha='center', fontsize=9, color=COLORS['text_light'])

    # Stats
    draw_card(ax, 1.5, 6.5, 7, 3)
    ax.text(5, 9, 'Statistiche', ha='center', fontsize=9, fontweight='bold', color=COLORS['text'])
    stats = [('Risposte corrette', '12/15'), ('Percentuale', '80%'), ('Tempo totale', '8:32')]
    for i, (label, value) in enumerate(stats):
        ax.text(2, 8.2 - i*0.7, label, ha='left', fontsize=7, color=COLORS['text_light'])
        ax.text(8, 8.2 - i*0.7, value, ha='right', fontsize=7, fontweight='bold', color=COLORS['text'])

    # AI Final feedback
    draw_card(ax, 1.5, 3.5, 7, 2.5)
    ax.text(5, 5.5, '🤖 Feedback Finale', ha='center', fontsize=8, fontweight='bold', color=COLORS['text'])
    ax.text(5, 4.5, 'Ottimo lavoro! Hai dimostrato\nuna buona conoscenza della\nmateria. Continua così!',
            ha='center', fontsize=7, color=COLORS['text_light'])

    # Buttons
    draw_button(ax, 1.5, 1.8, 7, 0.9, '🏆 VEDI CLASSIFICA', color=COLORS['success'])

    ax.text(5, 20.5, 'WIREFRAME: MOBILE RESULTS', ha='center', fontsize=10, fontweight='bold', color=COLORS['text'])

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/wireframe_mobile_results.svg',
                format='svg', bbox_inches='tight')
    plt.close()
    print("✓ wireframe_mobile_results.svg")


def create_wireframe_mobile_leaderboard():
    """Wireframe Mobile: Classifica"""
    fig, ax = plt.subplots(figsize=(6, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 19)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg'])

    draw_phone_frame(ax, "Classifica")

    ax.text(5, 14.8, '🏆 Top 20', ha='center', fontsize=12, fontweight='bold', color=COLORS['text'])

    # Your position highlight
    draw_card(ax, 1, 13, 8, 1.3)
    ax.add_patch(FancyBboxPatch((1, 13), 8, 1.3, boxstyle="round,pad=0,rounding_size=0.1",
                                facecolor='#E3F2FD', edgecolor=COLORS['primary'], linewidth=2))
    ax.text(1.5, 13.7, '#7', ha='left', fontsize=10, fontweight='bold', color=COLORS['primary'])
    ax.text(3, 13.7, 'Tu', ha='left', fontsize=9, fontweight='bold', color=COLORS['text'])
    ax.text(8.5, 13.7, '78 pts', ha='right', fontsize=9, fontweight='bold', color=COLORS['primary'])

    # Leaderboard
    leaders = [
        ('1', '🥇 Mario R.', '156'),
        ('2', '🥈 Anna B.', '142'),
        ('3', '🥉 Luigi V.', '138'),
        ('4', 'Sara N.', '125'),
        ('5', 'Paolo M.', '118'),
        ('6', 'Elena G.', '98'),
    ]
    for i, (pos, name, pts) in enumerate(leaders):
        y = 12 - i*1.1
        draw_card(ax, 1, y, 8, 0.9)
        ax.text(1.5, y + 0.45, pos, ha='left', fontsize=8, fontweight='bold',
                color=COLORS['warning'] if i < 3 else COLORS['text_light'])
        ax.text(2.5, y + 0.45, name, ha='left', fontsize=8, color=COLORS['text'])
        ax.text(8.5, y + 0.45, f'{pts} pts', ha='right', fontsize=8, color=COLORS['text_light'])

    # Refresh note
    ax.text(5, 4.5, '↻ Aggiornamento in tempo reale', ha='center', fontsize=7, color=COLORS['text_light'])

    # Share button
    draw_button(ax, 1.5, 2.5, 7, 0.9, '📤 CONDIVIDI RISULTATO', color=COLORS['secondary'])
    draw_button(ax, 1.5, 1.2, 7, 0.9, 'CHIUDI', color=COLORS['primary'])

    ax.text(5, 20.5, 'WIREFRAME: MOBILE LEADERBOARD', ha='center', fontsize=10, fontweight='bold', color=COLORS['text'])

    plt.tight_layout()
    plt.savefig('/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/wireframe_mobile_leaderboard.svg',
                format='svg', bbox_inches='tight')
    plt.close()
    print("✓ wireframe_mobile_leaderboard.svg")


# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    print("\n📐 Generazione Wireframe Clinical Quiz (SVG)\n")
    print("=" * 50)

    print("\n🔷 ADMIN WIREFRAMES")
    create_wireframe_login()
    create_wireframe_admin_dashboard()
    create_wireframe_admin_users()
    create_wireframe_admin_create_user()
    create_wireframe_admin_reports()

    print("\n🔶 CREATOR WIREFRAMES")
    create_wireframe_creator_dashboard()
    create_wireframe_wizard_step1()
    create_wireframe_wizard_step2()
    create_wireframe_wizard_step3()
    create_wireframe_wizard_step4()
    create_wireframe_wizard_step5()
    create_wireframe_qr_code()
    create_wireframe_monitor_live()

    print("\n📱 MOBILE WIREFRAMES (PARTECIPANTE)")
    create_wireframe_mobile_landing()
    create_wireframe_mobile_welcome()
    create_wireframe_mobile_registration()
    create_wireframe_mobile_question()
    create_wireframe_mobile_correct()
    create_wireframe_mobile_wrong()
    create_wireframe_mobile_results()
    create_wireframe_mobile_leaderboard()

    print("\n" + "=" * 50)
    print("✅ Tutti i wireframe generati in output/")
    print("=" * 50 + "\n")
