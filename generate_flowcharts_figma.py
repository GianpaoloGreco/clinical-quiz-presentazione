#!/usr/bin/env python3
"""
Clinical Quiz - Flowchart SVG per Figma
Genera SVG con elementi separati editabili in Figma
Versione semplificata e più leggibile
"""

import svgwrite
import re
import os

OUTPUT_DIR = '/Users/gianpaologreco/Desktop/Progetti/ClinicalQuiz/output/figma_wireframes'

# Colori
COLORS = {
    'bg': '#FFFFFF',
    'start_end': '#4CAF50',      # Verde per start/end
    'page': '#90CAF9',           # Azzurro per pagine/schermate
    'action': '#FFE082',         # Giallo per azioni utente
    'system': '#A5D6A7',         # Verde chiaro per azioni sistema
    'decision': '#FFCC80',       # Arancione chiaro per decisioni
    'ai': '#CE93D8',             # Viola per AI
    'text': '#212121',
    'text_light': '#757575',
    'arrow': '#616161',
    'border': '#BDBDBD',
    'admin_bg': '#E3F2FD',
    'creator_bg': '#FFF8E1',
    'participant_bg': '#E8F5E9',
}

def create_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================
# COMPONENTI FLOWCHART
# ============================================

def safe_id(text):
    """Genera ID sicuro per SVG"""
    return re.sub(r'[^a-zA-Z0-9_]', '', text.replace(" ", "_"))[:30]

def add_rounded_rect(dwg, group, x, y, w, h, fill, rx=8, stroke=None, stroke_width=1.5):
    """Rettangolo arrotondato"""
    rect = dwg.rect(insert=(x, y), size=(w, h), rx=rx, ry=rx, fill=fill)
    if stroke:
        rect['stroke'] = stroke
        rect['stroke-width'] = stroke_width
    group.add(rect)
    return rect

def add_text(dwg, group, x, y, text, size=14, color='#212121', anchor='middle', weight='normal'):
    """Testo"""
    t = dwg.text(text, insert=(x, y), fill=color,
                 style=f"font-family: Arial, sans-serif; font-size: {size}px; font-weight: {weight}")
    t['text-anchor'] = anchor
    group.add(t)
    return t

def add_start_end(dwg, group, cx, cy, text):
    """Nodo start/end (ovale)"""
    node = dwg.g(id=f'start_{safe_id(text)}')
    ellipse = dwg.ellipse(center=(cx, cy), r=(70, 30), fill=COLORS['start_end'])
    node.add(ellipse)
    add_text(dwg, node, cx, cy + 5, text, size=13, color='#FFFFFF', weight='bold')
    group.add(node)
    return node

def add_page(dwg, group, cx, cy, text, w=150, h=55):
    """Nodo pagina/schermata (rettangolo azzurro)"""
    node = dwg.g(id=f'page_{safe_id(text)}')
    add_rounded_rect(dwg, node, cx - w/2, cy - h/2, w, h, COLORS['page'], rx=8, stroke='#1976D2')

    lines = text.split('\n') if '\n' in text else [text]
    line_height = 16
    start_y = cy - (len(lines) - 1) * line_height / 2 + 5
    for i, line in enumerate(lines):
        add_text(dwg, node, cx, start_y + i * line_height, line, size=12, color=COLORS['text'])

    group.add(node)
    return node

def add_action(dwg, group, cx, cy, text, w=150, h=55):
    """Nodo azione utente (rettangolo giallo)"""
    node = dwg.g(id=f'action_{safe_id(text)}')
    add_rounded_rect(dwg, node, cx - w/2, cy - h/2, w, h, COLORS['action'], rx=8, stroke='#F9A825')

    lines = text.split('\n') if '\n' in text else [text]
    line_height = 16
    start_y = cy - (len(lines) - 1) * line_height / 2 + 5
    for i, line in enumerate(lines):
        add_text(dwg, node, cx, start_y + i * line_height, line, size=12, color=COLORS['text'])

    group.add(node)
    return node

