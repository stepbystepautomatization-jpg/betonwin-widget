#!/usr/bin/env python3
"""
BetonWin — Comprehensive Zendesk Analysis
January 2026: All tickets + comments, detailed topics, daily trends,
cross-analysis, sample messages, actionable recommendations.
"""

import os, requests, time, re
from datetime import datetime, timezone
from collections import defaultdict, Counter
from dotenv import load_dotenv

load_dotenv('zendesk.env')
AUTH = (f'{os.getenv("ZENDESK_EMAIL")}/token', os.getenv('ZENDESK_API_TOKEN'))
BASE = 'https://betonwin.zendesk.com/api/v2'

# ── API HELPERS ──────────────────────────────────────────────────────────────
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
    lines = re.findall(
        r'\(\d{2}:\d{2}:\d{2}\)\s+([^:]+):\s+(.+?)(?=\s*\(\d{2}:\d{2}:\d{2}\)|$)',
        text or '', re.DOTALL)
    user_lines = [msg.strip() for name, msg in lines if name.strip().upper() not in ('BOW', 'BOW ')]
    return ' '.join(user_lines) if user_lines else (text or '')

# ── DETAILED TOPIC TAXONOMY ─────────────────────────────────────────────────
TOPICS = {
    'Deposit Not Credited': [
        'no se reflejo','no se acredito','no se me acredito','no me acredito',
        'no aparece','no lo veo','no figura','no se ve','no fue acreditado',
        'hice una transferencia y no','realice un deposito y no','transferi y no',
        'recarga exitosa pero','exitoso pero no','saldo no cambio','no cambio el saldo',
        'no recibido','no llego','no recibi','deposite y no','hice un deposito y no',
        'hice una recarga y no','ya pague y no','pague y no','no veo el saldo',
        'hice el pago y no','realice un pago','not received','not credited',
        'deposit missing','not reflected','balance not updated',
        'non ricevuto','non arrivato','non accreditato',
        'nao recebi','nao chegou','nao foi creditado',
    ],
    'How to Deposit': [
        'como depositar','como deposito','como cargo','como puedo cargar',
        'quiero depositar','quiero cargar','como recargo','donde puedo depositar',
        'que metodos','formas de pago','como hago para depositar','puedo depositar con',
        'acepta','aceptan','how to deposit','come depositare','metodo deposito',
        'metodo de pago','monto minimo','cuanto es el minimo',
    ],
    'Deposit Failed / Declined': [
        'failed','fallido','rechazado','error al depositar','error de pago',
        'no se proceso','transaccion fallida','payment failed','transaction failed',
        'non e andato','non e riuscito','nao processado','declined','declinado',
    ],
    'Deposit Processing Delay': [
        'cuanto tarda','esperando deposito','en espera','pending deposit',
        'demora deposito','tarda mucho','lleva mucho tiempo','still processing',
        'quanto tempo deposito','waiting for deposit',
    ],
    'Recarga / Top-up': [
        'recarga','recargar','carga saldo','cargar saldo','cargar cuenta',
        'hice una recarga','mi recarga','recargue','recarge',
        'top up','topup','ricarica',
    ],
    'Withdrawal Not Received': [
        'retiro no recibido','no recibi el retiro','no llego el retiro',
        'donde esta mi retiro','withdrawal not received','withdrawal missing',
        'prelievo non ricevuto','saque nao recebido',
    ],
    'How to Withdraw': [
        'como retirar','como retiro','quiero retirar','quiero sacar',
        'como saco','quiero cobrar','como cobro','puedo retirar',
        'metodo de retiro','cobrar mi dinero','sacar mi plata','retirar mi plata',
        'how to withdraw','come prelevare','withdrawal method',
    ],
    'Withdrawal Pending / Delay': [
        'retiro pendiente','retiro demora','retiro tarda','esperando retiro',
        'en proceso retiro','cuanto tarda retiro','withdrawal pending',
        'prelievo in attesa','saque pendente',
    ],
    'Withdrawal Rejected': [
        'retiro rechazado','no me dejan retirar','no puedo retirar',
        'withdrawal rejected','withdrawal denied','prelievo rifiutato',
        'saque recusado','cannot withdraw',
    ],
    'Bonus / Promotions': [
        'bono','bonos','promocion','promos','bonus','free bet','freespin',
        'regalo','oferta','codigo promo','como uso el bono','activar',
        'cashback','giros gratis','tiradas','bono bienvenida','welcome bonus',
        'primer deposito bonus','rollover','wagering',
    ],
    'Account / Login Issues': [
        'no puedo entrar','no puedo ingresar','olvide mi','mi contrasena',
        'recuperar contrasena','no recuerdo','acceder','acceso','ingresar',
        'cuenta bloqueada','me bloqueo','no me deja entrar','suspendida',
        'login','password','contrasena','entrar a mi cuenta','crear cuenta',
        'abrir cuenta','registrarme','nueva cuenta','account blocked',
        'cannot login','forgot password',
    ],
    'Bank Transfer / Comprobante': [
        'transferencia','banco','cuenta bancaria','cuenta de banco',
        'comprobante','voucher','recibo','numero de cuenta','clabe',
        'cvu','cbu','iban','cuenta corriente','envie comprobante',
        'mande el comprobante','adjunto comprobante','bonifico',
        'transferencia bancaria',
    ],
    'Casino / Games / Bets': [
        'juego','juegos','apuesta','apuestas','slot','partida','no carga el juego',
        'error en el juego','resultado','mi apuesta','ganancia','gane','perdi',
        'casino','live','mesa','tragamonedas','apostar','scommessa',
        'jackpot','vincita','ganancias','winnings',
    ],
    'Technical / App / Website': [
        'no funciona','no abre','error','no carga','se cierra',
        'app','aplicacion','celular','telefono','android','iphone',
        'pagina','sitio','pantalla','se traba','problema tecnico',
        'website down','app crash','not loading',
    ],
    'KYC / Verification': [
        'verificar','verificacion','documento','dni','pasaporte',
        'validar','selfie','foto','comprobante domicilio',
        'identidad','kyc','cedula','identity verification',
    ],
    'Complaint / Dissatisfaction': [
        'queja','reclamo','no es justo','me robaron','estafados',
        'pesimo','muy malo','terrible','fraude','robo','estafa',
        'quiero quejarme','quiero hacer un reclamo','inaceptable',
    ],
    'Balance / Account Info': [
        'mi saldo','cual es mi saldo','saldo disponible','cuanto tengo',
        'mi cuenta','datos de mi cuenta','informacion de cuenta',
        'balance','my balance','mis datos',
    ],
    'Greeting Only (no question)': [
        'hola','buenas','buen dia','buenos dias','buenas tardes','buenas noches',
    ],
}

