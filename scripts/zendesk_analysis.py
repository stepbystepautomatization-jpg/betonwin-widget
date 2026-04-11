#!/usr/bin/env python3
"""
Zendesk Full Analysis — BetonWin
Gennaio 2026: tutti i ticket + commenti, subcategorie, PDF dettagliato.
"""

import os, requests, time
from datetime import datetime, timezone
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv('zendesk.env')

SUBDOMAIN = 'betonwin'
EMAIL     = os.getenv('ZENDESK_EMAIL')
API_TOKEN = os.getenv('ZENDESK_API_TOKEN')
AUTH      = (f'{EMAIL}/token', API_TOKEN)
BASE      = f'https://{SUBDOMAIN}.zendesk.com/api/v2'

# ── CHAT TRANSCRIPT EXTRACTOR ────────────────────────────────────────────────
import re as _re

def extract_user_text(text):
    """From chat transcript '(HH:MM:SS) Name: msg' extract only user (non-BOW) lines."""
    lines = _re.findall(r'\(\d{2}:\d{2}:\d{2}\)\s+([^:]+):\s+(.+?)(?=\s*\(\d{2}:\d{2}:\d{2}\)|$)',
                        text or '', _re.DOTALL)
    user_lines = [msg for name, msg in lines if name.strip().upper() not in ('BOW', 'BOW ')]
    return ' '.join(user_lines) if user_lines else text