def add_system(dwg, group, cx, cy, text, w=150, h=55):
    """Nodo azione sistema (rettangolo verde)"""
    node = dwg.g(id=f'system_{safe_id(text)}')
    add_rounded_rect(dwg, node, cx - w/2, cy - h/2, w, h, COLORS['system'], rx=8, stroke='#388E3C')

    lines = text.split('\n') if '\n' in text else [text]
    line_height = 16
    start_y = cy - (len(lines) - 1) * line_height / 2 + 5
    for i, line in enumerate(lines):
        add_text(dwg, node, cx, start_y + i * line_height, line, size=12, color=COLORS['text'])

    group.add(node)
    return node

def add_decision(dwg, group, cx, cy, text, w=130, h=70):
    """Nodo decisione (rombo)"""
    node = dwg.g(id=f'decision_{safe_id(text)}')

    points = [
        (cx, cy - h/2),
        (cx + w/2, cy),
        (cx, cy + h/2),
        (cx - w/2, cy),
    ]
    polygon = dwg.polygon(points, fill=COLORS['decision'], stroke='#EF6C00', stroke_width=1.5)
    node.add(polygon)

    add_text(dwg, node, cx, cy + 5, text, size=11, color=COLORS['text'])
    group.add(node)
    return node

def add_ai(dwg, group, cx, cy, text, w=150, h=55):
    """Nodo AI (rettangolo viola)"""
    node = dwg.g(id=f'ai_{safe_id(text)}')
    add_rounded_rect(dwg, node, cx - w/2, cy - h/2, w, h, COLORS['ai'], rx=8, stroke='#7B1FA2')

    lines = text.split('\n') if '\n' in text else [text]
    line_height = 16
    start_y = cy - (len(lines) - 1) * line_height / 2 + 5
    for i, line in enumerate(lines):
        add_text(dwg, node, cx, start_y + i * line_height, line, size=12, color=COLORS['text'])

    group.add(node)
    return node

def add_arrow(dwg, group, x1, y1, x2, y2, label=''):
    """Freccia di collegamento"""
    import math
    arrow = dwg.g(id=f'arrow_{int(x1)}_{int(y1)}')

    line = dwg.line(start=(x1, y1), end=(x2, y2), stroke=COLORS['arrow'], stroke_width=2)
    arrow.add(line)

    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_size = 10
    p1 = (x2 - arrow_size * math.cos(angle - 0.4), y2 - arrow_size * math.sin(angle - 0.4))
    p2 = (x2 - arrow_size * math.cos(angle + 0.4), y2 - arrow_size * math.sin(angle + 0.4))
    arrowhead = dwg.polygon([(x2, y2), p1, p2], fill=COLORS['arrow'])
    arrow.add(arrowhead)

    if label:
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        add_text(dwg, arrow, mid_x + 10, mid_y - 5, label, size=11, color=COLORS['text_light'])

    group.add(arrow)
    return arrow

def add_legend(dwg, group, x, y):
    """Legenda del flowchart"""
    legend = dwg.g(id='legend')
    add_rounded_rect(dwg, legend, x, y, 200, 180, '#FAFAFA', rx=8, stroke=COLORS['border'])
    add_text(dwg, legend, x + 100, y + 25, 'LEGENDA', size=13, color=COLORS['text'], weight='bold')

    items = [
        (COLORS['start_end'], 'Start / End'),
        (COLORS['page'], 'Pagina / Schermata'),
        (COLORS['action'], 'Azione Utente'),
        (COLORS['system'], 'Azione Sistema'),
        (COLORS['decision'], 'Decisione'),
    ]

    for i, (color, label) in enumerate(items):
        iy = y + 55 + i * 26
        add_rounded_rect(dwg, legend, x + 20, iy - 10, 24, 18, color, rx=4)
        add_text(dwg, legend, x + 55, iy + 4, label, size=11, color=COLORS['text'], anchor='start')

    group.add(legend)


# ============================================
# FLOWCHART: OVERVIEW
# ============================================

