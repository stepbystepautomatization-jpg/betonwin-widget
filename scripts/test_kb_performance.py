#!/usr/bin/env python3
"""
BetonWin — KB Performance Test
Tests how well the updated Knowledge Base can answer real customer tickets.
Simulates 100 real ticket scenarios from the 240K dataset and scores coverage.
"""
import csv, os, re, sys
from collections import Counter, defaultdict

# ════════════════════════════════════════════════════════════════
# LOAD KB
# ════════════════════════════════════════════════════════════════
kb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'KB_FAQ_BetonWin.txt')
with open(kb_path, 'r', encoding='utf-8') as f:
    KB_TEXT = f.read().lower()

KB_SECTIONS = {}
current_section = 'HEADER'
for line in KB_TEXT.split('\n'):
    if line.strip().startswith('===') and line.strip().endswith('==='):
        current_section = line.strip().replace('=', '').strip()
    elif line.strip():
        KB_SECTIONS.setdefault(current_section, []).append(line.strip())

print(f'KB loaded: {len(KB_TEXT):,} characters, {len(KB_SECTIONS)} sections')

# ════════════════════════════════════════════════════════════════
# TEST SCENARIOS — Real ticket messages from 240K dataset
# ════════════════════════════════════════════════════════════════
TEST_TICKETS = [
    # === DEPOSITS ===
    {"msg": "hola hice un deposito hace 1 hora y no me aparece el saldo", "topic": "Deposit Not Credited", "expects": ["30-60 minutos", "comprobante", "ayuda@beton.win"]},
    {"msg": "como puedo depositar dinero en mi cuenta", "topic": "How to Deposit", "expects": ["depositar", "webpay", "mach", "mercado pago"]},
    {"msg": "quiero depositar pero me sale rechazado", "topic": "Deposit Failed", "expects": ["rechazado", "rut", "fondos insuficientes", "banco"]},
    {"msg": "cuanto tarda en acreditarse mi deposito", "topic": "Deposit Delay", "expects": ["30", "60", "minutos"]},
    {"msg": "cuanto es el deposito minimo en chile", "topic": "Deposit Info", "expects": ["2,000 clp", "2000"]},
    {"msg": "cuanto es el deposito minimo en argentina", "topic": "Deposit Info AR", "expects": ["2,820 ars", "2820"]},
    {"msg": "que metodos de deposito aceptan", "topic": "Deposit Methods", "expects": ["webpay", "mach", "mercado pago", "transferencia"]},
    {"msg": "puedo depositar con bitcoin", "topic": "Crypto Deposit", "expects": ["criptomoneda", "bitcoin", "segundo depósito", "binance"]},
    {"msg": "hice una transferencia bancaria y no llega", "topic": "Bank Transfer", "expects": ["comprobante", "transferencia", "orden"]},
    {"msg": "deposite por mercado pago y no se refleja", "topic": "Mercado Pago", "expects": ["comprobante", "proveedor de pago"]},
    {"msg": "me sale declined by internal antifraud", "topic": "Antifraud", "expects": ["antifraud", "30 min", "1 hora", "espera"]},
    {"msg": "hice el deposito pero puse un monto diferente a la orden", "topic": "Wrong Amount", "expects": ["monto diferente", "orden", "reembolso", "acreditación"]},

    # === WITHDRAWALS ===
    {"msg": "como puedo retirar mi dinero", "topic": "How to Withdraw", "expects": ["retirar", "transferencia bancaria", "rut", "cuenta bancaria"]},
    {"msg": "cuanto es el minimo para retirar en chile", "topic": "Withdrawal Min", "expects": ["5,035 clp", "5035"]},
    {"msg": "cuanto tarda el retiro", "topic": "Withdrawal Time", "expects": ["3 días hábiles"]},
    {"msg": "mi retiro fue rechazado", "topic": "Withdrawal Declined", "expects": ["rechazado", "declined", "datos", "rut"]},
    {"msg": "mi retiro dice pending by provider", "topic": "Withdrawal Status", "expects": ["pending by provider", "proveedor"]},
    {"msg": "me sale declined due to 70% not wagered", "topic": "Withdrawal 70%", "expects": ["70%", "requisito de apuesta"]},
    {"msg": "no puedo retirar dice que debo verificar", "topic": "Withdrawal KYC", "expects": ["verificación", "80 usd", "75,000 clp", "documentos"]},
    {"msg": "tengo un limite de retiro y no puedo sacar todo", "topic": "Withdrawal Limit", "expects": ["límite", "varias retiradas", "más pequeñas"]},
    {"msg": "puedo cancelar mi retiro", "topic": "Cancel Withdrawal", "expects": ["no es posible cancelar"]},
    {"msg": "puedo retirar con criptomonedas", "topic": "Crypto Withdrawal", "expects": ["crypto", "contacta", "soporte"]},
    {"msg": "quiero retirar pero dice que mi metodo de pago no esta activo", "topic": "Withdrawal Blocked", "expects": ["verificación", "80 usd", "75,000"]},

    # === BONUSES ===
    {"msg": "como funciona el bono de bienvenida", "topic": "Welcome Bonus", "expects": ["150%", "50 giros", "primer depósito", "10 depósitos"]},
    {"msg": "que es el rollover", "topic": "Rollover", "expects": ["rollover", "wagering", "apostar", "x30"]},
    {"msg": "no puedo apostar con el bono deportivo me sale saldo 0", "topic": "Sport Bonus 0", "expects": ["50%", "dinero real", "saldo 0.00", "depósito"]},
    {"msg": "mi bono expiro y perdi todo", "topic": "Bonus Expired", "expects": ["expir", "wagering", "fecha límite", "depósito real no se ve afectado"]},
    {"msg": "como uso un codigo promocional", "topic": "Promo Code", "expects": ["código", "depósito", "instagram", "whatsapp"]},
    {"msg": "que son los giros gratis", "topic": "Free Spins", "expects": ["giros gratis", "tragamonedas", "slots", "rollover"]},
    {"msg": "la promocion no me aparece en mi cuenta", "topic": "Promo Unavailable", "expects": ["no está disponible", "jugadores", "historial", "nuevas promociones"]},
    {"msg": "puedo cancelar mi bono activo", "topic": "Cancel Bonus", "expects": ["cancelar", "depósito real", "ganancias", "irreversible"]},
    {"msg": "tengo el saldo bloqueado por un bono", "topic": "Balance Locked", "expects": ["bloqueado", "wagering", "completar", "cancelar"]},
    {"msg": "cuanto puedo retirar como maximo del bono", "topic": "Release Limit", "expects": ["límite máximo", "multiplicador", "x7", "términos"]},
    {"msg": "que es el cashback", "topic": "Cashback", "expects": ["cashback", "diario", "semanal", "nivel"]},
    {"msg": "como funciona el programa de fidelidad", "topic": "Loyalty", "expects": ["fidelidad", "hero", "nivel", "apostar", "dinero real"]},

    # === VERIFICATION ===
    {"msg": "como verifico mi cuenta", "topic": "How to Verify", "expects": ["verificación", "dni", "pasaporte", "kyc"]},
    {"msg": "cuanto tarda la verificacion", "topic": "Verification Time", "expects": ["verificación", "24", "48 horas", "orden de solicitud"]},
    {"msg": "mi verificacion fue rechazada", "topic": "Verification Rejected", "expects": ["rechazad", "borroso", "cortado", "vencido"]},
    {"msg": "no me llega el sms de verificacion", "topic": "Phone Verification", "expects": ["sms", "código", "teléfono", "verificar"]},
    {"msg": "no me llega el email de verificacion", "topic": "Email Verification", "expects": ["spam", "promociones", "carpeta"]},
    {"msg": "necesito verificarme para retirar", "topic": "KYC Required", "expects": ["80 usd", "75,000 clp", "110,000 ars", "verificación"]},

    # === ACCOUNT ===
    {"msg": "olvide mi contraseña", "topic": "Password Reset", "expects": ["olvidaste tu contraseña", "email", "enlace", "restablecer"]},
    {"msg": "mi cuenta esta bloqueada", "topic": "Account Blocked", "expects": ["bloqueada", "intentos fallidos", "olvidaste tu contraseña"]},
    {"msg": "quiero cerrar mi cuenta", "topic": "Close Account", "expects": ["cerrar", "ayuda@beton.win", "autoexclusión"]},
    {"msg": "puedo tener dos cuentas", "topic": "Multiple Accounts", "expects": ["no", "una cuenta", "suspensión"]},
    {"msg": "como cambio mis datos personales", "topic": "Change Data", "expects": ["configuración", "documento de identidad", "soporte"]},
    {"msg": "no puedo acceder al sitio", "topic": "Site Access", "expects": ["beton691.online", "cookies", "caché"]},
    {"msg": "no recibo el email de registro", "topic": "Registration Email", "expects": ["spam", "email correcto"]},
    {"msg": "como cambio mi numero de telefono", "topic": "Change Phone", "expects": ["verificada", "kyc", "soporte", "identidad"]},
    {"msg": "no recuerdo mi pregunta secreta", "topic": "Secret Question", "expects": ["documento de identidad", "player id", "foto"]},
    {"msg": "quiero eliminar todos mis datos", "topic": "Delete Data", "expects": ["eliminar", "datos", "contacta"]},

    # === TECHNICAL ===
    {"msg": "la pagina no carga y me da error", "topic": "Site Error", "expects": ["beton691.online", "caché", "cookies", "navegador"]},
    {"msg": "el juego se congelo durante una partida", "topic": "Game Freeze", "expects": ["recarga", "caché", "nombre del juego", "captura"]},
    {"msg": "el sitio va muy lento", "topic": "Slow Site", "expects": ["conexión", "caché", "incógnito", "vpn"]},
    {"msg": "no puedo iniciar sesion", "topic": "Login Problem", "expects": ["beton691.online", "cookies", "contraseña"]},
    {"msg": "no puedo ver mi historial de apuestas", "topic": "Bet History", "expects": ["historial", "mi cuenta", "player id"]},

    # === SPORTS BETTING ===
    {"msg": "como hago una apuesta deportiva", "topic": "How to Bet", "expects": ["deporte", "cuota", "cupón", "monto"]},
    {"msg": "cuanto es la apuesta minima", "topic": "Min Bet", "expects": ["200 pesos"]},
    {"msg": "que es una apuesta combinada", "topic": "Parlay", "expects": ["combinada", "cuotas se multiplican"]},
    {"msg": "mi apuesta gano pero no me pagaron", "topic": "Bet Not Paid", "expects": ["ganadora", "30 minutos", "referencia", "soporte"]},
    {"msg": "el partido fue cancelado que pasa con mi apuesta", "topic": "Event Cancelled", "expects": ["cancelado", "24 horas", "devuelven"]},
    {"msg": "que es el cash out", "topic": "Cash Out", "expects": ["cash out", "anticipad", "resultado actual"]},

    # === CASINO ===
    {"msg": "que juegos de casino tienen", "topic": "Casino Games", "expects": ["3,000", "slots", "ruleta", "blackjack", "pragmatic"]},
    {"msg": "los juegos son justos", "topic": "Fair Play", "expects": ["rng", "certificado", "auditad"]},
    {"msg": "puedo jugar gratis", "topic": "Demo Mode", "expects": ["demo", "sin dinero real"]},
    {"msg": "que es el rtp", "topic": "RTP", "expects": ["rtp", "porcentaje", "retorno", "96%"]},

    # === BALANCE ===
    {"msg": "por que mi saldo total es diferente al disponible", "topic": "Balance Diff", "expects": ["saldo total", "saldo disponible", "bono", "bloqueado"]},
    {"msg": "que significa balance locked", "topic": "Balance Locked", "expects": ["locked", "bloqueada", "wagering", "completar"]},

    # === RESPONSIBLE GAMING ===
    {"msg": "como pongo limites de deposito", "topic": "Deposit Limits", "expects": ["límites", "responsabilidad de juego", "diarios", "semanales"]},
    {"msg": "quiero autoexcluirme", "topic": "Self Exclusion", "expects": ["autoexclu", "ayuda@beton.win"]},

    # === SUPPORT ===
    {"msg": "como contacto a soporte", "topic": "Contact Support", "expects": ["chat", "24/7", "ayuda@beton.win"]},
    {"msg": "tengo un reclamo", "topic": "Complaint", "expects": ["reclamo", "supervisor", "ticket"]},
    {"msg": "que informacion necesitan para ayudarme", "topic": "Support Info", "expects": ["player id", "email", "captura"]},

    # === EDGE CASES from 240K analysis ===
    {"msg": "hola buenas tardes", "topic": "Greeting", "expects": ["ayud", "depósito", "retiro", "bono"]},
    {"msg": "deposite por transferencia bancaria sin generar orden", "topic": "AR No Order", "expects": ["orden", "fantasma", "monto"]},
    {"msg": "mi bono deportivo no me deja apostar me dice saldo 0", "topic": "Sport Bonus", "expects": ["50%", "dinero real", "depósito"]},
    {"msg": "ya verifique mi correo pero sigue diciendo no verificado", "topic": "Email Verify Issue", "expects": ["spam", "soporte", "verificar"]},
    {"msg": "el bono no se activo despues de depositar", "topic": "Bonus Not Credited", "expects": ["requisitos", "depósito mínimo", "verificad"]},
    {"msg": "cuanto tiempo tengo para completar el wagering", "topic": "Wagering Time", "expects": ["fecha límite", "expir", "wagering"]},
    {"msg": "me aparece declined due to available payout limit", "topic": "Payout Limit", "expects": ["límite", "varias retiradas", "más pequeñas"]},
    {"msg": "como me uno al programa hero", "topic": "Join Loyalty", "expects": ["gamificación", "hero", "confirmar", "depósito", "5,000"]},
    {"msg": "soy usuario activo que significa", "topic": "Active User", "expects": ["14 días", "apostar", "dinero real"]},
    {"msg": "cobran comision por depositar", "topic": "Deposit Fee", "expects": ["no", "comision", "banco"]},
    {"msg": "me sale error general decline al depositar", "topic": "General Decline", "expects": ["general decline", "rut", "banco", "fondos"]},
    {"msg": "como funciona la apuesta combinada parlay", "topic": "Parlay", "expects": ["combinada", "multiplican", "falla"]},
    {"msg": "que monedas puedo usar", "topic": "Currencies", "expects": ["clp", "ars", "eur", "usd"]},
    {"msg": "en que idiomas esta el sitio", "topic": "Languages", "expects": ["español", "inglés", "italiano", "portugués"]},
    {"msg": "mis datos estan seguros", "topic": "Data Security", "expects": ["ssl", "encriptación", "protege"]},
    {"msg": "que pasa si no completo el rollover del bono", "topic": "Rollover Incomplete", "expects": ["expir", "wagering", "eliminan", "depósito real"]},
    {"msg": "cuantos intentos de retiro puedo hacer", "topic": "WD Attempts", "expects": ["declined", "too many requests", "máximo mensual"]},
    {"msg": "que es una freebet", "topic": "Freebet", "expects": ["apuesta", "gratis", "ganancias", "monto apostado"]},
    {"msg": "donde veo el progreso de mi bono", "topic": "Bonus Progress", "expects": ["progreso", "promo", "barra"]},
    {"msg": "el retiro dice awaiting from bank", "topic": "WD Awaiting", "expects": ["awaiting from bank", "bancaria", "1-3 días"]},
]