# ── CATEGORY + SUBCATEGORY TAXONOMY ─────────────────────────────────────────
# Colloquial + formal keywords for ES/IT/PT/EN (latam chat style)
TAXONOMY = {
    'Deposit': {
        'Not Received / Not Credited': [
            # Spanish colloquial (latam)
            'no se reflejo','no se acredito','no se me acredito','no me acredito',
            'no aparece','no lo veo','no figura','no se ve','no fue acreditado',
            'hice una transferencia y no','realice un deposito y no','transferi y no',
            'recarga exitosa pero','exitoso pero no','saldo no cambio','no cambio el saldo',
            'no recibido','no llegó','no llego','no recibí','no recibi',
            # English
            'not received','not credited','not arrived','deposit missing','did not arrive',
            'deposit not showing','not reflected','balance not updated',
            # Italian
            'non ricevuto','non arrivato','non accreditato','non si vede','deposito mancante',
            # Portuguese
            'não recebi','não chegou','não foi creditado','não aparece','não encontro',
        ],
        'Failed / Declined':   [
            'failed','fallido','fallito','falhou','declined','rechazado','rifiutato','recusado',
            'error al depositar','error de pago','payment failed','transaction failed',
            'no se procesó','no se proceso','no proceso','transacción fallida',
            'non è andato','non è riuscito','não processado',
        ],
        'How to Deposit':      [
            'cómo depositar','como depositar','come depositare','how to deposit','how do i deposit',
            'how to recharge','cómo recargar','como recargar','come ricaricare',
            'quiero depositar','quiero hacer una recarga','want to deposit','voglio depositare',
            'deposit method','metodo deposito','método de pago','que metodos','qué métodos',
            'como puedo cargar','puedo depositar','cuánto es el mínimo','monto minimo',
        ],
        'Processing Delay':    [
            'still processing','cuánto tarda','quanto tempo','how long deposit',
            'esperando','waiting for deposit','en espera del deposito','in attesa del deposito',
            'pending deposit','demora','tarda mucho','lleva mucho tiempo',
        ],
        'Recarga / Top-up':    [
            'recarga','recargar','carga saldo','cargar saldo','cargar cuenta',
            'recarga no','recarga exitosa','hice una recarga','mi recarga',
            'top up','topup','ricarica','caricare saldo',
        ],
        'Limits':              [
            'deposit limit','límite depósito','limite deposito','limite de depósito',
            'monto máximo','massimo deposito','maximum deposit','increase limit',
        ],
    },
    'Withdrawal': {
        'Not Received':        [
            'retiro no recibido','prelievo non ricevuto','saque não recebido',
            'withdrawal not received','no recibí el retiro','no recibi el retiro',
            'no llegó el retiro','no llego el retiro','withdrawal missing',
            'retiro no llegó','dónde está mi retiro',
        ],
        'Pending / Delay':     [
            'retiro pendiente','prelievo in attesa','saque pendente','withdrawal pending',
            'cuánto tarda retiro','quanto tempo prelievo','how long withdrawal',
            'retiro demora','retiro tarda','esperando retiro','en proceso retiro',
        ],
        'How to Withdraw':     [
            'cómo retirar','como retirar','come prelevare','how to withdraw','how do i withdraw',
            'quiero retirar','voglio prelevare','want to withdraw','método de retiro',
            'metodo prelievo','withdrawal method','puedo retirar',
        ],
        'Rejected / Blocked':  [
            'withdrawal rejected','retiro rechazado','prelievo rifiutato','saque recusado',
            'withdrawal denied','refused withdrawal','no me dejan retirar',
            'no puedo retirar','cannot withdraw','non riesco a prelevare',
        ],
        'Verification Required': [
            'verification needed','verifica richiesta','verificación requerida',
            'verificação necessária','need documents','documenti richiesti',
            'kyc withdrawal','identity check','verify to withdraw',
        ],
    },
    'Bonus & Promotions': {
        'Bonus Not Credited':  [
            'bonus not credited','bono no acreditado','bonus non accreditato','bonus não creditado',
            'where is my bonus','no recibí el bono','no recibi el bono','mi bono no aparece',
            'bonus mancante','bonus missing','no se acreditó el bono','no se acredito el bono',
        ],
        'Welcome / First Deposit Bonus': [
            'welcome bonus','bono bienvenida','bonus benvenuto','bônus de boas-vindas',
            'first deposit bonus','primer depósito bonus','bono primer deposito',
        ],
        'Free Spins':          [
            'free spin','giri gratis','giros gratis','rodadas grátis','freespin',
            'tiradas gratis','giros gratuitos','free rounds',
        ],
        'Cashback':            [
            'cashback','cash back','rimborso','reembolso','devolución','devolucion',
            'cash de vuelta',
        ],
        'How to Use / Activate': [
            'como usar el bono','cómo usar el bono','come usare il bonus','how to use bonus',
            'activar bono','activate bonus','attivare bonus','activar promocion',
            'wagering','rollover','requisito','playthrough','termini bonus',
        ],
        'Promo Code':          [
            'promo code','código promo','código promocional','codice promo',
            'coupon','voucher','código bono','ingresar código',
        ],
    },
    'Account & Security': {
        'Login / Password':    [
            'cannot login','no puedo entrar','non riesco ad accedere','não consigo entrar',
            'login problem','forgot password','contraseña olvidada','password dimenticata',
            'recuperar contraseña','reset password','cambiar contraseña','no recuerdo',
            'access denied','no accedo','no puedo acceder','no puedo ingresar',
        ],
        'Account Blocked':     [
            'account blocked','cuenta bloqueada','account bloccato','conta bloqueada',
            'suspended','sospeso','banned','mi cuenta está bloqueada','bloqueo de cuenta',
            'account locked','locked out','no me deja entrar','no puedo entrar a mi cuenta',
        ],
        'KYC / Verification':  [
            'kyc','verify account','verifica conto','verificar cuenta','verificar conta',
            'identity verification','id verification','upload documents','caricare documenti',
            'passport','pasaporte','selfie','dni','documento','cedula','cédula',
            'comprobante','verificacion','verificación','verificatione',
        ],
        'Registration':        [
            'register','registrazione','registro','registrar','sign up','create account',
            'abrir cuenta','crear cuenta','aprire conto','abrir uma conta','come mi registro',
            'cómo me registro','cómo registrarme','new account','nueva cuenta',
        ],
        'Profile / Data Update': [
            'change email','cambiar email','cambiare email','change phone','cambiar teléfono',
            'update profile','datos personales','dati personali','personal data',
            'cambiar nombre','change name',
        ],
        'Close Account':       [
            'close account','cerrar cuenta','chiudere conto','fechar conta',
            'self exclusion','autoesclusione','delete account','cancel account',
            'quiero cerrar','voglio chiudere',
        ],
    },
    'Casino': {
        'Slot Games':          [
            'slot','slots','tragamonedas','tragaperras','slot machine','machine slot',
            'slot not loading','slot no carga','slot bloccata','slot problem',
        ],
        'Live Casino':         [
            'live casino','casino en vivo','live dealer','live roulette','live blackjack',
            'live baccarat','dealer','croupier','mesa en vivo',
        ],
        'Game Result Dispute': [
            'game result','resultado del juego','wrong result','resultado incorrecto',
            'bet result','dispute game','partida incorrecta','ganancia incorrecta',
        ],
        'Jackpot / Winnings':  [
            'jackpot','vincita','ganancia','ganancias','winnings','premio','prize',
            'big win','gané','gané y no','premio no acreditado',
        ],
        'Game Not Loading':    [
            'game not loading','juego no carga','juego no abre','juego no funciona',
            'gioco non carica','jogo não carrega','no puedo jugar','cannot play',
        ],
    },
    'Sports Betting': {
        'Bet Settlement':      [
            'settlement','liquidación','liquidazione','liquidação','settled wrong',
            'bet not settled','apuesta no liquidada','scommessa non liquidata',
            'resultado incorrecto apuesta','wrong settlement',
        ],
        'Bet Cancelled':       [
            'cancelled bet','apuesta cancelada','scommessa annullata','aposta cancelada',
            'voided bet','bet void','match cancelled','partita annullata','anulada',
        ],
        'Live Betting':        [
            'live bet','apuesta en vivo','scommessa live','aposta ao vivo',
            'in-play','in play','apuesta vivo',
        ],
        'How to Bet':          [
            'cómo apostar','como apostar','come scommettere','how to bet','how to place bet',
            'quiero apostar','voglio scommettere','colocar apuesta','hacer una apuesta',
        ],
        'Odds / Markets':      [
            'odds','quota','cuota','cota','cuotas','mercados','markets','changed odds',
            'quota cambiata','odds changed','apuesta bloqueada','mercado cerrado',
        ],
    },
    'Technical Issues': {
        'App Not Working':     [
            'app crash','app not working','app non funziona','app no funciona','app no abre',
            'app freezes','app error','app bug','aplicación no','aplicacion no',
        ],
        'Website / Page Error': [
            'website down','sito non funziona','sitio no funciona','site fora do ar',
            'page not load','pagina no carga','page error','no carga la página',
            'no carga la pagina','error en la página',
        ],
        'Login / Access Error': [
            'error al iniciar','error de acceso','error login','cannot access',
            'no puedo acceder al sitio','error al entrar','error de inicio',
        ],
        'Mobile / Browser':    [
            'mobile','iphone','android','ios','smartphone','browser','chrome','safari',
            'teléfono','telefono','celular','not compatible',
        ],
    },
    'Payment Methods': {
        'Bank Transfer':       [
            'bank transfer','transferencia bancaria','transferência bancária','bonifico',
            'wire transfer','iban','swift','transferencia','transfer bancario',
            'transferir desde banco','deposito bancario',
        ],
        'Credit / Debit Card': [
            'visa','mastercard','credit card','debit card','tarjeta','tarjeta de crédito',
            'carta credito','carta debito','cartão','cartao','tarjeta bancaria',
        ],
        'E-Wallet':            [
            'skrill','neteller','paypal','mifinity','ecopayz','jeton','much better',
            'wallet','billetera','monedero','portafoglio',
        ],
        'Crypto':              [
            'bitcoin','btc','ethereum','eth','usdt','tether','crypto','criptomoneda',
            'cryptocurrency','blockchain','criptografia','cripto',
        ],
        'Local Methods (PIX/MBway)': [
            'pix','mbway','multibanco','trustly','efecty','oxxo','spei','mercado pago',
            'nequi','daviplata','local payment','pago local',
        ],
    },
    'Responsible Gaming': {
        'Self Exclusion':      [
            'self exclusion','autoesclusione','exclusión voluntaria','autoexclusão',
            'exclude myself','voglio escludermi','quiero excluirme','cerrar mi cuenta por',
        ],
        'Deposit / Spend Limit': [
            'deposit limit request','set limit','imposta limite','gambling limit',
            'limite de depósito','quiero poner un límite','límite de gasto',
        ],
        'Problem Gambling':    [
            'gambling problem','problema gioco','addiction','dipendenza',
            'juego compulsivo','juego problemático','necesito ayuda con el juego',
        ],
    },
    'General Inquiry': {
        'Account Info':        [
            'mi cuenta','mia account','my account','saldo','balance','my balance',
            'cuál es mi saldo','quanto ho','how much','informazioni conto',
            'mis datos','i miei dati',
        ],
        'Promotions Info':     [
            'hay promociones','ci sono promozioni','any promotions','promozioni disponibili',
            'qué bonos','che bonus','what bonuses','ofertas disponibles',
        ],
        'General Question':    [
            'hola','buenas','ciao','hello','hi','oi','salve','buongiorno','good day',
            'pregunta','domanda','question','consulta','información','informacion',
        ],
        'Complaint':           [
            'queja','reclamo','reclami','complaint','reclamação','reclamacao',
            'quiero quejarme','voglio lamentarmi','disgusted','insoddisfatto',
            'pésimo servicio','pessimo servizio','terrible','muy malo',
        ],
    },
}

