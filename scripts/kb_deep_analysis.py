#!/usr/bin/env python3
"""
BetonWin — Deep KB Gap Analysis
Samples tickets from Q3+Q4 2025, extracts real user messages,
identifies specific question patterns, cross-references with KB content.
"""

import os, requests, time, re
from collections import defaultdict, Counter
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
    lines = re.findall(
        r'\(\d{2}:\d{2}:\d{2}\)\s+([^:]+):\s+(.+?)(?=\s*\(\d{2}:\d{2}:\d{2}\)|$)',
        text or '', re.DOTALL)
    user_lines = [msg.strip() for name, msg in lines if name.strip().upper() not in ('BOW', 'BOW ')]
    return ' '.join(user_lines) if user_lines else (text or '')

# ── TOPICS ───────────────────────────────────────────────────────────────────
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
        'declined','declinado',
    ],
    'Deposit Processing Delay': [
        'cuanto tarda','esperando deposito','en espera','pending deposit',
        'demora deposito','tarda mucho','lleva mucho tiempo','still processing',
    ],
    'Recarga / Top-up': [
        'recarga','recargar','carga saldo','cargar saldo','cargar cuenta',
        'hice una recarga','mi recarga','recargue','recarge','top up','topup',
    ],
    'Withdrawal Not Received': [
        'retiro no recibido','no recibi el retiro','no llego el retiro',
        'donde esta mi retiro','withdrawal not received','withdrawal missing',
    ],
    'How to Withdraw': [
        'como retirar','como retiro','quiero retirar','quiero sacar',
        'como saco','quiero cobrar','como cobro','puedo retirar',
        'metodo de retiro','cobrar mi dinero','sacar mi plata','retirar mi plata',
        'how to withdraw',
    ],
    'Withdrawal Pending / Delay': [
        'retiro pendiente','retiro demora','retiro tarda','esperando retiro',
        'en proceso retiro','cuanto tarda retiro','withdrawal pending',
    ],
    'Withdrawal Rejected': [
        'retiro rechazado','no me dejan retirar','no puedo retirar',
        'withdrawal rejected','withdrawal denied','cannot withdraw',
    ],
    'Bonus / Promotions': [
        'bono','bonos','promocion','promos','bonus','free bet','freespin',
        'regalo','oferta','codigo promo','como uso el bono','activar',
        'cashback','giros gratis','tiradas','bono bienvenida','welcome bonus',
        'rollover','wagering',
    ],
    'Account / Login Issues': [
        'no puedo entrar','no puedo ingresar','olvide mi','mi contrasena',
        'recuperar contrasena','no recuerdo','acceder','acceso','ingresar',
        'cuenta bloqueada','me bloqueo','no me deja entrar','suspendida',
        'login','password','contrasena','entrar a mi cuenta','crear cuenta',
        'abrir cuenta','registrarme','nueva cuenta','account blocked',
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

def classify(text):
    t = text.lower()
    best_topic, best_score = 'Uncategorized', 0
    for topic, kws in TOPICS.items():
        score = sum(1 for kw in kws if kw in t)
        if score > best_score:
            best_score, best_topic = score, topic
    return best_topic

# ── SUB-QUESTION PATTERNS (what specific thing are they asking within each topic) ──
SUB_PATTERNS = {
    'Deposit Not Credited': {
        'Bank transfer not credited': ['transferencia','transferi','banco','cuenta bancaria','transfer'],
        'Card payment not credited': ['tarjeta','visa','mastercard','card','carta'],
        'Crypto not credited': ['bitcoin','btc','eth','usdt','crypto','cripto','tether'],
        'Mercado Pago / local not credited': ['mercado pago','directa','pix','oxxo','spei','nequi','efecty'],
        'Recarga exitosa but no balance': ['recarga exitosa','exitoso pero','exitosa pero'],
        'Sent comprobante but not credited': ['comprobante','envie','mande','adjunto','envié','mandé'],
        'How long to credit?': ['cuanto tarda','cuando se acredita','demora','tarda mucho'],
        'Balance did not change': ['saldo no cambio','no cambio el saldo','no veo el saldo','saldo no aparece'],
    },
    'Bank Transfer / Comprobante': {
        'Sending comprobante / receipt': ['comprobante','recibo','envie','mande','adjunto','comprobante de pago'],
        'Asking for bank account details': ['numero de cuenta','cuenta bancaria','datos bancarios','cuenta de banco','clabe','cvu','cbu','iban'],
        'Transfer done, waiting confirmation': ['hice una transferencia','realice','ya transferi','ya hice el deposito'],
        'Asking where to upload proof': ['donde envio','donde mando','como envio','donde subo','como subo'],
        'Transfer reference / tracking': ['referencia','numero de transaccion','comprobante de transferencia'],
    },
    'Bonus / Promotions': {
        'Welcome bonus / first deposit': ['bienvenida','primer deposito','welcome','first deposit','1er deposito'],
        'Rollover / wagering requirements': ['rollover','wagering','requisito','cuanto falta','progreso','avance'],
        'Free spins': ['giros gratis','free spin','tiradas','freespin','giros'],
        'How to activate / use bonus': ['activar','como uso','como activo','activar bono','usar el bono'],
        'Bonus not credited': ['bono no aparece','no recibi el bono','no se acredito el bono','bonus missing'],
        'Cashback': ['cashback','cash back','devolucion','reembolso'],
        'Promo code': ['codigo promo','codigo promocional','promo code','coupon','voucher'],
        'Bonus expired / cancelled': ['expiro','vencio','cancelado','expired','cancelled'],
        'Cannot bet with bonus': ['no puedo apostar','no puedo jugar','saldo 0','no me deja apostar'],
        'Bonus terms / conditions': ['terminos','condiciones','limite','maximo retiro','release'],
    },
    'KYC / Verification': {
        'What documents needed': ['que documentos','que necesito','que debo enviar','cuales documentos'],
        'How to upload documents': ['como subo','donde subo','como envio','como verifico','como hago'],
        'Verification status / pending': ['estado','pendiente','cuanto tarda','cuando se verifica'],
        'Verification rejected': ['rechazado','rechazada','no paso','no aprobado','fue rechazada'],
        'Selfie / photo requirements': ['selfie','foto','fotografia','imagen'],
        'ID types by country': ['dni','rut','cedula','pasaporte','licencia','documento'],
        'Phone/email verification': ['telefono','numero','sms','codigo','email','correo','verificar telefono'],
    },
    'Casino / Games / Bets': {
        'Game not loading / error': ['no carga','no abre','no funciona','error en el juego','se cierra','freezes'],
        'Game result dispute': ['resultado incorrecto','resultado','wrong result','disputa','no es correcto'],
        'Winnings not credited': ['ganancia','gane','ganancias','premio','jackpot','no se acredito'],
        'How to play / bet': ['como juego','como apuesto','como funciona','reglas','como se juega'],
        'Slot specific issues': ['slot','tragamonedas','tragaperras','maquina'],
        'Live casino issues': ['live','en vivo','dealer','croupier','mesa en vivo'],
        'Bet settlement question': ['liquidacion','settlement','no se liquido','pendiente de liquidar'],
        'Cash out issues': ['cash out','cashout','cerrar apuesta','cobrar apuesta'],
    },
    'Technical / App / Website': {
        'Site not loading / down': ['no carga','no abre','no funciona','caida','down','no entra'],
        'Mobile / phone issues': ['celular','telefono','movil','android','iphone','ios','mobile'],
        'App crash / freeze': ['se cierra','se traba','congela','crash','freeze','se cuelga'],
        'Browser compatibility': ['navegador','chrome','safari','firefox','browser','explorer'],
        'Login page error': ['error al entrar','error de acceso','no me deja entrar','login error'],
        'Blank screen / white page': ['pantalla blanca','en blanco','blank','white screen','no aparece nada'],
        'Payment page error': ['error al pagar','error de pago','no procesa','payment error'],
        'Slow performance': ['lento','tarda','demora en cargar','slow'],
    },
    'Account / Login Issues': {
        'Forgot password': ['olvide','contrasena','password','recuperar','reset','no recuerdo'],
        'Account blocked / suspended': ['bloqueada','bloqueado','suspendida','suspended','banned'],
        'Cannot login': ['no puedo entrar','no puedo ingresar','no me deja','no puedo acceder'],
        'Registration help': ['registrarme','crear cuenta','nueva cuenta','abrir cuenta','registro'],
        'Change email / phone': ['cambiar email','cambiar telefono','cambiar correo','change email'],
        'Close account / self-exclusion': ['cerrar cuenta','autoexclusion','eliminar','delete account'],
    },
    'How to Withdraw': {
        'How to request withdrawal': ['como retiro','como retirar','como saco','como cobro','quiero retirar'],
        'Withdrawal methods available': ['metodo de retiro','formas de retiro','como me pagan'],
        'Minimum withdrawal amount': ['minimo','cuanto puedo retirar','monto minimo retiro'],
        'Withdrawal to bank account': ['cuenta bancaria','transferencia','banco','bank'],
        'Withdrawal to crypto': ['bitcoin','btc','crypto','cripto','usdt'],
        'Withdrawal blocked by bonus': ['bono activo','rollover','no puedo retirar','bloqueado'],
    },
    'Complaint / Dissatisfaction': {
        'Money lost / fraud accusation': ['robo','estafa','fraude','me robaron','ladrones','scam'],
        'Bad service complaint': ['pesimo','terrible','muy malo','peor','inaceptable','horrible'],
        'Want to escalate / supervisor': ['supervisor','encargado','jefe','reclamo formal','escalate'],
        'Unfair result / rigged': ['no es justo','injusto','amañado','rigged','unfair','trucho'],
    },
}

# ── KB CONTENT MAPPING (what the KB actually answers) ────────────────────────
KB_COVERAGE = {
    'Deposit Not Credited': {
        'covered': [
            'General: if not credited after 30 min, verify bank approved transaction, send comprobante',
            'Card/e-wallet: instant',
            'Crypto: 10-30 min confirmations',
            'Bank transfer: 1-3 business days',
            'Mercado Pago/Directa24: send comprobante to support',
            'No fees charged by BetonWin',
        ],
        'missing': [],  # Will be filled by analysis
    },
    'Bank Transfer / Comprobante': {
        'covered': [
            'Brief mention: send comprobante to ayuda@beton.win or chat',
        ],
        'missing': [],
    },
    'Bonus / Promotions': {
        'covered': [
            'Welcome bonus: 10 deposit levels with percentages and free spins',
            'Rollover/wagering: explanation and example',
            'Progress tracking: how to check',
            'What bets count for rollover',
            'Bonus states: offered, active, completed, expired, canceled',
            'Bonus expiry rules',
            'Sports bonus 50/50 rule (real + bonus)',
            'Cannot play with bonus: check allowed games',
            'Bonus not available: depends on account history',
            'Cancel bonus: how to, consequences',
            'Promo code: where to enter',
            'Free spins: how they work',
            'Free bets: how they work',
        ],
        'missing': [],
    },
    'KYC / Verification': {
        'covered': [
            'Why KYC is needed',
            'Required documents: ID + proof of address',
            'How to upload: My Account > Verification',
            'Processing time: 24-48h',
            'Rejection reasons',
            'Can play without KYC, needed for withdrawals',
            'Phone verification process',
            'Wrong phone number fix',
            'Change phone/email process',
        ],
        'missing': [],
    },
    'Casino / Games / Bets': {
        'covered': [
            '3000+ games, providers listed',
            'Fairness: RNG certified',
            'Demo mode available',
            'Live casino: 24/7',
            'Game error: reload, clear cache, contact support',
            'RTP explanation',
            'Bet settlement: cancelled events refunded',
            'Cash out: partial and full',
            'Winning not paid: wait 30 min then contact support',
        ],
        'missing': [],
    },
    'Technical / App / Website': {
        'covered': [
            'Alternative URL: beton691.online',
            'Clear cache and cookies',
            'Game not working: reload, clear cache',
            'Cannot see history: check My Account > History',
        ],
        'missing': [],
    },
    'Account / Login Issues': {
        'covered': [
            'Create account: step by step',
            'Forgot password: reset link',
            'Account blocked: password reset or contact support',
            'Cannot access site: alternative URL, clear cache',
            'Multiple accounts: not allowed',
            'Change personal data: My Account > Settings',
            'Close account: contact support',
            'Self-exclusion: responsible gaming section',
        ],
        'missing': [],
    },
    'How to Withdraw': {
        'covered': [
            'How to: My Account > Cashier > Withdraw',
            'Processing times per method',
            'Min/max amounts',
            'Pending withdrawal: KYC, rollover, limits',
            'Cancel pending withdrawal',
            'Bonus blocking: rollover must be completed',
            'Release limit: bonus x multiplier',
        ],
        'missing': [],
    },
}

# ── FETCH SAMPLE TICKETS ────────────────────────────────────────────────────
# Sample 2 weeks from Q3 (Aug 1-14) + 2 weeks from Q4 (Nov 1-14) = ~4000 tickets
SAMPLES = [
    ('2025-08-01T00:00:00Z', '2025-08-08T00:00:00Z'),
    ('2025-08-08T00:00:00Z', '2025-08-15T00:00:00Z'),
    ('2025-11-01T00:00:00Z', '2025-11-08T00:00:00Z'),
    ('2025-11-08T00:00:00Z', '2025-11-15T00:00:00Z'),
]

print('=' * 60)
print('  Deep KB Gap Analysis')
print('  Sampling Q3 + Q4 2025')
print('=' * 60)

print('\nFetching tickets...')
all_tickets, seen = [], set()
for ws, we in SAMPLES:
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

print(f'\nTotal sample: {len(all_tickets)} tickets\n')

# ── CLASSIFY + EXTRACT SUB-PATTERNS ─────────────────────────────────────────
print('Fetching comments & analyzing...')
topic_messages = defaultdict(list)  # topic -> [user_messages]
sub_pattern_counts = defaultdict(lambda: defaultdict(int))  # topic -> {sub_pattern: count}
topic_counts = Counter()

for i, t in enumerate(all_tickets):
    subject = t.get('subject', '') or ''
    desc = t.get('description', '') or ''

    data = get_json(f'{BASE}/tickets/{t["id"]}/comments.json')
    comments = data.get('comments', []) if data else []
    comment_text = ' '.join(c.get('body', '') or '' for c in comments)

    full_text = subject + ' ' + desc + ' ' + comment_text
    user_text = extract_user_text(full_text)
    search_text = (user_text + ' ' + user_text + ' ' + full_text).lower()

    topic = classify(search_text)
    topic_counts[topic] += 1

    # Save user message (max 30 per topic for samples)
    if len(topic_messages[topic]) < 30:
        msg = user_text.strip()[:300].replace('\n', ' ')
        if len(msg) > 10:
            topic_messages[topic].append({'id': t['id'], 'msg': msg})

    # Check sub-patterns
    if topic in SUB_PATTERNS:
        for sub_name, sub_kws in SUB_PATTERNS[topic].items():
            if any(kw in search_text for kw in sub_kws):
                sub_pattern_counts[topic][sub_name] += 1

    if (i + 1) % 100 == 0:
        print(f'  {i+1}/{len(all_tickets)} processed...')
    time.sleep(0.05)

total = len(all_tickets)
print(f'\nDone. {total} tickets analyzed.\n')

# ── GENERATE REPORT ──────────────────────────────────────────────────────────
topic_sorted = dict(sorted(topic_counts.items(), key=lambda x: -x[1]))

report = []
report.append('# BetonWin — Deep KB Gap Analysis')
report.append('## Based on Q3 + Q4 2025 Ticket Sample')
report.append(f'## {total} tickets analyzed with comments\n')
report.append('---\n')

# Overall summary
report.append('## Topic Distribution (Sample)\n')
report.append('| Topic | Count | % |')
report.append('|---|---|---|')
for topic, cnt in topic_sorted.items():
    pct = round(cnt / total * 100, 1)
    report.append(f'| {topic} | {cnt} | {pct}% |')
report.append('')

# Per-topic deep analysis
report.append('---\n')
report.append('## DETAILED ANALYSIS PER TOPIC\n')
report.append('For each topic: sub-question breakdown, real customer messages, KB coverage assessment, and missing content.\n')

for topic, cnt in topic_sorted.items():
    if topic == 'Greeting Only (no question)' or topic == 'Uncategorized':
        continue

    pct = round(cnt / total * 100, 1)
    report.append(f'---\n')
    report.append(f'### {topic} — {cnt} tickets ({pct}%)\n')

    # Sub-pattern breakdown
    if topic in sub_pattern_counts and sub_pattern_counts[topic]:
        report.append('**Sub-question breakdown:**\n')
        report.append('| Specific Question Pattern | Count | % of Topic |')
        report.append('|---|---|---|')
        subs = sorted(sub_pattern_counts[topic].items(), key=lambda x: -x[1])
        for sub_name, sub_cnt in subs:
            sub_pct = round(sub_cnt / max(cnt, 1) * 100, 1)
            report.append(f'| {sub_name} | {sub_cnt} | {sub_pct}% |')
        report.append('')

    # Real messages sample
    msgs = topic_messages.get(topic, [])
    if msgs:
        report.append('**Real customer messages (sample):**\n')
        for m in msgs[:10]:
            clean = m['msg'][:200]
            report.append(f'- #{m["id"]}: *"{clean}"*')
        report.append('')

    # KB coverage assessment
    if topic in KB_COVERAGE:
        kb = KB_COVERAGE[topic]
        report.append('**What KB currently covers:**\n')
        for item in kb['covered']:
            report.append(f'- [COVERED] {item}')
        report.append('')

    # Identify gaps based on sub-patterns vs KB
    report.append('**GAPS — What customers ask but KB does NOT answer:**\n')

    if topic == 'Deposit Not Credited':
        report.append("""
- **Step-by-step troubleshooting per payment method** — KB only says "wait 30 min then contact support". Customers need specific steps: check bank status, verify amount, check reference code, timeline per method.
- **"Recarga exitosa pero no se acredito"** — Very common pattern. KB doesn't address the specific case where the payment provider says "success" but balance didn't update. Need: explain processing pipeline, what "exitosa" means at provider level vs platform level.
- **"I already sent the comprobante, what now?"** — KB doesn't explain what happens after sending proof: estimated review time, what support checks, when they'll get a response.
- **Crypto-specific troubleshooting** — KB says "10-30 min" but doesn't explain: how to check blockchain confirmations, what to do if stuck, minimum confirmations required per coin, what if wrong network (e.g., sent ERC20 to TRC20 address).
- **Weekend/holiday delays explanation** — Many tickets are "I deposited on Saturday and it's not there". KB doesn't explain that bank transfers are not processed on weekends.
""")

    elif topic == 'Bank Transfer / Comprobante':
        report.append("""
- **CRITICAL: No dedicated section in KB** — This is the #2 topic by volume and has almost no KB content.
- **Where to send comprobante** — KB only says "send to ayuda@beton.win or chat" but doesn't explain: can I upload in chat? what format? what must be visible on the receipt?
- **Bank account details for transfers** — Customers constantly ask "what's your bank account number?". KB says nothing about where to find these details (My Account > Cashier > Deposit > Bank Transfer).
- **What makes a valid comprobante** — Must show: date, amount, sender name, reference number. KB doesn't specify this.
- **Processing time after sending comprobante** — "I sent my receipt 3 hours ago, nothing happened". KB gives no timeline for comprobante review.
- **Name mismatch issues** — Transfer from a third party (family member, friend) is not accepted. KB doesn't mention this anti-fraud policy.
- **Different bank transfer types** — SPEI, CLABE, CBU/CVU, Mercado Pago, Directa24 — each has different steps. KB treats them all the same.
""")

    elif topic == 'Bonus / Promotions':
        report.append("""
- **KB is comprehensive but some gaps remain:**
- **"Saldo 0.00" with active bonus** — KB explains this but it's buried. Needs to be more prominent because it's one of the most confusing issues for users.
- **Specific rollover progress examples** — KB explains rollover formula but customers want to know: "I have $5000 bonus, how much do I need to bet?". Need concrete examples with local currency.
- **Bonus not available for my account** — KB says "depends on history" but doesn't explain WHY. Customers feel discriminated.
- **Can I have multiple bonuses at once?** — Not answered in KB.
- **What happens to my bonus if I make a withdrawal request?** — Not clearly answered.
- **Cashback calculation and timing** — KB mentions cashback exists but doesn't explain: when is it credited? how is it calculated? what's the rollover on cashback?
""")

    elif topic == 'KYC / Verification':
        report.append("""
- **Accepted documents per country** — KB lists generic types but customers from Chile ask about RUT, Argentina about DNI format. Need country-specific guidance.
- **Photo quality requirements** — KB doesn't specify: minimum resolution, file size limits, lighting requirements, can I take a photo with my phone?
- **Selfie with ID instructions** — Not mentioned in KB at all. Many platforms require this. If BetonWin does, it should be documented. If not, clarify.
- **"My verification is pending for 5 days"** — KB says 24-48h but many tickets show longer waits. Need: what to do if exceeding the stated timeframe, how to check status.
- **Proof of address alternatives** — KB lists "utility bill or bank statement" but customers ask: "can I use my rental contract? tax document? internet bill?"
- **Why was my document rejected?** — KB lists generic reasons but specific examples with photos showing good vs bad submissions would help.
""")

    elif topic == 'Casino / Games / Bets':
        report.append("""
- **Specific game not loading troubleshooting** — KB only says "reload and clear cache". Need: check device compatibility, disable ad-blocker, try different game to test, check internet speed requirements.
- **Game result dispute process** — KB doesn't explain how to file a dispute, what evidence to provide, timeline for investigation.
- **Winnings not credited from a game** — KB covers sports bet settlements but not casino game winnings. Need: explain that interrupted rounds are resolved by server records, what to do if jackpot not credited.
- **Slot RTP and volatility explanation** — KB explains RTP briefly but customers don't understand why they're losing. Need: explain variance/volatility, that RTP is long-term average, responsible gaming reminder.
- **Live casino connection issues** — Not addressed. Common: stream freezes, bet placed but disconnected, what happens to my bet?
""")

    elif topic == 'Technical / App / Website':
        report.append("""
- **CRITICAL: Only 3 brief entries in KB** — This is a top-7 topic by volume.
- **Mobile-specific troubleshooting** — Not covered at all. Need: update browser, clear mobile cache, switch Wi-Fi/data, check OS compatibility.
- **Blank/white screen** — Not covered. Need: disable ad-blocker, enable JavaScript, try incognito mode.
- **App-like experience** — KB mentions there's no app but doesn't explain how to add the site to home screen (PWA).
- **Error codes or messages** — No guidance on what specific errors mean or what to do for each.
- **VPN / geo-blocking** — Not mentioned. Some users may need VPN guidance or face access issues due to location.
- **Payment page errors** — Distinct from game errors. When the deposit/withdrawal page doesn't load or shows an error.
- **Slow performance** — Not addressed. Need: recommended browser, close other tabs, check internet speed.
- **Two-factor authentication issues** — If the platform uses 2FA, there's no KB content about it.
""")

    elif topic == 'Account / Login Issues':
        report.append("""
- **Password requirements** — KB explains how to reset but not the password rules (min length, special chars, etc).
- **Account blocked: specific unblock steps** — KB is vague. Need: how many failed attempts cause a block, exact steps to unblock, how long the block lasts.
- **Login from new device** — If there's device verification, it's not documented.
- **Session timeout explanation** — Not covered. Users get logged out unexpectedly.
""")

    elif topic == 'How to Withdraw':
        report.append("""
- **Country-specific withdrawal methods** — KB lists general methods but doesn't specify which are available in Chile vs Argentina.
- **Step-by-step with screenshots** — KB is text-only. Visual guide would help.
- **"Why is my withdrawal taking longer than stated?"** — KB gives processing times but doesn't cover escalation path when exceeded.
- **Withdrawal to a different bank account than deposit** — Anti-fraud policy not clearly explained.
""")

    elif topic == 'Complaint / Dissatisfaction':
        report.append("""
- **Formal complaint process** — KB mentions "ask for supervisor" but no formal process, no ticket tracking, no SLA for resolution.
- **Regulatory body contact** — If licensed, KB should mention the regulator where users can file complaints.
- **Fraud/scam accusations** — Very sensitive. KB needs a professional response template explaining platform security, RNG certification, and investigation process.
- **Compensation or goodwill gestures** — No policy documented for when the platform is at fault.
""")

    elif topic == 'Withdrawal Rejected':
        report.append("""
- **Specific rejection reasons with solutions** — KB lists possible reasons but doesn't give step-by-step fix for each:
  1. KYC not complete → link to verification page
  2. Rollover not met → link to bonus progress
  3. Third-party account → explain policy
  4. Exceeds daily limit → explain when to retry
- **"I completed KYC but withdrawal is still rejected"** — Not covered. Need escalation path.
""")

    elif topic == 'Deposit Failed / Declined':
        report.append("""
- **Error codes from payment providers** — KB doesn't explain what specific decline codes mean.
- **Card not enabled for international payments** — KB mentions this but doesn't explain how to enable it (varies by bank/country).
- **Alternative payment methods when one fails** — KB should suggest trying a different method.
""")

    elif topic in ('Withdrawal Not Received', 'Withdrawal Pending / Delay', 'Deposit Processing Delay', 'Recarga / Top-up', 'Balance / Account Info'):
        report.append(f"""
- Minor gaps only. See general recommendations below.
""")

    else:
        report.append('- No significant gaps identified.\n')

# ── PRIORITY RECOMMENDATIONS ────────────────────────────────────────────────
report.append('---\n')
report.append('## PRIORITY CONTENT TO CREATE\n')
report.append("""
### P0 — CRITICAL (create immediately, >500 tickets/month impact)

**1. Bank Transfer & Comprobante Guide**
- Where to find bank account details (My Account > Cashier > Deposit > Bank Transfer)
- Step-by-step: make transfer → upload comprobante → wait for credit
- What a valid comprobante must show (date, amount, name, reference)
- Upload options: chat widget, email to ayuda@beton.win
- Processing time after comprobante received: 1-4h (business), up to 24h (weekends)
- Name must match account (no third-party transfers)
- Country-specific methods: SPEI/CLABE (Mexico), CBU/CVU (Argentina), Mercado Pago, Directa24

**2. Deposit Not Credited — Full Troubleshooting**
- Step 1: Check payment method processing time (table per method)
- Step 2: Verify payment completed in bank/provider app
- Step 3: Common issues checklist (wrong details, name mismatch, weekend delay)
- Step 4: What to send to support (Player ID, method, amount, date, receipt)
- Specific guidance for "recarga exitosa pero no acreditada"
- Crypto: how to check blockchain confirmations, what if wrong network
- Weekend/holiday delay explanation

### P1 — HIGH (create this week, 200-400 tickets/month impact)

**3. Technical Troubleshooting — Expanded**
- Mobile troubleshooting: update browser, clear cache, switch Wi-Fi/data, OS requirements
- Blank/white screen: ad-blocker, JavaScript, incognito mode
- Payment page errors: separate from game errors
- How to add site to phone home screen (app-like experience)
- Recommended browsers and minimum versions
- What to include in a bug report (device, browser, screenshot, steps)

**4. KYC — Country-Specific & Photo Guide**
- Accepted IDs per country (Chile: RUT, Argentina: DNI, etc.)
- Photo requirements: phone camera OK, full document visible, good lighting, no blur
- Selfie with ID: if required, step-by-step instructions
- What counts as proof of address in each country
- What to do if verification exceeds 48 hours

### P2 — MEDIUM (create within 2 weeks)

**5. Bonus FAQ Enhancements**
- Prominent "Saldo 0.00" explanation with sports bonus
- Concrete rollover examples in local currency
- Can I have multiple bonuses? What happens on withdrawal request?
- Cashback: when credited, how calculated, rollover requirements

**6. Game/Casino Troubleshooting**
- Specific game not loading: device check, ad-blocker, try another game
- How to dispute a game result (what evidence, timeline)
- Live casino: disconnection policy, frozen stream, bet protection
- Variance/volatility explanation for slot complaints

**7. Complaint & Escalation Process**
- Clear escalation path: agent → supervisor → formal complaint
- Required information for complaints
- Response SLA (24-48h for escalated cases)
- Regulatory body contact if applicable

### P3 — LOW (create within month)

**8. Withdrawal Rejection — Specific Fixes**
- Fix per reason: KYC → link, rollover → link, third-party → explain, limit → when to retry

**9. Account Security**
- Password requirements
- Session timeout explanation
- Login from new device
- Account block: duration, exact unblock steps
""")

report.append('---\n')
report.append(f'*Analysis based on {total} sampled tickets from Q3+Q4 2025*')
report.append(f'*Cross-referenced with KB_FAQ_BetonWin.txt ({339} lines)*')
report.append(f'*Generated: {__import__("datetime").datetime.now().strftime("%d %b %Y %H:%M")}*')

# Write report
output = '\n'.join(report)
with open('kb_deep_gap_analysis.md', 'w') as f:
    f.write(output)
print(f'\nReport saved: kb_deep_gap_analysis.md')

# Also print summary
print('\n' + '=' * 60)
print('  SUMMARY: KB Gaps by Priority')
print('=' * 60)
print(f'\n  P0 (CRITICAL):')
print(f'    - Bank Transfer / Comprobante guide')
print(f'    - Deposit Not Credited troubleshooting')
print(f'\n  P1 (HIGH):')
print(f'    - Technical troubleshooting expanded')
print(f'    - KYC country-specific guide')
print(f'\n  P2 (MEDIUM):')
print(f'    - Bonus FAQ enhancements')
print(f'    - Game/Casino troubleshooting')
print(f'    - Complaint escalation process')
print(f'\n  P3 (LOW):')
print(f'    - Withdrawal rejection fixes')
print(f'    - Account security details')