# Macro-categories for grouping
MACRO = {
    'DEPOSITS': ['Deposit Not Credited','How to Deposit','Deposit Failed / Declined',
                 'Deposit Processing Delay','Recarga / Top-up'],
    'WITHDRAWALS': ['Withdrawal Not Received','How to Withdraw',
                    'Withdrawal Pending / Delay','Withdrawal Rejected'],
    'BONUS': ['Bonus / Promotions'],
    'ACCOUNT': ['Account / Login Issues'],
    'PAYMENTS': ['Bank Transfer / Comprobante'],
    'GAMES': ['Casino / Games / Bets'],
    'TECHNICAL': ['Technical / App / Website'],
    'KYC': ['KYC / Verification'],
    'COMPLAINTS': ['Complaint / Dissatisfaction'],
    'INFO': ['Balance / Account Info'],
    'GREETINGS': ['Greeting Only (no question)'],
}

LANG_KW = {
    'Spanish':    ['hola','gracias','por favor','ayuda','no puedo','tengo','deposito',
                   'retiro','cuenta','bono','quiero','necesito','estoy'],
    'Italian':    ['ciao','grazie','per favore','aiuto','non riesco','prelievo',
                   'problema','salve','buongiorno','vorrei','mio conto'],
    'Portuguese': ['ola','obrigado','ajuda','nao consigo','saque',
                   'preciso','quero','minha','nao recebi'],
    'English':    ['hello','hi','please','help','cannot','deposit','withdraw','account',
                   'need','want','issue','problem','not received'],
}

