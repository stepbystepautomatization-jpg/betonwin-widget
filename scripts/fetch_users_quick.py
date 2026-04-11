#!/usr/bin/env python3
"""
Quick fetch of Oct-Feb tickets with requester_id for user-level analysis.
Uses weekly windows to bypass Zendesk 1000-result search limit.
"""
import os, requests, time, json, sys
from collections import defaultdict, Counter
from datetime import datetime, timedelta

# Zendesk credentials
EMAIL = 'mistydubteck@beton.win'
TOKEN = '5xOA7XwSl5hdp901d7d0RNi510UER9E6fPkURdg3'
AUTH = (f'{EMAIL}/token', TOKEN)
BASE = 'https://betonwin.zendesk.com/api/v2'

TOPICS = {
    'Deposit Not Credited': ['no se reflejo','no se acredito','no me acredito','no aparece','no lo veo','no figura','deposite y no','hice un deposito y no','not credited','balance not updated','saldo no cambio'],
    'How to Deposit': ['como depositar','como deposito','como cargo','quiero depositar','como recargo','formas de pago','how to deposit','metodo deposito','monto minimo'],
    'Deposit Failed / Declined': ['failed','fallido','rechazado','error al depositar','error de pago','transaccion fallida','payment failed','declined','declinado'],
    'Deposit Processing Delay': ['cuanto tarda','esperando deposito','en espera','pending deposit','demora deposito','tarda mucho','still processing'],
    'Recarga / Top-up': ['recarga','recargar','carga saldo','cargar saldo','cargar cuenta','recargue','recarge','top up','topup'],
    'How to Withdraw': ['como retirar','como retiro','quiero retirar','quiero sacar','como saco','quiero cobrar','como cobro','puedo retirar','metodo de retiro','how to withdraw'],
    'Withdrawal Pending / Delay': ['retiro pendiente','retiro demora','retiro tarda','esperando retiro','withdrawal pending'],
    'Withdrawal Rejected': ['retiro rechazado','no me dejan retirar','no puedo retirar','withdrawal rejected','withdrawal denied','cannot withdraw'],
    'Bonus / Promotions': ['bono','bonos','promocion','promos','bonus','free bet','freespin','regalo','oferta','codigo promo','cashback','giros gratis','tiradas','rollover','wagering'],
    'Account / Login Issues': ['no puedo entrar','no puedo ingresar','olvide mi','mi contrasena','recuperar contrasena','acceder','acceso','cuenta bloqueada','me bloqueo','login','password','contrasena','crear cuenta','abrir cuenta','registrarme'],
    'Bank Transfer / Comprobante': ['transferencia','banco','cuenta bancaria','comprobante','voucher','recibo','clabe','cvu','cbu','cuenta corriente','envie comprobante','transferencia bancaria'],
    'Casino / Games / Bets': ['juego','juegos','apuesta','apuestas','slot','partida','no carga el juego','resultado','mi apuesta','ganancia','gane','perdi','casino','live','tragamonedas','apostar','jackpot','ganancias'],
    'Technical / App / Website': ['no funciona','no abre','error','no carga','se cierra','app','aplicacion','celular','telefono','android','iphone','pagina','sitio','pantalla','se traba','problema tecnico'],
    'KYC / Verification': ['verificar','verificacion','documento','dni','pasaporte','validar','selfie','foto','comprobante domicilio','identidad','kyc','cedula'],
    'Complaint / Dissatisfaction': ['queja','reclamo','no es justo','me robaron','estafados','pesimo','muy malo','terrible','fraude','robo','estafa'],
    'Balance / Account Info': ['mi saldo','cual es mi saldo','saldo disponible','cuanto tengo','mi cuenta','datos de mi cuenta','informacion de cuenta','balance','my balance','mis datos'],
    'Greeting Only (no question)': ['hola','buenas','buen dia','buenos dias','buenas tardes','buenas noches'],
}

def classify(text):
    t = text.lower()
    scores = {}
    for topic, kws in TOPICS.items():
        score = sum(1 for kw in kws if kw in t)
        if score > 0:
            scores[topic] = score
    if not scores:
        return 'Uncategorized'
    # Greeting only wins if no other topic scored
    if 'Greeting Only (no question)' in scores and len(scores) > 1:
        del scores['Greeting Only (no question)']
    return max(scores, key=scores.get)

def get_json(url, retries=4):
    for attempt in range(retries):
        try:
            r = requests.get(url, auth=AUTH, timeout=30)
            if r.status_code == 429:
                wait = int(r.headers.get('Retry-After', 30))
                print(f'    Rate limited, waiting {wait}s...')
                time.sleep(wait)
                continue
            if r.status_code == 422:
                return None
            r.raise_for_status()
            return r.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            time.sleep(5 * (attempt + 1))
    return None

# Weekly windows Oct 2025 - Feb 2026
weeks = []
start = datetime(2025, 10, 1)
end = datetime(2026, 3, 1)
current = start
while current < end:
    week_end = min(current + timedelta(days=7), end)
    weeks.append((current.strftime('%Y-%m-%dT00:00:00Z'), week_end.strftime('%Y-%m-%dT00:00:00Z')))
    current = week_end

print(f'Fetching {len(weeks)} weekly windows (Oct 2025 - Feb 2026)')
print('=' * 60)

all_tickets = []
seen = set()