def categorize_full(raw_text):
    """Returns (category, subcategory). Extracts user chat lines first."""
    # Try to extract actual user messages from chat transcripts
    user_text = extract_user_text(raw_text)
    # Combine both for matching (user text weighted 2x by duplicating)
    text = (user_text + ' ' + user_text + ' ' + (raw_text or '')).lower()
    best_cat, best_sub, best_score = 'General Inquiry', 'General Question', 0
    for cat, subcats in TAXONOMY.items():
        for sub, keywords in subcats.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > best_score:
                best_score = score
                best_cat, best_sub = cat, sub
    return best_cat, best_sub

# ── LANGUAGE DETECTION ────────────────────────────────────────────────────────
LANG_PATTERNS = {
    'Spanish':    ['hola','gracias','por favor','ayuda','no puedo','tengo','cómo','deposito',
                   'retiro','cuenta','bono','quiero','necesito','estoy','mi cuenta','porqué','señor'],
    'Italian':    ['ciao','grazie','per favore','aiuto','non riesco','deposito','prelievo',
                   'problema','salve','buongiorno','vorrei','non ho ricevuto','ho fatto','mio conto'],
    'Portuguese': ['olá','obrigado','por favor','ajuda','não consigo','depósito','saque',
                   'preciso','quero','minha','não recebi','fiz','minha conta','transferência'],
    'English':    ['hello','hi','please','help','cannot','deposit','withdraw','account',
                   'need','want','have','issue','problem','not received','my account'],
}

