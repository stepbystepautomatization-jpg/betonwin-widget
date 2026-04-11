#!/usr/bin/env python3
"""
Fetch and analyze Jan + Feb 2026 tickets for inclusion in final report.
"""

import os, requests, time, re, sys, json
from collections import defaultdict, Counter
from datetime import datetime
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

# Weekly ranges for Jan + Feb 2026
WEEKS = []
from datetime import timedelta
start = datetime(2026, 1, 1)
end = datetime(2026, 3, 1)
current = start
while current < end:
    week_end = min(current + timedelta(days=7), end)
    WEEKS.append((current.strftime('%Y-%m-%dT00:00:00Z'), week_end.strftime('%Y-%m-%dT00:00:00Z')))
    current = week_end

print('=' * 60)
print('  Fetching Jan + Feb 2026 tickets')
print(f'  {len(WEEKS)} weekly ranges')
print('=' * 60)

# Phase 1: Fetch tickets
print('\nPhase 1: Fetching tickets...')
all_tickets, seen = [], set()
monthly_counts = defaultdict(int)

for idx, (ws, we) in enumerate(WEEKS):
    url = f'{BASE}/search.json?query=type:ticket+created>{ws}+created<{we}&sort_by=created_at&sort_order=asc&per_page=100'
    week_count = 0
    while url:
        data = get_json(url)
        if not data: break
        for t in data.get('results', []):
            if t['id'] not in seen:
                all_tickets.append(t)
                seen.add(t['id'])
                week_count += 1
                monthly_counts[t.get('created_at', '')[:7]] += 1
        url = data.get('next_page')
    print(f'  Week {idx+1}/{len(WEEKS)} ({ws[:10]} -> {we[:10]}): +{week_count} | Total: {len(all_tickets)}')
    sys.stdout.flush()

total = len(all_tickets)
print(f'\nTotal: {total} tickets')
for m in sorted(monthly_counts.keys()):
    print(f'  {m}: {monthly_counts[m]}')

# Phase 2: Classify with comments
print(f'\nPhase 2: Analyzing {total} tickets...')
topic_counts = Counter()
monthly_topic = defaultdict(lambda: Counter())

for i, t in enumerate(all_tickets):
    subject = t.get('subject', '') or ''
    desc = t.get('description', '') or ''
    created_month = t.get('created_at', '')[:7]

    data = get_json(f'{BASE}/tickets/{t["id"]}/comments.json')
    comments = data.get('comments', []) if data else []
    comment_text = ' '.join(c.get('body', '') or '' for c in comments)

    full_text = subject + ' ' + desc + ' ' + comment_text
    user_text = extract_user_text(full_text)
    search_text = (user_text + ' ' + user_text + ' ' + full_text).lower()

    topic = classify(search_text)
    topic_counts[topic] += 1
    monthly_topic[created_month][topic] += 1

    if (i + 1) % 200 == 0:
        print(f'  {i+1}/{total} ({round((i+1)/total*100,1)}%)...')
        sys.stdout.flush()
    time.sleep(0.05)

print(f'\nDone! {total} tickets analyzed.')

# Save results as JSON for the PDF script
results = {
    'total': total,
    'monthly_volume': dict(monthly_counts),
    'topic_counts': dict(topic_counts),
    'monthly_topic': {m: dict(tc) for m, tc in monthly_topic.items()},
}

with open('data_2026.json', 'w') as f:
    json.dump(results, f, indent=2)
print('\nResults saved: data_2026.json')

# Print summary
print('\n' + '=' * 60)
for m in sorted(monthly_topic.keys()):
    print(f'\n  {m}:')
    for topic, cnt in sorted(monthly_topic[m].items(), key=lambda x: -x[1]):
        print(f'    {topic}: {cnt}')
