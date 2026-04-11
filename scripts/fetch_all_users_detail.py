#!/usr/bin/env python3
"""
Fetch ALL 22,000 tickets (Oct 2025 - Feb 2026) and build comprehensive
user-level dataset with full detail for every single user.
Outputs: all_users_detail.json
"""
import os, requests, time, json, sys
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'zendesk.env'))
EMAIL = os.getenv('ZENDESK_EMAIL', 'mistydubteck@beton.win')
TOKEN = os.getenv('ZENDESK_API_TOKEN', '5xOA7XwSl5hdp901d7d0RNi510UER9E6fPkURdg3')
AUTH  = (f'{EMAIL}/token', TOKEN)
BASE  = 'https://betonwin.zendesk.com/api/v2'

TOPICS = {
    'Deposit Not Credited': ['no se reflejo','no se acredito','no me acredito','no aparece','no lo veo','no figura','deposite y no','hice un deposito y no','not credited','balance not updated','saldo no cambio','no fue acreditado','hice una transferencia y no','transferi y no','recarga exitosa pero','exitoso pero no','no recibido','no llego','no recibi','ya pague y no','pague y no','no veo el saldo'],
    'How to Deposit': ['como depositar','como deposito','como cargo','quiero depositar','como recargo','formas de pago','how to deposit','metodo deposito','monto minimo','como puedo cargar','donde puedo depositar','que metodos','acepta','aceptan'],
    'Deposit Failed / Declined': ['failed','fallido','rechazado','error al depositar','error de pago','transaccion fallida','payment failed','declined','declinado','no se proceso'],
    'Deposit Processing Delay': ['cuanto tarda','esperando deposito','en espera','pending deposit','demora deposito','tarda mucho','still processing','lleva mucho tiempo'],
    'Recarga / Top-up': ['recarga','recargar','carga saldo','cargar saldo','cargar cuenta','recargue','recarge','top up','topup','hice una recarga','mi recarga'],
    'How to Withdraw': ['como retirar','como retiro','quiero retirar','quiero sacar','como saco','quiero cobrar','como cobro','puedo retirar','metodo de retiro','how to withdraw','cobrar mi dinero','sacar mi plata','retirar mi plata'],
    'Withdrawal Pending / Delay': ['retiro pendiente','retiro demora','retiro tarda','esperando retiro','withdrawal pending','en proceso retiro','cuanto tarda retiro'],
    'Withdrawal Rejected': ['retiro rechazado','no me dejan retirar','no puedo retirar','withdrawal rejected','withdrawal denied','cannot withdraw'],
    'Bonus / Promotions': ['bono','bonos','promocion','promos','bonus','free bet','freespin','regalo','oferta','codigo promo','cashback','giros gratis','tiradas','rollover','wagering','bono bienvenida','welcome bonus','como uso el bono','activar'],
    'Account / Login Issues': ['no puedo entrar','no puedo ingresar','olvide mi','mi contrasena','recuperar contrasena','acceder','acceso','cuenta bloqueada','me bloqueo','login','password','contrasena','crear cuenta','abrir cuenta','registrarme','no me deja entrar','suspendida','nueva cuenta'],
    'Bank Transfer / Comprobante': ['transferencia','banco','cuenta bancaria','comprobante','voucher','recibo','clabe','cvu','cbu','cuenta corriente','envie comprobante','transferencia bancaria','cuenta de banco','numero de cuenta','iban','mande el comprobante','adjunto comprobante','bonifico'],
    'Casino / Games / Bets': ['juego','juegos','apuesta','apuestas','slot','partida','no carga el juego','resultado','mi apuesta','ganancia','gane','perdi','casino','live','tragamonedas','apostar','jackpot','ganancias','winnings','error en el juego','vincita','mesa'],
    'Technical / App / Website': ['no funciona','no abre','error','no carga','se cierra','app','aplicacion','celular','telefono','android','iphone','pagina','sitio','pantalla','se traba','problema tecnico','website down','app crash','not loading'],
    'KYC / Verification': ['verificar','verificacion','documento','dni','pasaporte','validar','selfie','foto','comprobante domicilio','identidad','kyc','cedula','identity verification'],
    'Complaint / Dissatisfaction': ['queja','reclamo','no es justo','me robaron','estafados','pesimo','muy malo','terrible','fraude','robo','estafa','quiero quejarme','inaceptable'],
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
                    'subject': (t.get('subject', '') or '')[:120],
                    'status': t.get('status', ''),
                })
                week_count += 1
        url = data.get('next_page')
        time.sleep(0.1)

    total = len(all_tickets)
    print(f'  Week {idx+1}/{len(weeks)} ({ws[:10]} -> {we[:10]}): +{week_count} | Total: {total}')
    sys.stdout.flush()