def detect_language(text):
    text = (text or '').lower()
    scores = {lang: sum(1 for w in words if w in text) for lang, words in LANG_PATTERNS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else 'Unknown'

# ── FETCH ─────────────────────────────────────────────────────────────────────
def get_json(url, retries=4):
    for attempt in range(retries):
        try:
            r = requests.get(url, auth=AUTH, timeout=30)
            if r.status_code == 429:
                wait = int(r.headers.get('Retry-After', 15))
                print(f'  Rate limited — waiting {wait}s...')
                time.sleep(wait)
                continue
            if r.status_code == 422:
                return None
            r.raise_for_status()
            return r.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            wait = 5 * (attempt + 1)
            print(f'  Connection error (attempt {attempt+1}/{retries}), retry in {wait}s...')
            time.sleep(wait)
    print(f'  Skipping: {url[-60:]}')
    return None

def fetch_tickets_range(start, end):
    tickets, url = [], (
        f'{BASE}/search.json?query=type:ticket+created>{start}+created<{end}'
        f'&sort_by=created_at&sort_order=asc&per_page=100'
    )
    while url:
        data = get_json(url)
        if data is None:
            break
        tickets.extend(data.get('results', []))
        url = data.get('next_page')
    return tickets

# ── MAIN ──────────────────────────────────────────────────────────────────────
print('=' * 58)
print('  BetonWin — Full Ticket Analysis with Subcategories')
print('  Period: January 2026')
print('=' * 58)

print('\nFetching tickets (week by week)...')
weeks = [
    ('2026-01-01T00:00:00Z', '2026-01-08T00:00:00Z'),
    ('2026-01-08T00:00:00Z', '2026-01-15T00:00:00Z'),
    ('2026-01-15T00:00:00Z', '2026-01-22T00:00:00Z'),
    ('2026-01-22T00:00:00Z', '2026-02-01T00:00:00Z'),
]

all_tickets, seen_ids = [], set()
for w_start, w_end in weeks:
    batch = fetch_tickets_range(w_start, w_end)
    new   = [t for t in batch if t['id'] not in seen_ids]
    seen_ids.update(t['id'] for t in new)
    all_tickets.extend(new)
    print(f'  {w_start[:10]} → {w_end[:10]}: {len(new)} tickets')

print(f'\nTotal: {len(all_tickets)} unique tickets')

print('\nFetching comments...')
ticket_comments = {}
for i, t in enumerate(all_tickets):
    data = get_json(f'{BASE}/tickets/{t["id"]}/comments.json')
    if data:
        ticket_comments[t['id']] = data.get('comments', [])
    if (i + 1) % 50 == 0:
        print(f'  {i+1}/{len(all_tickets)} comments fetched...')
    time.sleep(0.05)

print(f'Done. Comments for {len(ticket_comments)} tickets.')

# ── ANALYZE ───────────────────────────────────────────────────────────────────
print('\nAnalyzing & classifying...')
stats = {
    'total':           len(all_tickets),
    'by_status':       defaultdict(int),
    'by_category':     defaultdict(int),
    'by_subcategory':  defaultdict(lambda: defaultdict(int)),
    'by_priority':     defaultdict(int),
    'by_language':     defaultdict(int),
    'by_week':         defaultdict(int),
    'resolution_hours':[],
    'comments_total':  0,
    'ticket_details':  [],
}

for t in all_tickets:
    subject  = t.get('subject', '') or ''
    desc     = t.get('description', '') or ''
    status   = t.get('status', 'unknown')
    priority = t.get('priority') or 'normal'
    created  = t.get('created_at', '')
    solved   = t.get('updated_at', '')

    comments = ticket_comments.get(t['id'], [])
    comment_text = ' '.join(c.get('body', '') or '' for c in comments)
    stats['comments_total'] += len(comments)

    full_text = subject + ' ' + desc + ' ' + comment_text
    category, subcategory = categorize_full(full_text)
    language = detect_language(full_text)

    if created:
        day  = int(created[8:10])
        week = f'Week {min(4, (day-1)//7 + 1)}'
        stats['by_week'][week] += 1

    stats['by_status'][status]     += 1
    stats['by_category'][category] += 1
    stats['by_subcategory'][category][subcategory] += 1
    stats['by_priority'][priority] += 1
    stats['by_language'][language] += 1

    if status == 'solved' and created and solved:
        try:
            c = datetime.fromisoformat(created.replace('Z','+00:00'))
            s = datetime.fromisoformat(solved.replace('Z','+00:00'))
            stats['resolution_hours'].append((s - c).total_seconds() / 3600)
        except: pass

    stats['ticket_details'].append({
        'id':       t.get('id'),
        'subject':  subject[:65],
        'status':   status,
        'category': category,
        'subcat':   subcategory,
        'language': language,
        'priority': priority,
        'created':  created[:10] if created else '',
        'comments': len(comments),
    })

avg_res      = round(sum(stats['resolution_hours']) / len(stats['resolution_hours']), 1) if stats['resolution_hours'] else 0
avg_comments = round(stats['comments_total'] / max(stats['total'], 1), 1)
open_n       = stats['by_status'].get('open',0) + stats['by_status'].get('new',0)
solved_n     = stats['by_status'].get('solved',0)
pct_solved   = round(solved_n / max(stats['total'],1) * 100)

# ── PDF ───────────────────────────────────────────────────────────────────────
print('\nGenerating PDF...')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                Table, TableStyle, HRFlowable, PageBreak)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