def detect_lang(text):
    t = (text or '').lower()
    scores = {l: sum(1 for w in ws if w in t) for l, ws in LANG_KW.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else 'Unknown'

def classify(text):
    t = text.lower()
    best_topic, best_score = 'Uncategorized', 0
    for topic, kws in TOPICS.items():
        score = sum(1 for kw in kws if kw in t)
        if score > best_score:
            best_score, best_topic = score, topic
    return best_topic

# ── FETCH ALL TICKETS ────────────────────────────────────────────────────────
print('=' * 60)
print('  BetonWin — Comprehensive Ticket Analysis')
print('  January 2026')
print('=' * 60)

print('\nFetching tickets (week by week)...')
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
        for t in data.get('results', []):
            if t['id'] not in seen:
                all_tickets.append(t)
                seen.add(t['id'])
        url = data.get('next_page')
    print(f'  {ws[:10]}: {len(all_tickets)} total')

print(f'\nTotal: {len(all_tickets)} tickets\n')

# ── FETCH COMMENTS & CLASSIFY ───────────────────────────────────────────────
print('Fetching comments & classifying...')
records = []
topic_samples = defaultdict(list)

for i, t in enumerate(all_tickets):
    subject = t.get('subject', '') or ''
    desc = t.get('description', '') or ''
    status = t.get('status', 'unknown')
    created = t.get('created_at', '')
    updated = t.get('updated_at', '')

    data = get_json(f'{BASE}/tickets/{t["id"]}/comments.json')
    comments = data.get('comments', []) if data else []
    comment_text = ' '.join(c.get('body', '') or '' for c in comments)

    full_text = subject + ' ' + desc + ' ' + comment_text
    user_text = extract_user_text(full_text)
    search_text = user_text + ' ' + user_text + ' ' + full_text

    topic = classify(search_text)
    lang = detect_lang(full_text)

    day = int(created[8:10]) if created else 1
    weekday = ''
    if created:
        try:
            dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
            weekday = dt.strftime('%A')
        except: pass

    res_hours = None
    if status == 'solved' and created and updated:
        try:
            c = datetime.fromisoformat(created.replace('Z', '+00:00'))
            s = datetime.fromisoformat(updated.replace('Z', '+00:00'))
            res_hours = (s - c).total_seconds() / 3600
        except: pass

    records.append({
        'id': t['id'], 'subject': subject, 'status': status,
        'topic': topic, 'lang': lang, 'day': day, 'weekday': weekday,
        'created': created[:10] if created else '',
        'n_comments': len(comments), 'res_hours': res_hours,
        'user_msg': user_text[:300],
    })

    if len(topic_samples[topic]) < 6:
        sample = user_text.strip()[:200].replace('\n', ' ')
        if len(sample) > 15:
            topic_samples[topic].append({'id': t['id'], 'msg': sample})

    if (i + 1) % 100 == 0:
        print(f'  {i+1}/{len(all_tickets)} processed...')
    time.sleep(0.05)

print(f'\nDone. {len(records)} tickets classified.\n')

# ── COMPUTE STATS ────────────────────────────────────────────────────────────
total = len(records)
topic_counts = Counter(r['topic'] for r in records)
lang_counts = Counter(r['lang'] for r in records)
status_counts = Counter(r['status'] for r in records)
day_counts = Counter(r['day'] for r in records)
weekday_counts = Counter(r['weekday'] for r in records)
topic_lang = defaultdict(lambda: Counter())
topic_by_week = defaultdict(lambda: Counter())

for r in records:
    topic_lang[r['topic']][r['lang']] += 1
    week_n = min(4, (r['day'] - 1) // 7 + 1)
    topic_by_week[r['topic']][f'W{week_n}'] += 1

macro_counts = {}
for macro, topics_list in MACRO.items():
    macro_counts[macro] = sum(topic_counts.get(t, 0) for t in topics_list)

res_times = [r['res_hours'] for r in records if r['res_hours'] is not None]
avg_res = round(sum(res_times) / len(res_times), 1) if res_times else 0
median_res = round(sorted(res_times)[len(res_times)//2], 1) if res_times else 0

topic_res = defaultdict(list)
for r in records:
    if r['res_hours'] is not None:
        topic_res[r['topic']].append(r['res_hours'])

total_comments = sum(r['n_comments'] for r in records)
avg_comments = round(total_comments / max(total, 1), 1)
solved_n = status_counts.get('solved', 0)
open_n = status_counts.get('open', 0) + status_counts.get('new', 0)
pct_solved = round(solved_n / max(total, 1) * 100)

topic_sorted = dict(sorted(topic_counts.items(), key=lambda x: -x[1]))
macro_sorted = dict(sorted(macro_counts.items(), key=lambda x: -x[1]))

# Print summary
print('-' * 50)
print('MACRO-CATEGORY SUMMARY')
print('-' * 50)
for macro, cnt in macro_sorted.items():
    pct = round(cnt / total * 100, 1)
    print(f'  {cnt:>5} ({pct:>5.1f}%)  {macro}')

print(f'\n{"-" * 50}')
print('DETAILED TOPIC BREAKDOWN')
print('-' * 50)
for topic, cnt in topic_sorted.items():
    pct = round(cnt / total * 100, 1)
    print(f'  {cnt:>5} ({pct:>5.1f}%)  {topic}')

# ── PDF GENERATION ───────────────────────────────────────────────────────────
print('\nGenerating PDF...')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors as rl_colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                Table, TableStyle, HRFlowable, PageBreak, KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

GREEN = rl_colors.HexColor('#39d353')
DARK  = rl_colors.HexColor('#0f1623')
GRAY  = rl_colors.HexColor('#8892a4')
LGRAY = rl_colors.HexColor('#f5f5f5')

def sty(n, **k): return ParagraphStyle(n, **k)
title_s  = sty('t',   fontSize=20, textColor=DARK,  fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=3)
sub_s    = sty('s',   fontSize=10, textColor=GRAY,  alignment=TA_CENTER, spaceAfter=2)
h2_s     = sty('h2',  fontSize=14, textColor=DARK,  fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=6)
h3_s     = sty('h3',  fontSize=11, textColor=rl_colors.HexColor('#1a4731'), fontName='Helvetica-Bold', spaceBefore=8, spaceAfter=4)
body_s   = sty('b',   fontSize=9.5, textColor=rl_colors.HexColor('#333'), leading=14)
small_s  = sty('sm',  fontSize=8,  textColor=rl_colors.HexColor('#555'), leading=11)
cap_s    = sty('c',   fontSize=8,  textColor=GRAY,  alignment=TA_CENTER)
kpi_v_s  = sty('kv',  fontSize=26, textColor=GREEN, fontName='Helvetica-Bold', alignment=TA_CENTER)
kpi_l_s  = sty('kl',  fontSize=7.5, textColor=GRAY, alignment=TA_CENTER)
quote_s  = sty('q',   fontSize=8,  textColor=rl_colors.HexColor('#444'), leading=11,
               leftIndent=8, borderPadding=4, backColor=rl_colors.HexColor('#f0f9f0'))

def make_chart(func, *args, **kwargs):
    buf = io.BytesIO()
    fig = func(*args, **kwargs)
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf

def chart_hbar(data, title, figsize=(7, 4.5), color='#39d353'):
    fig, ax = plt.subplots(figsize=figsize)
    labels, vals = list(data.keys()), list(data.values())
    bars = ax.barh(labels, vals, color=color, edgecolor='white', linewidth=0.4)
    ax.set_xlabel('Tickets', fontsize=8)
    ax.set_title(title, fontsize=11, fontweight='bold', pad=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(labelsize=7.5)
    for bar, v in zip(bars, vals):
        pct = round(v / total * 100, 1)
        ax.text(v + max(vals)*0.01, bar.get_y() + bar.get_height()/2,
                f'{v} ({pct}%)', va='center', fontsize=7)
    plt.tight_layout()
    return fig

def chart_daily(day_data, title, figsize=(7, 3)):
    fig, ax = plt.subplots(figsize=figsize)
    days = sorted(day_data.keys())
    vals = [day_data[d] for d in days]
    ax.bar(days, vals, color='#39d353', edgecolor='white', linewidth=0.3, width=0.8)
    avg = sum(vals) / len(vals)
    ax.axhline(y=avg, color='#ef4444', linestyle='--', linewidth=1.2, label=f'Avg: {avg:.0f}/day')
    ax.set_xlabel('Day of January', fontsize=8)
    ax.set_ylabel('Tickets', fontsize=8)
    ax.set_title(title, fontsize=11, fontweight='bold', pad=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(labelsize=7)
    ax.legend(fontsize=8)
    plt.tight_layout()
    return fig

def chart_pie(data, title, figsize=(5, 4)):
    palette = ['#39d353','#2aa644','#4ade6e','#22c55e','#86efac','#bbf7d0',
               '#a3e635','#dcfce7','#f0fdf4','#d1fae5','#6ee7b7','#34d399']
    fig, ax = plt.subplots(figsize=figsize)
    labels = [f'{k} ({v})' for k, v in data.items()]
    ax.pie(list(data.values()), labels=labels, colors=palette[:len(data)],
           autopct='%1.0f%%', startangle=140, textprops={'fontsize': 7})
    ax.set_title(title, fontsize=10, fontweight='bold', pad=5)
    plt.tight_layout()
    return fig

def chart_weekday(wd_data, figsize=(6, 2.5)):
    order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    vals = [wd_data.get(d, 0) for d in order]
    short = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    fig, ax = plt.subplots(figsize=figsize)
    clrs = ['#39d353' if d in ('Saturday','Sunday') else '#2aa644' for d in order]
    ax.bar(short, vals, color=clrs, edgecolor='white', linewidth=0.3)
    ax.set_title('Tickets by Day of Week', fontsize=10, fontweight='bold', pad=6)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(labelsize=8)
    for xi, v in zip(short, vals):
        ax.text(xi, v + max(vals)*0.02, str(v), ha='center', fontsize=8, fontweight='bold')
    plt.tight_layout()
    return fig

def chart_stacked_macro(figsize=(7, 3.5)):
    weeks_list = ['W1','W2','W3','W4']
    top_macros = [m for m, c in sorted(macro_counts.items(), key=lambda x: -x[1]) if c > 0][:6]
    palette = ['#39d353','#2aa644','#4ade6e','#22c55e','#86efac','#bbf7d0']
    fig, ax = plt.subplots(figsize=figsize)
    bottom = [0]*4
    for idx, macro in enumerate(top_macros):
        topics_in = MACRO.get(macro, [])
        vals = [sum(topic_by_week[t].get(w, 0) for t in topics_in) for w in weeks_list]
        ax.bar(weeks_list, vals, bottom=bottom, label=macro, color=palette[idx % len(palette)])
        bottom = [b+v for b, v in zip(bottom, vals)]
    ax.set_title('Volume by Category per Week', fontsize=10, fontweight='bold', pad=6)
    ax.legend(fontsize=7, loc='upper right')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(labelsize=8)
    plt.tight_layout()
    return fig

# ── BUILD PDF ────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    'zendesk_comprehensive_jan2026.pdf', pagesize=A4,
    leftMargin=1.6*cm, rightMargin=1.6*cm,
    topMargin=1.6*cm, bottomMargin=1.6*cm)
story = []

# === PAGE 1: Executive Summary ===
story.append(Paragraph('BetonWin — Comprehensive Support Analysis', title_s))
story.append(Paragraph(f'January 2026 | {total} tickets | {total_comments} comments analyzed', sub_s))
story.append(HRFlowable(width='100%', thickness=2, color=GREEN, spaceAfter=14))

kpi_data = [[
    Paragraph(str(total), kpi_v_s),
    Paragraph(f'{round(total/31)}', kpi_v_s),
    Paragraph(f'{pct_solved}%', kpi_v_s),
    Paragraph(f'{avg_res}h', kpi_v_s),
    Paragraph(f'{median_res}h', kpi_v_s),
    Paragraph(str(avg_comments), kpi_v_s),
],[
    Paragraph('Total Tickets', kpi_l_s),
    Paragraph('Avg / Day', kpi_l_s),
    Paragraph('Resolved', kpi_l_s),
    Paragraph('Avg Resolution', kpi_l_s),
    Paragraph('Median Resolution', kpi_l_s),
    Paragraph('Avg Comments', kpi_l_s),
]]
kt = Table(kpi_data, colWidths=[2.7*cm]*6)
kt.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,-1),LGRAY),('BOX',(0,0),(-1,-1),0.5,GRAY),
    ('INNERGRID',(0,0),(-1,-1),0.3,GRAY),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),
]))
story.append(kt)
story.append(Spacer(1, 12))

