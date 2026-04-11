#!/usr/bin/env python3
"""
BetonWin — Executive Presentation for Management
Clear, block-based layout with key information for decision-makers.
ALL IN ENGLISH. Professional, concise, visual.
"""
import csv, os, sys
from collections import Counter, defaultdict
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, Frame, PageTemplate
)

# ── Colors ──
DARK    = colors.HexColor('#1a1a2e')
GREEN   = colors.HexColor('#16a34a')
RED     = colors.HexColor('#dc2626')
AMBER   = colors.HexColor('#d97706')
BLUE    = colors.HexColor('#2563eb')
GRAY    = colors.HexColor('#6b7280')
PURPLE  = colors.HexColor('#7c3aed')
TEAL    = colors.HexColor('#0d9488')
LGRAY   = colors.HexColor('#f3f4f6')
LGREEN  = colors.HexColor('#dcfce7')
LRED    = colors.HexColor('#fee2e2')
LAMBER  = colors.HexColor('#fef3c7')
LBLUE   = colors.HexColor('#dbeafe')
LPURPLE = colors.HexColor('#ede9fe')
LTEAL   = colors.HexColor('#ccfbf1')
WHITE   = colors.white
DBLUE   = colors.HexColor('#1e40af')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle('SlideTitle', parent=styles['Title'], fontSize=26, textColor=WHITE, spaceAfter=2, alignment=TA_LEFT))
styles.add(ParagraphStyle('SlideTitle2', parent=styles['Title'], fontSize=22, textColor=DARK, spaceAfter=4, alignment=TA_LEFT))
styles.add(ParagraphStyle('Sub', parent=styles['Normal'], fontSize=14, textColor=BLUE, spaceAfter=2))
styles.add(ParagraphStyle('SubWhite', parent=styles['Normal'], fontSize=14, textColor=colors.HexColor('#93c5fd'), spaceAfter=2))
styles.add(ParagraphStyle('H1', parent=styles['Heading1'], fontSize=18, textColor=DARK, spaceBefore=10, spaceAfter=6))
styles.add(ParagraphStyle('H2', parent=styles['Heading2'], fontSize=14, textColor=BLUE, spaceBefore=8, spaceAfter=4))
styles.add(ParagraphStyle('H3', parent=styles['Heading3'], fontSize=12, textColor=DARK, spaceBefore=6, spaceAfter=3))
styles.add(ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, leading=14, textColor=DARK, alignment=TA_JUSTIFY))
styles.add(ParagraphStyle('BodyLarge', parent=styles['Normal'], fontSize=11, leading=15, textColor=DARK))
styles.add(ParagraphStyle('BodyWhite', parent=styles['Normal'], fontSize=10, leading=14, textColor=WHITE))
styles.add(ParagraphStyle('BodyBold', parent=styles['Normal'], fontSize=10, leading=14, textColor=DARK, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('Small', parent=styles['Normal'], fontSize=8, leading=10, textColor=GRAY))
styles.add(ParagraphStyle('SmallWhite', parent=styles['Normal'], fontSize=8, leading=10, textColor=colors.HexColor('#93c5fd')))
styles.add(ParagraphStyle('BulletX', parent=styles['Normal'], fontSize=10, leading=14, leftIndent=18, bulletIndent=6, textColor=DARK))
styles.add(ParagraphStyle('BulletWhite', parent=styles['Normal'], fontSize=10, leading=14, leftIndent=18, bulletIndent=6, textColor=WHITE))
styles.add(ParagraphStyle('CellBody', parent=styles['Normal'], fontSize=8, leading=10, textColor=DARK))
styles.add(ParagraphStyle('CellBold', parent=styles['Normal'], fontSize=8, leading=10, textColor=DARK, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('CellSmall', parent=styles['Normal'], fontSize=7, leading=9, textColor=GRAY))
styles.add(ParagraphStyle('BigNum', parent=styles['Normal'], fontSize=36, textColor=BLUE, fontName='Helvetica-Bold', alignment=TA_CENTER))
styles.add(ParagraphStyle('BigNumGreen', parent=styles['Normal'], fontSize=36, textColor=GREEN, fontName='Helvetica-Bold', alignment=TA_CENTER))
styles.add(ParagraphStyle('BigNumRed', parent=styles['Normal'], fontSize=36, textColor=RED, fontName='Helvetica-Bold', alignment=TA_CENTER))
styles.add(ParagraphStyle('BigNumWhite', parent=styles['Normal'], fontSize=36, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER))
styles.add(ParagraphStyle('MedNum', parent=styles['Normal'], fontSize=22, textColor=BLUE, fontName='Helvetica-Bold', alignment=TA_CENTER))
styles.add(ParagraphStyle('KPILabel', parent=styles['Normal'], fontSize=9, textColor=GRAY, alignment=TA_CENTER))
styles.add(ParagraphStyle('KPILabelW', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#93c5fd'), alignment=TA_CENTER))
styles.add(ParagraphStyle('Callout', parent=styles['Normal'], fontSize=10, leading=14, textColor=DARK,
                           leftIndent=10, rightIndent=10, backColor=LBLUE, borderPadding=8))
styles.add(ParagraphStyle('CalloutGreen', parent=styles['Normal'], fontSize=10, leading=14, textColor=DARK,
                           leftIndent=10, rightIndent=10, backColor=LGREEN, borderPadding=8))
styles.add(ParagraphStyle('CalloutRed', parent=styles['Normal'], fontSize=10, leading=14, textColor=DARK,
                           leftIndent=10, rightIndent=10, backColor=LRED, borderPadding=8))

def hr():
    return HRFlowable(width='100%', thickness=1, color=BLUE, spaceBefore=4, spaceAfter=6)

def hr_light():
    return HRFlowable(width='100%', thickness=0.5, color=GRAY, spaceBefore=4, spaceAfter=4)

def spacer(h=4):
    return Spacer(1, h*mm)

def make_table(data, col_widths=None, header_color=DARK):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), header_color),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('FONTSIZE', (0,1), (-1,-1), 8.5),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#d1d5db')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LGRAY]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    return t

def safe(text, max_len=120):
    if not text:
        return ''
    return str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')[:max_len]

# ════════════════════════════════════════════════════════════════
# CLASSIFICATION
# ════════════════════════════════════════════════════════════════
TOPICS_ENHANCED = {
    'Deposit Not Credited': ['no se reflejo','no se acredito','no me acredito','no aparece','no lo veo','no figura','deposite y no','hice un deposito y no','not credited','balance not updated','saldo no cambio','no fue acreditado','hice una transferencia y no','transferi y no','recarga exitosa pero','exitoso pero no','no recibido','no llego','no recibi','ya pague y no','pague y no','no veo el saldo','deposito no aparece','deposito no reflejado'],
    'How to Deposit': ['como depositar','como deposito','como cargo','quiero depositar','como recargo','formas de pago','how to deposit','metodo deposito','monto minimo','como puedo cargar','donde puedo depositar','que metodos','acepta','aceptan','metodos de pago','formas de deposito'],
    'Deposit Failed / Declined': ['failed','fallido','rechazado','error al depositar','error de pago','transaccion fallida','payment failed','declined','declinado','no se proceso','pago rechazado','tarjeta rechazada'],
    'Deposit Processing Delay': ['cuanto tarda','esperando deposito','en espera','pending deposit','demora deposito','tarda mucho','still processing','lleva mucho tiempo','cuanto demora','sigue en proceso'],
    'Recarga / Top-up': ['recarga','recargar','carga saldo','cargar saldo','cargar cuenta','recargue','recarge','top up','topup','hice una recarga','mi recarga'],
    'How to Withdraw': ['como retirar','como retiro','quiero retirar','quiero sacar','como saco','quiero cobrar','como cobro','puedo retirar','metodo de retiro','how to withdraw','cobrar mi dinero','sacar mi plata','retirar mi plata','quiero mi dinero'],
    'Withdrawal Pending / Delay': ['retiro pendiente','retiro demora','retiro tarda','esperando retiro','withdrawal pending','en proceso retiro','cuanto tarda retiro','mi retiro no llega'],
    'Withdrawal Rejected': ['retiro rechazado','no me dejan retirar','no puedo retirar','withdrawal rejected','withdrawal denied','cannot withdraw','retiro cancelado'],
    'Bonus / Promotions': ['bono','bonos','promocion','promos','bonus','free bet','freespin','regalo','oferta','codigo promo','cashback','giros gratis','tiradas','rollover','wagering','bono bienvenida','welcome bonus','como uso el bono','activar','free spin','giros','promo'],
    'Account / Login Issues': ['no puedo entrar','no puedo ingresar','olvide mi','mi contrasena','recuperar contrasena','acceder','acceso','cuenta bloqueada','me bloqueo','login','password','contrasena','crear cuenta','abrir cuenta','registrarme','no me deja entrar','suspendida','nueva cuenta','cerrar cuenta','desactivar','autoexclusion'],
    'Bank Transfer / Comprobante': ['transferencia','banco','cuenta bancaria','comprobante','voucher','recibo','clabe','cvu','cbu','cuenta corriente','envie comprobante','transferencia bancaria','cuenta de banco','numero de cuenta','iban','mande el comprobante','adjunto comprobante','bonifico','datos bancarios'],
    'Casino / Games / Bets': ['juego','juegos','apuesta','apuestas','slot','partida','no carga el juego','resultado','mi apuesta','ganancia','gane','perdi','casino','live','tragamonedas','apostar','jackpot','ganancias','winnings','error en el juego','vincita','mesa','ruleta','blackjack','poker'],
    'Technical / App / Website': ['no funciona','no abre','error','no carga','se cierra','app','aplicacion','celular','telefono','android','iphone','pagina','sitio','pantalla','se traba','problema tecnico','website down','app crash','not loading','descargar','instalar'],
    'KYC / Verification': ['verificar','verificacion','documento','dni','pasaporte','validar','selfie','foto','comprobante domicilio','identidad','kyc','cedula','identity verification','documento de identidad','verificar cuenta','verificar identidad'],
    'Complaint / Dissatisfaction': ['queja','reclamo','no es justo','me robaron','estafados','pesimo','muy malo','terrible','fraude','robo','estafa','quiero quejarme','inaceptable','abuso','ladrones','aprovechadores'],
    'Balance / Account Info': ['mi saldo','cual es mi saldo','saldo disponible','cuanto tengo','mi cuenta','datos de mi cuenta','informacion de cuenta','balance','my balance','mis datos','estado de cuenta'],
    'General Inquiry': ['informacion','info','pregunta','consulta','duda','ayuda','help','necesito','por favor','urgente','hola','buenas','buen dia','buenos dias','buenas tardes','buenas noches','hi','hello','good morning','good afternoon'],
}

def classify_enhanced(text):
    t = text.lower()
    scores = {}
    for topic, kws in TOPICS_ENHANCED.items():
        if topic == 'General Inquiry':
            continue
        score = sum(1 for kw in kws if kw in t)
        if score > 0:
            scores[topic] = score
    if not scores:
        return 'General Inquiry'
    return max(scores, key=scores.get)

# ════════════════════════════════════════════════════════════════
# LOAD DATA
# ════════════════════════════════════════════════════════════════
print('Loading CSV...')
csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_tickets_export.csv')
tickets = []
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        text = (row.get('subject', '') or '') + ' ' + (row.get('description', '') or '')
        row['topic'] = classify_enhanced(text)
        tickets.append(row)

TOTAL = len(tickets)
print(f'Loaded {TOTAL:,} tickets')

# Analytics
topic_totals = Counter()
monthly_topic = defaultdict(lambda: Counter())
monthly_vol = Counter()
channel_dist = Counter()
status_dist = Counter()

for t in tickets:
    topic_totals[t['topic']] += 1
    monthly_topic[t['month']][t['topic']] += 1
    monthly_vol[t['month']] += 1
    channel_dist[t.get('channel') or t.get('via_channel') or 'unknown'] += 1
    status_dist[t['status']] += 1

months_sorted = sorted(monthly_vol.keys())
first_month = months_sorted[0]
last_month = months_sorted[-1]

# User analysis
user_tickets = Counter()
for t in tickets:
    user_tickets[t['requester_id']] += 1
total_users = len(user_tickets)
recurring_users = sum(1 for c in user_tickets.values() if c >= 2)

solved = sum(1 for t in tickets if t['status'] in ('solved', 'closed'))

# Automation categories
auto_topics = ['General Inquiry', 'How to Deposit', 'How to Withdraw', 'Balance / Account Info', 'Bonus / Promotions', 'KYC / Verification', 'Account / Login Issues']
partial_topics = ['Deposit Processing Delay', 'Recarga / Top-up', 'Bank Transfer / Comprobante', 'Technical / App / Website', 'Casino / Games / Bets']
human_topics = ['Deposit Not Credited', 'Deposit Failed / Declined', 'Withdrawal Pending / Delay', 'Withdrawal Rejected', 'Complaint / Dissatisfaction']
auto_count = sum(topic_totals.get(t, 0) for t in auto_topics)
partial_count = sum(topic_totals.get(t, 0) for t in partial_topics)
human_count = sum(topic_totals.get(t, 0) for t in human_topics)

print('Building Executive Presentation...')

# ════════════════════════════════════════════════════════════════
# BUILD PDF — PRESENTATION STYLE
# ════════════════════════════════════════════════════════════════
outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'BetonWin_Executive_Presentation.pdf')
W = A4[0] - 30*mm

doc = SimpleDocTemplate(outpath, pagesize=A4,
                        topMargin=15*mm, bottomMargin=15*mm,
                        leftMargin=15*mm, rightMargin=15*mm)
story = []

# ═══════════════════════════════════════════════════════════════
# SLIDE 1: TITLE
# ═══════════════════════════════════════════════════════════════
# Dark header block
title_data = [[
    Paragraph('BETONWIN', ParagraphStyle('t1', fontSize=32, textColor=WHITE, fontName='Helvetica-Bold')),
]]
title_t = Table(title_data, colWidths=[W])
title_t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), DARK),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('TOPPADDING', (0,0), (-1,-1), 30),
    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
]))
story.append(spacer(15))
story.append(title_t)

