#!/usr/bin/env python3
"""
Clinical Quiz - Wireframe SVG per Figma
Genera SVG con elementi separati editabili in Figma
"""

import svgwrite
from svgwrite import cm, mm
import os

OUTPUT_DIR = '/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/figma_wireframes'

# Colori
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

def create_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================
# COMPONENTI RIUTILIZZABILI
# ============================================

def add_rounded_rect(dwg, group, x, y, w, h, fill, rx=8, stroke=None, stroke_width=1, opacity=1.0):
    """Rettangolo arrotondato"""
    rect = dwg.rect(insert=(x, y), size=(w, h), rx=rx, ry=rx, fill=fill)
    if opacity < 1.0:
        rect['fill-opacity'] = opacity
    if stroke:
        rect['stroke'] = stroke
        rect['stroke-width'] = stroke_width
    group.add(rect)
    return rect

def add_text(dwg, group, x, y, text, size=14, color='#212121', anchor='start', weight='normal'):
    """Testo"""
    t = dwg.text(text, insert=(x, y), fill=color,
                 style=f"font-family: Arial, sans-serif; font-size: {size}px; font-weight: {weight}")
    t['text-anchor'] = anchor
    group.add(t)
    return t

def add_button(dwg, group, x, y, w, h, text, bg_color=None, text_color='#FFFFFF'):
    """Pulsante"""
    import re
    if bg_color is None:
        bg_color = COLORS['primary']
    safe_text = re.sub(r'[^a-zA-Z0-9_]', '', text.replace(" ", "_"))
    btn_group = dwg.g(id=f'button_{safe_text}')
    add_rounded_rect(dwg, btn_group, x, y, w, h, bg_color, rx=6)
    add_text(dwg, btn_group, x + w/2, y + h/2 + 5, text, size=12, color=text_color, anchor='middle', weight='bold')
    group.add(btn_group)
    return btn_group

def add_input(dwg, group, x, y, w, h, placeholder='', label=''):
    """Campo input"""
    import re
    safe_label = re.sub(r'[^a-zA-Z0-9_]', '', label.replace(" ", "_"))
    input_group = dwg.g(id=f'input_{safe_label}')
    if label:
        add_text(dwg, input_group, x, y - 8, label, size=11, color=COLORS['text'])
    add_rounded_rect(dwg, input_group, x, y, w, h, COLORS['input_bg'], rx=4, stroke=COLORS['border'])
    if placeholder:
        add_text(dwg, input_group, x + 12, y + h/2 + 4, placeholder, size=12, color=COLORS['text_light'])
    group.add(input_group)
    return input_group

def add_card(dwg, group, x, y, w, h):
    """Card"""
    return add_rounded_rect(dwg, group, x, y, w, h, COLORS['card'], rx=8, stroke=COLORS['border'])

def add_circle(dwg, group, cx, cy, r, fill):
    """Cerchio"""
    circle = dwg.circle(center=(cx, cy), r=r, fill=fill)
    group.add(circle)
    return circle

def add_sidebar(dwg, group, x, y, w, h, items, active_index=0):
    """Sidebar navigazione"""
    sidebar = dwg.g(id='sidebar')
    add_rounded_rect(dwg, sidebar, x, y, w, h, COLORS['primary'], rx=0)

    item_h = 40
    start_y = y + 60
    for i, item in enumerate(items):
        item_y = start_y + i * item_h
        if i == active_index:
            add_rounded_rect(dwg, sidebar, x, item_y, w, item_h, '#FFFFFF', rx=0, opacity=0.15)
        add_text(dwg, sidebar, x + 20, item_y + 26, item, size=13, color='#FFFFFF')

    group.add(sidebar)
    return sidebar

def add_browser_frame(dwg, group, w, h, title=''):
    """Frame browser desktop"""
    frame = dwg.g(id='browser_frame')
    # Window
    add_rounded_rect(dwg, frame, 0, 0, w, h, COLORS['bg'], rx=8, stroke=COLORS['border'], stroke_width=2)
    # Title bar
    add_rounded_rect(dwg, frame, 0, 0, w, 40, COLORS['frame'], rx=8)
    # Hide bottom corners of title bar
    dwg.rect(insert=(0, 32), size=(w, 10), fill=COLORS['frame'])
    frame.add(dwg.rect(insert=(0, 32), size=(w, 10), fill=COLORS['frame']))
    # Browser dots
    add_circle(dwg, frame, 20, 20, 6, '#FF5F56')
    add_circle(dwg, frame, 40, 20, 6, '#FFBD2E')
    add_circle(dwg, frame, 60, 20, 6, '#27CA3F')
    # URL bar
    add_rounded_rect(dwg, frame, 100, 10, w - 150, 22, '#FFFFFF', rx=4, stroke=COLORS['border'])
    add_text(dwg, frame, w/2, 25, f'clinicalquiz.app/{title}', size=10, color=COLORS['text_light'], anchor='middle')

    group.add(frame)
    return frame

def add_phone_frame(dwg, group, x, y, w, h, title=''):
    """Frame smartphone"""
    frame = dwg.g(id='phone_frame')
    # Phone outline
    add_rounded_rect(dwg, frame, x, y, w, h, COLORS['bg'], rx=24, stroke=COLORS['text'], stroke_width=3)
    # Status bar
    add_rounded_rect(dwg, frame, x, y, w, 30, COLORS['frame'], rx=24)
    frame.add(dwg.rect(insert=(x, y+20), size=(w, 12), fill=COLORS['frame']))
    add_text(dwg, frame, x + w/2, y + 20, '9:41', size=11, color=COLORS['text'], anchor='middle')
    # Title bar
    if title:
        add_rounded_rect(dwg, frame, x, y + 30, w, 44, COLORS['primary'], rx=0)
        add_text(dwg, frame, x + w/2, y + 58, title, size=14, color='#FFFFFF', anchor='middle', weight='bold')

    group.add(frame)
    return frame

def add_table(dwg, group, x, y, w, columns, rows):
    """Tabella"""
    table = dwg.g(id='table')
    col_w = w / len(columns)
    row_h = 36

    # Header
    add_rounded_rect(dwg, table, x, y, w, row_h, COLORS['frame'], rx=4)
    for i, col in enumerate(columns):
        add_text(dwg, table, x + i*col_w + col_w/2, y + 24, col, size=11, color=COLORS['text'], anchor='middle', weight='bold')

    # Rows
    for ri, row in enumerate(rows):
        row_y = y + row_h + ri * row_h
        add_rounded_rect(dwg, table, x, row_y, w, row_h, '#FFFFFF', rx=0, stroke=COLORS['frame'])
        for ci, cell in enumerate(row):
            add_text(dwg, table, x + ci*col_w + col_w/2, row_y + 24, str(cell), size=10, color=COLORS['text'], anchor='middle')

    group.add(table)
    return table


# ============================================
# WIREFRAME: LOGIN
# ============================================