def create_flow_overview():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/flow_overview.svg', size=(1100, 450))
    main = dwg.g(id='flow_overview')

    add_rounded_rect(dwg, main, 0, 0, 1100, 450, COLORS['bg'], rx=0)

    # Title
    add_text(dwg, main, 550, 35, 'FLOW: OVERVIEW SISTEMA CLINICAL QUIZ', size=20, color=COLORS['text'], weight='bold')
    add_text(dwg, main, 550, 55, 'Interazione tra Admin, Creator e Partecipante', size=12, color=COLORS['text_light'])

    lane_h = 110
    lane_w = 1050
    start_x = 25

    # === ADMIN LANE ===
    lane_y = 80
    add_rounded_rect(dwg, main, start_x, lane_y, lane_w, lane_h, COLORS['admin_bg'], rx=8, stroke='#1976D2')
    add_text(dwg, main, 70, lane_y + 20, 'ADMIN', size=13, color='#1565C0', weight='bold')

    y = lane_y + 65
    add_page(dwg, main, 150, y, 'Login', w=100, h=40)
    add_arrow(dwg, main, 200, y, 260, y)
    add_page(dwg, main, 330, y, 'Dashboard', w=110, h=40)
    add_arrow(dwg, main, 385, y, 450, y)
    add_action(dwg, main, 530, y, 'Crea Creator', w=120, h=40)
    add_arrow(dwg, main, 590, y, 660, y)
    add_page(dwg, main, 730, y, 'Report', w=100, h=40)
    add_arrow(dwg, main, 780, y, 850, y)
    add_action(dwg, main, 920, y, 'Esporta', w=100, h=40)

    # === CREATOR LANE ===
    lane_y = 200
    add_rounded_rect(dwg, main, start_x, lane_y, lane_w, lane_h, COLORS['creator_bg'], rx=8, stroke='#FF9800')
    add_text(dwg, main, 70, lane_y + 20, 'CREATOR', size=13, color='#E65100', weight='bold')

    y = lane_y + 65
    add_page(dwg, main, 150, y, 'Login', w=100, h=40)
    add_arrow(dwg, main, 200, y, 260, y)
    add_page(dwg, main, 330, y, 'Dashboard', w=110, h=40)
    add_arrow(dwg, main, 385, y, 450, y)
    add_action(dwg, main, 530, y, 'Wizard\n5 Steps', w=120, h=45)
    add_arrow(dwg, main, 590, y, 660, y)
    add_system(dwg, main, 730, y, 'Genera\nQR + Codice', w=110, h=45)
    add_arrow(dwg, main, 785, y, 850, y)
    add_page(dwg, main, 920, y, 'Monitor\nLive', w=100, h=45)

    # === PARTECIPANTE LANE ===
    lane_y = 320
    add_rounded_rect(dwg, main, start_x, lane_y, lane_w, lane_h, COLORS['participant_bg'], rx=8, stroke='#4CAF50')
    add_text(dwg, main, 70, lane_y + 20, 'PARTECIPANTE', size=13, color='#2E7D32', weight='bold')

    y = lane_y + 65
    add_action(dwg, main, 150, y, 'Scansiona\nQR', w=100, h=45)
    add_arrow(dwg, main, 200, y, 260, y)
    add_page(dwg, main, 330, y, 'Landing', w=100, h=40)
    add_arrow(dwg, main, 380, y, 450, y)
    add_page(dwg, main, 530, y, 'Quiz\nDomande', w=120, h=45)
    add_arrow(dwg, main, 590, y, 660, y)
    add_ai(dwg, main, 730, y, 'AI\nFeedback', w=110, h=45)
    add_arrow(dwg, main, 785, y, 850, y)
    add_page(dwg, main, 920, y, 'Risultati', w=100, h=40)

    dwg.add(main)
    dwg.save()
    print('✓ flow_overview.svg')


# ============================================
# FLOWCHART: ADMIN (Semplificato)
# ============================================

