#!/usr/bin/env python3
"""
Deep analysis of 'General Inquiry' tickets — BetonWin January 2026
Standalone script — does NOT import from zendesk_analysis.py
"""

import os, requests, time, re
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv('zendesk.env')
AUTH = (f'{os.getenv("ZENDESK_EMAIL")}/token', os.getenv('ZENDESK_API_TOKEN'))
BASE = 'https://betonwin.zendesk.com/api/v2'

def get_json(url, retries=4):
    for attempt in range(retries):
        try:
            r = requests.get(url, auth=AUTH, timeout=30)
            if r.status_code == 429:
                time.sleep(int(r.headers.get('Retry-After', 15)))
                continue
            if r.status_code == 422:
                return None
            r.raise_for_status()
            return r.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            time.sleep(5 * (attempt + 1))
    return None

def extract_user_text(text):
    lines = re.findall(r'\(\d{2}:\d{2}:\d{2}\)\s+([^:]+):\s+(.+?)(?=\s*\(\d{2}:\d{2}:\d{2}\)|$)',
                       text or '', re.DOTALL)
    user_lines = [msg for name, msg in lines if name.strip().upper() not in ('BOW', 'BOW ')]
    return ' '.join(user_lines) if user_lines else text

# ── TOPIC PATTERNS (detailed for General Inquiry breakdown) ──────────────────
TOPIC_PATTERNS = {
    'Deposit Not Received / Not Credited': [
        'no se reflejo','no se acredito','no se me acredito','no me acredito',
        'no aparece','no lo veo','no figura','no se ve','no fue acreditado',
        'hice una transferencia y no','realice un deposito y no','transferi y no',
        'recarga exitosa pero','exitoso pero no','saldo no cambio','no cambio el saldo',
        'no recibido','no llegó','no llego','no recibí','no recibi',
        'not received','not credited','not arrived','deposit missing',
        'non ricevuto','non arrivato','non accreditato',
        'não recebi','não chegou','não foi creditado',
        'deposite y no','hice un deposito y no','deposité y no',
        'hice una recarga y no','ya pagué y no','pagué y no','pague y no',
        'no veo el saldo','no tengo el saldo','no me aparece',
        'realicé un pago','hice el pago y no',
    ],
    'How to Deposit / Recharge': [
        'cómo depositar','como depositar','cómo deposito','como deposito',
        'cómo cargo','como cargo','como puedo cargar','cómo puedo depositar',
        'quiero cargar','quiero depositar','cómo recargo','como recargo',
        'donde puedo depositar','qué métodos','que metodos de pago',
        'puedo depositar con','acepta','aceptan','formas de pago',
        'como hago para depositar','cómo hago para depositar',
        'how to deposit','come depositare','como depositar',
    ],
    'Recarga / Top-up Issues': [
        'recarga','recargar','carga saldo','cargar saldo','cargar cuenta',
        'recarga no','recarga exitosa','hice una recarga','mi recarga',
        'top up','topup','ricarica','recargué','recarge',
    ],
    'Withdrawal / Payout': [
        'retirar','retiro','quiero sacar','como saco','cómo saco',
        'quiero cobrar','como cobro','cómo cobro','quiero retirar',
        'puedo retirar','cuándo me pagan','cuando me pagan',
        'mis ganancias','cuánto puedo retirar','como retiro',
        'cómo retiro','método de retiro','cobrar mi dinero',
        'sacar mi plata','retirar mi plata','prelievo','saque',
        'withdrawal','withdraw',
    ],
    'Bonus / Promotions': [
        'bono','bonos','promocion','promoción','promos','bonus',
        'free bet','freespin','regalo','oferta','código promo',
        'cómo uso el bono','como uso el bono','activar',
        'cashback','giros gratis','tiradas',
    ],
    'Account / Login': [
        'no puedo entrar','no puedo ingresar','olvidé','olvidé mi','mi contraseña',
        'recuperar contraseña','no recuerdo','acceder','acceso','ingresar',
        'cuenta bloqueada','me bloqueo','no me deja entrar','suspendida',
        'login','password','contraseña','entrar a mi cuenta','crear cuenta',
        'abrir cuenta','registrarme','nueva cuenta','verificar mi cuenta',
    ],
    'Transfer / Bank / Comprobante': [
        'transferencia','banco','cuenta bancaria','cuenta de banco',
        'comprobante','voucher','recibo','número de cuenta','nro de cuenta',
        'clabe','cvú','cbu','iban','cuenta corriente',
        'envié comprobante','mandé el comprobante','adjunto comprobante',
    ],
    'Game / Casino / Bet': [
        'juego','juegos','apuesta','apuestas','slot','partida','no carga el juego',
        'error en el juego','resultado','mi apuesta','ganancia','gané','perdí',
        'casino','live','mesa','tragamonedas','apostar','scommessa',
    ],
    'Technical / App / Website': [
        'no funciona','no abre','error','no carga','se cierra',
        'app','aplicación','celular','teléfono','android','iphone',
        'página','sitio','pantalla','se traba','problema técnico',
    ],
    'KYC / Verification / Documents': [
        'verificar','verificación','verificacion','documento','dni','pasaporte',
        'validar','selfie','foto','comprobante domicilio',
        'identidad','kyc','cedula','cédula',
    ],
    'Greeting / General Chat': [
        'hola','buenas','buen día','buenos días','buenas tardes','buenas noches',
    ],
    'Complaint / Dissatisfaction': [
        'queja','reclamo','no es justo','me robaron','estafados',
        'pésimo','muy malo','terrible','fraude','robo','estafa',
        'quiero quejarme','quiero hacer un reclamo','inaceptable',
    ],
    'Balance / Account Info': [
        'mi saldo','cuál es mi saldo','saldo disponible','cuanto tengo',
        'mi cuenta','datos de mi cuenta','información de cuenta',
        'balance','my balance','mis datos',
    ],
}

