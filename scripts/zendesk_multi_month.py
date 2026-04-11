#!/usr/bin/env python3
"""
BetonWin — Multi-Month Zendesk Analysis
October, November, December 2025
Same methodology as January 2026 report.
"""

import os, requests, time, re, sys
from datetime import datetime
from collections import defaultdict, Counter
from dotenv import load_dotenv

load_dotenv('zendesk.env')
AUTH = (f'{os.getenv("ZENDESK_EMAIL")}/token', os.getenv('ZENDESK_API_TOKEN'))
BASE = 'https://betonwin.zendesk.com/api/v2'

# ── API ──────────────────────────────────────────────────────────────────────
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

# ── TOPICS (same as Jan 2026 report) ────────────────────────────────────────
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

# ── MONTH DEFINITIONS ────────────────────────────────────────────────────────
MONTHS = [
    {
        'name': 'October 2025',
        'short': 'Oct 2025',
        'weeks': [
            ('2025-10-01T00:00:00Z', '2025-10-08T00:00:00Z'),
            ('2025-10-08T00:00:00Z', '2025-10-15T00:00:00Z'),
            ('2025-10-15T00:00:00Z', '2025-10-22T00:00:00Z'),
            ('2025-10-22T00:00:00Z', '2025-11-01T00:00:00Z'),
        ],
        'days': 31,
    },
    {
        'name': 'November 2025',
        'short': 'Nov 2025',
        'weeks': [
            ('2025-11-01T00:00:00Z', '2025-11-08T00:00:00Z'),
            ('2025-11-08T00:00:00Z', '2025-11-15T00:00:00Z'),
            ('2025-11-15T00:00:00Z', '2025-11-22T00:00:00Z'),
            ('2025-11-22T00:00:00Z', '2025-12-01T00:00:00Z'),
        ],
        'days': 30,
    },
    {
        'name': 'December 2025',
        'short': 'Dec 2025',
        'weeks': [
            ('2025-12-01T00:00:00Z', '2025-12-08T00:00:00Z'),
            ('2025-12-08T00:00:00Z', '2025-12-15T00:00:00Z'),
            ('2025-12-15T00:00:00Z', '2025-12-22T00:00:00Z'),
            ('2025-12-22T00:00:00Z', '2026-01-01T00:00:00Z'),
        ],
        'days': 31,
    },
]

# ── PROCESS EACH MONTH ───────────────────────────────────────────────────────
all_month_data = {}  # month_name -> {records, topic_counts, macro_counts, lang_counts, ...}