# Macro summary table with automation potential
story.append(Paragraph('Category Overview (Macro)', h2_s))
auto_map = {
    'DEPOSITS': 'HIGH - AI widget + deposit flow',
    'WITHDRAWALS': 'MEDIUM - FAQ + status check',
    'BONUS': 'HIGH - FAQ answers',
    'ACCOUNT': 'MEDIUM - self-service + FAQ',
    'PAYMENTS': 'LOW - needs manual review',
    'GAMES': 'LOW - needs investigation',
    'TECHNICAL': 'MEDIUM - FAQ + escalation',
    'KYC': 'LOW - manual process',
    'COMPLAINTS': 'LOW - needs human agent',
    'INFO': 'HIGH - AI can answer',
    'GREETINGS': 'HIGH - AI greeting handler',
}
m_rows = [['Category', 'Tickets', '% Total', 'Automation Potential']]
for macro, cnt in macro_sorted.items():
    if cnt == 0: continue
    pct = f'{round(cnt/total*100, 1)}%'
    m_rows.append([macro, str(cnt), pct, auto_map.get(macro, '')])
mt = Table(m_rows, colWidths=[3*cm, 2*cm, 2*cm, 9.5*cm])
mt.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0),DARK),('TEXTCOLOR',(0,0),(-1,0),rl_colors.white),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),8),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[rl_colors.white,LGRAY]),
    ('GRID',(0,0),(-1,-1),0.3,GRAY),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ('ALIGN',(1,0),(2,-1),'CENTER'),
]))
story.append(mt)