# ── FETCH ─────────────────────────────────────────────────────────────────────
print('=' * 58)
print('  Deep Analysis: "General Inquiry" Tickets')
print('  January 2026')
print('=' * 58)

print('\nFetching tickets...')
weeks = [
    ('2026-01-01T00:00:00Z', '2026-01-08T00:00:00Z'),
    ('2026-01-08T00:00:00Z', '2026-01-15T00:00:00Z'),
    ('2026-01-15T00:00:00Z', '2026-01-22T00:00:00Z'),
    ('2026-01-22T00:00:00Z', '2026-02-01T00:00:00Z'),
]

all_tickets, seen = [], set()
for ws, we in weeks:
    url = f'{BASE}/search.json?query=type:ticket+created>{ws}+created<{we}&sort_by=created_at&sort_order=asc&per_page=100'
    while url:
        data = get_json(url)
        if not data: break
        all_tickets.extend(t for t in data.get('results',[]) if t['id'] not in seen)
        seen.update(t['id'] for t in data.get('results',[]))
        url = data.get('next_page')
    print(f'  {ws[:10]}: {len(all_tickets)} total')

print(f'Total: {len(all_tickets)}\n')

# Fetch ALL comments and classify
print('Fetching comments + classifying...')
topic_counts   = defaultdict(int)
topic_tickets  = defaultdict(list)
classified     = 0
general_total  = 0

for i, t in enumerate(all_tickets):
    subject = t.get('subject','') or ''
    desc    = t.get('description','') or ''

    data = get_json(f'{BASE}/tickets/{t["id"]}/comments.json')
    comments = data.get('comments', []) if data else []
    comment_text = ' '.join(c.get('body','') or '' for c in comments)

    full_text = subject + ' ' + desc + ' ' + comment_text
    user_text = extract_user_text(full_text)
    text      = (user_text + ' ' + user_text + ' ' + full_text).lower()

    # Find best topic
    best_topic, best_score = None, 0
    for topic, patterns in TOPIC_PATTERNS.items():
        score = sum(1 for p in patterns if p in text)
        if score > best_score:
            best_score, best_topic = score, topic

    if not best_topic:
        best_topic = 'Uncategorized'

    topic_counts[best_topic] += 1
    if len(topic_tickets[best_topic]) < 8:  # Keep max 8 samples
        topic_tickets[best_topic].append({
            'id': t['id'],
            'subject': subject[:70],
            'user_msg': user_text[:200].replace('\n',' '),
        })

    if (i+1) % 100 == 0:
        print(f'  {i+1}/{len(all_tickets)} processed...')
    time.sleep(0.05)

print(f'\nDone. All {len(all_tickets)} tickets classified into {len(topic_counts)} topics.\n')