GREEN = colors.HexColor('#39d353')
DARK  = colors.HexColor('#0f1623')
GRAY  = colors.HexColor('#8892a4')
LGRAY = colors.HexColor('#f5f5f5')
MGRAY = colors.HexColor('#e8e8e8')

def sty(name, **kw):
    return ParagraphStyle(name, **kw)

title_s = sty('t', fontSize=20, textColor=DARK,  fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=3)
sub_s   = sty('s', fontSize=10, textColor=GRAY,  alignment=TA_CENTER, spaceAfter=2)
h2_s    = sty('h2',fontSize=13, textColor=DARK,  fontName='Helvetica-Bold', spaceBefore=12, spaceAfter=5)
h3_s    = sty('h3',fontSize=10, textColor=colors.HexColor('#1a4731'), fontName='Helvetica-Bold', spaceBefore=8, spaceAfter=3)
body_s  = sty('b', fontSize=9.5,textColor=colors.HexColor('#333'), leading=15)
cap_s   = sty('c', fontSize=8,  textColor=GRAY,  alignment=TA_CENTER)
kpi_v_s = sty('kv',fontSize=24, textColor=GREEN, fontName='Helvetica-Bold', alignment=TA_CENTER)
kpi_l_s = sty('kl',fontSize=7.5,textColor=GRAY,  alignment=TA_CENTER)
tag_s   = sty('tg',fontSize=8,  textColor=colors.HexColor('#555'))

def bar_h(data, title, color='#39d353', figsize=(6.5, 3.5)):
    fig, ax = plt.subplots(figsize=figsize)
    labels, vals = list(data.keys()), list(data.values())
    colors_list = [color] * len(vals)
    bars = ax.barh(labels, vals, color=colors_list, edgecolor='white', linewidth=0.4)
    ax.set_xlabel('Tickets', fontsize=8)
    ax.set_title(title, fontsize=10, fontweight='bold', pad=6)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    ax.tick_params(labelsize=7.5)
    for bar, v in zip(bars, vals):
        ax.text(v + 0.5, bar.get_y() + bar.get_height()/2, str(v), va='center', fontsize=7.5)
    plt.tight_layout()
    buf = io.BytesIO(); fig.savefig(buf, format='png', dpi=140, bbox_inches='tight')
    plt.close(fig); buf.seek(0); return buf