# === PAGE 2: Daily Volume + Day of Week ===
story.append(PageBreak())
story.append(Paragraph('Volume Analysis', h2_s))
story.append(Image(make_chart(chart_daily, dict(day_counts), 'Daily Ticket Volume - January 2026'),
                   width=16*cm, height=6.5*cm))
story.append(Spacer(1, 8))
story.append(Image(make_chart(chart_weekday, dict(weekday_counts)),
                   width=14*cm, height=5.5*cm))
story.append(Spacer(1, 8))

peak_day = max(day_counts, key=day_counts.get)
low_day = min(day_counts, key=day_counts.get)
story.append(Paragraph(
    f'<b>Peak day:</b> January {peak_day} ({day_counts[peak_day]} tickets) | '
    f'<b>Lowest:</b> January {low_day} ({day_counts[low_day]} tickets) | '
    f'<b>Daily average:</b> {round(total/31)} tickets',
    body_s))

# === PAGE 3: Topic Distribution ===
story.append(PageBreak())
story.append(Paragraph('Detailed Topic Distribution', h2_s))
story.append(Image(make_chart(chart_hbar, topic_sorted, f'All {total} Tickets by Topic'),
                   width=16*cm, height=10*cm))

# === PAGE 4: Pie + Stacked weekly ===
story.append(PageBreak())
story.append(Paragraph('Topic Share & Weekly Trend', h2_s))