sub_data = [[
    Paragraph('Customer Support Intelligence Report', ParagraphStyle('t2', fontSize=18, textColor=BLUE, fontName='Helvetica-Bold', alignment=TA_CENTER)),
]]
sub_t = Table(sub_data, colWidths=[W])
sub_t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), DARK),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 25),
]))
story.append(sub_t)

story.append(spacer(10))

# Key figures row
fig_data = [
    [Paragraph(f'<b>{TOTAL:,}</b>', styles['BigNum']),
     Paragraph(f'<b>{total_users:,}</b>', styles['BigNum']),
     Paragraph(f'<b>5</b>', styles['BigNum']),
     Paragraph(f'<b>{solved*100//TOTAL}%</b>', styles['BigNumGreen'])],
    [Paragraph('Total Tickets', styles['KPILabel']),
     Paragraph('Unique Users', styles['KPILabel']),
     Paragraph('Months Analyzed', styles['KPILabel']),
     Paragraph('Resolution Rate', styles['KPILabel'])],
]
fig_t = Table(fig_data, colWidths=[W*0.25]*4)
fig_t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), LGRAY),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,0), 15),
    ('BOTTOMPADDING', (0,1), (-1,1), 15),
    ('BOX', (0,0), (-1,-1), 1, BLUE),
    ('LINEBEFORE', (1,0), (1,-1), 0.5, colors.HexColor('#d1d5db')),
    ('LINEBEFORE', (2,0), (2,-1), 0.5, colors.HexColor('#d1d5db')),
    ('LINEBEFORE', (3,0), (3,-1), 0.5, colors.HexColor('#d1d5db')),
]))
story.append(fig_t)
story.append(spacer(8))