for idx, (ws, we) in enumerate(weeks):
    url = f'{BASE}/search.json?query=type:ticket+created>{ws}+created<{we}&sort_by=created_at&sort_order=asc&per_page=100'
    week_count = 0
    while url:
        data = get_json(url)
        if not data:
            break
        for t in data.get('results', []):
            if t['id'] not in seen:
                seen.add(t['id'])
                text = (t.get('subject', '') or '') + ' ' + (t.get('description', '') or '')
                topic = classify(text)
                month = t.get('created_at', '')[:7]
                all_tickets.append({
                    'id': t['id'],
                    'requester_id': t.get('requester_id'),
                    'month': month,
                    'topic': topic,
                    'created_at': t.get('created_at', '')[:19],
                })
                week_count += 1
        url = data.get('next_page')
        time.sleep(0.1)

    total = len(all_tickets)
    print(f'  Week {idx+1}/{len(weeks)} ({ws[:10]} -> {we[:10]}): +{week_count} | Total: {total}')
    sys.stdout.flush()

print(f'\n{"=" * 60}')
print(f'Total tickets fetched: {len(all_tickets)}')

# Analyze by user
user_data = defaultdict(lambda: {'count': 0, 'topics': Counter(), 'months': set(), 'first': '', 'last': ''})

for t in all_tickets:
    uid = str(t['requester_id'])
    user_data[uid]['count'] += 1
    user_data[uid]['topics'][t['topic']] += 1
    user_data[uid]['months'].add(t['month'])
    if not user_data[uid]['first'] or t['created_at'] < user_data[uid]['first']:
        user_data[uid]['first'] = t['created_at']
    if not user_data[uid]['last'] or t['created_at'] > user_data[uid]['last']:
        user_data[uid]['last'] = t['created_at']

total_users = len(user_data)
multi_ticket = {k: v for k, v in user_data.items() if v['count'] > 1}

# Buckets
buckets = {'exactly_2': 0, '3_to_5': 0, '6_to_10': 0, '11_to_20': 0, '20_plus': 0}
for uid, d in user_data.items():
    c = d['count']
    if c == 2: buckets['exactly_2'] += 1
    elif 3 <= c <= 5: buckets['3_to_5'] += 1
    elif 6 <= c <= 10: buckets['6_to_10'] += 1
    elif 11 <= c <= 20: buckets['11_to_20'] += 1
    elif c > 20: buckets['20_plus'] += 1

# Topic analysis for recurring users (2+ tickets)
topic_recurring = defaultdict(lambda: {'total_tickets': 0, 'unique_users': set()})
for uid, d in multi_ticket.items():
    for topic, cnt in d['topics'].items():
        topic_recurring[topic]['total_tickets'] += cnt
        topic_recurring[topic]['unique_users'].add(uid)

# Same-topic frustration (users opening 2+ tickets on SAME topic)
same_topic_frustration = defaultdict(lambda: {'users': 0, 'total_tickets': 0})
for uid, d in multi_ticket.items():
    for topic, cnt in d['topics'].items():
        if cnt >= 2:
            same_topic_frustration[topic]['users'] += 1
            same_topic_frustration[topic]['total_tickets'] += cnt

# Top frustrated users (most tickets)
top_users = sorted(user_data.items(), key=lambda x: -x[1]['count'])[:50]

# Monthly volume
monthly_vol = Counter()
for t in all_tickets:
    monthly_vol[t['month']] += 1

# Build output
output = {
    'total_tickets': len(all_tickets),
    'total_unique_users': total_users,
    'monthly_volume': dict(sorted(monthly_vol.items())),
    'user_buckets': buckets,
    'multi_ticket_user_count': len(multi_ticket),
    'single_ticket_user_count': total_users - len(multi_ticket),
    'topic_recurring_users': {
        topic: {
            'total_tickets_from_recurring': d['total_tickets'],
            'unique_recurring_users': len(d['unique_users'])
        }
        for topic, d in sorted(topic_recurring.items(), key=lambda x: -x[1]['total_tickets'])
    },
    'same_topic_frustration': {
        topic: d
        for topic, d in sorted(same_topic_frustration.items(), key=lambda x: -x[1]['users'])
    },
    'top_frustrated_users': [
        {
            'user_id': uid,
            'ticket_count': d['count'],
            'topics': dict(d['topics'].most_common()),
            'months_active': sorted(d['months']),
            'first_ticket': d['first'],
            'last_ticket': d['last'],
        }
        for uid, d in top_users
    ],
    'multi_ticket_users_by_month_span': {
        '1_month': sum(1 for d in multi_ticket.values() if len(d['months']) == 1),
        '2_months': sum(1 for d in multi_ticket.values() if len(d['months']) == 2),
        '3_months': sum(1 for d in multi_ticket.values() if len(d['months']) == 3),
        '4_months': sum(1 for d in multi_ticket.values() if len(d['months']) == 4),
        '5_months': sum(1 for d in multi_ticket.values() if len(d['months']) == 5),
    },
}

outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_analysis_data.json')
with open(outpath, 'w') as f:
    json.dump(output, f, indent=2, default=str)

print(f'\nResults saved to: {outpath}')
print(f'\n{"=" * 60}')
print(f'SUMMARY:')
print(f'  Total tickets: {output["total_tickets"]:,}')
print(f'  Unique users: {output["total_unique_users"]:,}')
print(f'  Multi-ticket users: {output["multi_ticket_user_count"]:,} ({output["multi_ticket_user_count"]/total_users*100:.1f}%)')
print(f'  Single-ticket users: {output["single_ticket_user_count"]:,}')
print(f'\n  User ticket buckets:')
for k, v in buckets.items():
    print(f'    {k}: {v:,}')
print(f'\n  Top same-topic frustration:')
for topic, d in list(output['same_topic_frustration'].items())[:8]:
    print(f'    {topic}: {d["users"]} users, {d["total_tickets"]} tickets')
print(f'\n  Top 10 most-ticket users:')
for u in output['top_frustrated_users'][:10]:
    topics_str = ', '.join(f'{t}:{c}' for t, c in list(u['topics'].items())[:3])
    print(f'    User {u["user_id"]}: {u["ticket_count"]} tickets ({topics_str})')