top10 = dict(list(topic_sorted.items())[:10])
rest = total - sum(top10.values())
if rest > 0:
    top10['Other'] = rest
story.append(Image(make_chart(chart_pie, top10, 'Top 10 Topics (Share)'),
                   width=13*cm, height=10*cm))
story.append(Spacer(1, 8))
story.append(Image(make_chart(chart_stacked_macro),
                   width=16*cm, height=8*cm))

# === PAGE 5: Language & Status ===
story.append(PageBreak())
story.append(Paragraph('Language & Status Distribution', h2_s))

lang_sorted = dict(sorted(lang_counts.items(), key=lambda x: -x[1]))
status_sorted = dict(sorted(status_counts.items(), key=lambda x: -x[1]))

l_buf = make_chart(chart_pie, lang_sorted, 'By Language', (4.5, 3.5))
s_buf = make_chart(chart_pie, status_sorted, 'By Status', (4.5, 3.5))
row = Table([[Image(l_buf, 8.5*cm, 7*cm), Image(s_buf, 8.5*cm, 7*cm)]])
row.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP')]))
story.append(row)
story.append(Spacer(1, 10))

# Language x Topic cross table
story.append(Paragraph('Top 5 Topics by Language', h3_s))
top5_topics = list(topic_sorted.keys())[:5]
top_langs = [l for l, _ in sorted(lang_counts.items(), key=lambda x: -x[1]) if _ > 10][:4]
cross_rows = [['Topic'] + top_langs]
for topic in top5_topics:
    row_data = [topic]
    for lang in top_langs:
        cnt = topic_lang[topic].get(lang, 0)
        row_data.append(str(cnt))
    cross_rows.append(row_data)