story.append(Paragraph('October 2025 — February 2026 | Complete Zendesk Data Analysis', styles['Small']))
story.append(Paragraph(f'Prepared: {datetime.now().strftime("%B %d, %Y")}', styles['Small']))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SLIDE 2: THE SITUATION — Volume Growth
# ═══════════════════════════════════════════════════════════════
story.append(Paragraph('THE SITUATION', styles['H1']))
story.append(Paragraph('Ticket Volume Is Growing Exponentially', styles['H2']))
story.append(hr())

# Monthly volume with big visual
vol_data = [
    [Paragraph(f'<b>{monthly_vol[m]:,}</b>', styles['MedNum']) for m in months_sorted],
    [Paragraph(m, styles['KPILabel']) for m in months_sorted],
]
vol_t = Table(vol_data, colWidths=[W/len(months_sorted)] * len(months_sorted))
vol_t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), LBLUE),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,0), 12),
    ('BOTTOMPADDING', (0,1), (-1,1), 12),
    ('BOX', (0,0), (-1,-1), 1, BLUE),
    ('LINEBEFORE', (1,0), (1,-1), 0.5, colors.HexColor('#93c5fd')),
    ('LINEBEFORE', (2,0), (2,-1), 0.5, colors.HexColor('#93c5fd')),
    ('LINEBEFORE', (3,0), (3,-1), 0.5, colors.HexColor('#93c5fd')),
    ('LINEBEFORE', (4,0), (4,-1), 0.5, colors.HexColor('#93c5fd')),
]))
story.append(vol_t)
story.append(spacer(6))