# Print summary to console
topic_sorted = dict(sorted(topic_counts.items(), key=lambda x: -x[1]))
for topic, cnt in topic_sorted.items():
    pct = round(cnt / len(all_tickets) * 100, 1)
    print(f'  {cnt:>5} ({pct:>5.1f}%)  {topic}')

# ── PDF ───────────────────────────────────────────────────────────────────────
print('\nGenerating PDF...')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                Table, TableStyle, HRFlowable, PageBreak)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER

GREEN = colors.HexColor('#39d353')
DARK  = colors.HexColor('#0f1623')
GRAY  = colors.HexColor('#8892a4')
LGRAY = colors.HexColor('#f5f5f5')

def sty(n,**k): return ParagraphStyle(n,**k)
title_s = sty('t',  fontSize=18, textColor=DARK, fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=3)
sub_s   = sty('s',  fontSize=10, textColor=GRAY, alignment=TA_CENTER)
h2_s    = sty('h2', fontSize=13, textColor=DARK, fontName='Helvetica-Bold', spaceBefore=12, spaceAfter=5)
h3_s    = sty('h3', fontSize=10, textColor=colors.HexColor('#1a4731'), fontName='Helvetica-Bold', spaceBefore=6, spaceAfter=3)
body_s  = sty('b',  fontSize=9,  textColor=colors.HexColor('#333'), leading=14)
cap_s   = sty('c',  fontSize=8,  textColor=GRAY, alignment=TA_CENTER)
kv_s    = sty('kv', fontSize=22, textColor=GREEN, fontName='Helvetica-Bold', alignment=TA_CENTER)
kl_s    = sty('kl', fontSize=8,  textColor=GRAY, alignment=TA_CENTER)

def bar_h(data, title, color='#39d353', figsize=(7,5)):
    fig, ax = plt.subplots(figsize=figsize)
    labels, vals = list(data.keys()), list(data.values())
    bars = ax.barh(labels, vals, color=color, edgecolor='white', linewidth=0.4)
    ax.set_xlabel('Tickets', fontsize=8)
    ax.set_title(title, fontsize=10, fontweight='bold', pad=6)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    ax.tick_params(labelsize=7)
    for bar, v in zip(bars, vals):
        pct = round(v/len(all_tickets)*100,1)
        ax.text(v+2, bar.get_y()+bar.get_height()/2, f'{v} ({pct}%)', va='center', fontsize=7)
    plt.tight_layout()
    buf = io.BytesIO(); fig.savefig(buf, format='png', dpi=140, bbox_inches='tight')
    plt.close(fig); buf.seek(0); return buf

def pie_c(data, title, figsize=(6,5)):
    palette = ['#39d353','#2aa644','#4ade6e','#22c55e','#86efac','#bbf7d0','#a3e635',
               '#dcfce7','#f0fdf4','#d1fae5','#6ee7b7','#34d399','#fbbf24','#f87171']
    fig, ax = plt.subplots(figsize=figsize)
    labels = [f'{k} ({v})' for k,v in data.items()]
    ax.pie(list(data.values()), labels=labels, colors=palette[:len(data)],
           autopct='%1.0f%%', startangle=140, textprops={'fontsize': 6.5})
    ax.set_title(title, fontsize=10, fontweight='bold', pad=5)
    plt.tight_layout()
    buf = io.BytesIO(); fig.savefig(buf, format='png', dpi=140, bbox_inches='tight')
    plt.close(fig); buf.seek(0); return buf

doc   = SimpleDocTemplate('zendesk_deep_general.pdf', pagesize=A4,
                          leftMargin=1.8*cm, rightMargin=1.8*cm,
                          topMargin=1.8*cm, bottomMargin=1.8*cm)
story = []

# Page 1
story.append(Paragraph('BetonWin — Deep Topic Analysis', title_s))
story.append(Paragraph(f'All {len(all_tickets)} tickets · January 2026 · Classified by actual content', sub_s))
story.append(HRFlowable(width='100%', thickness=2, color=GREEN, spaceAfter=12))

# KPI
non_greeting = sum(v for k,v in topic_counts.items() if k not in ('Greeting / General Chat','Uncategorized'))
kpi = [[
    Paragraph(str(len(all_tickets)), kv_s),
    Paragraph(str(len(topic_counts)), kv_s),
    Paragraph(str(non_greeting), kv_s),
    Paragraph(str(topic_counts.get('Uncategorized',0)), kv_s),
],[
    Paragraph('Total Tickets', kl_s),
    Paragraph('Topics Found', kl_s),
    Paragraph('Actionable', kl_s),
    Paragraph('Uncategorized', kl_s),
]]
kt = Table(kpi, colWidths=[4*cm]*4)
kt.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,-1),LGRAY),('BOX',(0,0),(-1,-1),0.5,GRAY),
    ('INNERGRID',(0,0),(-1,-1),0.3,GRAY),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),12),
]))
story.append(kt)
story.append(Spacer(1,14))