def create_flow_admin():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/flow_admin.svg', size=(900, 450))
    main = dwg.g(id='flow_admin')

    add_rounded_rect(dwg, main, 0, 0, 900, 450, COLORS['bg'], rx=0)

    # Title
    add_text(dwg, main, 450, 35, 'FLOW: ADMIN DELLA PIATTAFORMA', size=18, color=COLORS['text'], weight='bold')
    add_text(dwg, main, 450, 55, 'Gestione utenti e monitoraggio piattaforma', size=12, color=COLORS['text_light'])

    # Main flow (horizontal) - Row 1
    y1 = 130
    add_start_end(dwg, main, 80, y1, 'Inizio')
    add_arrow(dwg, main, 150, y1, 200, y1)
    add_page(dwg, main, 280, y1, 'Pagina Login', w=120, h=45)
    add_arrow(dwg, main, 340, y1, 400, y1)
    add_page(dwg, main, 490, y1, 'Dashboard Admin', w=140, h=45)

    # Row 2 - Gestione Utenti path
    y2 = 230
    add_arrow(dwg, main, 490, 155, 490, 205)
    add_page(dwg, main, 280, y2, 'Gestione Utenti', w=130, h=45)
    add_arrow(dwg, main, 490, y2, 345, y2)
    add_arrow(dwg, main, 215, y2, 160, y2)
    add_action(dwg, main, 80, y2, 'Crea / Modifica\nCreator', w=130, h=50)

    # Row 2 - Report path
    add_page(dwg, main, 490, y2, 'Report', w=110, h=45)
    add_arrow(dwg, main, 545, y2, 620, y2)
    add_action(dwg, main, 710, y2, 'Visualizza /\nEsporta', w=130, h=50)

    # Azioni Admin box
    box_x = 620
    box_y = 290
    add_rounded_rect(dwg, main, box_x, box_y, 250, 150, '#FAFAFA', rx=8, stroke=COLORS['border'])
    add_text(dwg, main, box_x + 125, box_y + 25, 'Azioni Admin', size=14, color=COLORS['text'], weight='bold')

    actions = ['Attiva / Disattiva Creator', 'Visualizza statistiche', 'Filtra per data / Creator', 'Export Excel', 'Logout']
    for i, action in enumerate(actions):
        add_rounded_rect(dwg, main, box_x + 15, box_y + 45 + i * 22, 220, 18, COLORS['action'], rx=4, stroke='#F9A825')
        add_text(dwg, main, box_x + 125, box_y + 58 + i * 22, action, size=10, color=COLORS['text'])

    # Legenda
    add_legend(dwg, main, 30, 270)

    dwg.add(main)
    dwg.save()
    print('✓ flow_admin.svg')


# ============================================
# FLOWCHART: CREATOR (Semplificato)
# ============================================