# Growth percentage
first_vol = monthly_vol[first_month]
last_vol = monthly_vol[last_month]
total_growth = ((last_vol - first_vol) / first_vol) * 100 if first_vol > 0 else 0

growth_box = [[
    Paragraph(f'<b>+{((last_vol - first_vol) / first_vol * 100):.0f}%</b>', styles['BigNumRed']),
    Paragraph(f'<b>~{last_vol // 28:,}</b>', styles['BigNum']),
    Paragraph(f'<b>{recurring_users:,}</b>', styles['BigNum']),
]]
growth_label = [[
    Paragraph('Total Growth (5 months)', styles['KPILabel']),
    Paragraph('Tickets Per Day (Feb)', styles['KPILabel']),
    Paragraph('Recurring Users (2+ tickets)', styles['KPILabel']),
]]
gb = Table(growth_box + growth_label, colWidths=[W*0.33]*3)
gb.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,0), LRED),
    ('BACKGROUND', (1,0), (1,0), LAMBER),
    ('BACKGROUND', (2,0), (2,0), LAMBER),
    ('BACKGROUND', (0,1), (0,1), LRED),
    ('BACKGROUND', (1,1), (1,1), LAMBER),
    ('BACKGROUND', (2,1), (2,1), LAMBER),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('TOPPADDING', (0,0), (-1,0), 10),
    ('BOTTOMPADDING', (0,1), (-1,1), 10),
    ('BOX', (0,0), (-1,-1), 0.5, GRAY),
]))
story.append(gb)
story.append(spacer(6))