print(f'\n{"=" * 60}')
print(f'Total tickets fetched: {len(all_tickets)}')

# ══════════════════════════════════════════════════════════
# Build COMPLETE user-level dataset
# ══════════════════════════════════════════════════════════

user_data = defaultdict(lambda: {
    'count': 0,
    'topics': Counter(),
    'months': set(),
    'first': '',
    'last': '',
    'ticket_ids': [],
    'subjects': [],
    'statuses': Counter(),
})

for t in all_tickets:
    uid = str(t['requester_id'])
    user_data[uid]['count'] += 1
    user_data[uid]['topics'][t['topic']] += 1
    user_data[uid]['months'].add(t['month'])
    user_data[uid]['statuses'][t['status']] += 1
    user_data[uid]['ticket_ids'].append(t['id'])
    if t['subject']:
        user_data[uid]['subjects'].append(t['subject'][:80])
    if not user_data[uid]['first'] or t['created_at'] < user_data[uid]['first']:
        user_data[uid]['first'] = t['created_at']
    if not user_data[uid]['last'] or t['created_at'] > user_data[uid]['last']:
        user_data[uid]['last'] = t['created_at']

total_users = len(user_data)

# Sort ALL users by ticket count
all_users_sorted = sorted(user_data.items(), key=lambda x: -x[1]['count'])

# Build output with ALL users
all_users_list = []
for uid, d in all_users_sorted:
    primary_topic = d['topics'].most_common(1)[0][0] if d['topics'] else 'Unknown'
    all_users_list.append({
        'user_id': uid,
        'ticket_count': d['count'],
        'primary_topic': primary_topic,
        'all_topics': dict(d['topics'].most_common()),
        'months_active': sorted(d['months']),
        'month_span': len(d['months']),
        'first_ticket': d['first'],
        'last_ticket': d['last'],
        'ticket_ids': d['ticket_ids'][:20],  # max 20 IDs to keep size manageable
        'sample_subjects': d['subjects'][:5],
        'statuses': dict(d['statuses']),
    })

# Aggregations
buckets = {
    '1_ticket': 0, '2_tickets': 0, '3_to_5': 0,
    '6_to_10': 0, '11_to_20': 0, '20_plus': 0
}
for u in all_users_list:
    c = u['ticket_count']
    if c == 1: buckets['1_ticket'] += 1
    elif c == 2: buckets['2_tickets'] += 1
    elif 3 <= c <= 5: buckets['3_to_5'] += 1
    elif 6 <= c <= 10: buckets['6_to_10'] += 1
    elif 11 <= c <= 20: buckets['11_to_20'] += 1
    elif c > 20: buckets['20_plus'] += 1

# Topic analysis for multi-ticket users
multi_users = [u for u in all_users_list if u['ticket_count'] >= 2]
topic_frustration = defaultdict(lambda: {'users': [], 'total_tickets': 0})
for u in multi_users:
    for topic, cnt in u['all_topics'].items():
        if cnt >= 2:  # same topic 2+ times
            topic_frustration[topic]['users'].append({
                'user_id': u['user_id'],
                'tickets_on_topic': cnt,
                'total_tickets': u['ticket_count'],
                'months': u['months_active'],
            })
            topic_frustration[topic]['total_tickets'] += cnt