def create_flow_creator():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/flow_creator.svg', size=(1100, 550))
    main = dwg.g(id='flow_creator')

    add_rounded_rect(dwg, main, 0, 0, 1100, 550, COLORS['bg'], rx=0)

    # Title
    add_text(dwg, main, 550, 35, 'FLOW: CREATOR (ORGANIZZATORE EVENTO)', size=18, color=COLORS['text'], weight='bold')
    add_text(dwg, main, 550, 55, 'Creazione quiz, pubblicazione e monitoraggio', size=12, color=COLORS['text_light'])

    # Row 1: Login -> Dashboard
    y1 = 120
    add_start_end(dwg, main, 80, y1, 'Inizio')
    add_arrow(dwg, main, 150, y1, 200, y1)
    add_page(dwg, main, 280, y1, 'Pagina Login', w=120, h=45)
    add_arrow(dwg, main, 340, y1, 400, y1)
    add_page(dwg, main, 500, y1, 'Dashboard Creator', w=150, h=45)

    # Row 2: Wizard 5 Steps
    y2 = 210
    add_arrow(dwg, main, 500, 145, 500, 185)

    steps = [
        (120, 'Step 1:\nInfo Base'),
        (270, 'Step 2:\nGrafica'),
        (420, 'Step 3:\nPrivacy/GDPR'),
        (570, 'Step 4:\nImport Domande'),
        (720, 'Step 5:\nClassifica')
    ]
    for i, (x, name) in enumerate(steps):
        add_page(dwg, main, x, y2, name, w=120, h=50)
        if i < len(steps) - 1:
            add_arrow(dwg, main, x + 60, y2, steps[i+1][0] - 60, y2)

    add_arrow(dwg, main, 500, 185, 120, y2 - 25)

    # Row 3: Decision Pubblica?
    y3 = 310
    add_arrow(dwg, main, 720, 235, 720, 275)
    add_decision(dwg, main, 720, 310, 'Pubblica?', w=100, h=55)

    # Bozza path
    add_arrow(dwg, main, 670, 310, 550, 310, 'Bozza')
    add_system(dwg, main, 450, 310, 'Salva Bozza', w=110, h=40)
    add_arrow(dwg, main, 450, 290, 450, 120)
    add_arrow(dwg, main, 450, 120, 425, 120)

    # Pubblica path
    add_arrow(dwg, main, 770, 310, 870, 310, 'Pubblica')
    add_system(dwg, main, 970, 310, 'Genera QR Code\n+ Codice Stanza', w=140, h=55)

    # Row 4: Post pubblicazione
    y4 = 410
    add_arrow(dwg, main, 970, 340, 970, 380)
    add_page(dwg, main, 970, y4, 'Pagina QR Code\n& Codice', w=140, h=50)

    # Monitor Live
    add_arrow(dwg, main, 900, y4, 780, y4)
    add_page(dwg, main, 680, y4, 'Monitor Live', w=120, h=45)
    add_arrow(dwg, main, 680, 435, 680, 480)
    add_action(dwg, main, 680, 510, 'Visualizza\nClassifica Real-time', w=150, h=50)

    # Event Detail
    add_arrow(dwg, main, 970, 435, 970, 480)
    add_page(dwg, main, 970, 510, 'Event Detail', w=120, h=45)
    add_arrow(dwg, main, 970, 535, 970, 540)

    # Fine
    add_arrow(dwg, main, 620, y4, 520, y4)
    add_start_end(dwg, main, 420, y4, 'Fine')

    # Export box
    add_rounded_rect(dwg, main, 850, 480, 130, 60, '#FFF3E0', rx=6, stroke='#FF9800')
    add_text(dwg, main, 915, 505, 'Export Report', size=10, color='#E65100', weight='bold')
    add_text(dwg, main, 915, 525, 'Excel', size=10, color='#FF9800')

    # Import Google Form box
    add_rounded_rect(dwg, main, 30, 280, 180, 70, '#FFF3E0', rx=6, stroke='#FF9800')
    add_text(dwg, main, 120, 305, 'Import da Google Form', size=10, color='#E65100', weight='bold')
    add_text(dwg, main, 120, 325, 'Domande + Risposte', size=9, color='#FF9800')
    add_text(dwg, main, 120, 340, '+ Difficoltà + Media', size=9, color='#FF9800')

    # Legenda
    add_legend(dwg, main, 30, 370)

    dwg.add(main)
    dwg.save()
    print('✓ flow_creator.svg')


# ============================================
# FLOWCHART: PARTICIPANT (Semplificato)
# ============================================