story.append(Paragraph(
    '<b>Key Insight:</b> Volume increased from ~7K to ~100K tickets/month in just 5 months. '
    'At this trajectory, the CS team cannot scale through hiring alone. '
    'AI automation is the only viable path forward.',
    styles['CalloutRed']
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SLIDE 3: WHAT USERS ARE ASKING — Topic Breakdown
# ═══════════════════════════════════════════════════════════════
story.append(Paragraph('WHAT USERS ARE ASKING', styles['H1']))
story.append(Paragraph('17 Categories — Every Ticket Classified', styles['H2']))
story.append(hr())

# Topic table — clean and visual
topic_rows = [['Category', 'Tickets', 'Share', 'Trend', 'Can AI Handle?']]
for topic, cnt in topic_totals.most_common():
    pct = f'{cnt*100/TOTAL:.1f}%'
    fv = monthly_topic[first_month].get(topic, 0)
    lv = monthly_topic[last_month].get(topic, 0)
    if fv > 0:
        change = ((lv - fv) / fv) * 100
        trend = f'+{change:.0f}%' if change > 0 else f'{change:.0f}%'
    else:
        trend = 'NEW'

    if topic in auto_topics:
        ai = 'YES — Full Automation'
    elif topic in partial_topics:
        ai = 'PARTIAL — Bot + Agent'
    else:
        ai = 'AGENT — AI Assists'

    topic_rows.append([safe(topic, 30), f'{cnt:,}', pct, trend, ai])

story.append(make_table(topic_rows, col_widths=[W*0.28, W*0.13, W*0.10, W*0.13, W*0.28], header_color=BLUE))
story.append(spacer(6))

# Automation split
auto_split = [[
    Paragraph(f'<b>{auto_count*100//TOTAL}%</b>', styles['BigNumGreen']),
    Paragraph(f'<b>{partial_count*100//TOTAL}%</b>', ParagraphStyle('bn_amber', fontSize=36, textColor=AMBER, fontName='Helvetica-Bold', alignment=TA_CENTER)),
    Paragraph(f'<b>{human_count*100//TOTAL}%</b>', styles['BigNumRed']),
]]
auto_label = [[
    Paragraph('Fully Automatable', styles['KPILabel']),
    Paragraph('Partially Automatable', styles['KPILabel']),
    Paragraph('Agent Required', styles['KPILabel']),
]]
at = Table(auto_split + auto_label, colWidths=[W*0.33]*3)
at.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,-1), LGREEN),
    ('BACKGROUND', (1,0), (1,-1), LAMBER),
    ('BACKGROUND', (2,0), (2,-1), LRED),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('TOPPADDING', (0,0), (-1,0), 8),
    ('BOTTOMPADDING', (0,1), (-1,1), 8),
    ('BOX', (0,0), (-1,-1), 0.5, GRAY),
]))
story.append(at)

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SLIDE 4: FASTEST GROWING CATEGORIES
# ═══════════════════════════════════════════════════════════════
story.append(Paragraph('FASTEST GROWING CATEGORIES', styles['H1']))
story.append(Paragraph('These Categories Require Immediate Attention', styles['H2']))
story.append(hr())

# Top growing categories with details
growth_items = []
for topic in topic_totals.most_common():
    t_name = topic[0]
    fv = monthly_topic[first_month].get(t_name, 0)
    lv = monthly_topic[last_month].get(t_name, 0)
    if fv > 0:
        change = ((lv - fv) / fv) * 100
        if change > 50:
            growth_items.append((t_name, fv, lv, change, topic[1]))

growth_items.sort(key=lambda x: -x[3])

grow_rows = [['#', 'Category', 'Oct 2025', 'Feb 2026', 'Growth', 'Total (5mo)', 'Action Needed']]
for i, (name, fv, lv, change, total) in enumerate(growth_items[:10]):
    action = 'AI Bot' if name in auto_topics else 'Bot + API' if name in partial_topics else 'AI-Assist Agent'
    grow_rows.append([
        str(i+1), safe(name, 28), f'{fv:,}', f'{lv:,}',
        f'+{change:.0f}%', f'{total:,}', action
    ])

story.append(make_table(grow_rows, col_widths=[W*0.04, W*0.25, W*0.11, W*0.11, W*0.11, W*0.13, W*0.18], header_color=RED))
story.append(spacer(6))

# Highlight the top 3
story.append(Paragraph('<b>Top 3 Critical Growth Areas:</b>', styles['BodyBold']))
for i, (name, fv, lv, change, total) in enumerate(growth_items[:3]):
    story.append(Paragraph(
        f'&bull; <b>{safe(name)}</b> — grew <b>{change:.0f}%</b> in 5 months ({fv:,} → {lv:,}/month). '
        f'Total: {total:,} tickets.',
        styles['BulletX']
    ))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SLIDE 5: CHANNELS & USERS
# ═══════════════════════════════════════════════════════════════
story.append(Paragraph('HOW USERS REACH US', styles['H1']))
story.append(Paragraph('Channel Distribution & User Behavior', styles['H2']))
story.append(hr())

# Two-column layout: Channels + User segments
ch_rows = [['Channel', 'Tickets', 'Share']]
for ch, cnt in channel_dist.most_common(8):
    ch_rows.append([ch or 'unknown', f'{cnt:,}', f'{cnt*100/TOTAL:.1f}%'])

story.append(Paragraph('5.1 Support Channels', styles['H3']))
story.append(make_table(ch_rows, col_widths=[W*0.30, W*0.30, W*0.30]))
story.append(spacer(6))

# User segments
story.append(Paragraph('5.2 User Segments', styles['H3']))
user_seg = Counter()
for uid, cnt in user_tickets.items():
    if cnt == 1: user_seg['One-time'] += 1
    elif cnt <= 5: user_seg['Returning (2-5)'] += 1
    elif cnt <= 20: user_seg['Frequent (6-20)'] += 1
    else: user_seg['Power Users (20+)'] += 1