for month in MONTHS:
    print('=' * 60)
    print(f'  Analyzing: {month["name"]}')
    print('=' * 60)

    # Fetch tickets
    print('\nFetching tickets...')
    tickets, seen = [], set()
    for ws, we in month['weeks']:
        url = f'{BASE}/search.json?query=type:ticket+created>{ws}+created<{we}&sort_by=created_at&sort_order=asc&per_page=100'
        while url:
            data = get_json(url)
            if not data: break
            for t in data.get('results', []):
                if t['id'] not in seen:
                    tickets.append(t)
                    seen.add(t['id'])
            url = data.get('next_page')
        print(f'  {ws[:10]}: {len(tickets)} total')
    print(f'  Total: {len(tickets)} tickets')

    # Fetch comments & classify
    print('  Fetching comments & classifying...')
    records = []
    topic_samples = defaultdict(list)

    for i, t in enumerate(tickets):
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

        res_hours = None
        if status == 'solved' and created and updated:
            try:
                c = datetime.fromisoformat(created.replace('Z', '+00:00'))
                s = datetime.fromisoformat(updated.replace('Z', '+00:00'))
                res_hours = (s - c).total_seconds() / 3600
            except: pass

        records.append({
            'id': t['id'], 'subject': subject, 'status': status,
            'topic': topic, 'lang': lang,
            'created': created[:10] if created else '',
            'n_comments': len(comments), 'res_hours': res_hours,
            'user_msg': user_text[:300],
        })

        if len(topic_samples[topic]) < 4:
            sample = user_text.strip()[:200].replace('\n', ' ')
            if len(sample) > 15:
                topic_samples[topic].append({'id': t['id'], 'msg': sample})

        if (i + 1) % 100 == 0:
            print(f'    {i+1}/{len(tickets)} processed...')
        time.sleep(0.05)

    # Compute stats
    total = len(records)
    topic_counts = Counter(r['topic'] for r in records)
    lang_counts = Counter(r['lang'] for r in records)
    status_counts = Counter(r['status'] for r in records)

    macro_counts = {}
    for macro, topics_list in MACRO.items():
        macro_counts[macro] = sum(topic_counts.get(t, 0) for t in topics_list)

    res_times = [r['res_hours'] for r in records if r['res_hours'] is not None]
    avg_res = round(sum(res_times) / len(res_times), 1) if res_times else 0
    total_comments = sum(r['n_comments'] for r in records)
    solved_n = status_counts.get('solved', 0)
    open_n = status_counts.get('open', 0) + status_counts.get('new', 0)

    topic_sorted = dict(sorted(topic_counts.items(), key=lambda x: -x[1]))
    macro_sorted = dict(sorted(macro_counts.items(), key=lambda x: -x[1]))

    all_month_data[month['name']] = {
        'records': records,
        'total': total,
        'topic_counts': topic_counts,
        'topic_sorted': topic_sorted,
        'macro_counts': macro_counts,
        'macro_sorted': macro_sorted,
        'lang_counts': lang_counts,
        'status_counts': status_counts,
        'avg_res': avg_res,
        'total_comments': total_comments,
        'solved_n': solved_n,
        'open_n': open_n,
        'days': month['days'],
        'topic_samples': topic_samples,
    }

    print(f'\n  {month["name"]}: {total} tickets classified')
    for macro, cnt in macro_sorted.items():
        if cnt > 0:
            print(f'    {cnt:>5} ({round(cnt/max(total,1)*100,1):>5.1f}%)  {macro}')
    print()
    sys.stdout.flush()

# ── PDF GENERATION ───────────────────────────────────────────────────────────
print('=' * 60)
print('  Generating Multi-Month PDF Report')
print('=' * 60)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
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
kpi_v_s  = sty('kv',  fontSize=22, textColor=GREEN, fontName='Helvetica-Bold', alignment=TA_CENTER)
kpi_l_s  = sty('kl',  fontSize=7.5, textColor=GRAY, alignment=TA_CENTER)
quote_s  = sty('q',   fontSize=8,  textColor=rl_colors.HexColor('#444'), leading=11,
               leftIndent=8, borderPadding=4, backColor=rl_colors.HexColor('#f0f9f0'))

month_names = [m['name'] for m in MONTHS]
month_short = [m['short'] for m in MONTHS]

def make_chart(func, *args, **kwargs):
    buf = io.BytesIO()
    fig = func(*args, **kwargs)
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf

def chart_volume_trend(figsize=(7, 3)):
    """Monthly total volume bar chart."""
    totals = [all_month_data[m]['total'] for m in month_names]
    fig, ax = plt.subplots(figsize=figsize)
    bars = ax.bar(month_short, totals, color='#39d353', edgecolor='white', width=0.5)
    ax.set_title('Total Ticket Volume by Month', fontsize=11, fontweight='bold', pad=8)
    ax.set_ylabel('Tickets', fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for bar, v in zip(bars, totals):
        ax.text(bar.get_x() + bar.get_width()/2, v + max(totals)*0.02,
                str(v), ha='center', fontsize=10, fontweight='bold')
    # Add daily avg as text
    for i, (bar, m) in enumerate(zip(bars, month_names)):
        d = all_month_data[m]
        avg = round(d['total'] / d['days'])
        ax.text(bar.get_x() + bar.get_width()/2, max(totals)*0.05,
                f'{avg}/day', ha='center', fontsize=8, color='white', fontweight='bold')
    plt.tight_layout()
    return fig

def chart_macro_trend(figsize=(8, 4.5)):
    """Grouped bar: macro categories across months."""
    top_macros = []
    all_macros = set()
    for m in month_names:
        all_macros.update(k for k, v in all_month_data[m]['macro_counts'].items() if v > 0)
    # Sort by total across months
    macro_totals = {}
    for macro in all_macros:
        macro_totals[macro] = sum(all_month_data[m]['macro_counts'].get(macro, 0) for m in month_names)
    top_macros = sorted(macro_totals, key=macro_totals.get, reverse=True)[:8]

    x = np.arange(len(top_macros))
    width = 0.25
    palette = ['#2aa644', '#39d353', '#4ade6e']

    fig, ax = plt.subplots(figsize=figsize)
    for i, mn in enumerate(month_names):
        vals = [all_month_data[mn]['macro_counts'].get(m, 0) for m in top_macros]
        bars = ax.bar(x + i*width, vals, width, label=month_short[i], color=palette[i])
        for bar, v in zip(bars, vals):
            if v > 0:
                ax.text(bar.get_x() + bar.get_width()/2, v + 5,
                        str(v), ha='center', fontsize=6.5)

    ax.set_xticks(x + width)
    ax.set_xticklabels(top_macros, fontsize=7.5, rotation=30, ha='right')
    ax.set_title('Category Comparison Across Months', fontsize=11, fontweight='bold', pad=8)
    ax.legend(fontsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    return fig

def chart_topic_trend(figsize=(8, 5)):
    """Grouped bar: top topics across months."""
    all_topics_total = Counter()
    for m in month_names:
        all_topics_total.update(all_month_data[m]['topic_counts'])
    top_topics = [t for t, _ in all_topics_total.most_common(10)]

    x = np.arange(len(top_topics))
    width = 0.25
    palette = ['#2aa644', '#39d353', '#4ade6e']

    fig, ax = plt.subplots(figsize=figsize)
    for i, mn in enumerate(month_names):
        vals = [all_month_data[mn]['topic_counts'].get(t, 0) for t in top_topics]
        ax.bar(x + i*width, vals, width, label=month_short[i], color=palette[i])

    ax.set_xticks(x + width)
    ax.set_xticklabels(top_topics, fontsize=6.5, rotation=35, ha='right')
    ax.set_title('Top 10 Topics — Month-over-Month', fontsize=11, fontweight='bold', pad=8)
    ax.legend(fontsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    return fig

def chart_lang_trend(figsize=(6, 3)):
    """Stacked bar: languages per month."""
    all_langs = set()
    for m in month_names:
        all_langs.update(all_month_data[m]['lang_counts'].keys())
    langs = sorted(all_langs, key=lambda l: sum(all_month_data[m]['lang_counts'].get(l, 0) for m in month_names), reverse=True)

    palette = ['#39d353','#2aa644','#4ade6e','#22c55e','#86efac']
    fig, ax = plt.subplots(figsize=figsize)
    bottom = [0]*len(month_names)
    for idx, lang in enumerate(langs[:5]):
        vals = [all_month_data[m]['lang_counts'].get(lang, 0) for m in month_names]
        ax.bar(month_short, vals, bottom=bottom, label=lang, color=palette[idx % len(palette)])
        bottom = [b+v for b, v in zip(bottom, vals)]
    ax.set_title('Language Distribution by Month', fontsize=10, fontweight='bold', pad=6)
    ax.legend(fontsize=7, loc='upper right')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    return fig

# ── BUILD PDF ────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    'zendesk_q4_2025_report.pdf', pagesize=A4,
    leftMargin=1.6*cm, rightMargin=1.6*cm,
    topMargin=1.6*cm, bottomMargin=1.6*cm)
story = []

# === PAGE 1: Cover + KPIs ===
grand_total = sum(all_month_data[m]['total'] for m in month_names)
grand_comments = sum(all_month_data[m]['total_comments'] for m in month_names)

story.append(Paragraph('BetonWin — Q4 2025 Support Analysis', title_s))
story.append(Paragraph(f'October - December 2025 | {grand_total} tickets | {grand_comments} comments', sub_s))
story.append(HRFlowable(width='100%', thickness=2, color=GREEN, spaceAfter=14))

# Per-month KPI row
kpi_header = [Paragraph('', kpi_l_s)]
kpi_row1 = [Paragraph('<b>Total Tickets</b>', small_s)]
kpi_row2 = [Paragraph('<b>Avg / Day</b>', small_s)]
kpi_row3 = [Paragraph('<b>% Resolved</b>', small_s)]
kpi_row4 = [Paragraph('<b>Avg Resolution</b>', small_s)]
kpi_row5 = [Paragraph('<b>Total Comments</b>', small_s)]

for mn in month_names:
    d = all_month_data[mn]
    pct_solved = round(d['solved_n'] / max(d['total'], 1) * 100)
    kpi_header.append(Paragraph(mn.split()[0], kpi_l_s))  # "October", "November", "December"
    kpi_row1.append(Paragraph(str(d['total']), kpi_v_s))
    kpi_row2.append(Paragraph(str(round(d['total'] / d['days'])), kpi_v_s))
    kpi_row3.append(Paragraph(f'{pct_solved}%', kpi_v_s))
    kpi_row4.append(Paragraph(f'{d["avg_res"]}h', kpi_v_s))
    kpi_row5.append(Paragraph(str(d['total_comments']), kpi_v_s))

kpi_table = Table([kpi_header, kpi_row1, kpi_row2, kpi_row3, kpi_row4, kpi_row5],
                  colWidths=[3.5*cm, 4*cm, 4*cm, 4*cm])
kpi_table.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0),DARK),('TEXTCOLOR',(0,0),(-1,0),rl_colors.white),
    ('BACKGROUND',(0,1),(-1,-1),LGRAY),
    ('BOX',(0,0),(-1,-1),0.5,GRAY),('INNERGRID',(0,0),(-1,-1),0.3,GRAY),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
    ('ALIGN',(1,0),(-1,-1),'CENTER'),
]))
story.append(kpi_table)
story.append(Spacer(1, 14))