cw = [5.5*cm] + [2.5*cm]*len(top_langs)
ct = Table(cross_rows, colWidths=cw)
ct.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0),DARK),('TEXTCOLOR',(0,0),(-1,0),rl_colors.white),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),8),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[rl_colors.white,LGRAY]),
    ('GRID',(0,0),(-1,-1),0.3,GRAY),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ('ALIGN',(1,0),(-1,-1),'CENTER'),
]))
story.append(ct)

# === PAGES 6+: Per-topic detail with samples ===
story.append(PageBreak())
story.append(Paragraph('Topic Detail with Sample Messages', h2_s))
story.append(HRFlowable(width='100%', thickness=1, color=GREEN, spaceAfter=8))

for topic, cnt in topic_sorted.items():
    pct = round(cnt / total * 100, 1)
    t_res = topic_res.get(topic, [])
    t_avg = f'{round(sum(t_res)/len(t_res), 1)}h' if t_res else 'N/A'
    t_langs = topic_lang[topic]
    t_top_lang = max(t_langs, key=t_langs.get) if t_langs else 'N/A'
    t_lang_pct = round(t_langs[t_top_lang] / max(cnt, 1) * 100) if t_langs else 0
    tw = topic_by_week[topic]
    trend_str = ' | '.join(f'W{w}: {tw.get(f"W{w}",0)}' for w in range(1,5))

    elements = []
    elements.append(Paragraph(f'{topic}', h3_s))
    elements.append(Paragraph(
        f'<b>{cnt} tickets ({pct}%)</b> | Avg resolution: {t_avg} | '
        f'Main language: {t_top_lang} ({t_lang_pct}%) | {trend_str}',
        small_s))
    elements.append(Spacer(1, 4))

    samples = topic_samples.get(topic, [])
    if samples:
        for s in samples[:4]:
            elements.append(Paragraph(f'#{s["id"]}: "{s["msg"]}"', quote_s))
            elements.append(Spacer(1, 2))

    elements.append(Spacer(1, 8))
    story.append(KeepTogether(elements))

# === ACTIONABLE INSIGHTS PAGE ===
story.append(PageBreak())
story.append(HRFlowable(width='100%', thickness=2, color=GREEN, spaceAfter=10))
story.append(Paragraph('Actionable Insights & Recommendations', h2_s))