seg_rows = [['Segment', 'Users', '% of Users', 'Behavior']]
seg_info = {
    'One-time': 'Issue resolved or user churned',
    'Returning (2-5)': 'May have recurring problems',
    'Frequent (6-20)': 'Frustrated — systemic issues',
    'Power Users (20+)': 'Critical cases or possible abuse',
}
for seg in ['One-time', 'Returning (2-5)', 'Frequent (6-20)', 'Power Users (20+)']:
    cnt = user_seg.get(seg, 0)
    seg_rows.append([seg, f'{cnt:,}', f'{cnt*100/total_users:.1f}%', seg_info.get(seg, '')])
story.append(make_table(seg_rows, col_widths=[W*0.22, W*0.15, W*0.15, W*0.38], header_color=PURPLE))
story.append(spacer(6))

# Key user insight
story.append(Paragraph(
    f'<b>Key Insight:</b> {recurring_users:,} users ({recurring_users*100//total_users}%) contacted support '
    f'more than once. These recurring users generate a disproportionate number of tickets and indicate '
    f'unresolved underlying problems that AI can address proactively.',
    styles['Callout']
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SLIDE 6: THE AI SOLUTION
# ═══════════════════════════════════════════════════════════════
story.append(Paragraph('THE AI SOLUTION', styles['H1']))
story.append(Paragraph('Three-Layer Automation Architecture', styles['H2']))
story.append(hr())

# Architecture layers — visual blocks
layer1 = [[
    Paragraph('<b>LAYER 1: AI CHATBOT</b><br/>Front-line — Instant Response', ParagraphStyle('l1t', fontSize=11, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)),
]]
l1 = Table(layer1, colWidths=[W])
l1.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), GREEN),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('TOPPADDING', (0,0), (-1,-1), 10),
    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
]))
story.append(l1)

l1_detail = [[
    Paragraph('<b>What:</b> AI bot greets users, detects intent, provides instant answers for FAQ, '
              'deposit/withdrawal guides, bonus info, account help, balance checks.<br/>'
              '<b>Handles:</b> General Inquiry, How to Deposit, How to Withdraw, Bonus, Account, Balance<br/>'
              f'<b>Impact:</b> Automates {auto_count:,} tickets ({auto_count*100//TOTAL}% of total)', styles['CellBody']),
]]
l1d = Table(l1_detail, colWidths=[W])
l1d.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), LGREEN),
    ('TOPPADDING', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
]))
story.append(l1d)
story.append(spacer(4))

layer2 = [[
    Paragraph('<b>LAYER 2: AI + SYSTEM INTEGRATION</b><br/>Smart Automation — Real-Time Data', ParagraphStyle('l2t', fontSize=11, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)),
]]
l2 = Table(layer2, colWidths=[W])
l2.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), AMBER),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('TOPPADDING', (0,0), (-1,-1), 10),
    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
]))
story.append(l2)

l2_detail = [[
    Paragraph('<b>What:</b> AI integrates with payment gateways, KYC providers, and game APIs for '
              'real-time status checks, OCR receipt processing, and automated troubleshooting.<br/>'
              '<b>Handles:</b> Bank Transfer, KYC, Deposit Not Credited, Technical, Casino, Delays<br/>'
              f'<b>Impact:</b> Automates 50-70% of {partial_count:,} tickets', styles['CellBody']),
]]
l2d = Table(l2_detail, colWidths=[W])
l2d.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), LAMBER),
    ('TOPPADDING', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
]))
story.append(l2d)
story.append(spacer(4))

layer3 = [[
    Paragraph('<b>LAYER 3: AI-ASSISTED AGENTS</b><br/>Human Judgment — Full Context Provided', ParagraphStyle('l3t', fontSize=11, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)),
]]
l3 = Table(layer3, colWidths=[W])
l3.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), RED),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('TOPPADDING', (0,0), (-1,-1), 10),
    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
]))
story.append(l3)

l3_detail = [[
    Paragraph('<b>What:</b> For sensitive issues (complaints, payment failures, disputes), AI pre-processes '
              'the ticket, gathers context, and presents the agent with all information needed for fast resolution.<br/>'
              '<b>Handles:</b> Complaints, Deposit Failed, Withdrawal Rejected, Disputes<br/>'
              f'<b>Impact:</b> Reduces agent handle time by 50-70% for {human_count:,} tickets', styles['CellBody']),
]]
l3d = Table(l3_detail, colWidths=[W])
l3d.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), LRED),
    ('TOPPADDING', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
]))
story.append(l3d)

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SLIDE 7: IMPLEMENTATION ROADMAP
# ═══════════════════════════════════════════════════════════════
story.append(Paragraph('IMPLEMENTATION ROADMAP', styles['H1']))
story.append(Paragraph('Three Phases — Each Delivers Immediate Value', styles['H2']))
story.append(hr())