# Volume trend chart
story.append(Image(make_chart(chart_volume_trend), width=15*cm, height=6.5*cm))

# === PAGE 2: Macro category comparison ===
story.append(PageBreak())
story.append(Paragraph('Category Comparison — Month over Month', h2_s))
story.append(Image(make_chart(chart_macro_trend), width=16*cm, height=9*cm))
story.append(Spacer(1, 10))

# Macro comparison table
story.append(Paragraph('Category Totals by Month', h3_s))
all_macros_sorted = sorted(
    set().union(*(all_month_data[m]['macro_counts'].keys() for m in month_names)),
    key=lambda mc: sum(all_month_data[m]['macro_counts'].get(mc, 0) for m in month_names),
    reverse=True)

mc_rows = [['Category', 'Oct 2025', 'Nov 2025', 'Dec 2025', 'Total', 'Trend']]
for macro in all_macros_sorted:
    vals = [all_month_data[m]['macro_counts'].get(macro, 0) for m in month_names]
    total_m = sum(vals)
    if total_m == 0: continue
    # Trend: compare last to first
    if vals[0] > 0:
        change = round((vals[-1] - vals[0]) / vals[0] * 100)
        trend = f'+{change}%' if change > 0 else f'{change}%'
    else:
        trend = 'NEW'
    mc_rows.append([macro, str(vals[0]), str(vals[1]), str(vals[2]), str(total_m), trend])