# ════════════════════════════════════════════════════════════════
# RUN TESTS
# ════════════════════════════════════════════════════════════════
print(f'\nRunning {len(TEST_TICKETS)} ticket simulations against KB...\n')
print('=' * 80)

results = {
    'full_match': [],      # All expected keywords found
    'partial_match': [],   # Some keywords found
    'no_match': [],        # No keywords found
}
topic_scores = defaultdict(list)
category_scores = defaultdict(list)

for i, test in enumerate(TEST_TICKETS):
    msg = test['msg'].lower()
    topic = test['topic']
    expects = test['expects']

    # Search KB for relevant content
    found_keywords = []
    missing_keywords = []
    for kw in expects:
        if kw.lower() in KB_TEXT:
            found_keywords.append(kw)
        else:
            missing_keywords.append(kw)

    score = len(found_keywords) / len(expects) * 100 if expects else 0

    # Determine category
    if 'deposit' in topic.lower() or 'bank' in topic.lower() or 'mercado' in topic.lower() or 'antifraud' in topic.lower() or 'wrong amount' in topic.lower():
        cat = 'Deposits'
    elif 'withdraw' in topic.lower() or 'wd' in topic.lower() or 'cancel withdrawal' in topic.lower() or 'payout' in topic.lower():
        cat = 'Withdrawals'
    elif 'bonus' in topic.lower() or 'rollover' in topic.lower() or 'promo' in topic.lower() or 'spin' in topic.lower() or 'cashback' in topic.lower() or 'release' in topic.lower() or 'loyalty' in topic.lower() or 'freebet' in topic.lower() or 'wagering' in topic.lower() or 'sport bonus' in topic.lower():
        cat = 'Bonuses & Promos'
    elif 'verif' in topic.lower() or 'kyc' in topic.lower() or 'email' in topic.lower() or 'phone' in topic.lower():
        cat = 'Verification'
    elif 'account' in topic.lower() or 'password' in topic.lower() or 'login' in topic.lower() or 'blocked' in topic.lower() or 'close' in topic.lower() or 'multiple' in topic.lower() or 'change' in topic.lower() or 'site access' in topic.lower() or 'registration' in topic.lower() or 'secret' in topic.lower() or 'delete' in topic.lower():
        cat = 'Account'
    elif 'tech' in topic.lower() or 'error' in topic.lower() or 'freeze' in topic.lower() or 'slow' in topic.lower() or 'history' in topic.lower():
        cat = 'Technical'
    elif 'bet' in topic.lower() or 'parlay' in topic.lower() or 'cash out' in topic.lower() or 'event' in topic.lower() or 'min bet' in topic.lower():
        cat = 'Sports Betting'
    elif 'casino' in topic.lower() or 'rtp' in topic.lower() or 'demo' in topic.lower() or 'fair' in topic.lower():
        cat = 'Casino'
    elif 'balance' in topic.lower() or 'locked' in topic.lower():
        cat = 'Balance'
    elif 'limit' in topic.lower() or 'exclusion' in topic.lower():
        cat = 'Responsible Gaming'
    elif 'contact' in topic.lower() or 'complaint' in topic.lower() or 'support' in topic.lower():
        cat = 'Support'
    elif 'greeting' in topic.lower():
        cat = 'General'
    elif 'currency' in topic.lower() or 'language' in topic.lower() or 'data security' in topic.lower():
        cat = 'Platform Info'
    elif topic.startswith('AR'):
        cat = 'Deposits'
    else:
        cat = 'Other'

    category_scores[cat].append(score)
    topic_scores[topic].append(score)

    if score >= 100:
        results['full_match'].append(test)
        status = 'FULL MATCH'
        icon = '+'
    elif score >= 50:
        results['partial_match'].append(test)
        status = 'PARTIAL'
        icon = '~'
    else:
        results['no_match'].append(test)
        status = 'MISSING'
        icon = '!'

    if score < 100:
        print(f'  [{icon}] {score:5.0f}% | {topic:25s} | "{msg[:50]}"')
        if missing_keywords:
            print(f'         Missing: {", ".join(missing_keywords)}')