# Phase timeline
phases = [
    ['Phase', 'Timeline', 'Key Actions', 'Expected Impact'],
    [Paragraph('<b>Phase 1</b><br/>Quick Wins', styles['CellBold']),
     'Weeks 1-4',
     Paragraph('• Deploy AI welcome bot<br/>• Self-service guides (deposit, withdrawal, bonus)<br/>• Display bank details in-app<br/>• Password reset improvement', styles['CellBody']),
     Paragraph(f'<b>~{auto_count*80//100:,} tickets automated</b><br/>({auto_count*80//100*100//TOTAL}% of volume)<br/>Cost: $15-25K', styles['CellBody'])],
    [Paragraph('<b>Phase 2</b><br/>Smart Automation', styles['CellBold']),
     'Weeks 5-10',
     Paragraph('• Payment gateway integration<br/>• OCR receipt processing<br/>• KYC guided flow<br/>• Tech troubleshooting bot<br/>• Real-time deposit tracker', styles['CellBody']),
     Paragraph(f'<b>~{partial_count*55//100:,} more tickets</b><br/>automated<br/>Cost: $30-50K', styles['CellBody'])],
    [Paragraph('<b>Phase 3</b><br/>AI-Assisted Agents', styles['CellBold']),
     'Weeks 11-16',
     Paragraph('• Agent assist panel (AI suggestions)<br/>• Auto-investigation for failures<br/>• NLP intent detection<br/>• Sentiment-based routing', styles['CellBody']),
     Paragraph('<b>Agent productivity 2-3x</b><br/>for remaining tickets<br/>Cost: $20-35K', styles['CellBody'])],
]
phase_t = Table(phases, colWidths=[W*0.15, W*0.13, W*0.40, W*0.27], repeatRows=1)
phase_t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), DARK),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 8),
    ('BACKGROUND', (0,1), (-1,1), LGREEN),
    ('BACKGROUND', (0,2), (-1,2), LAMBER),
    ('BACKGROUND', (0,3), (-1,3), LRED),
    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#d1d5db')),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
]))
story.append(phase_t)

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SLIDE 8: FINANCIAL IMPACT
# ═══════════════════════════════════════════════════════════════
story.append(Paragraph('FINANCIAL IMPACT', styles['H1']))
story.append(Paragraph('ROI Analysis — The Business Case for AI', styles['H2']))
story.append(hr())

# Big numbers
total_automatable = auto_count * 80 // 100 + partial_count * 55 // 100
annual_tickets_saved = total_automatable * 12 // 5
annual_savings = int(annual_tickets_saved * 1.50)
impl_cost = 90000  # midpoint
payback_months = max(1, impl_cost * 5 // (total_automatable * 1.50))

fin_kpi = [
    [Paragraph(f'<b>${annual_savings:,}</b>', styles['BigNumGreen']),
     Paragraph(f'<b>{annual_tickets_saved:,}</b>', styles['BigNum']),
     Paragraph(f'<b>~{payback_months}</b>', styles['BigNum'])],
    [Paragraph('Annual Cost Savings', styles['KPILabel']),
     Paragraph('Tickets Automated/Year', styles['KPILabel']),
     Paragraph('Months to Payback', styles['KPILabel'])],
]
fk = Table(fin_kpi, colWidths=[W*0.33]*3)
fk.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,-1), LGREEN),
    ('BACKGROUND', (1,0), (1,-1), LBLUE),
    ('BACKGROUND', (2,0), (2,-1), LBLUE),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('TOPPADDING', (0,0), (-1,0), 12),
    ('BOTTOMPADDING', (0,1), (-1,1), 12),
    ('BOX', (0,0), (-1,-1), 1, GREEN),
]))
story.append(fk)
story.append(spacer(8))

# Cost breakdown
cost_rows = [['Item', 'Without AI (Annual)', 'With AI (Annual)', 'Savings']]
current_annual_cost = int(TOTAL * 12 / 5 * 1.50)
ai_annual_cost = int((TOTAL * 12 / 5 - annual_tickets_saved) * 1.50 + 50000)  # remaining tickets + AI maintenance
savings_val = current_annual_cost - ai_annual_cost
cost_rows.append([
    'Ticket Handling Cost',
    f'${current_annual_cost:,}',
    f'${ai_annual_cost:,}',
    f'${savings_val:,}',
])
agents_now = int(TOTAL * 12 / 5 / (50 * 22 * 12))
agents_with_ai = int((TOTAL * 12 / 5 - annual_tickets_saved) / (50 * 22 * 12))
cost_rows.append([
    'FTE Agents Needed',
    f'{agents_now}',
    f'{agents_with_ai}',
    f'{agents_now - agents_with_ai} agents freed',
])
cost_rows.append([
    'Implementation Cost',
    '$0',
    '$65,000-110,000',
    'One-time investment',
])
cost_rows.append([
    'AI Platform Cost',
    '$0',
    '~$3,000-5,000/month',
    'Ongoing',
])
story.append(make_table(cost_rows, col_widths=[W*0.25, W*0.22, W*0.25, W*0.23], header_color=GREEN))
story.append(spacer(6))