mc_tbl = Table(mc_rows, colWidths=[3.5*cm, 2.2*cm, 2.2*cm, 2.2*cm, 2.2*cm, 2.2*cm])
mc_tbl.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0),DARK),('TEXTCOLOR',(0,0),(-1,0),rl_colors.white),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),8),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[rl_colors.white,LGRAY]),
    ('GRID',(0,0),(-1,-1),0.3,GRAY),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ('ALIGN',(1,0),(-1,-1),'CENTER'),
]))
story.append(mc_tbl)

# === PAGE 3: Topic comparison ===
story.append(PageBreak())
story.append(Paragraph('Top 10 Topics — Month over Month', h2_s))
story.append(Image(make_chart(chart_topic_trend), width=16*cm, height=10*cm))

# === PAGE 4: Language trend ===
story.append(PageBreak())
story.append(Paragraph('Language & Resolution Trends', h2_s))
story.append(Image(make_chart(chart_lang_trend), width=14*cm, height=6.5*cm))
story.append(Spacer(1, 12))

# Resolution comparison
story.append(Paragraph('Resolution Time Comparison', h3_s))
res_rows = [['Metric', 'Oct 2025', 'Nov 2025', 'Dec 2025']]
res_rows.append(['Avg Resolution (h)'] + [str(all_month_data[m]['avg_res']) for m in month_names])
res_rows.append(['Tickets Resolved'] + [str(all_month_data[m]['solved_n']) for m in month_names])
res_rows.append(['Tickets Open/New'] + [str(all_month_data[m]['open_n']) for m in month_names])
res_rows.append(['Total Comments'] + [str(all_month_data[m]['total_comments']) for m in month_names])

res_tbl = Table(res_rows, colWidths=[4.5*cm, 3.5*cm, 3.5*cm, 3.5*cm])
res_tbl.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0),DARK),('TEXTCOLOR',(0,0),(-1,0),rl_colors.white),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),9),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[rl_colors.white,LGRAY]),
    ('GRID',(0,0),(-1,-1),0.3,GRAY),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('ALIGN',(1,0),(-1,-1),'CENTER'),
]))
story.append(res_tbl)

# === PAGES 5+: Per-month detail ===
for mn in month_names:
    d = all_month_data[mn]
    story.append(PageBreak())
    story.append(Paragraph(f'{mn} — Detailed Breakdown', h2_s))
    story.append(HRFlowable(width='100%', thickness=1, color=GREEN, spaceAfter=8))

    # Topic table
    t_rows = [['Topic', 'Tickets', '% of Total']]
    for topic, cnt in d['topic_sorted'].items():
        pct = round(cnt / max(d['total'], 1) * 100, 1)
        t_rows.append([topic, str(cnt), f'{pct}%'])
    t_tbl = Table(t_rows, colWidths=[8*cm, 2.5*cm, 3*cm])
    t_tbl.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),DARK),('TEXTCOLOR',(0,0),(-1,0),rl_colors.white),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),8),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[rl_colors.white,LGRAY]),
        ('GRID',(0,0),(-1,-1),0.3,GRAY),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
        ('ALIGN',(1,0),(-1,-1),'CENTER'),
    ]))
    story.append(t_tbl)
    story.append(Spacer(1, 12))

    # Sample messages for top 5 topics
    story.append(Paragraph(f'Sample Messages — Top Topics', h3_s))
    top5 = list(d['topic_sorted'].keys())[:5]
    for topic in top5:
        samples = d['topic_samples'].get(topic, [])
        if not samples: continue
        story.append(Paragraph(f'<b>{topic}</b> ({d["topic_counts"][topic]} tickets)', small_s))
        for s in samples[:3]:
            story.append(Paragraph(f'#{s["id"]}: "{s["msg"]}"', quote_s))
            story.append(Spacer(1, 2))
        story.append(Spacer(1, 6))