# Bar chart
story.append(Image(bar_h(topic_sorted, f'Topic Distribution — {len(all_tickets)} tickets'),
                   width=15*cm, height=10*cm))

# Page 2 — Pie
story.append(PageBreak())
story.append(Paragraph('Topic Share', h2_s))
story.append(Image(pie_c(topic_sorted, 'Proportion of Each Topic'), width=14*cm, height=11*cm))

# Page 3 — Summary table
story.append(PageBreak())
story.append(Paragraph('Topic Summary Table', h2_s))
rows = [['Topic', 'Tickets', '% of Total']]
for topic, cnt in topic_sorted.items():
    rows.append([topic, str(cnt), f'{round(cnt/len(all_tickets)*100,1)}%'])
tbl = Table(rows, colWidths=[8.5*cm, 2.5*cm, 3*cm])
tbl.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0),DARK),('TEXTCOLOR',(0,0),(-1,0),colors.white),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),9),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,LGRAY]),
    ('GRID',(0,0),(-1,-1),0.3,GRAY),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('ALIGN',(1,0),(-1,-1),'CENTER'),
]))
story.append(tbl)

# Pages 4+ — Per-topic samples
story.append(PageBreak())
story.append(Paragraph('Topic Detail with Sample Messages', h2_s))
story.append(HRFlowable(width='100%', thickness=1, color=GREEN, spaceAfter=8))

for topic, cnt in topic_sorted.items():
    pct = round(cnt / len(all_tickets) * 100, 1)
    story.append(Paragraph(f'{topic} — {cnt} tickets ({pct}%)', h3_s))

    samples = topic_tickets[topic][:5]
    sr = [['ID', 'User Message Sample']]
    for s in samples:
        msg = s['user_msg'][:130] if s['user_msg'].strip() else s['subject'][:130]
        sr.append([str(s['id']), msg])
    st = Table(sr, colWidths=[1.5*cm, 14*cm])
    st.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),DARK),('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),7),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,LGRAY]),
        ('GRID',(0,0),(-1,-1),0.3,GRAY),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
    ]))
    story.append(st)
    story.append(Spacer(1,6))

# Recommendations
story.append(PageBreak())
story.append(HRFlowable(width='100%', thickness=2, color=GREEN, spaceAfter=8))
story.append(Paragraph('Key Findings & Recommendations', h2_s))

top5 = list(topic_sorted.items())[:5]
findings = [
    f'<b>#1 Issue:</b> "{top5[0][0]}" — {top5[0][1]} tickets ({round(top5[0][1]/len(all_tickets)*100,1)}%). This is the top automation candidate for the AI widget.',
    f'<b>#2 Issue:</b> "{top5[1][0]}" — {top5[1][1]} tickets ({round(top5[1][1]/len(all_tickets)*100,1)}%).',
    f'<b>#3 Issue:</b> "{top5[2][0]}" — {top5[2][1]} tickets ({round(top5[2][1]/len(all_tickets)*100,1)}%).',
    f'<b>Automatable by AI Widget:</b> {top5[0][0]}, {top5[1][0]}, {top5[2][0]} — together represent {round(sum(x[1] for x in top5[:3])/len(all_tickets)*100)}% of all tickets.',
    f'<b>Uncategorized:</b> {topic_counts.get("Uncategorized",0)} tickets may need manual review or more keyword patterns.',
    f'<b>Volume:</b> {len(all_tickets)} tickets/month = ~{round(len(all_tickets)/31)} tickets/day average.',
]
for f in findings:
    story.append(Paragraph(f'• {f}', body_s))
    story.append(Spacer(1,5))

from datetime import datetime
story.append(Spacer(1,12))
story.append(Paragraph(f'Generated {datetime.now().strftime("%d %b %Y %H:%M")} · BetonWin Zendesk · {len(all_tickets)} tickets analyzed', cap_s))

doc.build(story)
print(f'\n✅ Report saved: zendesk_deep_general.pdf')