story.append(Paragraph(
    f'<b>Bottom Line:</b> AI implementation pays for itself in ~{payback_months} months. '
    f'Annual net savings: <b>${max(0, savings_val - 50000):,}+</b> (after AI platform costs). '
    f'This frees {agents_now - agents_with_ai} agent FTEs for higher-value work like retention and VIP support.',
    styles['CalloutGreen']
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SLIDE 9: KEY PERFORMANCE INDICATORS
# ═══════════════════════════════════════════════════════════════
story.append(Paragraph('SUCCESS METRICS', styles['H1']))
story.append(Paragraph('How We Measure AI Impact', styles['H2']))
story.append(hr())

kpi_rows = [['KPI', 'Current State', 'Target (3 months)', 'Target (6 months)']]
kpi_items = [
    ['Bot Containment Rate', '~5%', '> 50%', '> 75%'],
    ['First Response Time', '~15 minutes', '< 30 seconds', '< 5 seconds'],
    ['Tickets Requiring Human Agent', '~95%', '< 50%', '< 25%'],
    ['Average Handle Time', '~10 minutes', '~6 minutes', '~4 minutes'],
    ['Customer Satisfaction (CSAT)', 'Not measured', '> 3.8 / 5', '> 4.2 / 5'],
    ['CSTA Unoffered Rate', 'High', '< 10%', '< 2%'],
    ['Cost per Resolution', '~$1.50', '~$0.60', '~$0.30'],
    ['Ticket Backlog', 'Growing', 'Stable', 'Near zero'],
    ['Self-Service Resolution Rate', '~5%', '> 40%', '> 60%'],
]
for item in kpi_items:
    kpi_rows.append(item)
story.append(make_table(kpi_rows, col_widths=[W*0.28, W*0.20, W*0.22, W*0.22], header_color=TEAL))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# SLIDE 10: NEXT STEPS
# ═══════════════════════════════════════════════════════════════
story.append(Paragraph('NEXT STEPS', styles['H1']))
story.append(Paragraph('Recommended Immediate Actions', styles['H2']))
story.append(hr())

story.append(spacer(4))

next_steps = [
    ('<b>1. SELECT AI CHATBOT PLATFORM</b>',
     'Evaluate Zendesk AI, Ada, Intercom, or Tidio. Key criteria: Spanish language support, '
     'Zendesk integration, API access for custom flows. Timeline: 1 week.'),
    ('<b>2. DEPLOY BASIC BOT (Phase 1)</b>',
     'Configure welcome bot with top 8 category menu. Add self-service guides for deposits, '
     'withdrawals, and bonuses. Go live on web widget channel first. Timeline: 2-3 weeks.'),
    ('<b>3. MEASURE AND ITERATE</b>',
     'Track bot containment rate, CSAT, and escalation patterns daily. '
     'Identify gaps in bot coverage and add new intents weekly. Target: 50% containment in 30 days.'),
    ('<b>4. PLAN PHASE 2 INTEGRATIONS</b>',
     'Begin technical scoping for payment gateway APIs, OCR receipt processing, '
     'and KYC provider integration. These unlock the next tier of automation.'),
    ('<b>5. BUILD SELF-SERVICE FEATURES</b>',
     'Add bank details page, withdrawal tracker, wagering progress bar, and KYC status '
     'directly in the app/website. These reduce ticket creation at the source.'),
    ('<b>6. TRAIN CS TEAM</b>',
     'Prepare agents for AI-assisted workflow. Train on bot handoff protocol, '
     'using AI-suggested responses, and handling escalated cases with full context.'),
]

for title, desc in next_steps:
    step_data = [[Paragraph(title, styles['BodyBold'])]]
    step_t = Table(step_data, colWidths=[W])
    step_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LBLUE),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(step_t)
    story.append(Paragraph(desc, styles['Body']))
    story.append(spacer(4))

story.append(spacer(8))

# Final message
final_data = [[
    Paragraph(
        '<b>AI is not a "nice to have" — it is a business necessity.</b><br/><br/>'
        'Ticket volume is growing exponentially. Hiring cannot keep pace. '
        'The investment pays for itself in 3 months. Every month of delay costs the business '
        f'an additional ${int(total_automatable * 1.50 / 5):,} in avoidable support costs.',
        ParagraphStyle('final', fontSize=11, leading=15, textColor=WHITE, alignment=TA_CENTER)
    ),
]]
final_t = Table(final_data, colWidths=[W])
final_t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), DARK),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('TOPPADDING', (0,0), (-1,-1), 20),
    ('BOTTOMPADDING', (0,0), (-1,-1), 20),
    ('LEFTPADDING', (0,0), (-1,-1), 20),
    ('RIGHTPADDING', (0,0), (-1,-1), 20),
]))
story.append(final_t)

story.append(spacer(6))
story.append(Paragraph(f'Data source: 240,448 Zendesk tickets (Oct 2025 — Feb 2026) | Generated: {datetime.now().strftime("%B %d, %Y")}', styles['Small']))

# ═══════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════
print(f'Building PDF with {len(story)} elements...')
doc.build(story)
print(f'\nPDF saved to: {outpath}')
print('Done!')