def pie_c(data, title, figsize=(4, 3)):
    palette = ['#39d353','#2aa644','#4ade6e','#22c55e','#86efac','#bbf7d0','#dcfce7','#a3e635','#f0fdf4']
    fig, ax = plt.subplots(figsize=figsize)
    ax.pie(list(data.values()), labels=list(data.keys()), colors=palette[:len(data)],
           autopct='%1.0f%%', startangle=140, textprops={'fontsize': 7})
    ax.set_title(title, fontsize=10, fontweight='bold', pad=5)
    plt.tight_layout()
    buf = io.BytesIO(); fig.savefig(buf, format='png', dpi=140, bbox_inches='tight')
    plt.close(fig); buf.seek(0); return buf

def line_c(data, title, figsize=(6.5, 2.8)):
    x, y = list(data.keys()), list(data.values())
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(x, y, color='#39d353', lw=2.5, marker='o', ms=7, markerfacecolor='white', markeredgewidth=2)
    ax.fill_between(x, y, alpha=0.1, color='#39d353')
    ax.set_title(title, fontsize=10, fontweight='bold', pad=5)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    ax.tick_params(labelsize=8)
    for xi, yi in zip(x, y):
        ax.text(xi, yi + max(y)*0.04, str(yi), ha='center', fontsize=8.5, fontweight='bold', color='#2aa644')
    plt.tight_layout()
    buf = io.BytesIO(); fig.savefig(buf, format='png', dpi=140, bbox_inches='tight')
    plt.close(fig); buf.seek(0); return buf

def subcat_bar(cat_name, sub_data, figsize=(6, 2.6)):
    """Horizontal bar for subcategories of a single category."""
    sorted_d = dict(sorted(sub_data.items(), key=lambda x: -x[1]))
    palette  = ['#39d353','#2aa644','#4ade6e','#22c55e','#86efac','#bbf7d0','#a3e635']
    fig, ax  = plt.subplots(figsize=figsize)
    labels, vals = list(sorted_d.keys()), list(sorted_d.values())
    bars = ax.barh(labels, vals, color=palette[:len(vals)], edgecolor='white', linewidth=0.3)
    ax.set_title(f'{cat_name} — Subcategories', fontsize=9, fontweight='bold', pad=5)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    ax.tick_params(labelsize=7)
    for bar, v in zip(bars, vals):
        ax.text(v + 0.3, bar.get_y() + bar.get_height()/2, str(v), va='center', fontsize=7)
    plt.tight_layout()
    buf = io.BytesIO(); fig.savefig(buf, format='png', dpi=130, bbox_inches='tight')
    plt.close(fig); buf.seek(0); return buf

# ─────────────────────────────────────────────────────────────────────────────
doc   = SimpleDocTemplate('zendesk_report_jan2026.pdf', pagesize=A4,
                          leftMargin=1.8*cm, rightMargin=1.8*cm,
                          topMargin=1.8*cm, bottomMargin=1.8*cm)
story = []

# ── PAGE 1: Cover + KPIs + Weekly trend ──────────────────────────────────────
story.append(Paragraph('BetonWin Support — Ticket Analysis', title_s))
story.append(Paragraph('January 2026 · Full Month · Categories & Subcategories', sub_s))
story.append(HRFlowable(width='100%', thickness=2, color=GREEN, spaceAfter=12))

kpi_data = [[
    Paragraph(str(stats['total']),  kpi_v_s),
    Paragraph(str(open_n),          kpi_v_s),
    Paragraph(f'{pct_solved}%',     kpi_v_s),
    Paragraph(f'{avg_res}h',        kpi_v_s),
    Paragraph(str(avg_comments),    kpi_v_s),
],[
    Paragraph('Total Tickets',      kpi_l_s),
    Paragraph('Open / New',         kpi_l_s),
    Paragraph('Resolved',           kpi_l_s),
    Paragraph('Avg Resolution',     kpi_l_s),
    Paragraph('Avg Comments',       kpi_l_s),
]]
kt = Table(kpi_data, colWidths=[3.15*cm]*5)
kt.setStyle(TableStyle([
    ('BACKGROUND', (0,0),(-1,-1), LGRAY),
    ('BOX',        (0,0),(-1,-1), 0.5, GRAY),
    ('INNERGRID',  (0,0),(-1,-1), 0.3, GRAY),
    ('VALIGN',     (0,0),(-1,-1), 'MIDDLE'),
    ('TOPPADDING',    (0,0),(-1,-1), 10),
    ('BOTTOMPADDING', (0,0),(-1,-1), 10),
]))
story.append(kt)
story.append(Spacer(1, 12))