def create_flow_participant():
    dwg = svgwrite.Drawing(f'{OUTPUT_DIR}/flow_participant.svg', size=(1100, 550))
    main = dwg.g(id='flow_participant')

    add_rounded_rect(dwg, main, 0, 0, 1100, 550, COLORS['bg'], rx=0)

    # Title
    add_text(dwg, main, 550, 35, 'FLOW: PARTECIPANTE (MOBILE)', size=18, color=COLORS['text'], weight='bold')
    add_text(dwg, main, 550, 55, 'Accesso quiz, risposta domande e visualizzazione risultati', size=12, color=COLORS['text_light'])

    # Row 1: Accesso
    y1 = 130
    add_start_end(dwg, main, 100, y1, 'Scansiona QR\no Codice')
    add_arrow(dwg, main, 170, y1, 230, y1)
    add_page(dwg, main, 320, y1, 'Mobile Landing', w=130, h=45)
    add_arrow(dwg, main, 385, y1, 450, y1)
    add_action(dwg, main, 550, y1, 'Inserisce\nCodice Stanza', w=140, h=50)
    add_arrow(dwg, main, 620, y1, 690, y1)
    add_decision(dwg, main, 780, y1, 'Valido?', w=100, h=50)

    # No -> Errore (semplice)
    add_action(dwg, main, 950, y1, 'Errore:\nCodice non valido', w=140, h=50)
    add_arrow(dwg, main, 830, y1, 880, y1, 'No')

    # Row 2: Registrazione
    y2 = 240
    add_arrow(dwg, main, 780, 160, 780, 210, 'Si')
    add_page(dwg, main, 320, y2, 'Registrazione\n(Nome, GDPR)', w=140, h=50)
    add_arrow(dwg, main, 780, y2, 390, y2)
    add_arrow(dwg, main, 250, y2, 180, y2)
    add_action(dwg, main, 100, y2, 'Clicca\n"Inizia Quiz"', w=120, h=50)

    # Row 3: Quiz loop
    y3 = 340
    add_arrow(dwg, main, 100, 265, 100, 310)
    add_page(dwg, main, 200, y3, 'Schermata\nDomanda', w=130, h=50)
    add_arrow(dwg, main, 100, y3, 135, y3)
    add_arrow(dwg, main, 265, y3, 340, y3)
    add_action(dwg, main, 440, y3, 'Seleziona\nRisposta', w=130, h=50)
    add_arrow(dwg, main, 505, y3, 580, y3)
    add_system(dwg, main, 680, y3, 'Sistema valuta\nrisposta', w=140, h=50)
    add_arrow(dwg, main, 750, y3, 830, y3)
    add_decision(dwg, main, 920, y3, 'Corretta?', w=100, h=50)

    # Feedback
    y4 = 440
    add_arrow(dwg, main, 920, 365, 920, 410, 'No')
    add_ai(dwg, main, 920, y4, 'AI Feedback\n(GPT-4 Mini)', w=140, h=50)

    add_page(dwg, main, 1020, y4, 'Risposta\nCorretta!', w=110, h=45)
    add_arrow(dwg, main, 970, y3, 1020, y3, 'Si')
    add_arrow(dwg, main, 1020, y3 + 25, 1020, y4 - 25)

    # Row 4: Risultati
    y5 = 500
    add_arrow(dwg, main, 920, 465, 920, y5)
    add_arrow(dwg, main, 1020, 465, 1020, y5)
    add_arrow(dwg, main, 920, y5, 700, y5)
    add_arrow(dwg, main, 1020, y5, 920, y5)

    add_page(dwg, main, 600, y5, 'Risultati\nPersonali', w=120, h=45)
    add_arrow(dwg, main, 540, y5, 450, y5)
    add_page(dwg, main, 350, y5, 'Classifica\nFinale', w=120, h=45)
    add_arrow(dwg, main, 290, y5, 200, y5)
    add_start_end(dwg, main, 100, y5, 'Fine')

    # Box Sistema Punteggio
    add_rounded_rect(dwg, main, 30, 380, 150, 100, '#E8F5E9', rx=6, stroke='#4CAF50')
    add_text(dwg, main, 105, 400, 'Sistema Punteggio', size=10, color='#2E7D32', weight='bold')
    add_text(dwg, main, 105, 420, 'Facile: 10 pts', size=9, color='#4CAF50')
    add_text(dwg, main, 105, 438, 'Media: 15 pts', size=9, color='#4CAF50')
    add_text(dwg, main, 105, 456, 'Difficile: 20 pts', size=9, color='#4CAF50')
    add_text(dwg, main, 105, 474, 'Difficoltà adattiva', size=8, color='#388E3C', weight='bold')

    # Legenda
    add_legend(dwg, main, 750, 80)

    dwg.add(main)
    dwg.save()
    print('✓ flow_participant.svg')


# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    print('\n📊 Generazione Flowchart SVG per Figma\n')
    print('=' * 50)

    create_output_dir()

    print('\n🔷 FLOWCHARTS')
    create_flow_overview()
    create_flow_admin()
    create_flow_creator()
    create_flow_participant()

    print('\n' + '=' * 50)
    print(f'✅ Flowchart generati in: {OUTPUT_DIR}')
    print('=' * 50 + '\n')