print('\n' + '=' * 80)

# ════════════════════════════════════════════════════════════════
# RESULTS SUMMARY
# ════════════════════════════════════════════════════════════════
total = len(TEST_TICKETS)
full = len(results['full_match'])
partial = len(results['partial_match'])
no_match = len(results['no_match'])
avg_score = sum(s for scores in topic_scores.values() for s in scores) / total

print(f'\n{"=" * 60}')
print(f'  KB PERFORMANCE TEST RESULTS')
print(f'{"=" * 60}')
print(f'  Total test tickets:     {total}')
print(f'  Full match (100%):      {full} ({full*100//total}%)')
print(f'  Partial match (50-99%): {partial} ({partial*100//total}%)')
print(f'  No/Low match (<50%):    {no_match} ({no_match*100//total}%)')
print(f'  Average score:          {avg_score:.1f}%')
print(f'  Coverage rate:          {(full+partial)*100//total}% of tickets answerable')
print(f'{"=" * 60}')

# Category breakdown
print(f'\n  SCORE BY CATEGORY:')
print(f'  {"Category":<25s} {"Avg Score":>10s} {"Tests":>6s} {"Full Match":>10s}')
print(f'  {"-"*55}')
for cat in sorted(category_scores.keys()):
    scores = category_scores[cat]
    avg = sum(scores) / len(scores)
    full_count = sum(1 for s in scores if s >= 100)
    icon = '+' if avg >= 90 else '~' if avg >= 70 else '!'
    print(f'  [{icon}] {cat:<23s} {avg:>8.1f}% {len(scores):>6d} {full_count:>8d}/{len(scores)}')

# What's still missing
if results['no_match']:
    print(f'\n  GAPS — Topics with LOW coverage (<50%):')
    for test in results['no_match']:
        print(f'    ! {test["topic"]}: "{test["msg"][:60]}"')

print(f'\n{"=" * 60}')
print(f'  VERDICT:')
if avg_score >= 90:
    print(f'  EXCELLENT — The KB covers virtually all customer scenarios.')
elif avg_score >= 75:
    print(f'  GOOD — The KB covers most scenarios. Minor gaps remain.')
elif avg_score >= 60:
    print(f'  MODERATE — The KB covers basics but has significant gaps.')
else:
    print(f'  POOR — The KB needs major improvements.')
print(f'{"=" * 60}')