auto_high = sum(macro_counts.get(m, 0) for m in ['DEPOSITS','BONUS','INFO','GREETINGS'])
auto_med = sum(macro_counts.get(m, 0) for m in ['WITHDRAWALS','ACCOUNT','TECHNICAL'])
auto_low = sum(macro_counts.get(m, 0) for m in ['PAYMENTS','GAMES','KYC','COMPLAINTS'])

insights = [
    f'<b>VOLUME:</b> {total} tickets in January = ~{round(total/31)} tickets/day. '
    f'Peak on day {peak_day} ({day_counts[peak_day]} tickets).',

    f'<b>TOP ISSUE:</b> "{list(topic_sorted.keys())[0]}" with {list(topic_sorted.values())[0]} tickets '
    f'({round(list(topic_sorted.values())[0]/total*100,1)}%). This is the #1 automation target.',

    f'<b>DEPOSIT-RELATED:</b> {macro_counts.get("DEPOSITS",0)} tickets '
    f'({round(macro_counts.get("DEPOSITS",0)/total*100,1)}%) — combining all deposit subtopics. '
    f'The AI widget deposit flow can directly address these.',

    f'<b>WITHDRAWAL-RELATED:</b> {macro_counts.get("WITHDRAWALS",0)} tickets '
    f'({round(macro_counts.get("WITHDRAWALS",0)/total*100,1)}%). FAQ + status check automation recommended.',

    f'<b>GREETINGS:</b> {macro_counts.get("GREETINGS",0)} tickets '
    f'({round(macro_counts.get("GREETINGS",0)/total*100,1)}%) are just "hola/hello" with no real question. '
    f'AI widget handles these instantly.',

    f'<b>AUTOMATION POTENTIAL:</b><br/>'
    f'&nbsp;&nbsp;HIGH: {auto_high} tickets ({round(auto_high/total*100)}%) — deposits, bonus FAQ, account info, greetings<br/>'
    f'&nbsp;&nbsp;MEDIUM: {auto_med} tickets ({round(auto_med/total*100)}%) — withdrawals, account, technical<br/>'
    f'&nbsp;&nbsp;LOW: {auto_low} tickets ({round(auto_low/total*100)}%) — payments, games, KYC, complaints',

    f'<b>LANGUAGE:</b> {list(lang_sorted.keys())[0]} dominates '
    f'({list(lang_sorted.values())[0]} tickets, {round(list(lang_sorted.values())[0]/total*100,1)}%). '
    f'Widget KB should prioritize this language.',

    f'<b>RESOLUTION:</b> Average {avg_res}h, median {median_res}h. '
    f'{pct_solved}% resolved, {open_n} still open.',
]

for ins in insights:
    story.append(Paragraph(f'<bullet>&bull;</bullet> {ins}', body_s))
    story.append(Spacer(1, 6))

# ROI estimate
story.append(Spacer(1, 10))
story.append(Paragraph('ROI Estimate — AI Widget Impact', h3_s))
roi_text = (
    f'If the AI widget handles <b>{round(auto_high/total*100)}%</b> of tickets automatically '
    f'({auto_high} tickets/month), at an estimated cost of $2-5 per manual ticket resolution, '
    f'the monthly savings would be <b>${auto_high*3:,} - ${auto_high*5:,}</b>. '
    f'Additionally, {round(auto_med/total*100)}% ({auto_med} tickets) can be partially automated '
    f'with FAQ responses, reducing agent handling time by ~50%.'
)
story.append(Paragraph(roi_text, body_s))

# Footer
story.append(Spacer(1, 20))
story.append(HRFlowable(width='100%', thickness=1, color=GRAY, spaceAfter=6))
story.append(Paragraph(
    f'Generated {datetime.now().strftime("%d %b %Y %H:%M")} | '
    f'BetonWin Zendesk | {total} tickets | {total_comments} comments | '
    f'{len(topic_counts)} topics classified',
    cap_s))

doc.build(story)
print(f'\n✅ Report saved: zendesk_comprehensive_jan2026.pdf')