week_sorted = {k: stats['by_week'][k] for k in sorted(stats['by_week'].keys())}
story.append(Paragraph('Weekly Volume', h2_s))
story.append(Image(line_c(week_sorted, 'Tickets per Week — January 2026'), width=14.5*cm, height=5.8*cm))

# ── PAGE 2: Category overview ─────────────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph('Ticket Categories Overview', h2_s))

cat_sorted = dict(sorted(stats['by_category'].items(), key=lambda x: -x[1]))
story.append(Image(bar_h(cat_sorted, 'All Tickets by Category'), width=14.5*cm, height=7*cm))
story.append(Spacer(1, 10))

story.append(Paragraph('Status & Language Distribution', h2_s))
s_buf = pie_c(dict(stats['by_status']),   'By Status',   (3.5, 2.8))
l_buf = pie_c(dict(stats['by_language']), 'By Language', (3.5, 2.8))
row = Table([[Image(s_buf, 8*cm, 6.5*cm), Image(l_buf, 8*cm, 6.5*cm)]])
row.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP')]))
story.append(row)

# ── PAGES 3+: Subcategory detail per category ─────────────────────────────────
story.append(PageBreak())
story.append(Paragraph('Detailed Breakdown by Category & Subcategory', h2_s))
story.append(HRFlowable(width='100%', thickness=1, color=GREEN, spaceAfter=8))

# Build subcategory tables — 2 per page, alternating with charts
cats_by_volume = sorted(stats['by_subcategory'].keys(),
                        key=lambda c: -stats['by_category'][c])

for idx, cat in enumerate(cats_by_volume):
    sub_data = dict(stats['by_subcategory'][cat])
    if not sub_data:
        continue
    total_cat = stats['by_category'][cat]
    pct_cat   = round(total_cat / max(stats['total'],1) * 100, 1)

    story.append(Paragraph(f'{cat} — {total_cat} tickets ({pct_cat}%)', h3_s))

    # Subcategory bar chart
    sub_sorted = dict(sorted(sub_data.items(), key=lambda x: -x[1]))
    story.append(Image(subcat_bar(cat, sub_sorted), width=14.5*cm, height=max(2.5, len(sub_sorted)*0.55)*cm))

    # Subcategory table
    sub_rows = [['Subcategory', 'Tickets', '% of Category', '% of Total']]
    for sub, cnt in sorted(sub_data.items(), key=lambda x: -x[1]):
        pct_of_cat   = round(cnt / max(total_cat,1) * 100, 1)
        pct_of_total = round(cnt / max(stats['total'],1) * 100, 1)
        sub_rows.append([sub, str(cnt), f'{pct_of_cat}%', f'{pct_of_total}%'])

    sub_tbl = Table(sub_rows, colWidths=[7*cm, 2.5*cm, 3*cm, 2.8*cm])
    sub_tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,0),  DARK),
        ('TEXTCOLOR',     (0,0),(-1,0),  colors.white),
        ('FONTNAME',      (0,0),(-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0,0),(-1,-1), 8),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [colors.white, LGRAY]),
        ('GRID',          (0,0),(-1,-1), 0.3, GRAY),
        ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0),(-1,-1), 4),
        ('BOTTOMPADDING', (0,0),(-1,-1), 4),
        ('ALIGN',         (1,0),(-1,-1), 'CENTER'),
    ]))
    story.append(sub_tbl)
    story.append(Spacer(1, 12))

    if idx < len(cats_by_volume) - 1 and (idx + 1) % 2 == 0:
        story.append(PageBreak())

# ── TICKET TABLE ─────────────────────────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph(f'Ticket Detail — Top 50 (of {stats["total"]} total)', h2_s))
hdr = ['ID', 'Subject', 'Category', 'Subcategory', 'Lang', 'Status', 'C', 'Date']
rows = [hdr]
for t in stats['ticket_details'][:50]:
    rows.append([
        str(t['id']),
        (t['subject'][:40]+'…') if len(t['subject'])>40 else t['subject'],
        t['category'], t['subcat'], t['language'],
        t['status'], str(t['comments']), t['created'],
    ])
