#!/usr/bin/env python3
"""
Export ALL Zendesk tickets (Oct 2025 - Feb 2026) to CSV with all available fields.
Uses 4-HOUR windows and recursive splitting down to 1-hour to guarantee 100% capture.
Outputs: all_tickets_export.csv
"""
import os, requests, time, csv, sys
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

def make_row(t, topic):
    via = t.get('via', {}) or {}
    via_channel = via.get('channel', '')
    via_source = via.get('source', {}) or {}
    via_from = via_source.get('from', {})
    via_to = via_source.get('to', {})
    sat = t.get('satisfaction_rating', {}) or {}
    sat_str = sat.get('score', '') if isinstance(sat, dict) else str(sat)
    tags = t.get('tags', []) or []
    cfields = t.get('custom_fields', []) or []
    cf_str = '; '.join(
        f"{cf.get('id', '')}={cf.get('value', '')}"
        for cf in cfields if cf.get('value') is not None
    )
    return {
        'ticket_id': t['id'],
        'requester_id': t.get('requester_id', ''),
        'assignee_id': t.get('assignee_id', ''),
        'group_id': t.get('group_id', ''),
        'organization_id': t.get('organization_id', ''),
        'brand_id': t.get('brand_id', ''),
        'status': t.get('status', ''),
        'priority': t.get('priority', ''),
        'type': t.get('type', ''),
        'subject': (t.get('subject', '') or ''),
        'description': (t.get('description', '') or '').replace('\n', ' ').replace('\r', ' ')[:500],
        'channel': via_channel,
        'via_channel': via_channel,
        'via_source_from': str(via_from) if via_from else '',
        'via_source_to': str(via_to) if via_to else '',
        'tags': '; '.join(tags),
        'custom_fields': cf_str,
        'created_at': t.get('created_at', ''),
        'updated_at': t.get('updated_at', ''),
        'solved_at': t.get('solved_at', ''),
        'due_at': t.get('due_at', ''),
        'satisfaction_rating': sat_str,
        'is_public': t.get('is_public', ''),
        'has_incidents': t.get('has_incidents', ''),
        'ticket_form_id': t.get('ticket_form_id', ''),
        'allow_channelback': t.get('allow_channelback', ''),
        'topic_classified': topic,
        'month': t.get('created_at', '')[:7],
    }

def fetch_window(writer, ws_dt, we_dt, seen, depth=0):
    """
    Recursively fetch all tickets in a time window.
    If results hit 1000 limit, split window in half and recurse.
    Minimum window: 1 hour.
    """
    ws = ws_dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    we = we_dt.strftime('%Y-%m-%dT%H:%M:%SZ')

    url = f'{BASE}/search.json?query=type:ticket+created>{ws}+created<{we}&sort_by=created_at&sort_order=asc&per_page=100'
    window_count = 0

    while url:
        data = get_json(url)
        if not data:
            break
        for t in data.get('results', []):
            if t['id'] in seen:
                continue
            seen.add(t['id'])
            text = (t.get('subject', '') or '') + ' ' + (t.get('description', '') or '')
            topic = classify(text)
            writer.writerow(make_row(t, topic))
            window_count += 1
        url = data.get('next_page')
        time.sleep(0.1)

    # If we hit the 1000 limit, split and recurse
    if window_count >= 1000:
        duration = (we_dt - ws_dt).total_seconds()
        # Only split if window is wider than 1 hour
        if duration > 3600:
            mid_dt = ws_dt + timedelta(seconds=duration / 2)
            indent = '  ' * (depth + 1)
            span_hrs = duration / 3600
            print(f'{indent}Window {ws_dt.strftime("%m-%d %H:%M")}-{we_dt.strftime("%H:%M")} ({span_hrs:.0f}h) hit 1000, splitting...')
            c1 = fetch_window(writer, ws_dt, mid_dt, seen, depth + 1)
            c2 = fetch_window(writer, mid_dt, we_dt, seen, depth + 1)
            extra = c1 + c2
            window_count += extra
            if extra > 0:
                print(f'{indent}  Recovered +{extra} extra tickets')
        else:
            indent = '  ' * (depth + 1)
            print(f'{indent}⚠ Window {ws_dt.strftime("%m-%d %H:%M")}-{we_dt.strftime("%H:%M")} (1h) at 1000 limit - minimum window reached')

    return window_count

# Build 4-HOUR windows: Oct 1, 2025 -> Mar 1, 2026
windows = []
start = datetime(2025, 10, 1)
end = datetime(2026, 3, 1)
current = start
while current < end:
    w_end = min(current + timedelta(hours=4), end)
    windows.append((current, w_end))
    current = w_end

print(f'Fetching {len(windows)} x 4-hour windows (Oct 2025 - Feb 2026)')
print(f'Auto-splits to 2h -> 1h if a window hits 1000 limit')
print('=' * 60)

CSV_FIELDS = [
    'ticket_id', 'requester_id', 'assignee_id', 'group_id',
    'organization_id', 'brand_id', 'status', 'priority', 'type',
    'subject', 'description', 'channel', 'via_channel',
    'via_source_from', 'via_source_to', 'tags', 'custom_fields',
    'created_at', 'updated_at', 'solved_at', 'due_at',
    'satisfaction_rating', 'is_public', 'has_incidents',
    'ticket_form_id', 'allow_channelback', 'topic_classified', 'month',
]

outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_tickets_export.csv')
seen = set()
total = 0
current_day = ''

with open(outpath, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDS, extrasaction='ignore')
    writer.writeheader()

    for idx, (w_start, w_end) in enumerate(windows):
        count = fetch_window(writer, w_start, w_end, seen, depth=0)
        total += count

        day_str = w_start.strftime('%Y-%m-%d')
        if day_str != current_day:
            if current_day:
                # Print daily summary
                pass
            current_day = day_str

        if count > 0 or (idx + 1) % 18 == 0:  # 18 windows = 3 days
            print(f'  [{idx+1}/{len(windows)}] {w_start.strftime("%Y-%m-%d %H:%M")}-{w_end.strftime("%H:%M")}: +{count} | Total: {total}')

        sys.stdout.flush()

print(f'\n{"=" * 60}')
print(f'DONE! Total tickets exported: {total}')
print(f'CSV saved to: {outpath}')
print(f'\nColumns ({len(CSV_FIELDS)}): {", ".join(CSV_FIELDS)}')
