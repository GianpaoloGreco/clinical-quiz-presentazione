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
# WIREFRAME: TREE QUIZ - SCHEMA ALBERO
# ============================================

def create_tree_schema():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_tree_schema.svg', size=(1200, 800))
    main = dwg.g(id='tree_schema')

    # Background
    add_rounded_rect(dwg, main, 0, 0, 1200, 800, '#FAFAFA', rx=0)

    # Title
    add_text(dwg, main, 600, 40, 'Quiz ad Albero Decisionale - Schema', size=24, color=COLORS['text'], anchor='middle', weight='bold')
    add_text(dwg, main, 600, 65, 'Ogni risposta determina il percorso successivo', size=14, color=COLORS['text_light'], anchor='middle')

    # Legend
    legend = dwg.g(id='legend')
    add_rounded_rect(dwg, legend, 20, 90, 200, 120, '#FFFFFF', rx=8, stroke=COLORS['border'])
    add_text(dwg, legend, 120, 115, 'Legenda', size=12, color=COLORS['text'], anchor='middle', weight='bold')

    # Legend items
    add_circle(dwg, legend, 45, 140, 8, COLORS['success'])
    add_text(dwg, legend, 60, 145, 'Risposta corretta', size=10, color=COLORS['text'])
    add_circle(dwg, legend, 45, 165, 8, COLORS['error'])
    add_text(dwg, legend, 60, 170, 'Risposta errata', size=10, color=COLORS['text'])
    add_circle(dwg, legend, 45, 190, 8, COLORS['primary'])
    add_text(dwg, legend, 60, 195, 'Nodo convergenza', size=10, color=COLORS['text'])
    main.add(legend)

    # Root node (D1)
    root = dwg.g(id='root')
    add_rounded_rect(dwg, root, 525, 100, 150, 60, COLORS['primary'], rx=8)
    add_text(dwg, root, 600, 125, 'D1', size=16, color='#FFFFFF', anchor='middle', weight='bold')
    add_text(dwg, root, 600, 145, 'Domanda Iniziale', size=10, color='#FFFFFF', anchor='middle')
    main.add(root)

    # Level 2 - Two branches
    # Left branch (correct)
    l2_left = dwg.g(id='l2_left')
    add_rounded_rect(dwg, l2_left, 300, 220, 130, 50, COLORS['success'], rx=8)
    add_text(dwg, l2_left, 365, 240, 'D2a', size=14, color='#FFFFFF', anchor='middle', weight='bold')
    add_text(dwg, l2_left, 365, 258, 'Approfondimento', size=9, color='#FFFFFF', anchor='middle')
    main.add(l2_left)

    # Right branch (wrong)
    l2_right = dwg.g(id='l2_right')
    add_rounded_rect(dwg, l2_right, 770, 220, 130, 50, COLORS['error'], rx=8)
    add_text(dwg, l2_right, 835, 240, 'D2b', size=14, color='#FFFFFF', anchor='middle', weight='bold')
    add_text(dwg, l2_right, 835, 258, 'Recupero', size=9, color='#FFFFFF', anchor='middle')
    main.add(l2_right)

    # Arrows from root
    main.add(dwg.line(start=(560, 160), end=(365, 220), stroke=COLORS['success'], stroke_width=2))
    main.add(dwg.line(start=(640, 160), end=(835, 220), stroke=COLORS['error'], stroke_width=2))
    add_text(dwg, main, 440, 185, 'Corretta', size=9, color=COLORS['success'])
    add_text(dwg, main, 740, 185, 'Errata', size=9, color=COLORS['error'])

    # Level 3
    # From D2a - two more branches
    l3_1 = dwg.g(id='l3_1')
    add_rounded_rect(dwg, l3_1, 150, 330, 120, 45, COLORS['success'], rx=8)
    add_text(dwg, l3_1, 210, 350, 'D3a', size=12, color='#FFFFFF', anchor='middle', weight='bold')
    add_text(dwg, l3_1, 210, 365, 'Esperto', size=8, color='#FFFFFF', anchor='middle')
    main.add(l3_1)

    l3_2 = dwg.g(id='l3_2')
    add_rounded_rect(dwg, l3_2, 350, 330, 120, 45, COLORS['warning'], rx=8)
    add_text(dwg, l3_2, 410, 350, 'D3b', size=12, color='#FFFFFF', anchor='middle', weight='bold')
    add_text(dwg, l3_2, 410, 365, 'Intermedio', size=8, color='#FFFFFF', anchor='middle')
    main.add(l3_2)

    # From D2b - two branches
    l3_3 = dwg.g(id='l3_3')
    add_rounded_rect(dwg, l3_3, 700, 330, 120, 45, COLORS['warning'], rx=8)
    add_text(dwg, l3_3, 760, 350, 'D3c', size=12, color='#FFFFFF', anchor='middle', weight='bold')
    add_text(dwg, l3_3, 760, 365, 'Rinforzo', size=8, color='#FFFFFF', anchor='middle')
    main.add(l3_3)

    l3_4 = dwg.g(id='l3_4')
    add_rounded_rect(dwg, l3_4, 900, 330, 120, 45, COLORS['error'], rx=8)
    add_text(dwg, l3_4, 960, 350, 'D3d', size=12, color='#FFFFFF', anchor='middle', weight='bold')
    add_text(dwg, l3_4, 960, 365, 'Base', size=8, color='#FFFFFF', anchor='middle')
    main.add(l3_4)

    # Arrows level 2->3
    main.add(dwg.line(start=(320, 270), end=(210, 330), stroke=COLORS['success'], stroke_width=2))
    main.add(dwg.line(start=(400, 270), end=(410, 330), stroke=COLORS['warning'], stroke_width=2))
    main.add(dwg.line(start=(800, 270), end=(760, 330), stroke=COLORS['warning'], stroke_width=2))
    main.add(dwg.line(start=(870, 270), end=(960, 330), stroke=COLORS['error'], stroke_width=2))

    # Level 4 - Convergence nodes
    conv1 = dwg.g(id='conv1')
    add_rounded_rect(dwg, conv1, 230, 440, 140, 50, COLORS['primary'], rx=25)
    add_text(dwg, conv1, 300, 460, 'CONV-A', size=12, color='#FFFFFF', anchor='middle', weight='bold')
    add_text(dwg, conv1, 300, 478, 'Convergenza', size=8, color='#FFFFFF', anchor='middle')
    main.add(conv1)

    conv2 = dwg.g(id='conv2')
    add_rounded_rect(dwg, conv2, 780, 440, 140, 50, COLORS['primary'], rx=25)
    add_text(dwg, conv2, 850, 460, 'CONV-B', size=12, color='#FFFFFF', anchor='middle', weight='bold')
    add_text(dwg, conv2, 850, 478, 'Convergenza', size=8, color='#FFFFFF', anchor='middle')
    main.add(conv2)

    # Arrows to convergence
    main.add(dwg.line(start=(210, 375), end=(270, 440), stroke=COLORS['text_light'], stroke_width=1.5))
    main.add(dwg.line(start=(410, 375), end=(330, 440), stroke=COLORS['text_light'], stroke_width=1.5))
    main.add(dwg.line(start=(760, 375), end=(820, 440), stroke=COLORS['text_light'], stroke_width=1.5))
    main.add(dwg.line(start=(960, 375), end=(880, 440), stroke=COLORS['text_light'], stroke_width=1.5))

    # Final nodes
    end1 = dwg.g(id='end1')
    add_rounded_rect(dwg, end1, 200, 550, 100, 40, '#9C27B0', rx=20)
    add_text(dwg, end1, 250, 575, 'FINE A', size=11, color='#FFFFFF', anchor='middle', weight='bold')
    main.add(end1)

    end2 = dwg.g(id='end2')
    add_rounded_rect(dwg, end2, 350, 550, 100, 40, '#9C27B0', rx=20)
    add_text(dwg, end2, 400, 575, 'FINE B', size=11, color='#FFFFFF', anchor='middle', weight='bold')
    main.add(end2)

    end3 = dwg.g(id='end3')
    add_rounded_rect(dwg, end3, 750, 550, 100, 40, '#9C27B0', rx=20)
    add_text(dwg, end3, 800, 575, 'FINE C', size=11, color='#FFFFFF', anchor='middle', weight='bold')
    main.add(end3)

    end4 = dwg.g(id='end4')
    add_rounded_rect(dwg, end4, 900, 550, 100, 40, '#9C27B0', rx=20)
    add_text(dwg, end4, 950, 575, 'FINE D', size=11, color='#FFFFFF', anchor='middle', weight='bold')
    main.add(end4)

    # Arrows to end
    main.add(dwg.line(start=(270, 490), end=(250, 550), stroke='#9C27B0', stroke_width=2))
    main.add(dwg.line(start=(330, 490), end=(400, 550), stroke='#9C27B0', stroke_width=2))
    main.add(dwg.line(start=(820, 490), end=(800, 550), stroke='#9C27B0', stroke_width=2))
    main.add(dwg.line(start=(880, 490), end=(950, 550), stroke='#9C27B0', stroke_width=2))

    # Rules box
    rules = dwg.g(id='rules')
    add_rounded_rect(dwg, rules, 20, 620, 1160, 160, '#FFFFFF', rx=8, stroke=COLORS['border'])
    add_text(dwg, rules, 600, 650, 'Regole del Quiz ad Albero', size=16, color=COLORS['text'], anchor='middle', weight='bold')

    rule_lines = [
        '1. Ogni risposta determina la domanda successiva - non esiste un percorso unico',
        '2. Risposta corretta: percorso di approfondimento (+15 punti base + bonus profondità)',
        '3. Risposta errata: percorso di recupero (+10 punti, domande di rinforzo)',
        '4. Nodi di convergenza: punti dove percorsi diversi si riuniscono',
        '5. Profondità variabile: da 5 a 15 domande in base al percorso scelto',
        '6. Valutazione finale personalizzata in base al percorso effettuato'
    ]
    for i, line in enumerate(rule_lines):
        add_text(dwg, rules, 50, 685 + i * 22, line, size=11, color=COLORS['text_light'])
    main.add(rules)

    # Title
    add_text(dwg, main, 600, 795, 'WIREFRAME: TREE QUIZ SCHEMA', size=10, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_tree_schema.svg')


# ============================================
# WIREFRAME: TREE QUIZ - CREATOR BUILDER
# ============================================

def create_tree_builder():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_tree_builder.svg', size=(1440, 900))
    main = dwg.g(id='tree_builder')

    # Sidebar
    add_rounded_rect(dwg, main, 0, 0, 280, 900, '#F5F5F5', rx=0)
    add_text(dwg, main, 140, 40, 'Clinical Quiz', size=18, color=COLORS['primary'], anchor='middle', weight='bold')
    add_text(dwg, main, 140, 60, 'Tree Builder', size=12, color=COLORS['text_light'], anchor='middle')

    # Sidebar menu
    menu_items = ['Dashboard', 'I Miei Alberi']
    for i, item in enumerate(menu_items):
        y = 120 + i * 50
        if i == 1:
            add_rounded_rect(dwg, main, 15, y - 15, 250, 45, COLORS['primary'], rx=8)
            add_text(dwg, main, 140, y + 10, item, size=14, color='#FFFFFF', anchor='middle', weight='bold')
        else:
            add_text(dwg, main, 140, y + 10, item, size=14, color=COLORS['text'], anchor='middle')

    # Tree list
    add_text(dwg, main, 20, 230, 'Quiz Albero', size=12, color=COLORS['text_light'])
    trees = ['Diagnosi Cardiaca', 'Triage Emergenza', 'Farmacologia Base']
    for i, tree in enumerate(trees):
        y = 260 + i * 45
        bg_color = '#E3F2FD' if i == 0 else '#FFFFFF'
        add_rounded_rect(dwg, main, 15, y, 250, 40, bg_color, rx=6, stroke=COLORS['border'])
        add_text(dwg, main, 30, y + 25, tree, size=12, color=COLORS['text'])

    # Main content
    add_rounded_rect(dwg, main, 280, 0, 1160, 900, '#FFFFFF', rx=0)

    # Header
    add_text(dwg, main, 310, 45, 'Costruttore Albero: Diagnosi Cardiaca', size=20, color=COLORS['text'], weight='bold')
    add_text(dwg, main, 310, 70, 'Trascina i nodi per costruire il percorso decisionale', size=12, color=COLORS['text_light'])

    # Toolbar
    toolbar = dwg.g(id='toolbar')
    add_rounded_rect(dwg, toolbar, 310, 90, 1100, 50, COLORS['frame'], rx=8)

    tools = [('+ Domanda', COLORS['primary']), ('+ Convergenza', COLORS['secondary']), ('+ Fine', '#9C27B0'), ('Collega', COLORS['text_light']), ('Elimina', COLORS['error'])]
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

    # Sample tree nodes on canvas
    # Root
    root = dwg.g(id='canvas_root')
    add_rounded_rect(dwg, root, 600, 180, 180, 60, COLORS['primary'], rx=8)
    add_text(dwg, root, 690, 205, 'START', size=12, color='#FFFFFF', anchor='middle', weight='bold')
    add_text(dwg, root, 690, 225, 'Dolore toracico?', size=10, color='#FFFFFF', anchor='middle')
    main.add(root)

    # Level 2
    l2a = dwg.g(id='canvas_l2a')
    add_rounded_rect(dwg, l2a, 420, 290, 160, 55, COLORS['success'], rx=8)
    add_text(dwg, l2a, 500, 312, 'Sì - ECG anormale?', size=10, color='#FFFFFF', anchor='middle', weight='bold')
    main.add(l2a)

    l2b = dwg.g(id='canvas_l2b')
    add_rounded_rect(dwg, l2b, 780, 290, 160, 55, COLORS['warning'], rx=8)
    add_text(dwg, l2b, 860, 312, 'No - Altri sintomi?', size=10, color='#FFFFFF', anchor='middle', weight='bold')
    main.add(l2b)

    # Arrows
    main.add(dwg.line(start=(650, 240), end=(500, 290), stroke=COLORS['success'], stroke_width=2))
    main.add(dwg.line(start=(730, 240), end=(860, 290), stroke=COLORS['warning'], stroke_width=2))

    # Level 3 nodes
    l3a = dwg.g(id='canvas_l3a')
    add_rounded_rect(dwg, l3a, 340, 400, 140, 50, COLORS['success'], rx=8)
    add_text(dwg, l3a, 410, 430, 'STEMI?', size=10, color='#FFFFFF', anchor='middle')
    main.add(l3a)

    l3b = dwg.g(id='canvas_l3b')
    add_rounded_rect(dwg, l3b, 520, 400, 140, 50, COLORS['error'], rx=8)
    add_text(dwg, l3b, 590, 430, 'Enzimi cardiaci', size=10, color='#FFFFFF', anchor='middle')
    main.add(l3b)

    # More arrows
    main.add(dwg.line(start=(450, 345), end=(410, 400), stroke=COLORS['success'], stroke_width=2))
    main.add(dwg.line(start=(550, 345), end=(590, 400), stroke=COLORS['error'], stroke_width=2))

    # End node
    end_node = dwg.g(id='canvas_end')
    add_rounded_rect(dwg, end_node, 380, 510, 120, 45, '#9C27B0', rx=20)
    add_text(dwg, end_node, 440, 538, 'Diagnosi A', size=10, color='#FFFFFF', anchor='middle', weight='bold')
    main.add(end_node)
    main.add(dwg.line(start=(410, 450), end=(430, 510), stroke='#9C27B0', stroke_width=2))

    main.add(canvas)

    # Properties panel
    props = dwg.g(id='properties')
    add_rounded_rect(dwg, props, 1110, 160, 280, 580, '#FFFFFF', rx=8, stroke=COLORS['border'])
    add_text(dwg, props, 1250, 195, 'Proprietà Nodo', size=14, color=COLORS['text'], anchor='middle', weight='bold')

    # Selected node info
    add_text(dwg, props, 1130, 230, 'Nodo selezionato:', size=11, color=COLORS['text_light'])
    add_rounded_rect(dwg, props, 1130, 245, 240, 35, COLORS['primary'], rx=4)
    add_text(dwg, props, 1250, 268, 'START - Dolore toracico?', size=10, color='#FFFFFF', anchor='middle')

    # Form fields
    add_text(dwg, props, 1130, 310, 'Testo domanda:', size=11, color=COLORS['text_light'])
    add_input(dwg, props, 1130, 325, 240, 40, 'Il paziente presenta dolore toracico?')

    add_text(dwg, props, 1130, 390, 'Tipo nodo:', size=11, color=COLORS['text_light'])
    add_rounded_rect(dwg, props, 1130, 405, 240, 35, '#FFFFFF', rx=4, stroke=COLORS['border'])
    add_text(dwg, props, 1140, 428, 'Domanda a scelta', size=11, color=COLORS['text'])

    add_text(dwg, props, 1130, 465, 'Risposte:', size=11, color=COLORS['text_light'])

    # Response options
    resp1 = dwg.g(id='resp1')
    add_rounded_rect(dwg, resp1, 1130, 485, 240, 50, '#E8F5E9', rx=4, stroke=COLORS['success'])
    add_text(dwg, resp1, 1145, 505, 'Sì', size=11, color=COLORS['text'], weight='bold')
    add_text(dwg, resp1, 1145, 522, '→ ECG anormale?', size=9, color=COLORS['success'])
    main.add(resp1)

    resp2 = dwg.g(id='resp2')
    add_rounded_rect(dwg, resp2, 1130, 545, 240, 50, '#FFF3E0', rx=4, stroke=COLORS['warning'])
    add_text(dwg, resp2, 1145, 565, 'No', size=11, color=COLORS['text'], weight='bold')
    add_text(dwg, resp2, 1145, 582, '→ Altri sintomi?', size=9, color=COLORS['warning'])
    main.add(resp2)

    add_text(dwg, props, 1130, 620, 'Punti base:', size=11, color=COLORS['text_light'])
    add_input(dwg, props, 1130, 635, 100, 35, '10')

    add_text(dwg, props, 1250, 620, 'Bonus:', size=11, color=COLORS['text_light'])
    add_input(dwg, props, 1250, 635, 100, 35, '+5')

    add_button(dwg, props, 1130, 695, 240, 35, 'APPLICA MODIFICHE', COLORS['primary'])
    main.add(props)

    # Stats bar
    stats = dwg.g(id='stats')
    add_rounded_rect(dwg, stats, 310, 760, 1080, 60, COLORS['frame'], rx=8)

    stat_items = [('Nodi totali', '12'), ('Domande', '8'), ('Convergenze', '2'), ('Endpoint', '4'), ('Profondità max', '5')]
    for i, (label, value) in enumerate(stat_items):
        x = 380 + i * 200
        add_text(dwg, stats, x, 785, label, size=10, color=COLORS['text_light'], anchor='middle')
        add_text(dwg, stats, x, 808, value, size=18, color=COLORS['primary'], anchor='middle', weight='bold')
    main.add(stats)

    # Title
    add_text(dwg, main, 860, 880, 'WIREFRAME: TREE BUILDER - CREATOR', size=10, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_tree_builder.svg')


# ============================================
# WIREFRAME: TREE QUIZ - MOBILE QUESTION
# ============================================

def create_tree_mobile_question():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_tree_mobile_question.svg', size=(375, 812))
    main = dwg.g(id='tree_mobile_question')

    add_phone_frame(dwg, main, 0, 0, 375, 812, 'Quiz Albero')

    # Logo
    logo = dwg.g(id='logo')
    add_rounded_rect(dwg, logo, 20, 90, 80, 35, COLORS['frame'], rx=4, stroke=COLORS['border'])
    add_text(dwg, logo, 60, 113, 'LOGO', size=10, color=COLORS['text_light'], anchor='middle')
    main.add(logo)

    # Path indicator
    path = dwg.g(id='path_indicator')
    add_rounded_rect(dwg, path, 110, 90, 155, 35, '#E3F2FD', rx=17)
    add_text(dwg, path, 187, 108, 'Percorso: Livello 3', size=10, color=COLORS['primary'], anchor='middle', weight='bold')
    add_text(dwg, path, 187, 120, 'Approfondimento', size=8, color=COLORS['primary'], anchor='middle')
    main.add(path)

    # Points
    add_text(dwg, main, 320, 115, '45 pts', size=14, color=COLORS['text'], anchor='middle', weight='bold')

    # Visual path progress
    progress = dwg.g(id='progress')
    add_rounded_rect(dwg, progress, 20, 140, 335, 50, '#FAFAFA', rx=8)

    # Path dots
    path_x = [50, 110, 170, 230, 290, 320]
    path_colors = [COLORS['success'], COLORS['success'], COLORS['primary'], COLORS['frame'], COLORS['frame'], COLORS['frame']]
    for i, (x, col) in enumerate(zip(path_x, path_colors)):
        add_circle(dwg, progress, x, 165, 10 if i == 2 else 6, col)
        if i < len(path_x) - 1:
            line_col = COLORS['success'] if i < 2 else COLORS['frame']
            main.add(dwg.line(start=(x + 8, 165), end=(path_x[i+1] - 8, 165), stroke=line_col, stroke_width=2))
    add_text(dwg, progress, 230, 180, '?', size=10, color=COLORS['text_light'], anchor='middle')
    main.add(progress)

    # Question card
    question = dwg.g(id='question')
    add_card(dwg, question, 20, 210, 335, 130)
    add_text(dwg, question, 187, 250, 'In caso di ECG con', size=14, color=COLORS['text'], anchor='middle', weight='bold')
    add_text(dwg, question, 187, 275, 'sopraslivellamento ST,', size=14, color=COLORS['text'], anchor='middle', weight='bold')
    add_text(dwg, question, 187, 300, 'quale diagnosi sospetti?', size=14, color=COLORS['text'], anchor='middle', weight='bold')
    main.add(question)

    # Answer options - each leads to different path
    options = [
        ('A) STEMI', 'Percorso Emergenza', COLORS['error']),
        ('B) NSTEMI', 'Percorso Urgenza', COLORS['warning']),
        ('C) Angina stabile', 'Percorso Standard', COLORS['primary']),
        ('D) Non cardiaco', 'Percorso Esclusione', COLORS['text_light'])
    ]
    for i, (opt, path_label, path_color) in enumerate(options):
        opt_y = 360 + i * 80
        opt_group = dwg.g(id=f'option_{i}')
        add_card(dwg, opt_group, 20, opt_y, 335, 65)
        add_circle(dwg, opt_group, 55, opt_y + 32, 12, '#FFFFFF')
        main.add(dwg.circle(center=(55, opt_y + 32), r=12, fill='none', stroke=COLORS['primary'], stroke_width=2))
        add_text(dwg, opt_group, 80, opt_y + 28, opt, size=13, color=COLORS['text'], weight='bold')
        # Path indicator for each option
        add_rounded_rect(dwg, opt_group, 80, opt_y + 38, 100, 18, path_color, rx=9)
        add_text(dwg, opt_group, 130, opt_y + 51, path_label, size=8, color='#FFFFFF', anchor='middle')
        main.add(opt_group)

    # Info
    add_text(dwg, main, 187, 700, 'Ogni risposta ti porterà su un percorso diverso', size=10, color=COLORS['text_light'], anchor='middle')

    # Confirm button
    add_button(dwg, main, 40, 720, 295, 55, 'CONFERMA SCELTA', COLORS['primary'])

    # Title
    add_text(dwg, main, 187, 795, 'WIREFRAME: TREE MOBILE QUESTION', size=10, color=COLORS['text'], anchor='middle', weight='bold')

    dwg.add(main)
    dwg.save()
    print('✓ wireframe_tree_mobile_question.svg')


# ============================================
# WIREFRAME: TREE QUIZ - MOBILE RESULTS
# ============================================

def create_tree_mobile_results():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/wireframe_tree_mobile_results.svg', size=(375, 812))
    main = dwg.g(id='tree_mobile_results')

    add_phone_frame(dwg, main, 0, 0, 375, 812, 'Risultato Percorso')

    # Logo
    logo = dwg.g(id='logo')
    add_rounded_rect(dwg, logo, 147, 90, 80, 35, COLORS['frame'], rx=4, stroke=COLORS['border'])
    add_text(dwg, logo, 187, 113, 'LOGO', size=10, color=COLORS['text_light'], anchor='middle')
    main.add(logo)

    # Title
    add_text(dwg, main, 187, 155, 'Percorso Completato!', size=20, color=COLORS['text'], anchor='middle', weight='bold')

    # Path visualization
    path_viz = dwg.g(id='path_viz')
    add_card(dwg, path_viz, 20, 175, 335, 120)
    add_text(dwg, path_viz, 187, 200, 'Il tuo percorso', size=12, color=COLORS['text_light'], anchor='middle')

    # Visual path
    nodes = [
        (50, 'D1', COLORS['primary']),
        (95, 'D2a', COLORS['success']),
        (140, 'D3a', COLORS['success']),
        (185, 'C-A', COLORS['primary']),
        (230, 'D4', COLORS['success']),
        (275, 'D5', COLORS['warning']),
        (320, 'END', '#9C27B0')
    ]
    for i, (x, label, color) in enumerate(nodes):
        add_circle(dwg, path_viz, x, 250, 15, color)
        add_text(dwg, path_viz, x, 255, label, size=7, color='#FFFFFF', anchor='middle', weight='bold')
        if i < len(nodes) - 1:
            main.add(dwg.line(start=(x + 15, 250), end=(nodes[i+1][0] - 15, 250), stroke=color, stroke_width=2))

    add_text(dwg, path_viz, 187, 285, '7 domande • Profondità: 5 livelli', size=10, color=COLORS['text_light'], anchor='middle')
    main.add(path_viz)

    # Result badge
    badge = dwg.g(id='badge')
    add_rounded_rect(dwg, badge, 100, 310, 175, 80, COLORS['success'], rx=12)
    add_text(dwg, badge, 187, 345, 'ESPERTO', size=20, color='#FFFFFF', anchor='middle', weight='bold')
    add_text(dwg, badge, 187, 375, 'Diagnosi Cardiaca', size=11, color='#FFFFFF', anchor='middle')
    main.add(badge)

    # Score breakdown
    score = dwg.g(id='score')
    add_card(dwg, score, 20, 410, 335, 140)
    add_text(dwg, score, 187, 440, 'Dettaglio Punteggio', size=14, color=COLORS['text'], anchor='middle', weight='bold')

    score_items = [
        ('Risposte corrette (5x15)', '+75'),
        ('Risposte parziali (2x10)', '+20'),
        ('Bonus profondità (5 livelli)', '+25'),
        ('TOTALE', '120 pts')
    ]
    for i, (label, pts) in enumerate(score_items):
        y = 470 + i * 25
        weight = 'bold' if i == 3 else 'normal'
        color = COLORS['success'] if i == 3 else COLORS['text_light']
        add_text(dwg, score, 40, y, label, size=11, color=COLORS['text_light'] if i < 3 else COLORS['text'], weight=weight)
        add_text(dwg, score, 335, y, pts, size=11, color=color, anchor='end', weight=weight)
    main.add(score)

    # AI Feedback
    feedback = dwg.g(id='feedback')
    add_card(dwg, feedback, 20, 565, 335, 100)
    add_text(dwg, feedback, 187, 595, 'Valutazione AI', size=12, color=COLORS['text'], anchor='middle', weight='bold')
    add_text(dwg, feedback, 187, 620, 'Hai dimostrato ottime capacità', size=11, color=COLORS['text_light'], anchor='middle')
    add_text(dwg, feedback, 187, 640, 'diagnostiche nel percorso cardiologico.', size=11, color=COLORS['text_light'], anchor='middle')
    main.add(feedback)

    # Button
    add_button(dwg, main, 40, 685, 295, 50, 'VEDI CLASSIFICA', COLORS['primary'])

    # Title
    add_text(dwg, main, 187, 795, 'WIREFRAME: TREE MOBILE RESULTS', size=10, color=COLORS['text'], anchor='middle', weight='bold')

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