def create_login():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_login.svg', size=(800, 600))
    main = dwg.g(id='login_page')

    add_browser_frame(dwg, main, 800, 600, 'login')

    # Logo placeholder
    logo = dwg.g(id='logo')
    add_rounded_rect(dwg, logo, 300, 80, 200, 80, COLORS['frame'], rx=8, stroke=COLORS['border'])
    add_text(dwg, logo, 400, 128, 'LOGO', size=18, color=COLORS['text_light'], anchor='middle')
    main.add(logo)

    # Login card
    card = dwg.g(id='login_card')
    add_card(dwg, card, 225, 190, 350, 320)
    add_text(dwg, card, 400, 240, 'Accedi alla piattaforma', size=18, color=COLORS['text'], anchor='middle', weight='bold')

    add_input(dwg, card, 260, 280, 280, 44, 'Username', 'Username')
    add_input(dwg, card, 260, 360, 280, 44, '••••••••', 'Password')
    add_button(dwg, card, 260, 440, 280, 48, 'ACCEDI')

    main.add(card)

    # Title
    add_text(dwg, main, 400, 560, 'WIREFRAME: LOGIN', size=14, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_login.svg')


# ============================================
# WIREFRAME: ADMIN DASHBOARD
# ============================================

def create_admin_dashboard():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_admin_dashboard.svg', size=(1000, 700))
    main = dwg.g(id='admin_dashboard')

    add_browser_frame(dwg, main, 1000, 700, 'admin/dashboard')
    add_sidebar(dwg, main, 0, 40, 200, 660, ['Dashboard', 'Gestione Utenti', 'Report'], 0)

    # Header
    add_text(dwg, main, 240, 90, 'Dashboard Admin', size=22, color=COLORS['text'], weight='bold')

    # Stats cards
    stats = [('Creator Attivi', '24'), ('Quiz Totali', '156'), ('Partecipazioni', '3.2K')]
    for i, (label, value) in enumerate(stats):
        card_x = 240 + i * 250
        card = dwg.g(id=f'stat_card_{i}')
        add_card(dwg, card, card_x, 120, 220, 100)
        add_text(dwg, card, card_x + 110, 165, value, size=28, color=COLORS['primary'], anchor='middle', weight='bold')
        add_text(dwg, card, card_x + 110, 195, label, size=12, color=COLORS['text_light'], anchor='middle')
        main.add(card)

    # Recent activity
    activity = dwg.g(id='recent_activity')
    add_card(dwg, activity, 240, 250, 720, 350)
    add_text(dwg, activity, 270, 290, 'Attività Recente', size=16, color=COLORS['text'], weight='bold')

    columns = ['Data', 'Creator', 'Evento', 'Partecipanti']
    rows = [
        ('04/01', 'Dr. Rossi', 'Congresso Cardiologia', '145'),
        ('03/01', 'Dr. Bianchi', 'Workshop Chirurgia', '89'),
        ('02/01', 'Dr. Verdi', 'Corso ECM', '234'),
        ('01/01', 'Dr. Neri', 'Seminario Oncologia', '67'),
    ]
    add_table(dwg, activity, 260, 310, 680, columns, rows)
    main.add(activity)

    # Title
    add_text(dwg, main, 500, 660, 'WIREFRAME: ADMIN DASHBOARD', size=14, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_admin_dashboard.svg')


# ============================================
# WIREFRAME: GESTIONE UTENTI
# ============================================

def create_admin_users():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_admin_users.svg', size=(1000, 700))
    main = dwg.g(id='admin_users')

    add_browser_frame(dwg, main, 1000, 700, 'admin/users')
    add_sidebar(dwg, main, 0, 40, 200, 660, ['Dashboard', 'Gestione Utenti', 'Report'], 1)

    # Header
    add_text(dwg, main, 240, 90, 'Gestione Creator', size=22, color=COLORS['text'], weight='bold')
    add_button(dwg, main, 840, 65, 130, 40, '+ Nuovo Creator', COLORS['success'])

    # Search
    add_input(dwg, main, 240, 110, 300, 40, 'Cerca creator...')

    # Users table
    columns = ['Nome', 'Email', 'Quiz', 'Stato', 'Azioni']
    rows = [
        ('Dr. Mario Rossi', 'm.rossi@email.it', '12', 'Attivo', 'Edit | Del'),
        ('Dr. Anna Bianchi', 'a.bianchi@email.it', '8', 'Attivo', 'Edit | Del'),
        ('Dr. Luigi Verdi', 'l.verdi@email.it', '5', 'Inattivo', 'Edit | Del'),
        ('Dr. Sara Neri', 's.neri@email.it', '15', 'Attivo', 'Edit | Del'),
        ('Dr. Paolo Gialli', 'p.gialli@email.it', '3', 'Attivo', 'Edit | Del'),
    ]
    add_table(dwg, main, 240, 170, 720, columns, rows)

    # Pagination
    add_text(dwg, main, 600, 420, '< 1 2 3 ... 10 >', size=12, color=COLORS['text_light'], anchor='middle')

    # Title
    add_text(dwg, main, 500, 660, 'WIREFRAME: GESTIONE UTENTI', size=14, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_admin_users.svg')


# ============================================
# WIREFRAME: CREA CREATOR
# ============================================

def create_admin_create_user():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_admin_create_user.svg', size=(1000, 700))
    main = dwg.g(id='admin_create_user')

    add_browser_frame(dwg, main, 1000, 700, 'admin/users/new')
    add_sidebar(dwg, main, 0, 40, 200, 660, ['Dashboard', 'Gestione Utenti', 'Report'], 1)

    # Form card
    form = dwg.g(id='form_card')
    add_card(dwg, form, 240, 70, 720, 520)
    add_text(dwg, form, 600, 120, 'Nuovo Account Creator', size=20, color=COLORS['text'], anchor='middle', weight='bold')

    # Form fields
    add_input(dwg, form, 280, 160, 300, 44, 'Mario Rossi', 'Nome Completo *')
    add_input(dwg, form, 620, 160, 300, 44, 'm.rossi', 'Username *')
    add_input(dwg, form, 280, 260, 300, 44, 'mario.rossi@email.it', 'Email *')
    add_input(dwg, form, 620, 260, 300, 44, '••••••••', 'Password *')
    add_input(dwg, form, 280, 360, 640, 80, 'Note opzionali...', 'Note Interne')

    # Checkbox
    checkbox = dwg.g(id='checkbox')
    add_rounded_rect(dwg, checkbox, 280, 470, 20, 20, COLORS['primary'], rx=4, stroke=COLORS['border'])
    add_text(dwg, checkbox, 282, 486, '✓', size=14, color='#FFFFFF')
    add_text(dwg, checkbox, 310, 485, 'Invia credenziali via email', size=12, color=COLORS['text'])
    form.add(checkbox)

    # Buttons
    add_button(dwg, form, 720, 520, 100, 44, 'Annulla', COLORS['secondary'])
    add_button(dwg, form, 840, 520, 100, 44, 'Crea', COLORS['success'])

    main.add(form)

    # Title
    add_text(dwg, main, 500, 660, 'WIREFRAME: CREA CREATOR', size=14, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_admin_create_user.svg')


# ============================================
# WIREFRAME: CREATOR DASHBOARD
# ============================================

def create_creator_dashboard():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_creator_dashboard.svg', size=(1000, 700))
    main = dwg.g(id='creator_dashboard')

    add_browser_frame(dwg, main, 1000, 700, 'creator/dashboard')
    add_sidebar(dwg, main, 0, 40, 200, 660, ['Dashboard'], 0)

    # Header
    add_text(dwg, main, 240, 90, 'Benvenuto, Dr. Rossi', size=22, color=COLORS['text'], weight='bold')
    add_button(dwg, main, 840, 65, 130, 40, '+ Nuovo Quiz', COLORS['success'])

    # Stats
    stats = [('Quiz Attivi', '3'), ('Partecipanti', '456'), ('Media Risposte Esatte', '82%')]
    for i, (label, value) in enumerate(stats):
        card_x = 240 + i * 250
        card = dwg.g(id=f'stat_card_{i}')
        add_card(dwg, card, card_x, 120, 220, 100)
        add_text(dwg, card, card_x + 110, 165, value, size=28, color=COLORS['primary'], anchor='middle', weight='bold')
        add_text(dwg, card, card_x + 110, 195, label, size=11, color=COLORS['text_light'], anchor='middle')
        main.add(card)

    # Quiz list with scrollable container
    add_text(dwg, main, 260, 270, 'I Miei Quiz', size=16, color=COLORS['text'], weight='bold')

    # Scrollable container
    scroll_container = dwg.g(id='scroll_container')
    add_rounded_rect(dwg, scroll_container, 240, 290, 720, 310, '#FFFFFF', rx=8, stroke=COLORS['border'])

    quizzes = [
        ('Congresso Cardiologia 2024', 'Attivo', '04/01/2024', 'Centro Congressi Roma'),
        ('Workshop Chirurgia Mini-invasiva', 'Attivo', '15/02/2024', 'Ospedale San Raffaele'),
        ('ECM Medicina Interna', 'Bozza', '20/03/2024', '-'),
        ('Corso Aggiornamento Pediatria', 'Concluso', '10/12/2023', 'Università Milano'),
    ]
    for i, (title, status, date, location) in enumerate(quizzes):
        card_y = 300 + i * 72
        quiz_card = dwg.g(id=f'quiz_card_{i}')
        add_rounded_rect(dwg, quiz_card, 250, card_y, 690, 62, COLORS['card'], rx=6, stroke=COLORS['frame'])
        add_text(dwg, quiz_card, 270, card_y + 25, title, size=13, color=COLORS['text'], weight='bold')
        if status == 'Attivo':
            status_color = COLORS['success']
        elif status == 'Bozza':
            status_color = COLORS['warning']
        else:
            status_color = COLORS['text_light']
        add_text(dwg, quiz_card, 270, card_y + 48, f'● {status}  •  {date}  •  {location}', size=10, color=status_color)
        add_button(dwg, quiz_card, 850, card_y + 15, 70, 32, 'Apri', COLORS['secondary'])
        scroll_container.add(quiz_card)

    # Scroll indicator
    add_rounded_rect(dwg, scroll_container, 948, 300, 6, 60, COLORS['primary'], rx=3)
    add_rounded_rect(dwg, scroll_container, 948, 370, 6, 220, COLORS['frame'], rx=3)

    main.add(scroll_container)

    # Title
    add_text(dwg, main, 500, 660, 'WIREFRAME: CREATOR DASHBOARD', size=14, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_creator_dashboard.svg')


# ============================================
# WIREFRAME: WIZARD STEP 1
# ============================================

def create_wizard_step1():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_wizard_step1.svg', size=(1000, 700))
    main = dwg.g(id='wizard_step1')

    add_browser_frame(dwg, main, 1000, 700, 'creator/quiz/new')

    # Progress steps
    steps = ['Info Base', 'Grafica', 'Privacy', 'Import', 'Classifica']
    for i, step in enumerate(steps):
        cx = 200 + i * 150
        color = COLORS['primary'] if i == 0 else COLORS['frame']
        add_circle(dwg, main, cx, 80, 18, color)
        text_color = '#FFFFFF' if i == 0 else COLORS['text_light']
        add_text(dwg, main, cx, 85, str(i+1), size=12, color=text_color, anchor='middle', weight='bold')
        label_color = COLORS['text'] if i == 0 else COLORS['text_light']
        add_text(dwg, main, cx, 115, step, size=11, color=label_color, anchor='middle')
        if i < 4:
            main.add(dwg.line(start=(cx+25, 80), end=(cx+125, 80), stroke=COLORS['frame'], stroke_width=2))

    # Form card
    form = dwg.g(id='form')
    add_card(dwg, form, 100, 140, 800, 420)
    add_text(dwg, form, 500, 190, 'Step 1: Informazioni Base', size=18, color=COLORS['text'], anchor='middle', weight='bold')

    add_input(dwg, form, 150, 230, 700, 50, 'Es: Congresso Cardiologia 2024', 'Titolo Quiz *')
    add_input(dwg, form, 150, 330, 700, 100, 'Descrizione del quiz e istruzioni per i partecipanti...', 'Descrizione *')
    add_input(dwg, form, 150, 470, 320, 50, '04/01/2024', 'Data Evento')
    add_input(dwg, form, 530, 470, 320, 50, 'Centro Congressi Roma', 'Luogo (opzionale)')

    main.add(form)

    # Buttons
    add_button(dwg, main, 700, 590, 100, 44, 'Annulla', COLORS['secondary'])
    add_button(dwg, main, 820, 590, 100, 44, 'Avanti →', COLORS['primary'])

    # Title
    add_text(dwg, main, 500, 670, 'WIREFRAME: WIZARD STEP 1', size=14, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_wizard_step1.svg')


# ============================================
# WIREFRAME: WIZARD STEP 2 (GRAFICA)
# ============================================

def create_wizard_step2():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_wizard_step2.svg', size=(1000, 700))
    main = dwg.g(id='wizard_step2')

    add_browser_frame(dwg, main, 1000, 700, 'creator/quiz/new')

    # Progress steps
    steps = ['Info Base', 'Grafica', 'Privacy', 'Import', 'Classifica']
    for i, step in enumerate(steps):
        cx = 200 + i * 150
        color = COLORS['primary'] if i <= 1 else COLORS['frame']
        add_circle(dwg, main, cx, 80, 18, color)
        text_color = '#FFFFFF' if i <= 1 else COLORS['text_light']
        add_text(dwg, main, cx, 85, str(i+1), size=12, color=text_color, anchor='middle', weight='bold')
        label_color = COLORS['text'] if i <= 1 else COLORS['text_light']
        add_text(dwg, main, cx, 115, step, size=11, color=label_color, anchor='middle')
        if i < 4:
            line_color = COLORS['primary'] if i < 1 else COLORS['frame']
            main.add(dwg.line(start=(cx+25, 80), end=(cx+125, 80), stroke=line_color, stroke_width=2))

    # Form card
    form = dwg.g(id='form')
    add_card(dwg, form, 100, 140, 800, 420)
    add_text(dwg, form, 500, 190, 'Step 2: Personalizzazione Grafica', size=18, color=COLORS['text'], anchor='middle', weight='bold')

    # Logo upload
    add_text(dwg, form, 150, 240, 'Logo Evento', size=14, color=COLORS['text'], weight='bold')
    add_rounded_rect(dwg, form, 150, 260, 200, 120, COLORS['input_bg'], rx=8, stroke=COLORS['border'], stroke_width=2)
    add_text(dwg, form, 250, 320, 'Trascina logo', size=12, color=COLORS['text_light'], anchor='middle')
    add_text(dwg, form, 250, 340, 'o clicca per caricare', size=10, color=COLORS['text_light'], anchor='middle')
    add_text(dwg, form, 250, 365, 'PNG, JPG (max 2MB)', size=9, color=COLORS['text_light'], anchor='middle')

    # Color pickers
    add_text(dwg, form, 420, 240, 'Colori Tema', size=14, color=COLORS['text'], weight='bold')

    colors_data = [
        ('Primario', '#1976D2', 420),
        ('Secondario', '#757575', 560),
        ('Accento', '#FF5722', 700)
    ]

    for label, color, x in colors_data:
        add_text(dwg, form, x, 280, label, size=11, color=COLORS['text'])
        add_rounded_rect(dwg, form, x, 295, 100, 40, color, rx=6, stroke=COLORS['border'])
        add_text(dwg, form, x + 50, 320, color, size=10, color='#FFFFFF', anchor='middle')

    # Preview
    add_text(dwg, form, 420, 380, 'Anteprima', size=14, color=COLORS['text'], weight='bold')
    add_rounded_rect(dwg, form, 420, 400, 380, 130, COLORS['frame'], rx=8, stroke=COLORS['border'])
    add_rounded_rect(dwg, form, 430, 410, 360, 40, '#1976D2', rx=4)
    add_text(dwg, form, 610, 435, 'Header Quiz', size=12, color='#FFFFFF', anchor='middle')
    add_button(dwg, form, 530, 470, 140, 36, 'Pulsante', '#1976D2')

    main.add(form)

    # Buttons
    add_button(dwg, main, 580, 590, 100, 44, '← Indietro', COLORS['secondary'])
    add_button(dwg, main, 820, 590, 100, 44, 'Avanti →', COLORS['primary'])

    # Title
    add_text(dwg, main, 500, 670, 'WIREFRAME: WIZARD STEP 2', size=14, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_wizard_step2.svg')


# ============================================
# WIREFRAME: WIZARD STEP 3 (PRIVACY)
# ============================================

def create_wizard_step3():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_wizard_step3.svg', size=(1000, 700))
    main = dwg.g(id='wizard_step3')

    add_browser_frame(dwg, main, 1000, 700, 'creator/quiz/new')

    # Progress steps
    steps = ['Info Base', 'Grafica', 'Privacy', 'Import', 'Classifica']
    for i, step in enumerate(steps):
        cx = 200 + i * 150
        color = COLORS['primary'] if i <= 2 else COLORS['frame']
        add_circle(dwg, main, cx, 80, 18, color)
        text_color = '#FFFFFF' if i <= 2 else COLORS['text_light']
        add_text(dwg, main, cx, 85, str(i+1), size=12, color=text_color, anchor='middle', weight='bold')
        label_color = COLORS['text'] if i <= 2 else COLORS['text_light']
        add_text(dwg, main, cx, 115, step, size=11, color=label_color, anchor='middle')
        if i < 4:
            line_color = COLORS['primary'] if i < 2 else COLORS['frame']
            main.add(dwg.line(start=(cx+25, 80), end=(cx+125, 80), stroke=line_color, stroke_width=2))

    # Form card
    form = dwg.g(id='form')
    add_card(dwg, form, 100, 140, 800, 420)
    add_text(dwg, form, 500, 190, 'Step 3: Configurazione Privacy', size=18, color=COLORS['text'], anchor='middle', weight='bold')

    # Data fields section
    add_text(dwg, form, 150, 240, 'Dati richiesti ai partecipanti', size=14, color=COLORS['text'], weight='bold')

    checkboxes = [
        ('Nome', True, 270),
        ('Cognome', True, 310),
        ('Email', False, 350),
        ('Professione', False, 390)
    ]

    for label, checked, y in checkboxes:
        # Checkbox
        add_rounded_rect(dwg, form, 150, y, 20, 20, '#FFFFFF' if not checked else COLORS['primary'], rx=4, stroke=COLORS['border'])
        if checked:
            add_text(dwg, form, 160, y + 16, '✓', size=14, color='#FFFFFF', anchor='middle')
        add_text(dwg, form, 185, y + 15, label, size=13, color=COLORS['text'])

    # GDPR section
    add_text(dwg, form, 450, 240, 'Consenso GDPR', size=14, color=COLORS['text'], weight='bold')

    # Toggle
    add_rounded_rect(dwg, form, 450, 275, 50, 26, COLORS['primary'], rx=13)
    add_circle(dwg, form, 487, 288, 10, '#FFFFFF')
    add_text(dwg, form, 515, 292, 'Richiedi consenso obbligatorio', size=13, color=COLORS['text'])

    # Privacy text area
    add_text(dwg, form, 450, 340, 'Testo privacy personalizzato', size=12, color=COLORS['text'])
    add_rounded_rect(dwg, form, 450, 360, 400, 100, COLORS['input_bg'], rx=4, stroke=COLORS['border'])
    add_text(dwg, form, 465, 390, 'I tuoi dati saranno trattati secondo', size=11, color=COLORS['text_light'])
    add_text(dwg, form, 465, 410, 'la normativa GDPR vigente...', size=11, color=COLORS['text_light'])

    # Info box
    add_rounded_rect(dwg, form, 450, 480, 400, 50, '#E3F2FD', rx=6, stroke='#1976D2')
    add_text(dwg, form, 470, 510, 'ℹ I dati saranno visibili solo al Creator e Admin', size=11, color='#1976D2')

    main.add(form)

    # Buttons
    add_button(dwg, main, 580, 590, 100, 44, '← Indietro', COLORS['secondary'])
    add_button(dwg, main, 820, 590, 100, 44, 'Avanti →', COLORS['primary'])

    # Title
    add_text(dwg, main, 500, 670, 'WIREFRAME: WIZARD STEP 3', size=14, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_wizard_step3.svg')


# ============================================
# WIREFRAME: WIZARD STEP 4 (IMPORT)
# ============================================

def create_wizard_step4():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_wizard_step4.svg', size=(1000, 700))
    main = dwg.g(id='wizard_step4')

    add_browser_frame(dwg, main, 1000, 700, 'creator/quiz/new')

    # Progress steps
    steps = ['Info Base', 'Grafica', 'Privacy', 'Import', 'Classifica']
    for i, step in enumerate(steps):
        cx = 200 + i * 150
        color = COLORS['primary'] if i <= 3 else COLORS['frame']
        add_circle(dwg, main, cx, 80, 18, color)
        text_color = '#FFFFFF' if i <= 3 else COLORS['text_light']
        add_text(dwg, main, cx, 85, str(i+1), size=12, color=text_color, anchor='middle', weight='bold')
        label_color = COLORS['text'] if i <= 3 else COLORS['text_light']
        add_text(dwg, main, cx, 115, step, size=11, color=label_color, anchor='middle')
        if i < 4:
            line_color = COLORS['primary'] if i < 3 else COLORS['frame']
            main.add(dwg.line(start=(cx+25, 80), end=(cx+125, 80), stroke=line_color, stroke_width=2))

    # Form card
    form = dwg.g(id='form')
    add_card(dwg, form, 100, 140, 800, 420)
    add_text(dwg, form, 500, 190, 'Step 4: Importa Domande', size=18, color=COLORS['text'], anchor='middle', weight='bold')

    add_text(dwg, form, 150, 240, 'Link Google Form:', size=14, color=COLORS['text'], weight='bold')
    add_input(dwg, form, 150, 260, 550, 50, 'https://docs.google.com/forms/d/...')
    add_button(dwg, form, 720, 260, 130, 50, 'Importa', COLORS['primary'])

    add_text(dwg, form, 150, 350, 'Domande importate: 15', size=14, color=COLORS['success'])

    columns = ['#', 'Domanda', 'Difficoltà', 'Media']
    rows = [
        ('1', 'Qual è il trattamento di prima linea...', 'Facile', '-'),
        ('2', 'In caso di fibrillazione atriale...', 'Media', 'IMG'),
        ('3', 'Quale farmaco è controindicato...', 'Difficile', '-'),
    ]
    add_table(dwg, form, 150, 380, 700, columns, rows)

    main.add(form)

    # Buttons
    add_button(dwg, main, 580, 590, 100, 44, '← Indietro', COLORS['secondary'])
    add_button(dwg, main, 820, 590, 100, 44, 'Avanti →', COLORS['primary'])

    # Title
    add_text(dwg, main, 500, 670, 'WIREFRAME: WIZARD STEP 4', size=14, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_wizard_step4.svg')


# ============================================
# WIREFRAME: WIZARD STEP 5 (CLASSIFICA)
# ============================================

def create_wizard_step5():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_wizard_step5.svg', size=(1000, 700))
    main = dwg.g(id='wizard_step5')

    add_browser_frame(dwg, main, 1000, 700, 'creator/quiz/new')

    # Progress steps - all complete
    steps = ['Info Base', 'Grafica', 'Privacy', 'Import', 'Classifica']
    for i, step in enumerate(steps):
        cx = 200 + i * 150
        add_circle(dwg, main, cx, 80, 18, COLORS['primary'])
        add_text(dwg, main, cx, 85, str(i+1), size=12, color='#FFFFFF', anchor='middle', weight='bold')
        add_text(dwg, main, cx, 115, step, size=11, color=COLORS['text'], anchor='middle')
        if i < 4:
            main.add(dwg.line(start=(cx+25, 80), end=(cx+125, 80), stroke=COLORS['primary'], stroke_width=2))

    # Form card
    form = dwg.g(id='form')
    add_card(dwg, form, 100, 140, 800, 420)
    add_text(dwg, form, 500, 190, 'Step 5: Configurazione Classifica', size=18, color=COLORS['text'], anchor='middle', weight='bold')

    # Privacy username section
    add_text(dwg, form, 150, 235, 'Privacy Username', size=14, color=COLORS['text'], weight='bold')

    # Checkbox - Nome pubblico
    add_rounded_rect(dwg, form, 150, 260, 20, 20, COLORS['primary'], rx=4, stroke=COLORS['border'])
    add_text(dwg, form, 152, 276, '✓', size=14, color='#FFFFFF')
    add_text(dwg, form, 185, 275, 'Nome pubblico (Mario Rossi)', size=13, color=COLORS['text'])

    # Checkbox - Nome privato (iniziali)
    add_rounded_rect(dwg, form, 150, 295, 20, 20, '#FFFFFF', rx=4, stroke=COLORS['border'])
    add_text(dwg, form, 185, 310, 'Nome privato - solo iniziali (M.R.)', size=13, color=COLORS['text'])

    # Checkbox - Anonimo
    add_rounded_rect(dwg, form, 150, 330, 20, 20, '#FFFFFF', rx=4, stroke=COLORS['border'])
    add_text(dwg, form, 185, 345, 'Completamente anonimo (#123)', size=13, color=COLORS['text'])

    # Positions visible section
    add_text(dwg, form, 500, 235, 'Posizioni Visibili in Classifica', size=14, color=COLORS['text'], weight='bold')

    # Checkbox - Top 10
    add_rounded_rect(dwg, form, 500, 260, 20, 20, COLORS['primary'], rx=4, stroke=COLORS['border'])
    add_text(dwg, form, 502, 276, '✓', size=14, color='#FFFFFF')
    add_text(dwg, form, 535, 275, 'Top 10 partecipanti', size=13, color=COLORS['text'])

    # Checkbox - Top 20
    add_rounded_rect(dwg, form, 500, 295, 20, 20, '#FFFFFF', rx=4, stroke=COLORS['border'])
    add_text(dwg, form, 535, 310, 'Top 20 partecipanti', size=13, color=COLORS['text'])

    # Checkbox - Tutti
    add_rounded_rect(dwg, form, 500, 330, 20, 20, '#FFFFFF', rx=4, stroke=COLORS['border'])
    add_text(dwg, form, 535, 345, 'Tutti i partecipanti', size=13, color=COLORS['text'])

    # Additional options
    add_text(dwg, form, 150, 390, 'Opzioni Aggiuntive', size=14, color=COLORS['text'], weight='bold')

    # Mostra punti
    add_rounded_rect(dwg, form, 150, 415, 20, 20, COLORS['primary'], rx=4, stroke=COLORS['border'])
    add_text(dwg, form, 152, 431, '✓', size=14, color='#FFFFFF')
    add_text(dwg, form, 185, 430, 'Mostra punteggio in classifica', size=13, color=COLORS['text'])

    # Aggiornamento real-time
    add_rounded_rect(dwg, form, 150, 450, 20, 20, COLORS['primary'], rx=4, stroke=COLORS['border'])
    add_text(dwg, form, 152, 466, '✓', size=14, color='#FFFFFF')
    add_text(dwg, form, 185, 465, 'Aggiornamento classifica in tempo reale', size=13, color=COLORS['text'])

    # Notifica posizione
    add_rounded_rect(dwg, form, 500, 415, 20, 20, '#FFFFFF', rx=4, stroke=COLORS['border'])
    add_text(dwg, form, 535, 430, 'Notifica cambio posizione', size=13, color=COLORS['text'])

    # Condivisione social
    add_rounded_rect(dwg, form, 500, 450, 20, 20, COLORS['primary'], rx=4, stroke=COLORS['border'])
    add_text(dwg, form, 502, 466, '✓', size=14, color='#FFFFFF')
    add_text(dwg, form, 535, 465, 'Abilita condivisione risultato', size=13, color=COLORS['text'])

    # Preview leaderboard
    add_text(dwg, form, 150, 505, 'Anteprima', size=12, color=COLORS['text_light'])
    add_rounded_rect(dwg, form, 150, 515, 300, 35, COLORS['frame'], rx=4)
    add_text(dwg, form, 165, 538, '1. Mario Rossi  -  1250 pts', size=11, color=COLORS['text'])

    main.add(form)

    # Buttons
    add_button(dwg, main, 450, 590, 120, 44, '← Indietro', COLORS['secondary'])
    add_button(dwg, main, 590, 590, 150, 44, 'Salva Bozza', COLORS['secondary'])
    add_button(dwg, main, 760, 590, 150, 44, 'Pubblica', COLORS['success'])

    # Title
    add_text(dwg, main, 500, 670, 'WIREFRAME: WIZARD STEP 5', size=14, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_wizard_step5.svg')


# ============================================
# WIREFRAME: ADMIN REPORT
# ============================================

def create_admin_report():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_admin_report.svg', size=(1000, 700))
    main = dwg.g(id='admin_report')

    add_browser_frame(dwg, main, 1000, 700, 'admin')

    # Sidebar
    add_sidebar(dwg, main, 0, 40, 200, 660, ['Dashboard', 'Gestione Utenti', 'Report'], 2)

    # Main content
    content = dwg.g(id='content')
    add_text(dwg, content, 230, 85, 'Report Aggregati', size=24, color=COLORS['text'], weight='bold')

    # Filters
    add_input(dwg, content, 230, 110, 180, 40, 'Da: 01/01/2024', 'Periodo')
    add_input(dwg, content, 430, 110, 180, 40, 'A: 31/12/2024')
    add_button(dwg, content, 850, 120, 120, 40, 'Esporta Excel', COLORS['secondary'])

    # Stats cards
    stats = [
        ('Creator Attivi', '24', 230),
        ('Quiz Creati', '156', 430),
        ('Partecipazioni', '12.450', 630),
        ('Media Risposte', '78%', 830)
    ]
    for label, value, x in stats:
        add_card(dwg, content, x, 180, 170, 100)
        add_text(dwg, content, x + 85, 220, value, size=28, color=COLORS['primary'], anchor='middle', weight='bold')
        add_text(dwg, content, x + 85, 255, label, size=11, color=COLORS['text_light'], anchor='middle')

    # Chart placeholder
    add_card(dwg, content, 230, 300, 480, 200)
    add_text(dwg, content, 470, 340, 'Andamento Partecipazioni', size=14, color=COLORS['text'], anchor='middle', weight='bold')
    add_rounded_rect(dwg, content, 260, 360, 420, 120, COLORS['frame'], rx=4)
    add_text(dwg, content, 470, 430, '[Grafico a linee]', size=14, color=COLORS['text_light'], anchor='middle')

    # Top events
    add_card(dwg, content, 730, 300, 250, 200)
    add_text(dwg, content, 855, 340, 'Top Eventi', size=14, color=COLORS['text'], anchor='middle', weight='bold')
    events = ['Congresso Cardiologia', 'Summit Oncologia', 'Forum Neurologia']
    for i, evt in enumerate(events):
        add_text(dwg, content, 750, 380 + i * 30, f'{i+1}. {evt}', size=11, color=COLORS['text'])

    # Recent activity table
    add_text(dwg, content, 230, 530, 'Attivita Recente', size=14, color=COLORS['text'], weight='bold')
    columns = ['Data', 'Evento', 'Creator', 'Partecipanti', 'Completati']
    rows = [
        ('04/01/24', 'Quiz Cardiologia', 'Dr. Rossi', '45', '42 (93%)'),
        ('03/01/24', 'Test Oncologia', 'Dr. Bianchi', '120', '98 (82%)'),
    ]
    add_table(dwg, content, 230, 550, 750, columns, rows)

    main.add(content)

    # Title
    add_text(dwg, main, 600, 680, 'WIREFRAME: ADMIN REPORT', size=14, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_admin_report.svg')


# ============================================
# WIREFRAME: EVENT DETAIL
# ============================================

def create_event_detail():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_event_detail.svg', size=(1000, 700))
    main = dwg.g(id='event_detail')

    add_browser_frame(dwg, main, 1000, 700, 'creator/event/EVT-2024-ABC')

    # Header
    header = dwg.g(id='header')
    add_text(dwg, header, 30, 85, '← Torna ai miei quiz', size=12, color=COLORS['primary'])
    add_text(dwg, header, 30, 120, 'Congresso Nazionale Cardiologia 2024', size=22, color=COLORS['text'], weight='bold')

    # Status badge
    add_rounded_rect(dwg, header, 500, 100, 80, 28, COLORS['success'], rx=14)
    add_text(dwg, header, 540, 120, 'Attivo', size=11, color='#FFFFFF', anchor='middle')

    add_button(dwg, header, 800, 95, 80, 36, 'Modifica', COLORS['secondary'])
    add_button(dwg, header, 895, 95, 80, 36, 'Termina', COLORS['error'])
    main.add(header)

    # Stats row
    stats = [
        ('Partecipanti', '127', 30),
        ('Completati', '98 (77%)', 210),
        ('In corso', '12', 390),
        ('Media punteggio', '845 pts', 570),
        ('Tempo medio', '4:32 min', 750)
    ]
    for label, value, x in stats:
        add_card(dwg, main, x, 145, 160, 80)
        add_text(dwg, main, x + 80, 175, value, size=18, color=COLORS['primary'], anchor='middle', weight='bold')
        add_text(dwg, main, x + 80, 200, label, size=10, color=COLORS['text_light'], anchor='middle')

    # Two columns
    # Left: Access info
    access = dwg.g(id='access_info')
    add_card(dwg, access, 30, 245, 300, 200)
    add_text(dwg, access, 50, 280, 'Accesso Quiz', size=14, color=COLORS['text'], weight='bold')

    add_text(dwg, access, 50, 315, 'Codice stanza:', size=11, color=COLORS['text_light'])
    add_rounded_rect(dwg, access, 50, 325, 180, 40, COLORS['input_bg'], rx=4, stroke=COLORS['primary'])
    add_text(dwg, access, 140, 350, 'EVT-2024-ABC', size=14, color=COLORS['text'], anchor='middle', weight='bold')

    add_text(dwg, access, 50, 390, 'QR Code:', size=11, color=COLORS['text_light'])
    add_rounded_rect(dwg, access, 50, 400, 60, 60, COLORS['frame'], rx=4)
    add_button(dwg, access, 130, 415, 100, 30, 'Scarica', COLORS['secondary'])
    main.add(access)

    # Right: Leaderboard preview
    leaderboard = dwg.g(id='leaderboard')
    add_card(dwg, leaderboard, 350, 245, 310, 200)
    add_text(dwg, leaderboard, 370, 280, 'Classifica Live', size=14, color=COLORS['text'], weight='bold')

    leaders = [
        ('1', 'Mario Rossi', '1250 pts'),
        ('2', 'Luigi Bianchi', '1180 pts'),
        ('3', 'Anna Verdi', '1050 pts'),
        ('4', 'Paolo Neri', '980 pts')
    ]
    for i, (pos, name, pts) in enumerate(leaders):
        y = 310 + i * 30
        add_text(dwg, leaderboard, 380, y, pos, size=12, color=COLORS['primary'], weight='bold')
        add_text(dwg, leaderboard, 410, y, name, size=12, color=COLORS['text'])
        add_text(dwg, leaderboard, 580, y, pts, size=12, color=COLORS['text_light'])
    main.add(leaderboard)

    # Questions stats
    questions = dwg.g(id='questions')
    add_card(dwg, questions, 680, 245, 290, 200)
    add_text(dwg, questions, 700, 280, 'Domande (15)', size=14, color=COLORS['text'], weight='bold')

    q_stats = [
        ('Facili', '5', '92%', COLORS['success']),
        ('Medie', '7', '68%', COLORS['warning']),
        ('Difficili', '3', '45%', COLORS['error'])
    ]
    for i, (diff, count, pct, color) in enumerate(q_stats):
        y = 310 + i * 35
        add_text(dwg, questions, 700, y, diff, size=11, color=COLORS['text'])
        add_text(dwg, questions, 780, y, f'x{count}', size=11, color=COLORS['text_light'])
        add_rounded_rect(dwg, questions, 820, y - 12, 100, 16, COLORS['frame'], rx=3)
        w = int(float(pct.replace('%', '')))
        add_rounded_rect(dwg, questions, 820, y - 12, w, 16, color, rx=3)
        add_text(dwg, questions, 935, y, pct, size=10, color=COLORS['text_light'])
    main.add(questions)

    # Participants table
    add_text(dwg, main, 30, 480, 'Partecipanti Recenti', size=14, color=COLORS['text'], weight='bold')
    add_button(dwg, main, 820, 465, 150, 36, 'Esporta Excel', COLORS['primary'])

    columns = ['Nome', 'Email', 'Punteggio', 'Tempo', 'Stato']
    rows = [
        ('Mario Rossi', 'm.rossi@email.com', '1250 pts', '3:45', 'Completato'),
        ('Luigi Bianchi', 'l.bianchi@email.com', '1180 pts', '4:12', 'Completato'),
        ('Sara Verdi', 's.verdi@email.com', '-', '2:30', 'In corso'),
    ]
    add_table(dwg, main, 30, 500, 940, columns, rows)

    # Title
    add_text(dwg, main, 500, 680, 'WIREFRAME: DETTAGLIO QUIZ', size=14, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_event_detail.svg')


# ============================================
# WIREFRAME: QR CODE
# ============================================

def create_qr_code():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_qr_code.svg', size=(1000, 700))
    main = dwg.g(id='qr_code_page')

    add_browser_frame(dwg, main, 1000, 700, 'creator/quiz/published')

    # Success banner
    success = dwg.g(id='success_banner')
    add_rounded_rect(dwg, success, 150, 70, 700, 80, '#E8F5E9', rx=8, stroke=COLORS['success'])
    add_text(dwg, success, 500, 105, '✓ Quiz pubblicato con successo!', size=18, color=COLORS['success'], anchor='middle', weight='bold')
    add_text(dwg, success, 500, 130, 'Condividi il QR code o il codice stanza con i partecipanti', size=12, color=COLORS['text'], anchor='middle')
    main.add(success)

    # QR Code section
    qr_section = dwg.g(id='qr_section')
    add_card(dwg, qr_section, 150, 180, 300, 380)
    add_text(dwg, qr_section, 300, 220, 'QR Code', size=16, color=COLORS['text'], anchor='middle', weight='bold')
    # QR placeholder
    add_rounded_rect(dwg, qr_section, 200, 250, 200, 200, COLORS['frame'], rx=8, stroke=COLORS['border'])
    add_text(dwg, qr_section, 300, 360, 'QR CODE', size=20, color=COLORS['text_light'], anchor='middle')
    add_button(dwg, qr_section, 200, 480, 200, 44, 'Scarica PNG', COLORS['primary'])
    main.add(qr_section)

    # Room code section
    code_section = dwg.g(id='code_section')
    add_card(dwg, code_section, 550, 180, 300, 380)
    add_text(dwg, code_section, 700, 220, 'Codice Stanza', size=16, color=COLORS['text'], anchor='middle', weight='bold')
    # Code box
    add_rounded_rect(dwg, code_section, 580, 280, 240, 80, COLORS['input_bg'], rx=8, stroke=COLORS['primary'], stroke_width=3)
    add_text(dwg, code_section, 700, 330, 'EVT-2024-ABC', size=24, color=COLORS['text'], anchor='middle', weight='bold')

    add_text(dwg, code_section, 700, 400, 'URL diretto:', size=12, color=COLORS['text_light'], anchor='middle')
    add_text(dwg, code_section, 700, 425, 'clinicalquiz.app/q/EVT-2024-ABC', size=11, color=COLORS['primary'], anchor='middle')

    add_button(dwg, code_section, 600, 480, 200, 44, 'Copia Link', COLORS['secondary'])
    main.add(code_section)

    # Title
    add_text(dwg, main, 500, 660, 'WIREFRAME: QR CODE & CODICE', size=14, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_qr_code.svg')


# ============================================
# WIREFRAME: MOBILE LANDING
# ============================================

def create_mobile_landing():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_mobile_landing.svg', size=(375, 812))
    main = dwg.g(id='mobile_landing')

    add_phone_frame(dwg, main, 0, 0, 375, 812, 'Clinical Quiz')

    # Logo
    logo = dwg.g(id='logo')
    add_rounded_rect(dwg, logo, 87, 140, 200, 80, COLORS['frame'], rx=8, stroke=COLORS['border'])
    add_text(dwg, logo, 187, 190, 'LOGO', size=20, color=COLORS['text_light'], anchor='middle')
    main.add(logo)

    # Welcome text
    add_text(dwg, main, 187, 270, 'Benvenuto!', size=24, color=COLORS['text'], anchor='middle', weight='bold')
    add_text(dwg, main, 187, 310, 'Inserisci il codice stanza', size=14, color=COLORS['text_light'], anchor='middle')
    add_text(dwg, main, 187, 330, 'per accedere al quiz', size=14, color=COLORS['text_light'], anchor='middle')

    # Code input
    add_input(dwg, main, 40, 380, 295, 55, 'EVT-2024-ABC', 'Codice Stanza')

    # Divider
    main.add(dwg.line(start=(40, 480), end=(150, 480), stroke=COLORS['frame'], stroke_width=1))
    add_text(dwg, main, 187, 485, 'oppure', size=12, color=COLORS['text_light'], anchor='middle')
    main.add(dwg.line(start=(225, 480), end=(335, 480), stroke=COLORS['frame'], stroke_width=1))

    # QR button
    add_button(dwg, main, 40, 520, 295, 55, 'Scansiona QR Code', COLORS['secondary'])

    # Enter button
    add_button(dwg, main, 40, 620, 295, 55, 'ACCEDI', COLORS['primary'])

    # Title
    add_text(dwg, main, 187, 780, 'WIREFRAME: MOBILE LANDING', size=10, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_mobile_landing.svg')


# ============================================
# WIREFRAME: MOBILE START QUIZ (REGISTRAZIONE)
# ============================================

def create_mobile_start():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_mobile_start.svg', size=(375, 812))
    main = dwg.g(id='mobile_start')

    add_phone_frame(dwg, main, 0, 0, 375, 812, 'Congresso Cardiologia 2024')

    # Event logo placeholder
    logo = dwg.g(id='logo')
    add_rounded_rect(dwg, logo, 112, 100, 150, 70, COLORS['frame'], rx=8, stroke=COLORS['border'])
    add_text(dwg, logo, 187, 140, 'LOGO EVENTO', size=12, color=COLORS['text_light'], anchor='middle')
    main.add(logo)

    # Welcome message
    add_text(dwg, main, 187, 210, 'Benvenuto al Quiz!', size=20, color=COLORS['text'], anchor='middle', weight='bold')
    add_text(dwg, main, 187, 240, 'Compila i tuoi dati per iniziare', size=12, color=COLORS['text_light'], anchor='middle')

    # Registration form
    form = dwg.g(id='form')
    add_input(dwg, form, 40, 280, 295, 50, 'Mario', 'Nome *')
    add_input(dwg, form, 40, 370, 295, 50, 'Rossi', 'Cognome *')
    add_input(dwg, form, 40, 460, 295, 50, 'mario.rossi@email.it', 'Email (opzionale)')
    main.add(form)

    # GDPR Consent
    gdpr = dwg.g(id='gdpr')
    add_rounded_rect(dwg, gdpr, 40, 540, 24, 24, COLORS['primary'], rx=4)
    add_text(dwg, gdpr, 52, 558, '✓', size=16, color='#FFFFFF', anchor='middle')
    add_text(dwg, gdpr, 75, 548, 'Accetto il trattamento dei dati', size=11, color=COLORS['text'])
    add_text(dwg, gdpr, 75, 565, 'personali secondo la normativa GDPR', size=11, color=COLORS['text'])
    add_text(dwg, gdpr, 75, 585, 'Leggi informativa', size=10, color=COLORS['primary'])
    main.add(gdpr)

    # Quiz info
    info = dwg.g(id='info')
    add_rounded_rect(dwg, info, 40, 620, 295, 60, '#E3F2FD', rx=8)
    add_text(dwg, info, 187, 645, '15 domande • Tempo: ~10 min', size=11, color=COLORS['primary'], anchor='middle')
    add_text(dwg, info, 187, 665, 'Rispondi correttamente per scalare la classifica!', size=10, color=COLORS['text_light'], anchor='middle')
    main.add(info)

    # Start button
    add_button(dwg, main, 40, 710, 295, 55, 'INIZIA QUIZ', COLORS['success'])

    # Title
    add_text(dwg, main, 187, 790, 'WIREFRAME: MOBILE START', size=10, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_mobile_start.svg')


# ============================================
# WIREFRAME: MOBILE QUESTION
# ============================================

def create_mobile_question():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_mobile_question.svg', size=(375, 812))
    main = dwg.g(id='mobile_question')

    add_phone_frame(dwg, main, 0, 0, 375, 812, 'Domanda 3/15')

    # Small logo in header
    logo = dwg.g(id='logo_small')
    add_rounded_rect(dwg, logo, 20, 90, 80, 35, COLORS['frame'], rx=4, stroke=COLORS['border'])
    add_text(dwg, logo, 60, 113, 'LOGO', size=10, color=COLORS['text_light'], anchor='middle')
    main.add(logo)

    # Difficulty badge
    add_rounded_rect(dwg, main, 137, 90, 100, 24, COLORS['warning'], rx=12)
    add_text(dwg, main, 187, 107, 'Difficoltà: Media', size=10, color='#FFFFFF', anchor='middle', weight='bold')

    # Timer
    add_circle(dwg, main, 330, 105, 20, '#FFFFFF')
    main.add(dwg.circle(center=(330, 105), r=20, fill='none', stroke=COLORS['warning'], stroke_width=3))
    add_text(dwg, main, 330, 111, '45', size=12, color=COLORS['warning'], anchor='middle', weight='bold')

    # Progress bar
    add_rounded_rect(dwg, main, 20, 140, 335, 8, COLORS['frame'], rx=4)
    add_rounded_rect(dwg, main, 20, 140, 67, 8, COLORS['primary'], rx=4)  # 20% progress

    # Points
    add_text(dwg, main, 40, 170, '24 pts', size=14, color=COLORS['text'], weight='bold')

    # Question card
    question = dwg.g(id='question')
    add_card(dwg, question, 20, 190, 335, 120)
    add_text(dwg, question, 187, 225, 'Qual è il trattamento di prima', size=14, color=COLORS['text'], anchor='middle', weight='bold')
    add_text(dwg, question, 187, 250, 'linea per la fibrillazione', size=14, color=COLORS['text'], anchor='middle', weight='bold')
    add_text(dwg, question, 187, 275, 'atriale parossistica?', size=14, color=COLORS['text'], anchor='middle', weight='bold')
    main.add(question)

    # Answer options
    options = ['A) Beta-bloccanti', 'B) ACE inibitori', 'C) Anticoagulanti', 'D) Calcio antagonisti']
    for i, opt in enumerate(options):
        opt_y = 330 + i * 75
        opt_group = dwg.g(id=f'option_{i}')
        add_card(dwg, opt_group, 20, opt_y, 335, 60)
        add_circle(dwg, opt_group, 55, opt_y + 30, 12, '#FFFFFF')
        main.add(dwg.circle(center=(55, opt_y + 30), r=12, fill='none', stroke=COLORS['primary'], stroke_width=2))
        add_text(dwg, opt_group, 80, opt_y + 36, opt, size=14, color=COLORS['text'])
        main.add(opt_group)

    # Confirm button
    add_button(dwg, main, 40, 640, 295, 55, 'CONFERMA', COLORS['primary'])

    # Title
    add_text(dwg, main, 187, 780, 'WIREFRAME: MOBILE QUESTION', size=10, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_mobile_question.svg')


# ============================================
# WIREFRAME: MOBILE CORRECT
# ============================================

def create_mobile_correct():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_mobile_correct.svg', size=(375, 812))
    main = dwg.g(id='mobile_correct')

    add_phone_frame(dwg, main, 0, 0, 375, 812, 'Domanda 3/15')

    # Small logo in header
    logo = dwg.g(id='logo_small')
    add_rounded_rect(dwg, logo, 20, 90, 80, 35, COLORS['frame'], rx=4, stroke=COLORS['border'])
    add_text(dwg, logo, 60, 113, 'LOGO', size=10, color=COLORS['text_light'], anchor='middle')
    main.add(logo)

    # Difficulty badge
    add_rounded_rect(dwg, main, 137, 90, 100, 24, COLORS['warning'], rx=12)
    add_text(dwg, main, 187, 107, 'Difficoltà: Media', size=10, color='#FFFFFF', anchor='middle', weight='bold')

    # Progress bar
    add_rounded_rect(dwg, main, 20, 140, 335, 8, COLORS['frame'], rx=4)
    add_rounded_rect(dwg, main, 20, 140, 67, 8, COLORS['primary'], rx=4)

    # Success icon
    add_circle(dwg, main, 187, 210, 45, COLORS['success'])
    add_text(dwg, main, 187, 225, '✓', size=36, color='#FFFFFF', anchor='middle')

    # Message
    add_text(dwg, main, 187, 290, 'Corretto!', size=24, color=COLORS['success'], anchor='middle', weight='bold')
    add_text(dwg, main, 187, 320, '+15 punti', size=16, color=COLORS['success'], anchor='middle')

    # Feedback card
    feedback = dwg.g(id='feedback')
    add_card(dwg, feedback, 20, 360, 335, 220)
    add_text(dwg, feedback, 187, 395, 'Feedback', size=16, color=COLORS['text'], anchor='middle', weight='bold')
    add_text(dwg, feedback, 40, 430, 'Esatto! I beta-bloccanti sono', size=12, color=COLORS['text_light'])
    add_text(dwg, feedback, 40, 455, 'effettivamente il trattamento di', size=12, color=COLORS['text_light'])
    add_text(dwg, feedback, 40, 480, 'prima linea per il controllo della', size=12, color=COLORS['text_light'])
    add_text(dwg, feedback, 40, 505, 'frequenza nella FA parossistica.', size=12, color=COLORS['text_light'])
    main.add(feedback)

    # Points
    add_text(dwg, main, 187, 620, 'Punteggio attuale: 34 pts', size=14, color=COLORS['text'], anchor='middle', weight='bold')

    # Continue button
    add_button(dwg, main, 40, 660, 295, 55, 'PROSSIMA DOMANDA →', COLORS['primary'])

    # Title
    add_text(dwg, main, 187, 780, 'WIREFRAME: MOBILE CORRECT', size=10, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_mobile_correct.svg')


# ============================================
# WIREFRAME: MOBILE WRONG
# ============================================

def create_mobile_wrong():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_mobile_wrong.svg', size=(375, 812))
    main = dwg.g(id='mobile_wrong')

    add_phone_frame(dwg, main, 0, 0, 375, 812, 'Domanda 3/15')

    # Small logo in header
    logo = dwg.g(id='logo_small')
    add_rounded_rect(dwg, logo, 20, 90, 80, 35, COLORS['frame'], rx=4, stroke=COLORS['border'])
    add_text(dwg, logo, 60, 113, 'LOGO', size=10, color=COLORS['text_light'], anchor='middle')
    main.add(logo)

    # Difficulty badge
    add_rounded_rect(dwg, main, 137, 90, 100, 24, COLORS['warning'], rx=12)
    add_text(dwg, main, 187, 107, 'Difficoltà: Media', size=10, color='#FFFFFF', anchor='middle', weight='bold')

    # Progress bar
    add_rounded_rect(dwg, main, 20, 140, 335, 8, COLORS['frame'], rx=4)
    add_rounded_rect(dwg, main, 20, 140, 67, 8, COLORS['primary'], rx=4)

    # Error icon
    add_circle(dwg, main, 187, 195, 40, COLORS['error'])
    add_text(dwg, main, 187, 207, '✗', size=32, color='#FFFFFF', anchor='middle')

    # Message
    add_text(dwg, main, 187, 260, 'Non corretto', size=20, color=COLORS['error'], anchor='middle', weight='bold')
    add_text(dwg, main, 187, 290, 'Risposta corretta: A) Beta-bloccanti', size=12, color=COLORS['success'], anchor='middle', weight='bold')

    # AI Feedback card
    feedback = dwg.g(id='ai_feedback')
    add_card(dwg, feedback, 20, 320, 335, 270)
    add_text(dwg, feedback, 187, 355, 'Feedback del Dr. AI', size=14, color=COLORS['text'], anchor='middle', weight='bold')

    lines = [
        'Gli ACE inibitori, sebbene utili nel',
        'trattamento dello scompenso cardiaco,',
        'non sono indicati come prima linea',
        'per la FA.',
        '',
        'I beta-bloccanti sono preferiti perché',
        'agiscono direttamente sul nodo AV,',
        'rallentando la conduzione e',
        'controllando la frequenza ventricolare.'
    ]
    for i, line in enumerate(lines):
        add_text(dwg, feedback, 40, 390 + i * 20, line, size=11, color=COLORS['text_light'])
    main.add(feedback)

    # Points
    add_text(dwg, main, 187, 620, 'Punteggio attuale: 19 pts', size=14, color=COLORS['text'], anchor='middle', weight='bold')

    # Continue button
    add_button(dwg, main, 40, 660, 295, 55, 'PROSEGUI →', COLORS['primary'])

    # Title
    add_text(dwg, main, 187, 780, 'WIREFRAME: MOBILE WRONG + AI', size=10, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_mobile_wrong.svg')


# ============================================
# WIREFRAME: MOBILE RESULTS
# ============================================

def create_mobile_results():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_mobile_results.svg', size=(375, 812))
    main = dwg.g(id='mobile_results')

    add_phone_frame(dwg, main, 0, 0, 375, 812, 'Risultati')

    # Logo centered
    logo = dwg.g(id='logo')
    add_rounded_rect(dwg, logo, 147, 90, 80, 35, COLORS['frame'], rx=4, stroke=COLORS['border'])
    add_text(dwg, logo, 187, 113, 'LOGO', size=10, color=COLORS['text_light'], anchor='middle')
    main.add(logo)

    # Congrats
    add_text(dwg, main, 187, 155, 'Quiz Completato!', size=22, color=COLORS['text'], anchor='middle', weight='bold')

    # Score card
    score = dwg.g(id='score_card')
    add_card(dwg, score, 100, 175, 175, 110)
    add_circle(dwg, score, 187, 220, 35, COLORS['primary'])
    add_text(dwg, score, 187, 230, '78', size=24, color='#FFFFFF', anchor='middle', weight='bold')
    add_text(dwg, score, 187, 270, 'punti', size=12, color=COLORS['text_light'], anchor='middle')
    main.add(score)

    # Stats card
    stats = dwg.g(id='stats_card')
    add_card(dwg, stats, 40, 305, 295, 130)
    add_text(dwg, stats, 187, 340, 'Statistiche', size=14, color=COLORS['text'], anchor='middle', weight='bold')

    stat_items = [('Risposte corrette', '12/15'), ('Percentuale', '80%'), ('Tempo totale', '8:32')]
    for i, (label, value) in enumerate(stat_items):
        add_text(dwg, stats, 60, 375 + i * 28, label, size=12, color=COLORS['text_light'])
        add_text(dwg, stats, 315, 375 + i * 28, value, size=12, color=COLORS['text'], anchor='end', weight='bold')
    main.add(stats)

    # AI Final feedback
    ai_feedback = dwg.g(id='ai_final')
    add_card(dwg, ai_feedback, 40, 455, 295, 120)
    add_text(dwg, ai_feedback, 187, 490, 'Feedback Finale', size=14, color=COLORS['text'], anchor='middle', weight='bold')
    add_text(dwg, ai_feedback, 187, 520, 'Ottimo lavoro! Hai dimostrato', size=11, color=COLORS['text_light'], anchor='middle')
    add_text(dwg, ai_feedback, 187, 545, 'una buona conoscenza della materia.', size=11, color=COLORS['text_light'], anchor='middle')
    main.add(ai_feedback)

    # Buttons
    add_button(dwg, main, 40, 610, 295, 55, 'VEDI CLASSIFICA', COLORS['success'])

    # Title
    add_text(dwg, main, 187, 780, 'WIREFRAME: MOBILE RESULTS', size=10, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_mobile_results.svg')


# ============================================
# WIREFRAME: MOBILE LEADERBOARD
# ============================================

def create_mobile_leaderboard():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_mobile_leaderboard.svg', size=(375, 812))
    main = dwg.g(id='mobile_leaderboard')

    add_phone_frame(dwg, main, 0, 0, 375, 812, 'Classifica')

    # Logo centered
    logo = dwg.g(id='logo')
    add_rounded_rect(dwg, logo, 147, 90, 80, 35, COLORS['frame'], rx=4, stroke=COLORS['border'])
    add_text(dwg, logo, 187, 113, 'LOGO', size=10, color=COLORS['text_light'], anchor='middle')
    main.add(logo)

    # Title
    add_text(dwg, main, 187, 155, 'Top 20', size=20, color=COLORS['text'], anchor='middle', weight='bold')

    # Your position highlight
    your_pos = dwg.g(id='your_position')
    add_rounded_rect(dwg, your_pos, 20, 175, 335, 55, '#E3F2FD', rx=8, stroke=COLORS['primary'], stroke_width=2)
    add_text(dwg, your_pos, 50, 210, '#7', size=16, color=COLORS['primary'], weight='bold')
    add_text(dwg, your_pos, 90, 210, 'Tu', size=14, color=COLORS['text'], weight='bold')
    add_text(dwg, your_pos, 330, 210, '78 pts', size=14, color=COLORS['primary'], anchor='end', weight='bold')
    main.add(your_pos)

    # Leaderboard
    leaders = [
        ('1', '1. Mario R.', '156'),
        ('2', '2. Anna B.', '142'),
        ('3', '3. Luigi V.', '138'),
        ('4', '4. Sara N.', '125'),
        ('5', '5. Paolo M.', '118'),
        ('6', '6. Elena G.', '98'),
    ]
    for i, (pos, name, pts) in enumerate(leaders):
        y = 245 + i * 58
        row = dwg.g(id=f'row_{i}')
        add_card(dwg, row, 20, y, 335, 50)
        medal_colors = [COLORS['warning'], '#C0C0C0', '#CD7F32']
        pos_color = medal_colors[i] if i < 3 else COLORS['text_light']
        add_text(dwg, row, 50, y + 32, pos, size=14, color=pos_color, weight='bold')
        add_text(dwg, row, 90, y + 32, name, size=14, color=COLORS['text'])
        add_text(dwg, row, 330, y + 32, f'{pts} pts', size=12, color=COLORS['text_light'], anchor='end')
        main.add(row)

    # Warning box - quiz non ripetibile
    add_rounded_rect(dwg, main, 40, 610, 295, 45, '#FFF3E0', rx=6, stroke=COLORS['warning'])
    add_text(dwg, main, 187, 630, 'Il quiz non può essere ripetuto.', size=10, color=COLORS['warning'], anchor='middle', weight='bold')
    add_text(dwg, main, 187, 645, 'Questa pagina resterà sempre accessibile.', size=9, color=COLORS['text_light'], anchor='middle')

    # Buttons
    add_button(dwg, main, 40, 670, 140, 45, 'CONDIVIDI', COLORS['secondary'])
    add_button(dwg, main, 195, 670, 140, 45, 'CHIUDI', COLORS['primary'])

    # Title
    add_text(dwg, main, 187, 790, 'WIREFRAME: MOBILE LEADERBOARD', size=10, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_mobile_leaderboard.svg')


# ============================================
# WIREFRAME: SCENARIO FORMATIVO - SCHEMA
# ============================================

def create_tree_schema():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_tree_schema.svg', size=(1200, 800))
    main = dwg.g(id='scenario_schema')

    # Background
    add_rounded_rect(dwg, main, 0, 0, 1200, 800, '#FAFAFA', rx=0)

    # Title
    add_text(dwg, main, 600, 35, 'Scenario Formativo - Schema Decisionale', size=24, color=COLORS['text'], anchor='middle', weight='bold')
    add_text(dwg, main, 600, 60, 'Ogni scelta determina l\'evoluzione del caso clinico', size=14, color=COLORS['text_light'], anchor='middle')

    # Legend
    legend = dwg.g(id='legend')
    add_rounded_rect(dwg, legend, 20, 85, 220, 140, '#FFFFFF', rx=8, stroke=COLORS['border'])
    add_text(dwg, legend, 130, 108, 'Legenda', size=12, color=COLORS['text'], anchor='middle', weight='bold')

    # Legend items
    add_circle(dwg, legend, 40, 132, 8, COLORS['success'])
    add_text(dwg, legend, 55, 137, 'Scelta ottimale', size=10, color=COLORS['text'])
    add_circle(dwg, legend, 40, 157, 8, COLORS['warning'])
    add_text(dwg, legend, 55, 162, 'Scelta accettabile', size=10, color=COLORS['text'])
    add_circle(dwg, legend, 40, 182, 8, COLORS['error'])
    add_text(dwg, legend, 55, 187, 'Scelta non ottimale', size=10, color=COLORS['text'])
    add_circle(dwg, legend, 40, 207, 8, '#9C27B0')
    add_text(dwg, legend, 55, 212, 'Esito finale', size=10, color=COLORS['text'])
    main.add(legend)

    # Clinical case box
    case_box = dwg.g(id='case')
    add_rounded_rect(dwg, case_box, 260, 85, 680, 55, '#E3F2FD', rx=8, stroke=COLORS['primary'])
    add_text(dwg, case_box, 600, 108, 'CASO: Paziente con ittero (cute gialla) e febbre a 40°C', size=13, color=COLORS['primary'], anchor='middle', weight='bold')
    add_text(dwg, case_box, 600, 128, 'Pronto Soccorso - Codice Giallo', size=11, color=COLORS['text_light'], anchor='middle')
    main.add(case_box)

    # Root node - Initial choice
    root = dwg.g(id='root')
    add_rounded_rect(dwg, root, 480, 160, 240, 55, COLORS['primary'], rx=8)
    add_text(dwg, root, 600, 182, 'SCELTA 1', size=12, color='#FFFFFF', anchor='middle', weight='bold')
    add_text(dwg, root, 600, 200, 'Quale primo intervento?', size=10, color='#FFFFFF', anchor='middle')
    main.add(root)

    # Level 2 - Three branches
    # Left branch (optimal)
    l2_left = dwg.g(id='l2_left')
    add_rounded_rect(dwg, l2_left, 120, 270, 180, 55, COLORS['success'], rx=8)
    add_text(dwg, l2_left, 210, 290, 'A) Ecografia addome', size=11, color='#FFFFFF', anchor='middle', weight='bold')
    add_text(dwg, l2_left, 210, 308, 'Scelta ottimale', size=9, color='#FFFFFF', anchor='middle')
    main.add(l2_left)

    # Middle branch (acceptable)
    l2_mid = dwg.g(id='l2_mid')
    add_rounded_rect(dwg, l2_mid, 510, 270, 180, 55, COLORS['warning'], rx=8)
    add_text(dwg, l2_mid, 600, 290, 'B) Antipiretico + Temp', size=11, color='#FFFFFF', anchor='middle', weight='bold')
    add_text(dwg, l2_mid, 600, 308, 'Scelta accettabile', size=9, color='#FFFFFF', anchor='middle')
    main.add(l2_mid)

    # Right branch (not optimal - worsening)
    l2_right = dwg.g(id='l2_right')
    add_rounded_rect(dwg, l2_right, 900, 270, 180, 55, COLORS['error'], rx=8)
    add_text(dwg, l2_right, 990, 290, 'C) Osservazione 24h', size=11, color='#FFFFFF', anchor='middle', weight='bold')
    add_text(dwg, l2_right, 990, 308, 'Paziente peggiora!', size=9, color='#FFFFFF', anchor='middle')
    main.add(l2_right)

    # Arrows from root
    main.add(dwg.line(start=(520, 215), end=(260, 270), stroke=COLORS['success'], stroke_width=2))
    main.add(dwg.line(start=(600, 215), end=(600, 270), stroke=COLORS['warning'], stroke_width=2))
    main.add(dwg.line(start=(680, 215), end=(940, 270), stroke=COLORS['error'], stroke_width=2))

    # Level 3 - Evolutions
    # From optimal choice
    l3_opt = dwg.g(id='l3_opt')
    add_rounded_rect(dwg, l3_opt, 70, 380, 160, 50, '#E8F5E9', rx=8, stroke=COLORS['success'])
    add_text(dwg, l3_opt, 150, 400, 'Calcoli biliari', size=10, color=COLORS['text'], anchor='middle', weight='bold')
    add_text(dwg, l3_opt, 150, 418, 'Diagnosi confermata', size=9, color=COLORS['success'], anchor='middle')
    main.add(l3_opt)

    l3_opt2 = dwg.g(id='l3_opt2')
    add_rounded_rect(dwg, l3_opt2, 250, 380, 160, 50, '#E8F5E9', rx=8, stroke=COLORS['success'])
    add_text(dwg, l3_opt2, 330, 400, 'SCELTA 2', size=10, color=COLORS['text'], anchor='middle', weight='bold')
    add_text(dwg, l3_opt2, 330, 418, 'Trattamento?', size=9, color=COLORS['text_light'], anchor='middle')
    main.add(l3_opt2)

    # From acceptable choice
    l3_acc = dwg.g(id='l3_acc')
    add_rounded_rect(dwg, l3_acc, 510, 380, 180, 50, '#FFF3E0', rx=8, stroke=COLORS['warning'])
    add_text(dwg, l3_acc, 600, 400, 'Febbre scende ma', size=10, color=COLORS['text'], anchor='middle', weight='bold')
    add_text(dwg, l3_acc, 600, 418, 'causa non identificata', size=9, color=COLORS['warning'], anchor='middle')
    main.add(l3_acc)

    # From wrong choice - WORSENING
    l3_worse = dwg.g(id='l3_worse')
    add_rounded_rect(dwg, l3_worse, 850, 380, 180, 65, '#FFEBEE', rx=8, stroke=COLORS['error'])
    add_text(dwg, l3_worse, 940, 398, 'PEGGIORAMENTO', size=10, color=COLORS['error'], anchor='middle', weight='bold')
    add_text(dwg, l3_worse, 940, 416, 'Vomito, febbre 41°C', size=9, color=COLORS['text'], anchor='middle')
    add_text(dwg, l3_worse, 940, 432, 'Nuova scelta urgente!', size=9, color=COLORS['error'], anchor='middle')
    main.add(l3_worse)

    # Arrows level 2->3
    main.add(dwg.line(start=(180, 325), end=(150, 380), stroke=COLORS['success'], stroke_width=2))
    main.add(dwg.line(start=(240, 325), end=(310, 380), stroke=COLORS['success'], stroke_width=2))
    main.add(dwg.line(start=(600, 325), end=(600, 380), stroke=COLORS['warning'], stroke_width=2))
    main.add(dwg.line(start=(990, 325), end=(940, 380), stroke=COLORS['error'], stroke_width=2))

    # Final outcomes
    # Best outcome - Recovery
    end_best = dwg.g(id='end_best')
    add_rounded_rect(dwg, end_best, 140, 490, 140, 50, COLORS['success'], rx=25)
    add_text(dwg, end_best, 210, 512, 'GUARIGIONE', size=11, color='#FFFFFF', anchor='middle', weight='bold')
    add_text(dwg, end_best, 210, 528, '100 punti', size=9, color='#FFFFFF', anchor='middle')
    main.add(end_best)

    # Good outcome
    end_good = dwg.g(id='end_good')
    add_rounded_rect(dwg, end_good, 320, 490, 140, 50, COLORS['warning'], rx=25)
    add_text(dwg, end_good, 390, 512, 'DIMISSIONE', size=11, color='#FFFFFF', anchor='middle', weight='bold')
    add_text(dwg, end_good, 390, 528, '70 punti', size=9, color='#FFFFFF', anchor='middle')
    main.add(end_good)

    # Delayed outcome
    end_delayed = dwg.g(id='end_delayed')
    add_rounded_rect(dwg, end_delayed, 530, 490, 140, 50, COLORS['warning'], rx=25)
    add_text(dwg, end_delayed, 600, 512, 'RICOVERO', size=11, color='#FFFFFF', anchor='middle', weight='bold')
    add_text(dwg, end_delayed, 600, 528, '50 punti', size=9, color='#FFFFFF', anchor='middle')
    main.add(end_delayed)

    # Recovery after error
    end_recover = dwg.g(id='end_recover')
    add_rounded_rect(dwg, end_recover, 800, 490, 140, 50, '#9C27B0', rx=25)
    add_text(dwg, end_recover, 870, 512, 'RECUPERO', size=11, color='#FFFFFF', anchor='middle', weight='bold')
    add_text(dwg, end_recover, 870, 528, '30 punti', size=9, color='#FFFFFF', anchor='middle')
    main.add(end_recover)

    # Worst outcome
    end_worst = dwg.g(id='end_worst')
    add_rounded_rect(dwg, end_worst, 980, 490, 140, 50, COLORS['error'], rx=25)
    add_text(dwg, end_worst, 1050, 512, 'CRITICO', size=11, color='#FFFFFF', anchor='middle', weight='bold')
    add_text(dwg, end_worst, 1050, 528, '10 punti', size=9, color='#FFFFFF', anchor='middle')
    main.add(end_worst)

    # Arrows to outcomes
    main.add(dwg.line(start=(150, 430), end=(190, 490), stroke=COLORS['success'], stroke_width=2))
    main.add(dwg.line(start=(330, 430), end=(370, 490), stroke=COLORS['success'], stroke_width=2))
    main.add(dwg.line(start=(600, 430), end=(600, 490), stroke=COLORS['warning'], stroke_width=2))
    main.add(dwg.line(start=(900, 445), end=(870, 490), stroke='#9C27B0', stroke_width=2))
    main.add(dwg.line(start=(980, 445), end=(1030, 490), stroke=COLORS['error'], stroke_width=2))

    # Rules box
    rules = dwg.g(id='rules')
    add_rounded_rect(dwg, rules, 20, 560, 1160, 220, '#FFFFFF', rx=8, stroke=COLORS['border'])
    add_text(dwg, rules, 600, 590, 'Regole dello Scenario Formativo', size=16, color=COLORS['text'], anchor='middle', weight='bold')

    rule_lines = [
        '1. Le scelte NON sono "giuste o sbagliate" ma "più appropriate o meno appropriate"',
        '2. Scelta ottimale: percorso diretto verso la guarigione (massimo punteggio)',
        '3. Scelta accettabile: funziona ma non è la prassi ideale (punteggio medio)',
        '4. Scelta non ottimale: porta al peggioramento del paziente (richiede recupero)',
        '5. Il punteggio finale dipende dal percorso complessivo effettuato',
        '6. Anche dopo errori si può "recuperare" ma con punteggio ridotto',
        '7. Esiti possibili: Guarigione (100pt), Dimissione (70pt), Ricovero (50pt), Recupero (30pt), Critico (10pt)'
    ]
    for i, line in enumerate(rule_lines):
        add_text(dwg, rules, 50, 625 + i * 22, line, size=11, color=COLORS['text_light'])
    main.add(rules)

    # Title
    add_text(dwg, main, 600, 795, 'WIREFRAME: SCENARIO FORMATIVO SCHEMA', size=10, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_tree_schema.svg')


# ============================================
# WIREFRAME: SCENARIO BUILDER - CREATOR
# ============================================

def create_tree_builder():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_tree_builder.svg', size=(1440, 900))
    main = dwg.g(id='scenario_builder')

    # Sidebar
    add_rounded_rect(dwg, main, 0, 0, 280, 900, '#F5F5F5', rx=0)
    add_text(dwg, main, 140, 40, 'Clinical Quiz', size=18, color=COLORS['primary'], anchor='middle', weight='bold')
    add_text(dwg, main, 140, 60, 'Scenario Builder', size=12, color=COLORS['text_light'], anchor='middle')

    # Sidebar menu
    menu_items = ['Dashboard', 'I Miei Scenari']
    for i, item in enumerate(menu_items):
        y = 120 + i * 50
        if i == 1:
            add_rounded_rect(dwg, main, 15, y - 15, 250, 45, COLORS['primary'], rx=8)
            add_text(dwg, main, 140, y + 10, item, size=14, color='#FFFFFF', anchor='middle', weight='bold')
        else:
            add_text(dwg, main, 140, y + 10, item, size=14, color=COLORS['text'], anchor='middle')

    # Scenario list
    add_text(dwg, main, 20, 230, 'Scenari Formativi', size=12, color=COLORS['text_light'])
    scenarios = ['Ittero + Febbre', 'Triage Emergenza', 'Dolore Toracico']
    for i, scenario in enumerate(scenarios):
        y = 260 + i * 45
        bg_color = '#E3F2FD' if i == 0 else '#FFFFFF'
        add_rounded_rect(dwg, main, 15, y, 250, 40, bg_color, rx=6, stroke=COLORS['border'])
        add_text(dwg, main, 30, y + 25, scenario, size=12, color=COLORS['text'])

    # Main content
    add_rounded_rect(dwg, main, 280, 0, 1160, 900, '#FFFFFF', rx=0)

    # Header
    add_text(dwg, main, 310, 45, 'Scenario: Ittero + Febbre', size=20, color=COLORS['text'], weight='bold')
    add_text(dwg, main, 310, 70, 'Costruisci il percorso decisionale con scelte cliniche', size=12, color=COLORS['text_light'])

    # Toolbar
    toolbar = dwg.g(id='toolbar')
    add_rounded_rect(dwg, toolbar, 310, 90, 1100, 50, COLORS['frame'], rx=8)

    tools = [('+ Scelta', COLORS['primary']), ('+ Evoluzione', COLORS['warning']), ('+ Esito', '#9C27B0'), ('Collega', COLORS['text_light']), ('Elimina', COLORS['error'])]
    for i, (tool, color) in enumerate(tools):
        x = 330 + i * 150
        add_rounded_rect(dwg, toolbar, x, 100, 130, 30, color, rx=4)
        add_text(dwg, toolbar, x + 65, 120, tool, size=11, color='#FFFFFF', anchor='middle')

    add_button(dwg, toolbar, 1120, 98, 120, 35, 'SALVA', COLORS['success'])
    add_button(dwg, toolbar, 1260, 98, 120, 35, 'ANTEPRIMA', COLORS['warning'])
    main.add(toolbar)

    # Canvas area
    canvas = dwg.g(id='canvas')
    add_rounded_rect(dwg, canvas, 310, 160, 780, 580, '#FAFAFA', rx=8, stroke=COLORS['border'])

    # Grid pattern hint
    for i in range(15):
        for j in range(11):
            add_circle(dwg, canvas, 340 + i * 52, 190 + j * 52, 2, '#E0E0E0')

    # Sample scenario nodes on canvas
    # Case presentation
    case_node = dwg.g(id='canvas_case')
    add_rounded_rect(dwg, case_node, 550, 175, 280, 55, '#E3F2FD', rx=8, stroke=COLORS['primary'])
    add_text(dwg, case_node, 690, 198, 'CASO CLINICO', size=11, color=COLORS['primary'], anchor='middle', weight='bold')
    add_text(dwg, case_node, 690, 218, 'Paziente ittero + febbre 40°C', size=10, color=COLORS['text'], anchor='middle')
    main.add(case_node)

    # Root choice
    root = dwg.g(id='canvas_root')
    add_rounded_rect(dwg, root, 580, 260, 220, 50, COLORS['primary'], rx=8)
    add_text(dwg, root, 690, 282, 'SCELTA 1', size=11, color='#FFFFFF', anchor='middle', weight='bold')
    add_text(dwg, root, 690, 298, 'Primo intervento?', size=9, color='#FFFFFF', anchor='middle')
    main.add(root)

    # Arrow from case to choice
    main.add(dwg.line(start=(690, 230), end=(690, 260), stroke=COLORS['primary'], stroke_width=2))

    # Level 2 - Three choices
    l2a = dwg.g(id='canvas_l2a')
    add_rounded_rect(dwg, l2a, 350, 360, 150, 50, COLORS['success'], rx=8)
    add_text(dwg, l2a, 425, 380, 'A) Ecografia', size=10, color='#FFFFFF', anchor='middle', weight='bold')
    add_text(dwg, l2a, 425, 398, 'Ottimale', size=8, color='#FFFFFF', anchor='middle')
    main.add(l2a)

    l2b = dwg.g(id='canvas_l2b')
    add_rounded_rect(dwg, l2b, 615, 360, 150, 50, COLORS['warning'], rx=8)
    add_text(dwg, l2b, 690, 380, 'B) Antipiretico', size=10, color='#FFFFFF', anchor='middle', weight='bold')
    add_text(dwg, l2b, 690, 398, 'Accettabile', size=8, color='#FFFFFF', anchor='middle')
    main.add(l2b)

    l2c = dwg.g(id='canvas_l2c')
    add_rounded_rect(dwg, l2c, 880, 360, 150, 50, COLORS['error'], rx=8)
    add_text(dwg, l2c, 955, 380, 'C) Osservazione', size=10, color='#FFFFFF', anchor='middle', weight='bold')
    add_text(dwg, l2c, 955, 398, 'Peggiora!', size=8, color='#FFFFFF', anchor='middle')
    main.add(l2c)

    # Arrows
    main.add(dwg.line(start=(620, 310), end=(425, 360), stroke=COLORS['success'], stroke_width=2))
    main.add(dwg.line(start=(690, 310), end=(690, 360), stroke=COLORS['warning'], stroke_width=2))
    main.add(dwg.line(start=(760, 310), end=(955, 360), stroke=COLORS['error'], stroke_width=2))

    # Evolution nodes
    evol1 = dwg.g(id='canvas_evol1')
    add_rounded_rect(dwg, evol1, 350, 460, 150, 45, '#E8F5E9', rx=8, stroke=COLORS['success'])
    add_text(dwg, evol1, 425, 480, 'Diagnosi', size=9, color=COLORS['text'], anchor='middle', weight='bold')
    add_text(dwg, evol1, 425, 495, 'confermata', size=8, color=COLORS['success'], anchor='middle')
    main.add(evol1)

    evol2 = dwg.g(id='canvas_evol2')
    add_rounded_rect(dwg, evol2, 850, 460, 180, 55, '#FFEBEE', rx=8, stroke=COLORS['error'])
    add_text(dwg, evol2, 940, 482, 'PEGGIORAMENTO', size=9, color=COLORS['error'], anchor='middle', weight='bold')
    add_text(dwg, evol2, 940, 500, 'Vomito, febbre 41°C', size=8, color=COLORS['text'], anchor='middle')
    main.add(evol2)

    main.add(dwg.line(start=(425, 410), end=(425, 460), stroke=COLORS['success'], stroke_width=2))
    main.add(dwg.line(start=(955, 410), end=(940, 460), stroke=COLORS['error'], stroke_width=2))

    # End nodes
    end_good = dwg.g(id='canvas_end_good')
    add_rounded_rect(dwg, end_good, 350, 550, 150, 45, COLORS['success'], rx=20)
    add_text(dwg, end_good, 425, 578, 'GUARIGIONE', size=10, color='#FFFFFF', anchor='middle', weight='bold')
    main.add(end_good)

    end_bad = dwg.g(id='canvas_end_bad')
    add_rounded_rect(dwg, end_bad, 880, 560, 120, 40, COLORS['error'], rx=20)
    add_text(dwg, end_bad, 940, 585, 'CRITICO', size=10, color='#FFFFFF', anchor='middle', weight='bold')
    main.add(end_bad)

    main.add(dwg.line(start=(425, 505), end=(425, 550), stroke=COLORS['success'], stroke_width=2))
    main.add(dwg.line(start=(970, 515), end=(940, 560), stroke=COLORS['error'], stroke_width=2))

    main.add(canvas)

    # Properties panel
    props = dwg.g(id='properties')
    add_rounded_rect(dwg, props, 1110, 160, 280, 580, '#FFFFFF', rx=8, stroke=COLORS['border'])
    add_text(dwg, props, 1250, 195, 'Proprietà Scelta', size=14, color=COLORS['text'], anchor='middle', weight='bold')

    # Selected node info
    add_text(dwg, props, 1130, 230, 'Nodo selezionato:', size=11, color=COLORS['text_light'])
    add_rounded_rect(dwg, props, 1130, 245, 240, 35, COLORS['primary'], rx=4)
    add_text(dwg, props, 1250, 268, 'SCELTA 1 - Primo intervento', size=9, color='#FFFFFF', anchor='middle')

    # Form fields
    add_text(dwg, props, 1130, 310, 'Situazione clinica:', size=11, color=COLORS['text_light'])
    add_input(dwg, props, 1130, 325, 240, 40, 'Quale primo intervento eseguire?')

    add_text(dwg, props, 1130, 390, 'Tipo nodo:', size=11, color=COLORS['text_light'])
    add_rounded_rect(dwg, props, 1130, 405, 240, 35, '#FFFFFF', rx=4, stroke=COLORS['border'])
    add_text(dwg, props, 1140, 428, 'Scelta clinica', size=11, color=COLORS['text'])

    add_text(dwg, props, 1130, 465, 'Opzioni (2-3):', size=11, color=COLORS['text_light'])

    # Response options with quality indicators
    resp1 = dwg.g(id='resp1')
    add_rounded_rect(dwg, resp1, 1130, 485, 240, 50, '#E8F5E9', rx=4, stroke=COLORS['success'])
    add_text(dwg, resp1, 1145, 503, 'A) Ecografia addome', size=10, color=COLORS['text'], weight='bold')
    add_text(dwg, resp1, 1145, 520, 'Ottimale → Diagnosi', size=9, color=COLORS['success'])
    main.add(resp1)

    resp2 = dwg.g(id='resp2')
    add_rounded_rect(dwg, resp2, 1130, 545, 240, 50, '#FFF3E0', rx=4, stroke=COLORS['warning'])
    add_text(dwg, resp2, 1145, 563, 'B) Antipiretico + Temp', size=10, color=COLORS['text'], weight='bold')
    add_text(dwg, resp2, 1145, 580, 'Accettabile → Ricovero', size=9, color=COLORS['warning'])
    main.add(resp2)

    resp3 = dwg.g(id='resp3')
    add_rounded_rect(dwg, resp3, 1130, 605, 240, 50, '#FFEBEE', rx=4, stroke=COLORS['error'])
    add_text(dwg, resp3, 1145, 623, 'C) Osservazione 24h', size=10, color=COLORS['text'], weight='bold')
    add_text(dwg, resp3, 1145, 640, 'Non ottimale → Peggiora', size=9, color=COLORS['error'])
    main.add(resp3)

    add_button(dwg, props, 1130, 680, 240, 35, 'APPLICA MODIFICHE', COLORS['primary'])
    main.add(props)

    # Stats bar
    stats = dwg.g(id='stats')
    add_rounded_rect(dwg, stats, 310, 760, 1080, 60, COLORS['frame'], rx=8)

    stat_items = [('Scelte totali', '8'), ('Evoluzioni', '5'), ('Esiti finali', '4'), ('Percorsi', '6'), ('Max profondità', '4')]
    for i, (label, value) in enumerate(stat_items):
        x = 380 + i * 200
        add_text(dwg, stats, x, 785, label, size=10, color=COLORS['text_light'], anchor='middle')
        add_text(dwg, stats, x, 808, value, size=18, color=COLORS['primary'], anchor='middle', weight='bold')
    main.add(stats)

    # Title
    add_text(dwg, main, 860, 880, 'WIREFRAME: SCENARIO BUILDER - CREATOR', size=10, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_tree_builder.svg')


# ============================================
# WIREFRAME: SCENARIO MOBILE - SCELTA
# ============================================

def create_tree_mobile_question():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_tree_mobile_question.svg', size=(375, 812))
    main = dwg.g(id='scenario_mobile_choice')

    add_phone_frame(dwg, main, 0, 0, 375, 812, 'Scenario Clinico')

    # Logo
    logo = dwg.g(id='logo')
    add_rounded_rect(dwg, logo, 20, 90, 80, 35, COLORS['frame'], rx=4, stroke=COLORS['border'])
    add_text(dwg, logo, 60, 113, 'LOGO', size=10, color=COLORS['text_light'], anchor='middle')
    main.add(logo)

    # Scenario indicator
    scenario_ind = dwg.g(id='scenario_indicator')
    add_rounded_rect(dwg, scenario_ind, 110, 90, 155, 35, '#E3F2FD', rx=17)
    add_text(dwg, scenario_ind, 187, 108, 'Scelta 1 di 4', size=10, color=COLORS['primary'], anchor='middle', weight='bold')
    add_text(dwg, scenario_ind, 187, 120, 'Caso: Ittero + Febbre', size=8, color=COLORS['primary'], anchor='middle')
    main.add(scenario_ind)

    # Points
    add_text(dwg, main, 320, 115, '0 pts', size=14, color=COLORS['text'], anchor='middle', weight='bold')

    # Clinical case card
    case_card = dwg.g(id='case_card')
    add_rounded_rect(dwg, case_card, 20, 140, 335, 70, '#E3F2FD', rx=8, stroke=COLORS['primary'])
    add_text(dwg, case_card, 187, 165, 'SITUAZIONE CLINICA', size=10, color=COLORS['primary'], anchor='middle', weight='bold')
    add_text(dwg, case_card, 187, 185, 'Paziente con ittero e febbre a 40°C', size=12, color=COLORS['text'], anchor='middle')
    add_text(dwg, case_card, 187, 200, 'arriva in Pronto Soccorso', size=11, color=COLORS['text_light'], anchor='middle')
    main.add(case_card)

    # Question card
    question = dwg.g(id='question')
    add_card(dwg, question, 20, 225, 335, 80)
    add_text(dwg, question, 187, 255, 'Quale primo intervento', size=14, color=COLORS['text'], anchor='middle', weight='bold')
    add_text(dwg, question, 187, 280, 'decidi di eseguire?', size=14, color=COLORS['text'], anchor='middle', weight='bold')
    main.add(question)

    # Answer options - with quality indicators
    options = [
        ('A) Ecografia addominale', 'Scelta ottimale', COLORS['success']),
        ('B) Antipiretico + Temperatura', 'Scelta accettabile', COLORS['warning']),
        ('C) Osservazione 24 ore', 'Attenzione!', COLORS['error'])
    ]
    for i, (opt, quality, color) in enumerate(options):
        opt_y = 325 + i * 95
        opt_group = dwg.g(id=f'option_{i}')
        add_card(dwg, opt_group, 20, opt_y, 335, 80)
        add_circle(dwg, opt_group, 55, opt_y + 40, 14, '#FFFFFF')
        main.add(dwg.circle(center=(55, opt_y + 40), r=14, fill='none', stroke=COLORS['primary'], stroke_width=2))
        add_text(dwg, opt_group, 80, opt_y + 35, opt, size=12, color=COLORS['text'], weight='bold')
        # Quality indicator
        add_rounded_rect(dwg, opt_group, 80, opt_y + 50, 120, 20, color, rx=10)
        add_text(dwg, opt_group, 140, opt_y + 64, quality, size=9, color='#FFFFFF', anchor='middle')
        main.add(opt_group)

    # Info
    add_text(dwg, main, 187, 625, 'Non esistono risposte "sbagliate"', size=10, color=COLORS['text_light'], anchor='middle')
    add_text(dwg, main, 187, 642, 'ma alcune scelte sono più appropriate di altre', size=9, color=COLORS['text_light'], anchor='middle')

    # Warning about consequences
    warn = dwg.g(id='warning')
    add_rounded_rect(dwg, warn, 40, 660, 295, 40, '#FFF3E0', rx=6, stroke=COLORS['warning'])
    add_text(dwg, warn, 187, 685, 'Ogni scelta influenza lo stato del paziente', size=10, color=COLORS['warning'], anchor='middle', weight='bold')
    main.add(warn)

    # Confirm button
    add_button(dwg, main, 40, 715, 295, 50, 'CONFERMA SCELTA', COLORS['primary'])

    # Title
    add_text(dwg, main, 187, 795, 'WIREFRAME: SCENARIO MOBILE SCELTA', size=10, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_tree_mobile_question.svg')


# ============================================
# WIREFRAME: SCENARIO MOBILE - ESITO
# ============================================

def create_tree_mobile_results():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_tree_mobile_results.svg', size=(375, 812))
    main = dwg.g(id='scenario_mobile_results')

    add_phone_frame(dwg, main, 0, 0, 375, 812, 'Esito Scenario')

    # Logo
    logo = dwg.g(id='logo')
    add_rounded_rect(dwg, logo, 147, 90, 80, 35, COLORS['frame'], rx=4, stroke=COLORS['border'])
    add_text(dwg, logo, 187, 113, 'LOGO', size=10, color=COLORS['text_light'], anchor='middle')
    main.add(logo)

    # Title
    add_text(dwg, main, 187, 155, 'Scenario Completato!', size=20, color=COLORS['text'], anchor='middle', weight='bold')

    # Patient outcome card
    outcome = dwg.g(id='outcome')
    add_rounded_rect(dwg, outcome, 20, 175, 335, 100, '#E8F5E9', rx=12, stroke=COLORS['success'])
    add_text(dwg, outcome, 187, 205, 'ESITO PAZIENTE', size=11, color=COLORS['success'], anchor='middle', weight='bold')
    add_text(dwg, outcome, 187, 235, 'GUARIGIONE', size=24, color=COLORS['success'], anchor='middle', weight='bold')
    add_text(dwg, outcome, 187, 260, 'Dimesso dopo 3 giorni', size=11, color=COLORS['text_light'], anchor='middle')
    main.add(outcome)

    # Path visualization
    path_viz = dwg.g(id='path_viz')
    add_card(dwg, path_viz, 20, 290, 335, 100)
    add_text(dwg, path_viz, 187, 315, 'Le tue scelte', size=12, color=COLORS['text_light'], anchor='middle')

    # Visual path - clinical choices
    nodes = [
        (60, 'S1', COLORS['success']),
        (120, 'S2', COLORS['success']),
        (180, 'S3', COLORS['warning']),
        (240, 'S4', COLORS['success']),
        (300, 'OK', COLORS['success'])
    ]
    for i, (x, label, color) in enumerate(nodes):
        add_circle(dwg, path_viz, x, 355, 18, color)
        add_text(dwg, path_viz, x, 360, label, size=8, color='#FFFFFF', anchor='middle', weight='bold')
        if i < len(nodes) - 1:
            main.add(dwg.line(start=(x + 18, 355), end=(nodes[i+1][0] - 18, 355), stroke=color, stroke_width=2))

    add_text(dwg, path_viz, 187, 382, '4 scelte • 3 ottimali • 1 accettabile', size=9, color=COLORS['text_light'], anchor='middle')
    main.add(path_viz)

    # Score breakdown
    score = dwg.g(id='score')
    add_card(dwg, score, 20, 405, 335, 150)
    add_text(dwg, score, 187, 432, 'Dettaglio Punteggio', size=14, color=COLORS['text'], anchor='middle', weight='bold')

    score_items = [
        ('Scelte ottimali (3)', '+60'),
        ('Scelte accettabili (1)', '+15'),
        ('Esito paziente: Guarigione', '+25'),
        ('TOTALE', '100 pts')
    ]
    for i, (label, pts) in enumerate(score_items):
        y = 462 + i * 25
        weight = 'bold' if i == 3 else 'normal'
        color = COLORS['success'] if i == 3 else COLORS['text_light']
        add_text(dwg, score, 40, y, label, size=11, color=COLORS['text_light'] if i < 3 else COLORS['text'], weight=weight)
        add_text(dwg, score, 335, y, pts, size=11, color=color, anchor='end', weight=weight)
    main.add(score)

    # AI Feedback
    feedback = dwg.g(id='feedback')
    add_card(dwg, feedback, 20, 570, 335, 100)
    add_text(dwg, feedback, 187, 598, 'Feedback Clinico', size=12, color=COLORS['text'], anchor='middle', weight='bold')
    add_text(dwg, feedback, 187, 623, 'Ottima gestione del caso! L\'ecografia', size=10, color=COLORS['text_light'], anchor='middle')
    add_text(dwg, feedback, 187, 640, 'immediata ha permesso diagnosi rapida', size=10, color=COLORS['text_light'], anchor='middle')
    add_text(dwg, feedback, 187, 657, 'e trattamento tempestivo del paziente.', size=10, color=COLORS['text_light'], anchor='middle')
    main.add(feedback)

    # Button
    add_button(dwg, main, 40, 690, 295, 50, 'VEDI CLASSIFICA', COLORS['primary'])

    # Title
    add_text(dwg, main, 187, 795, 'WIREFRAME: SCENARIO MOBILE ESITO', size=10, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_tree_mobile_results.svg')


# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    print('\n📐 Generazione Wireframe SVG per Figma\n')
    print('=' * 50)

    create_output_dir()

    print('\n🔷 ADMIN WIREFRAMES')
    create_login()
    create_admin_dashboard()
    create_admin_users()
    create_admin_create_user()
    create_admin_report()

    print('\n🔶 CREATOR WIREFRAMES')
    create_creator_dashboard()
    create_wizard_step1()
    create_wizard_step2()
    create_wizard_step3()
    create_wizard_step4()
    create_wizard_step5()
    create_qr_code()
    create_event_detail()

    print('\n📱 MOBILE WIREFRAMES')
    create_mobile_landing()
    create_mobile_start()
    create_mobile_question()
    create_mobile_correct()
    create_mobile_wrong()
    create_mobile_results()
    create_mobile_leaderboard()

    print('\n🌳 TREE QUIZ WIREFRAMES')
    create_tree_schema()
    create_tree_builder()
    create_tree_mobile_question()
    create_tree_mobile_results()

    print('\n' + '=' * 50)
    print(f'✅ Wireframe generati in: {OUTPUT_DIR}')
    print('=' * 50 + '\n')