tbl = Table(rows, colWidths=[1.1*cm, 5.2*cm, 2*cm, 2.3*cm, 1.5*cm, 1.3*cm, 0.7*cm, 1.6*cm])
tbl.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,0),  DARK),
    ('TEXTCOLOR',     (0,0),(-1,0),  colors.white),
    ('FONTNAME',      (0,0),(-1,0),  'Helvetica-Bold'),
    ('FONTSIZE',      (0,0),(-1,-1), 6.5),
    ('ROWBACKGROUNDS',(0,1),(-1,-1), [colors.white, LGRAY]),
    ('GRID',          (0,0),(-1,-1), 0.3, GRAY),
    ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
    ('TOPPADDING',    (0,0),(-1,-1), 3),
    ('BOTTOMPADDING', (0,0),(-1,-1), 3),
]))
story.append(tbl)

# ── KEY INSIGHTS ──────────────────────────────────────────────────────────────
story.append(PageBreak())
story.append(HRFlowable(width='100%', thickness=2, color=GREEN, spaceAfter=10))
story.append(Paragraph('Key Insights — January 2026', h2_s))

top_cat  = max(stats['by_category'],  key=stats['by_category'].get)
top_lang = max(stats['by_language'],  key=stats['by_language'].get)
top_sub  = max(stats['by_subcategory'][top_cat], key=stats['by_subcategory'][top_cat].get)

insights = [
    (f'<b>Volume:</b> {stats["total"]} tickets in January — '
     f'~{round(stats["total"]/31,1)}/day average.'),
    (f'<b>Top Category:</b> "{top_cat}" leads with {stats["by_category"][top_cat]} tickets '
     f'({round(stats["by_category"][top_cat]/stats["total"]*100,1)}%).'),
    (f'<b>Top Subcategory:</b> "{top_sub}" is the #1 specific issue within {top_cat} '
     f'({stats["by_subcategory"][top_cat][top_sub]} tickets).'),
    (f'<b>Language:</b> {top_lang} is dominant '
     f'({stats["by_language"][top_lang]} tickets, '
     f'{round(stats["by_language"][top_lang]/stats["total"]*100,1)}%).'),
    (f'<b>Resolution:</b> {pct_solved}% resolved — {open_n} tickets still open.'),
    (f'<b>Avg Resolution Time:</b> {avg_res} hours.'),
    (f'<b>Engagement:</b> {stats["comments_total"]} total comments analysed '
     f'(avg {avg_comments} per ticket).'),
]
for line in insights:
    story.append(Paragraph(f'• {line}', body_s))
    story.append(Spacer(1, 5))

story.append(Spacer(1, 14))
story.append(Paragraph('Full Category + Subcategory Summary', h2_s))

summ_rows = [['Category', 'Subcategory', 'Tickets', '% Total']]
for cat in cats_by_volume:
    for sub, cnt in sorted(stats['by_subcategory'][cat].items(), key=lambda x: -x[1]):
        pct = round(cnt / max(stats['total'],1) * 100, 1)
        summ_rows.append([cat, sub, str(cnt), f'{pct}%'])

summ_tbl = Table(summ_rows, colWidths=[4.5*cm, 5.5*cm, 2.5*cm, 2.5*cm])
summ_tbl.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,0),  DARK),
    ('TEXTCOLOR',     (0,0),(-1,0),  colors.white),
    ('FONTNAME',      (0,0),(-1,0),  'Helvetica-Bold'),
    ('FONTSIZE',      (0,0),(-1,-1), 8),
    ('ROWBACKGROUNDS',(0,1),(-1,-1), [colors.white, LGRAY]),
    ('GRID',          (0,0),(-1,-1), 0.3, GRAY),
    ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
    ('TOPPADDING',    (0,0),(-1,-1), 4),
    ('BOTTOMPADDING', (0,0),(-1,-1), 4),
    ('ALIGN',         (2,0),(-1,-1), 'CENTER'),
]))
story.append(summ_tbl)

story.append(Spacer(1, 12))
story.append(Paragraph(
    f'Report generated {datetime.now().strftime("%d %b %Y %H:%M")} · '
    f'Source: Zendesk betonwin · {stats["total"]} tickets · {stats["comments_total"]} comments',
    cap_s))

doc.build(story)
print(f'\n✅ Report saved: zendesk_report_jan2026.pdf')