# Monthly volume
monthly_vol = Counter()
monthly_topic = defaultdict(lambda: Counter())
for t in all_tickets:
    monthly_vol[t['month']] += 1
    monthly_topic[t['month']][t['topic']] += 1

# Topic totals
topic_totals = Counter()
for t in all_tickets:
    topic_totals[t['topic']] += 1

output = {
    'meta': {
        'total_tickets': len(all_tickets),
        'total_unique_users': total_users,
        'generated': datetime.now().isoformat()[:19],
        'period': 'Oct 2025 - Feb 2026',
    },
    'monthly_volume': dict(sorted(monthly_vol.items())),
    'topic_totals': dict(topic_totals.most_common()),
    'monthly_topic': {m: dict(sorted(tc.items(), key=lambda x: -x[1])) for m, tc in sorted(monthly_topic.items())},
    'user_buckets': buckets,
    'multi_ticket_count': len(multi_users),
    'single_ticket_count': total_users - len(multi_users),

    # ALL users with 6+ tickets (detailed)
    'users_6plus': [u for u in all_users_list if u['ticket_count'] >= 6],
    # ALL users with 3-5 tickets
    'users_3to5': [u for u in all_users_list if 3 <= u['ticket_count'] <= 5],
    # ALL users with 2 tickets (IDs + primary topic only to save space)
    'users_2tickets': [
        {'user_id': u['user_id'], 'primary_topic': u['primary_topic'],
         'months_active': u['months_active'], 'first_ticket': u['first_ticket'], 'last_ticket': u['last_ticket']}
        for u in all_users_list if u['ticket_count'] == 2
    ],
    # Summary of 1-ticket users by topic
    'users_1ticket_by_topic': dict(Counter(
        u['primary_topic'] for u in all_users_list if u['ticket_count'] == 1
    ).most_common()),

    # Same-topic frustration with user IDs
    'same_topic_frustration': {
        topic: {
            'user_count': len(d['users']),
            'total_tickets': d['total_tickets'],
            'users': sorted(d['users'], key=lambda x: -x['tickets_on_topic'])[:30],  # top 30 per topic
        }
        for topic, d in sorted(topic_frustration.items(), key=lambda x: -len(x[1]['users']))
        if topic != 'Uncategorized'
    },

    # Month span analysis
    'users_by_month_span': {
        f'{i}_months': len([u for u in multi_users if u['month_span'] == i])
        for i in range(1, 6)
    },
    # Users active ALL 5 months
    'users_all_5_months': [
        u for u in all_users_list if u['month_span'] >= 5
    ],
    # Users active 4+ months
    'users_4plus_months': [
        u for u in all_users_list if u['month_span'] >= 4
    ],
}

outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_users_detail.json')
with open(outpath, 'w') as f:
    json.dump(output, f, indent=2, default=str)

print(f'\nResults saved to: {outpath}')
print(f'\n{"=" * 60}')
print(f'SUMMARY:')
print(f'  Total tickets: {output["meta"]["total_tickets"]:,}')
print(f'  Unique users: {output["meta"]["total_unique_users"]:,}')
print(f'  Multi-ticket users: {output["multi_ticket_count"]:,}')
print(f'  Users 6+ tickets: {len(output["users_6plus"])}')
print(f'  Users 3-5 tickets: {len(output["users_3to5"])}')
print(f'  Users 2 tickets: {len(output["users_2tickets"])}')
print(f'  Users 1 ticket: {output["single_ticket_count"] - len(output["users_2tickets"]):,}')
print(f'  Users active 4+ months: {len(output["users_4plus_months"])}')
print(f'  Users active 5 months: {len(output["users_all_5_months"])}')
print(f'\n  Topic frustration (same-topic 2+ tickets):')
for topic, d in list(output['same_topic_frustration'].items())[:10]:
    print(f'    {topic}: {d["user_count"]} users, {d["total_tickets"]} tickets')