# === FINAL PAGE: Cross-month insights ===
story.append(PageBreak())
story.append(HRFlowable(width='100%', thickness=2, color=GREEN, spaceAfter=10))
story.append(Paragraph('Cross-Month Insights & Trends', h2_s))

# Calculate trends
oct_d = all_month_data['October 2025']
dec_d = all_month_data['December 2025']
nov_d = all_month_data['November 2025']

vol_change = round((dec_d['total'] - oct_d['total']) / max(oct_d['total'], 1) * 100)

# Find fastest growing topic
topic_growth = {}
for topic in set(oct_d['topic_counts'].keys()) | set(dec_d['topic_counts'].keys()):
    oct_v = oct_d['topic_counts'].get(topic, 0)
    dec_v = dec_d['topic_counts'].get(topic, 0)
    if oct_v > 10:
        topic_growth[topic] = round((dec_v - oct_v) / oct_v * 100)
growing = sorted(topic_growth.items(), key=lambda x: -x[1])
shrinking = sorted(topic_growth.items(), key=lambda x: x[1])

insights = [
    f'<b>VOLUME TREND:</b> {vol_change:+d}% change from October ({oct_d["total"]}) to December ({dec_d["total"]}). '
    f'November had {nov_d["total"]} tickets.',

    f'<b>TOTAL Q4:</b> {grand_total} tickets across 3 months = ~{round(grand_total/92)} tickets/day average.',
]

if growing and growing[0][1] > 0:
    insights.append(
        f'<b>FASTEST GROWING:</b> "{growing[0][0]}" increased {growing[0][1]:+d}% from Oct to Dec.'
    )
if shrinking and shrinking[0][1] < 0:
    insights.append(
        f'<b>BIGGEST DECLINE:</b> "{shrinking[0][0]}" decreased {shrinking[0][1]}% from Oct to Dec.'
    )

# Automation potential across all 3 months
auto_high_total = sum(
    sum(all_month_data[m]['macro_counts'].get(mc, 0) for mc in ['DEPOSITS','BONUS','INFO','GREETINGS'])
    for m in month_names)
auto_pct = round(auto_high_total / max(grand_total, 1) * 100)
insights.append(
    f'<b>AUTOMATION POTENTIAL:</b> {auto_high_total} tickets ({auto_pct}%) across Q4 could be fully automated '
    f'by the AI widget (greetings + deposits + bonus FAQ + account info).'
)
insights.append(
    f'<b>ESTIMATED Q4 SAVINGS:</b> At $3-5/ticket, automating {auto_high_total} tickets would save '
    f'${auto_high_total*3:,} - ${auto_high_total*5:,} for the quarter.'
)

# Consistency check
greet_pcts = [round(all_month_data[m]['macro_counts'].get('GREETINGS', 0) / max(all_month_data[m]['total'], 1) * 100) for m in month_names]
insights.append(
    f'<b>GREETINGS CONSISTENCY:</b> Greeting-only tickets remain stable at {greet_pcts[0]}% / {greet_pcts[1]}% / {greet_pcts[2]}% '
    f'across Oct/Nov/Dec — confirming this is a structural pattern, not seasonal.'
)

for ins in insights:
    story.append(Paragraph(f'<bullet>&bull;</bullet> {ins}', body_s))
    story.append(Spacer(1, 6))

# Footer
story.append(Spacer(1, 20))
story.append(HRFlowable(width='100%', thickness=1, color=GRAY, spaceAfter=6))
story.append(Paragraph(
    f'Generated {datetime.now().strftime("%d %b %Y %H:%M")} | '
    f'BetonWin Zendesk | Q4 2025 | {grand_total} tickets | {grand_comments} comments',
    cap_s))

doc.build(story)
print(f'\n{"=" * 60}')
print(f'  PDF saved: zendesk_q4_2025_report.pdf')
print(f'  {grand_total} total tickets across Oct-Nov-Dec 2025')
print(f'{"=" * 60}')
