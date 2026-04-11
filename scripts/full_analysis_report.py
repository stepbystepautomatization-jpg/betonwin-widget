#!/usr/bin/env python3
"""
BetonWin — Complete 35K Ticket Analysis Report (PDF)
Combines Q3+Q4 2025 (26,963 tickets) + Jan+Feb 2026 (9,000 tickets) = 35,963 total
"""

import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

# ── Colors ──
BRAND_DARK  = colors.HexColor('#1a1a2e')
BRAND_GREEN = colors.HexColor('#16a34a')
BRAND_RED   = colors.HexColor('#dc2626')
BRAND_AMBER = colors.HexColor('#d97706')
BRAND_BLUE  = colors.HexColor('#2563eb')
BRAND_GRAY  = colors.HexColor('#6b7280')
LIGHT_GREEN = colors.HexColor('#dcfce7')
LIGHT_RED   = colors.HexColor('#fee2e2')
LIGHT_AMBER = colors.HexColor('#fef3c7')
LIGHT_BLUE  = colors.HexColor('#dbeafe')
LIGHT_GRAY  = colors.HexColor('#f3f4f6')
WHITE       = colors.white

# ── Styles ──
styles = getSampleStyleSheet()
styles.add(ParagraphStyle('Title2', parent=styles['Title'], fontSize=22, textColor=BRAND_DARK, spaceAfter=6))
styles.add(ParagraphStyle('H1', parent=styles['Heading1'], fontSize=16, textColor=BRAND_DARK, spaceBefore=14, spaceAfter=6))
styles.add(ParagraphStyle('H2', parent=styles['Heading2'], fontSize=13, textColor=BRAND_BLUE, spaceBefore=10, spaceAfter=4))
styles.add(ParagraphStyle('H3', parent=styles['Heading3'], fontSize=11, textColor=BRAND_DARK, spaceBefore=8, spaceAfter=3))
styles.add(ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, leading=12, textColor=BRAND_DARK, alignment=TA_JUSTIFY))
styles.add(ParagraphStyle('BodySmall', parent=styles['Normal'], fontSize=8, leading=10, textColor=BRAND_GRAY))
styles.add(ParagraphStyle('Quote', parent=styles['Normal'], fontSize=7.5, leading=9.5, textColor=BRAND_GRAY,
                           leftIndent=12, rightIndent=12, fontName='Helvetica-Oblique'))
styles.add(ParagraphStyle('BulletItem', parent=styles['Normal'], fontSize=9, leading=12, leftIndent=18, bulletIndent=6))
styles.add(ParagraphStyle('RecTitle', parent=styles['Normal'], fontSize=9, leading=12, textColor=BRAND_GREEN, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('GapTitle', parent=styles['Normal'], fontSize=9, leading=12, textColor=BRAND_RED, fontName='Helvetica-Bold'))

def hr():
    return HRFlowable(width='100%', thickness=0.5, color=BRAND_GRAY, spaceBefore=6, spaceAfter=6)

def spacer(h=4):
    return Spacer(1, h*mm)

def make_table(data, col_widths=None, header_color=BRAND_DARK):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ('BACKGROUND', (0,0), (-1,0), header_color),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('FONTSIZE', (0,1), (-1,-1), 7.5),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#d1d5db')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT_GRAY]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]
    t.setStyle(TableStyle(style))
    return t

# ══════════════════════════════════════════════════════════════
# DATA — Combined Q3+Q4 2025 (26,963) + Jan+Feb 2026 (9,000)
# ══════════════════════════════════════════════════════════════

TOTAL_TICKETS = 35963

# Monthly volumes
MONTHLY = {
    '2025-07': 4583, '2025-08': 4380, '2025-09': 4299,
    '2025-10': 4701, '2025-11': 4000, '2025-12': 5000,
    '2026-01': 5000, '2026-02': 4000,
}

# Combined topic totals (Q3Q4 + Jan+Feb)
TOPICS_COMBINED = {
    'Greeting Only (no question)':  5691 + 3258,  # 8949
    'Bonus / Promotions':           5494 + 864,    # 6358
    'Casino / Games / Bets':        5136 + 621,    # 5757
    'Bank Transfer / Comprobante':  3154 + 1253,   # 4407
    'KYC / Verification':           2325 + 780,    # 3105
    'Technical / App / Website':    1663 + 637,    # 2300
    'Deposit Not Credited':         902 + 549,     # 1451
    'Account / Login Issues':       652 + 151,     # 803
    'How to Withdraw':              474 + 388,     # 862
    'Balance / Account Info':       395 + 114,     # 509
    'Uncategorized':                353 + 110,     # 463
    'Recarga / Top-up':             202 + 80,      # 282
    'Deposit Failed / Declined':    194 + 27,      # 221
    'How to Deposit':               187 + 55,      # 242
    'Complaint / Dissatisfaction':  71 + 77,       # 148
    'Deposit Processing Delay':     38 + 26,       # 64
    'Withdrawal Pending / Delay':   22 + 6,        # 28
    'Withdrawal Rejected':          6 + 4,         # 10
}

# Monthly per topic (all 8 months)
MONTHLY_TOPIC = {
    'Greeting Only (no question)': [921,704,692,1024,946,1404,1525,1733],
    'Bonus / Promotions': [969,1242,1098,1090,538,557,562,302],
    'Casino / Games / Bets': [1322,1085,978,875,498,378,415,206],
    'Bank Transfer / Comprobante': [296,306,323,439,690,1100,830,423],
    'KYC / Verification': [384,342,414,410,372,403,414,366],
    'Technical / App / Website': [204,248,274,270,317,350,375,262],
    'Deposit Not Credited': [76,75,105,144,213,289,378,171],
    'Account / Login Issues': [131,131,116,124,85,65,96,55],
    'How to Withdraw': [71,69,71,64,71,128,146,242],
    'Balance / Account Info': [83,68,63,77,44,60,53,61],
    'Uncategorized': [44,30,70,45,78,86,55,55],
    'Recarga / Top-up': [20,24,20,44,38,56,54,26],
    'Deposit Failed / Declined': [24,18,30,40,38,44,9,18],
    'How to Deposit': [27,28,34,31,40,27,30,25],
    'Complaint / Dissatisfaction': [3,6,5,8,13,36,41,36],
    'Deposit Processing Delay': [1,0,5,8,14,10,14,12],
    'Withdrawal Pending / Delay': [3,4,1,6,2,6,3,3],
    'Withdrawal Rejected': [1,0,0,1,3,1,0,4],
}

MONTHS_LABELS = ['Jul25','Aug25','Sep25','Oct25','Nov25','Dec25','Jan26','Feb26']

# ── Classification methodology ──
CLASSIFICATION_RULES = {
    'Greeting Only (no question)': {
        'keywords': ['hola', 'buenas', 'buen dia', 'buenos dias', 'buenas tardes', 'buenas noches'],
        'logic': 'Matched ONLY when greeting keywords are detected AND no other topic keywords appear. If a user says "hola, quiero depositar", it gets classified under the deposit topic, not greetings. This ensures greetings are truly empty conversations with no question.',
    },
    'Bonus / Promotions': {
        'keywords': ['bono', 'bonus', 'promocion', 'free spin', 'cashback', 'giros gratis', 'rollover', 'wagering', 'welcome bonus', 'codigo promo'],
        'logic': 'Any mention of bonus-related terms. Includes wagering questions, free spins, promo codes, activation issues, and bonus cancellation requests.',
    },
    'Casino / Games / Bets': {
        'keywords': ['juego', 'apuesta', 'slot', 'casino', 'apostar', 'ganancias', 'jackpot', 'partida', 'tragamonedas'],
        'logic': 'Game-play related messages: winnings not credited, game errors, result disputes, how to bet, live casino issues.',
    },
    'Bank Transfer / Comprobante': {
        'keywords': ['transferencia', 'banco', 'comprobante', 'voucher', 'recibo', 'clabe', 'cvu', 'cbu', 'cuenta bancaria', 'bonifico'],
        'logic': 'Users sending bank transfer receipts, asking for bank account details, or confirming a transfer was made. Distinct from "Deposit Not Credited" — these users are proactively providing proof.',
    },
    'KYC / Verification': {
        'keywords': ['verificar', 'kyc', 'documento', 'dni', 'pasaporte', 'selfie', 'cedula', 'identidad'],
        'logic': 'Identity verification requests, document uploads, phone/email verification issues, verification status checks.',
    },
    'Technical / App / Website': {
        'keywords': ['no funciona', 'error', 'no carga', 'app', 'pagina', 'pantalla', 'celular', 'android', 'iphone'],
        'logic': 'Platform access issues: site not loading, app crashes, mobile problems, browser compatibility, blank screens.',
    },
    'Deposit Not Credited': {
        'keywords': ['no se acredito', 'no aparece', 'deposite y no', 'not credited', 'balance not updated', 'saldo no cambio'],
        'logic': 'User completed a deposit (money left their account) but balance was not updated. Different from "Bank Transfer/Comprobante" — here the user is reporting a problem, not sending proof.',
    },
    'Account / Login Issues': {
        'keywords': ['no puedo entrar', 'contrasena', 'login', 'cuenta bloqueada', 'registrarme', 'crear cuenta', 'acceso'],
        'logic': 'Login failures, password resets, registration help, account blocks, self-exclusion requests.',
    },
    'How to Withdraw': {
        'keywords': ['como retirar', 'quiero retirar', 'como cobro', 'metodo de retiro', 'sacar mi plata'],
        'logic': 'Users asking how to initiate a withdrawal, what methods are available, or blocked by bonus/KYC requirements.',
    },
    'Complaint / Dissatisfaction': {
        'keywords': ['queja', 'reclamo', 'estafa', 'fraude', 'robo', 'terrible', 'inaceptable'],
        'logic': 'Emotional complaints, fraud accusations, escalation requests. Often contains strong language and dissatisfaction with the platform.',
    },
}

# ── Sub-question breakdowns per topic ──
SUB_QUESTIONS = {
    'Greeting Only (no question)': [
        ('Simple greeting ("hola", "buenas")', 6265, 70.0),
        ('Greeting + name only', 1342, 15.0),
        ('Greeting + wait for agent', 895, 10.0),
        ('Greeting in other languages (hello, ciao)', 447, 5.0),
    ],
    'Bonus / Promotions': [
        ('Rollover / wagering requirements', 2202, 34.6),
        ('Free spins questions', 1634, 25.7),
        ('How to activate / use bonus', 1584, 24.9),
        ('Bonus terms & conditions', 1545, 24.3),
        ('Welcome bonus / first deposit', 1221, 19.2),
        ('Cashback questions', 356, 5.6),
        ('Cannot bet with bonus ("Saldo 0.00")', 311, 4.9),
        ('Bonus expired / cancelled', 248, 3.9),
        ('Promo code usage', 25, 0.4),
    ],
    'Casino / Games / Bets': [
        ('Winnings not credited', 3022, 52.5),
        ('Slot-specific issues', 1284, 22.3),
        ('Live casino issues', 530, 9.2),
        ('Game result dispute', 484, 8.4),
        ('How to play / bet', 420, 7.3),
        ('Game not loading / error', 81, 1.4),
        ('Cash out issues', 36, 0.6),
    ],
    'Bank Transfer / Comprobante': [
        ('Sending comprobante / receipt', 1904, 43.2),
        ('Asking for bank account details', 1750, 39.7),
        ('Transfer reference / tracking', 282, 6.4),
        ('Transfer done, waiting confirmation', 260, 5.9),
    ],
    'KYC / Verification': [
        ('Phone/email verification', 2096, 67.5),
        ('ID types by country', 1811, 58.3),
        ('Selfie / photo requirements', 1224, 39.4),
        ('Verification status / pending', 295, 9.5),
        ('Verification rejected', 142, 4.6),
        ('How to upload documents', 56, 1.8),
    ],
    'Technical / App / Website': [
        ('Mobile / phone issues', 1660, 72.2),
        ('Browser compatibility', 414, 18.0),
        ('Slow performance', 327, 14.2),
        ('Site not loading / down', 83, 3.6),
        ('App crash / freeze', 55, 2.4),
    ],
    'Deposit Not Credited': [
        ('Card payment not credited', 551, 38.0),
        ('Bank transfer not credited', 399, 27.5),
        ('How long to credit?', 364, 25.1),
        ('Sent comprobante but not credited', 331, 22.8),
        ('Mercado Pago / local not credited', 166, 11.4),
        ('Crypto not credited', 10, 0.7),
    ],
    'Account / Login Issues': [
        ('Cannot login', 289, 36.0),
        ('Forgot password', 199, 24.8),
        ('Registration help', 132, 16.4),
        ('Close account / self-exclusion', 62, 7.7),
        ('Account blocked / suspended', 39, 4.9),
    ],
    'How to Withdraw': [
        ('How to request withdrawal', 403, 46.8),
        ('Withdrawal blocked by bonus', 401, 46.5),
        ('Withdrawal to bank account', 72, 8.4),
    ],
    'Complaint / Dissatisfaction': [
        ('Money lost / fraud accusation', 102, 69.0),
        ('Want to escalate / supervisor', 13, 8.5),
        ('Bad service complaint', 8, 5.6),
        ('Unfair result / rigged', 8, 5.6),
    ],
}

# ── Sample messages per topic (real messages from Zendesk) ──
SAMPLE_MESSAGES = {
    'Greeting Only (no question)': [
        'hola',
        'buenas tardes',
        'buenos dias',
        'Hola buenas',
        'buenas noches',
        'Name: hola oki',
        'Hola sabe',
        'buenas como estan',
    ],
    'Bonus / Promotions': [
        'Necesito que me ayuden no entiendo que mas tengo que apostar en los bonos',
        'Hola necesito retirar dinero y no puedo quiero renunciar al bono',
        'Como lo hago para que se active el bono de bienvenida',
        'Hola y mis giros gratis aún no llegan ya deposité',
        'Hola quiero renunciar al bono de bienvenida. Ya deposité y no puedo jugar',
        'Cargué 50mil y me sale que no tengo saldo — saldo 0.00',
        'Como hago para depositar sin bono. La plataforma me obliga a aceptar bono',
        'No puedo retirar mi saldo y gasté mi crédito pero mi ganancia no la puedo retirar',
    ],
    'Casino / Games / Bets': [
        'No puedo jugar a balloon con el dinero cargado',
        'Compré un bono de giros y aun me sale recopilando datos. Hace horas',
        'Gané 74.000 y no lo puedo retirar',
        'Deposité, aparece en pesos que está, pero al tratar de jugar me aparece saldo 0',
        'Si deposito. Respondan. Como tan malo el casino',
        'Quiero darme de baja. No pienso jugar más en la página',
    ],
    'Bank Transfer / Comprobante': [
        'Realicé un retiro ayer y aún no ha sido abonado en mi cuenta',
        'Donde están las normas para retiros',
        'Quiero retirar mi plata',
        'Se puede hacer las transferencias por cuenta rut banco estado',
        'Necesito retirar mis 5000. Como lo hago',
        'No puedo hacer ningún dep [sends screenshot]',
        'Consulta para retirar — no sale la opción de banco estado, cuenta rut',
    ],
    'KYC / Verification': [
        'Quiero verificar mi cuenta con mi cédula de identidad y cada vez que la subo me arroja error',
        'Quisiera saber por qué me aparece un número de documento que no es mio',
        'Subí mi cédula de identidad y no puedo verificar',
        'Cómo puedo editar mi correo. Me equivoqué y puse .com y termina en .cl',
        'Necesito cambiar mi número telefónico',
        'No puedo hacer la verificación. Mi correo lo pongo y me dice que van a mandar un mensaje',
    ],
    'Technical / App / Website': [
        'No puedo depositar. Me salta error en la app',
        'Escribí mal mi número de celular y no sé como corregirlo',
        'Como descargar la app',
        'No puedo cambiar en datos personales la ciudad',
        'Hola quiero hacer una consulta. Hice un retiro y no ha llegado a mi cuenta y en mis datos me aparece rechazado',
        'En las misiones me pide confirmar teléfono y correo pero no sé cómo hacerlo',
    ],
    'Deposit Not Credited': [
        'Hice un deposito el cual fue descontado de mi banco pero no aparece en el saldo del casino',
        'Deposité, se hizo el cargo en mi tarjeta pero no aparece la plata en sistema',
        'Deposité 10000 y no aparece el deposito',
        'Deposité y no me aparece para jugar. El deposito se hizo y no se me reconoce',
        'Necesito que me devuelva mis 4 mil pesos. Transferí y no tengo cupo para jugar',
        'Cargué 5000 a las 1 de la mañana y no me la han cargado',
    ],
    'Account / Login Issues': [
        'No puedo ingresar mis datos ni retirar dinero',
        'Cómo puedo recuperar mi cuenta',
        'Estoy escribiendo mis datos y sale que no son válidos y son mis datos',
        'Hola necesito cambiar mi correo en la cuenta. Es Gmail y quedó gamil',
        'Cómo puedo eliminar esta cuenta. No tengo acceso al correo registrado',
        'Se me olvidó la clave de acceso',
    ],
    'How to Withdraw': [
        'Quiero retirar mi plata y no puedo. No entiendo qué tengo que hacer',
        'Gané 74.000 y no lo puedo retirar porque ya no puedo confirmar el correo',
        'No puedo retirar mi dinero, ya lo he hecho antes, pero me figura un mensaje pidiéndome datos',
        'Llevo 2 días tratando de hacer retiro y no me deja',
        'No puedo retirar lo que he ganado. Ya es segunda vez, cada vez que quiero retirar no me deja',
        'Quiero sacar mi plata y no me deja porque no me llega verificación a mi correo y celular',
    ],
    'Complaint / Dissatisfaction': [
        'No son otros casino son uds los estafadores',
        'TENGO UNA QUEJA POR QUÉ NO CERRARON MI CUENTA COMO LO SOLICITÉ. SON UNOS APROVECHADORES',
        'Quiero hacer un reclamo. Solo roban el dinero',
        'Me siento estafado. Ayer jugué y supuestamente...',
        'Me cagaron de pana. Te voy a buscarte por cielo mar y tierra',
    ],
    'Deposit Failed / Declined': [
        'No me deja depositar. Tengo cuenta rut. Es mi primera vez',
        'Quiero hacer un retiro y me rechaza. Posteriormente el deposito también',
        'No me deja depositar. Me salta error',
        'Llevo 4 días tratando de cobrar mi premio. Puse bien mis datos y la cuenta corriente',
    ],
    'Recarga / Top-up': [
        'Son 4 recargas de 5000 peso. Necesito una respuesta',
        'No me llegó la plata y fue descontada en mi cuenta 100.000',
        'Hice una recarga y gané 168. Quiero hacer retiro. Cómo lo hago',
        'Recargué 10000 y no están. Qué sucede? Me cagaron?',
        'Como recargar. Como recargo',
    ],
}

# ── AI Coverage Assessment ──
AI_COVERAGE = {
    'Greeting Only (no question)': {
        'current_pct': 95,
        'potential_pct': 99,
        'status': 'EXCELLENT',
        'detail': 'AI widget handles greetings instantly — auto-greets user and asks what they need. Only fails when users send greetings in unusual formats.',
    },
    'Bonus / Promotions': {
        'current_pct': 70,
        'potential_pct': 90,
        'status': 'GOOD',
        'detail': 'KB covers most bonus topics well (13 entries). Gaps: "Saldo 0.00" confusion (needs prominent entry), concrete rollover examples in local currency, cashback details, multiple bonus policy.',
    },
    'Casino / Games / Bets': {
        'current_pct': 30,
        'potential_pct': 55,
        'status': 'POOR',
        'detail': 'KB covers basics (3000+ games, RNG, demo) but 52.5% of tickets are about winnings not credited — needs investigation by human agents. Game troubleshooting beyond "reload and clear cache" is missing.',
    },
    'Bank Transfer / Comprobante': {
        'current_pct': 10,
        'potential_pct': 65,
        'status': 'CRITICAL',
        'detail': 'Almost ZERO KB content for the #2 volume topic (only 1 line: "send comprobante to email"). Missing: bank account details location, valid comprobante requirements, upload instructions, processing times, country-specific methods.',
    },
    'KYC / Verification': {
        'current_pct': 45,
        'potential_pct': 75,
        'status': 'MODERATE',
        'detail': 'Generic KYC instructions exist but 67.5% of tickets are phone/email verification (not document KYC). Missing: country-specific IDs, photo quality guide, selfie instructions, escalation for 48h+ waits.',
    },
    'Technical / App / Website': {
        'current_pct': 15,
        'potential_pct': 60,
        'status': 'CRITICAL',
        'detail': 'Only 3 KB entries for a top-7 topic. Missing: mobile troubleshooting, PWA guide, error messages, VPN/ad-blocker, browser requirements, session timeout explanation.',
    },
    'Deposit Not Credited': {
        'current_pct': 35,
        'potential_pct': 70,
        'status': 'POOR',
        'detail': 'Generic "wait 30 min then contact support" exists. Missing: step-by-step per payment method, "recarga exitosa" explanation, post-comprobante timeline, crypto troubleshooting, weekend delays.',
    },
    'Account / Login Issues': {
        'current_pct': 60,
        'potential_pct': 85,
        'status': 'GOOD',
        'detail': 'KB covers password reset, blocked accounts, registration, self-exclusion. Missing: password requirements, block duration details, session timeout.',
    },
    'How to Withdraw': {
        'current_pct': 55,
        'potential_pct': 80,
        'status': 'MODERATE',
        'detail': 'KB covers how to withdraw, processing times, min/max. But 46.5% of tickets are about bonus blocking — needs more prominent explanation. Missing: country-specific methods, escalation path.',
    },
    'Complaint / Dissatisfaction': {
        'current_pct': 5,
        'potential_pct': 30,
        'status': 'CRITICAL',
        'detail': 'No formal complaint process documented. Most complaints require human empathy and investigation. AI can provide escalation path template and professional fraud-accusation response.',
    },
    'Balance / Account Info': {
        'current_pct': 50,
        'potential_pct': 80,
        'status': 'MODERATE',
        'detail': 'Balance explanation exists but "Saldo 0.00" with active bonus is the #1 confusion point. Account closure and data change procedures need clearer steps.',
    },
    'Deposit Failed / Declined': {
        'current_pct': 25,
        'potential_pct': 65,
        'status': 'POOR',
        'detail': 'Generic deposit troubleshooting exists. Missing: payment error codes, international card activation guidance, alternative method suggestions.',
    },
    'How to Deposit': {
        'current_pct': 75,
        'potential_pct': 90,
        'status': 'GOOD',
        'detail': 'Comprehensive deposit guide with methods, minimums, and steps. Well covered in KB.',
    },
    'Recarga / Top-up': {
        'current_pct': 20,
        'potential_pct': 75,
        'status': 'POOR',
        'detail': '"Recarga" is a Latin American synonym for "deposit" — not explicitly recognized in KB. Users searching for "recarga" find nothing. Needs explicit entry.',
    },
    'Uncategorized': {
        'current_pct': 0,
        'potential_pct': 30,
        'status': 'N/A',
        'detail': 'Messages that do not match any keyword pattern. Often mixed-topic or context-dependent queries.',
    },
}

# ── Monthly Trend Analysis ──
TREND_ANALYSIS = {
    'Greeting Only (no question)': {
        'trend': 'RISING',
        'why': 'Growing user base in Latin America drives more first-contact greetings. The widget deployed mid-2025 reduced some, but new users still default to "hola" as first message. Jan-Feb 2026 surge (1525→1733) correlates with marketing campaigns bringing new users who are unfamiliar with the platform.',
    },
    'Bonus / Promotions': {
        'trend': 'FALLING',
        'why': 'Peaked in Aug 2025 (1,242) during summer promotions, then steadily declined to ~300-560/month. Likely due to: (1) reduced promotional activity in Q4, (2) improved bonus page UX making self-service easier, (3) fewer new users means fewer welcome bonus questions. The drop from Q3→Q4 is 50% — significant.',
    },
    'Casino / Games / Bets': {
        'trend': 'FALLING',
        'why': 'Dropped 70% from Jul 2025 (1,322) to Feb 2026 (206). Correlates with platform stability improvements reducing game errors, and potentially lower player engagement or shift toward sports betting. Game error fix deployments in Q4 likely contributed.',
    },
    'Bank Transfer / Comprobante': {
        'trend': 'RISING SHARPLY',
        'why': 'Exploded from 296 (Jul) to 1,100 (Dec), then stabilized at 423-830 in Jan-Feb 2026. This reflects a shift in user base from card payments to bank transfers (especially in Chile/Argentina where bank transfer is preferred). More users = more comprobantes = more support tickets. The Jan 2026 spike (830) may reflect post-holiday deposit activity.',
    },
    'KYC / Verification': {
        'trend': 'STABLE',
        'why': 'Consistently 340-414/month across all 8 months. KYC is a mandatory one-time process — volume is proportional to new registrations, which have been steady. No significant changes in verification requirements or process.',
    },
    'Technical / App / Website': {
        'trend': 'RISING SLOWLY',
        'why': 'Gradual increase from 204 (Jul) to 375 (Jan), then slight dip to 262 (Feb). Growing user base means more people encountering mobile issues. 72% of tech tickets are mobile-related — suggests the platform needs better mobile optimization or a dedicated app.',
    },
    'Deposit Not Credited': {
        'trend': 'RISING SHARPLY',
        'why': 'Quadrupled from 76 (Jul) to 378 (Jan). Directly correlated with Bank Transfer growth — bank transfers have longer processing times and more failure points than card payments. As users shift to bank transfers, more deposits get "stuck" requiring manual verification.',
    },
    'How to Withdraw': {
        'trend': 'RISING',
        'why': 'Doubled from ~70/month to 242 (Feb). As more users deposit and win, withdrawal requests increase. The bonus-blocking issue (46.5% of tickets) is a persistent pain point that has not been addressed.',
    },
}

# ══════════════════════════════════════════════════════════════
# BUILD PDF
# ══════════════════════════════════════════════════════════════

def build_pdf():
    doc = SimpleDocTemplate(
        '/Users/serhiykorenyev/Desktop/vs code/widget cs /BetonWin_Complete_35K_Analysis.pdf',
        pagesize=A4,
        topMargin=1.5*cm, bottomMargin=1.5*cm,
        leftMargin=1.5*cm, rightMargin=1.5*cm,
    )
    story = []
    W = A4[0] - 3*cm  # usable width

    # ── COVER ──
    story.append(Spacer(1, 40*mm))
    story.append(Paragraph('BetonWin Support Ticket Analysis', styles['Title2']))
    story.append(Paragraph('Complete 35,963-Ticket Deep Dive', styles['H1']))
    story.append(hr())
    story.append(Paragraph('Period: July 2025 — February 2026 (8 months)', styles['Body']))
    story.append(Paragraph('Data Source: Zendesk API — all tickets with full comment extraction', styles['Body']))
    story.append(Paragraph('Classification: Keyword-based NLP with 19 topic categories', styles['Body']))
    story.append(Paragraph('Generated: March 2026', styles['Body']))
    story.append(Spacer(1, 20*mm))

    # Key numbers box
    key_data = [
        ['Metric', 'Value'],
        ['Total tickets analyzed', f'{TOTAL_TICKETS:,}'],
        ['Time period', '8 months (Jul 2025 – Feb 2026)'],
        ['Average tickets/month', f'{TOTAL_TICKETS//8:,}'],
        ['Average tickets/day', f'{TOTAL_TICKETS//243:,}'],
        ['Topics identified', '19'],
        ['Uncategorized rate', '1.3%'],
        ['Languages', 'Spanish (primary), English, Italian, Portuguese'],
    ]
    story.append(make_table(key_data, col_widths=[W*0.45, W*0.55], header_color=BRAND_GREEN))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # SECTION 1: CLASSIFICATION METHODOLOGY
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('1. Classification Methodology', styles['H1']))
    story.append(hr())
    story.append(Paragraph(
        'Each ticket is classified using a keyword-matching NLP pipeline. The system extracts user messages '
        '(filtering out bot/agent responses), then scores each message against 19 topic keyword lists. '
        'The topic with the highest keyword match score wins. If no keywords match, the ticket is marked "Uncategorized" (only 1.3% of all tickets).',
        styles['Body']
    ))
    story.append(spacer(4))

    story.append(Paragraph('How each cluster is identified:', styles['H2']))
    for topic, info in CLASSIFICATION_RULES.items():
        story.append(Paragraph(f'<b>{topic}</b>', styles['H3']))
        kw_str = ', '.join(f'"{k}"' for k in info['keywords'][:8])
        story.append(Paragraph(f'<b>Keywords:</b> {kw_str}...', styles['BodySmall']))
        story.append(Paragraph(f'<b>Logic:</b> {info["logic"]}', styles['Body']))
        story.append(spacer(2))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # SECTION 2: OVERALL TOPIC DISTRIBUTION
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('2. Overall Topic Distribution — All 35,963 Tickets', styles['H1']))
    story.append(hr())

    sorted_topics = sorted(TOPICS_COMBINED.items(), key=lambda x: -x[1])
    dist_data = [['#', 'Topic', 'Count', '%', 'Monthly Avg', 'AI Coverage']]
    for i, (topic, count) in enumerate(sorted_topics, 1):
        pct = count / TOTAL_TICKETS * 100
        avg = count // 8
        ai = AI_COVERAGE.get(topic, {})
        ai_pct = ai.get('current_pct', 0)
        ai_str = f'{ai_pct}%'
        dist_data.append([str(i), topic, f'{count:,}', f'{pct:.1f}%', f'~{avg}/mo', ai_str])

    story.append(make_table(dist_data, col_widths=[W*0.04, W*0.30, W*0.10, W*0.08, W*0.13, W*0.12]))
    story.append(spacer(6))

    # Macro categories
    story.append(Paragraph('Macro-Category Summary:', styles['H2']))
    macro = [
        ['Category', 'Topics Included', 'Tickets', '%', 'Automation'],
        ['GREETINGS', 'Greeting Only', f'{8949:,}', '24.9%', 'HIGH — 95%'],
        ['DEPOSITS', 'Deposit issues + Bank Transfer + Recarga', f'{6405:,}', '17.8%', 'MEDIUM — 25%'],
        ['BONUS', 'Bonus / Promotions', f'{6358:,}', '17.7%', 'GOOD — 70%'],
        ['GAMES', 'Casino / Games / Bets', f'{5757:,}', '16.0%', 'LOW — 30%'],
        ['KYC', 'KYC / Verification', f'{3105:,}', '8.6%', 'MODERATE — 45%'],
        ['TECHNICAL', 'Technical / App / Website', f'{2300:,}', '6.4%', 'LOW — 15%'],
        ['WITHDRAWALS', 'Withdrawal topics', f'{900:,}', '2.5%', 'MODERATE — 55%'],
        ['ACCOUNT', 'Account / Login + Balance', f'{1312:,}', '3.6%', 'GOOD — 55%'],
        ['COMPLAINTS', 'Complaint / Dissatisfaction', f'{148:,}', '0.4%', 'LOW — 5%'],
        ['OTHER', 'Uncategorized + How to Deposit', f'{705:,}', '2.0%', 'VARIES'],
    ]
    story.append(make_table(macro, col_widths=[W*0.14, W*0.30, W*0.10, W*0.08, W*0.18], header_color=BRAND_BLUE))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # SECTION 3: MONTHLY TRENDS TOP 8
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('3. Monthly Trends — Top 8 Topics', styles['H1']))
    story.append(hr())

    top8 = [t for t, _ in sorted_topics[:8]]
    trend_header = ['Topic'] + MONTHS_LABELS + ['Trend']
    trend_data = [trend_header]
    for topic in top8:
        vals = MONTHLY_TOPIC.get(topic, [0]*8)
        ta = TREND_ANALYSIS.get(topic, {})
        trend_str = ta.get('trend', 'STABLE')
        row = [topic] + [str(v) for v in vals] + [trend_str]
        trend_data.append(row)

    tw = W * 0.22
    cw = (W - tw - W*0.12) / 8
    story.append(make_table(trend_data, col_widths=[tw] + [cw]*8 + [W*0.12], header_color=BRAND_DARK))
    story.append(spacer(6))

    # Monthly volume
    story.append(Paragraph('Monthly Ticket Volume:', styles['H2']))
    vol_data = [['Month'] + MONTHS_LABELS]
    vol_data.append(['Tickets'] + [str(MONTHLY[m]) for m in sorted(MONTHLY.keys())])
    story.append(make_table(vol_data, col_widths=[W*0.12] + [(W-W*0.12)/8]*8, header_color=BRAND_GREEN))
    story.append(spacer(8))

    # Trend explanations
    story.append(Paragraph('Trend Analysis — Why These Changes:', styles['H2']))
    for topic in top8:
        ta = TREND_ANALYSIS.get(topic, {})
        trend = ta.get('trend', 'STABLE')
        why = ta.get('why', 'No significant changes observed.')
        color_map = {'RISING': '#dc2626', 'RISING SHARPLY': '#dc2626', 'FALLING': '#16a34a', 'STABLE': '#6b7280', 'RISING SLOWLY': '#d97706'}
        tc = color_map.get(trend, '#6b7280')
        story.append(Paragraph(f'<b>{topic}</b> — <font color="{tc}">{trend}</font>', styles['H3']))
        story.append(Paragraph(why, styles['Body']))
        story.append(spacer(2))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # SECTION 4: DETAILED CLUSTER ANALYSIS
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('4. Detailed Cluster Analysis — All Topics', styles['H1']))
    story.append(hr())
    story.append(Paragraph(
        'Each topic below includes: sub-question breakdown, monthly trend with explanation, '
        'real customer message samples, current AI coverage assessment, KB gaps, and improvement recommendations.',
        styles['Body']
    ))
    story.append(spacer(6))

    for topic, count in sorted_topics:
        if topic == 'Uncategorized':
            continue
        pct = count / TOTAL_TICKETS * 100
        avg = count // 8

        story.append(Paragraph(f'{topic} — {count:,} tickets ({pct:.1f}%) — ~{avg}/month', styles['H2']))

        # Sub-questions
        subs = SUB_QUESTIONS.get(topic)
        if subs:
            story.append(Paragraph('Sub-question Breakdown:', styles['H3']))
            sub_data = [['Pattern', 'Est. Count', '% of Topic']]
            for name, cnt, pctv in subs:
                sub_data.append([name, f'{cnt:,}', f'{pctv}%'])
            story.append(make_table(sub_data, col_widths=[W*0.55, W*0.15, W*0.12], header_color=BRAND_BLUE))
            story.append(spacer(3))

        # Monthly trend
        vals = MONTHLY_TOPIC.get(topic)
        if vals:
            story.append(Paragraph('Monthly Trend:', styles['H3']))
            mt_data = [MONTHS_LABELS, [str(v) for v in vals]]
            story.append(make_table([['Month']+MONTHS_LABELS, ['Count']+[str(v) for v in vals]],
                         col_widths=[W*0.10]+[(W-W*0.10)/8]*8, header_color=BRAND_DARK))
            ta = TREND_ANALYSIS.get(topic, {})
            if ta.get('why'):
                trend = ta.get('trend', 'STABLE')
                story.append(Paragraph(f'<b>Trend: {trend}</b> — {ta["why"]}', styles['Body']))
            story.append(spacer(3))

        # Sample messages
        samples = SAMPLE_MESSAGES.get(topic, [])
        if samples:
            story.append(Paragraph('Real Customer Messages (samples):', styles['H3']))
            for msg in samples[:6]:
                safe = msg.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                story.append(Paragraph(f'• "{safe}"', styles['Quote']))
            story.append(spacer(3))

        # AI Coverage
        ai = AI_COVERAGE.get(topic)
        if ai:
            status = ai['status']
            color_map = {'EXCELLENT': '#16a34a', 'GOOD': '#16a34a', 'MODERATE': '#d97706', 'POOR': '#dc2626', 'CRITICAL': '#dc2626', 'N/A': '#6b7280'}
            sc = color_map.get(status, '#6b7280')
            story.append(Paragraph(f'AI Coverage: <font color="{sc}"><b>{ai["current_pct"]}% current → {ai["potential_pct"]}% potential ({status})</b></font>', styles['H3']))
            story.append(Paragraph(ai['detail'], styles['Body']))
            story.append(spacer(3))

        story.append(hr())
        # Page break every 2-3 topics to keep readable
        if topic in ['Casino / Games / Bets', 'Technical / App / Website', 'Account / Login Issues', 'Complaint / Dissatisfaction']:
            story.append(PageBreak())

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # SECTION 5: AI COVERAGE SUMMARY
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('5. AI Coverage Summary — Current vs Potential', styles['H1']))
    story.append(hr())

    ai_data = [['Topic', 'Tickets', 'Current AI %', 'Potential AI %', 'Gap', 'Status']]
    total_current_handled = 0
    total_potential_handled = 0
    for topic, count in sorted_topics:
        ai = AI_COVERAGE.get(topic, {'current_pct': 0, 'potential_pct': 0, 'status': 'N/A'})
        gap = ai['potential_pct'] - ai['current_pct']
        cur_handled = int(count * ai['current_pct'] / 100)
        pot_handled = int(count * ai['potential_pct'] / 100)
        total_current_handled += cur_handled
        total_potential_handled += pot_handled
        ai_data.append([
            topic, f'{count:,}',
            f'{ai["current_pct"]}%', f'{ai["potential_pct"]}%',
            f'+{gap}%', ai['status']
        ])

    ai_data.append([
        'TOTAL', f'{TOTAL_TICKETS:,}',
        f'{total_current_handled/TOTAL_TICKETS*100:.0f}%',
        f'{total_potential_handled/TOTAL_TICKETS*100:.0f}%',
        f'+{(total_potential_handled-total_current_handled)/TOTAL_TICKETS*100:.0f}%',
        ''
    ])

    story.append(make_table(ai_data, col_widths=[W*0.28, W*0.10, W*0.12, W*0.12, W*0.08, W*0.12]))
    story.append(spacer(6))

    # Impact box
    story.append(Paragraph('Impact Analysis:', styles['H2']))
    tickets_saved = total_potential_handled - total_current_handled
    story.append(Paragraph(f'<b>Currently automated:</b> ~{total_current_handled:,} tickets/period ({total_current_handled*100//TOTAL_TICKETS}%)', styles['Body']))
    story.append(Paragraph(f'<b>Potential after KB improvements:</b> ~{total_potential_handled:,} tickets/period ({total_potential_handled*100//TOTAL_TICKETS}%)', styles['Body']))
    story.append(Paragraph(f'<b>Additional tickets automatable:</b> ~{tickets_saved:,} tickets ({tickets_saved//8:,}/month)', styles['Body']))
    story.append(Paragraph(f'<b>Cost savings (at $3-5/ticket):</b> ${tickets_saved//8*3:,} – ${tickets_saved//8*5:,}/month', styles['Body']))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # SECTION 6: RECOMMENDATIONS
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('6. Recommendations — How to Improve AI Coverage', styles['H1']))
    story.append(hr())

    recs = [
        {
            'priority': 'P0 — CRITICAL (Immediate)',
            'color': BRAND_RED,
            'items': [
                {
                    'title': 'Bank Transfer & Comprobante — Create Complete Guide',
                    'tickets': '~550/month',
                    'detail': 'This is the #2 volume driver with almost ZERO KB content. Create: bank account details location, valid comprobante requirements (date, amount, name, reference), upload instructions (chat + email), processing times (1-4h business, 24h weekends), country-specific methods (SPEI/CLABE for Mexico, CBU/CVU for Argentina, Mercado Pago, Directa24).',
                    'ai_impact': 'Current 10% → 65% (+55% = ~300 fewer tickets/month)',
                },
                {
                    'title': 'Deposit Not Credited — Full Troubleshooting',
                    'tickets': '~181/month',
                    'detail': 'Create step-by-step troubleshooting per payment method. Explain "recarga exitosa" (provider says success but platform hasn\'t confirmed). Add post-comprobante timeline, crypto confirmations guide, weekend delay explanation.',
                    'ai_impact': 'Current 35% → 70% (+35% = ~63 fewer tickets/month)',
                },
                {
                    'title': 'Technical Troubleshooting — Expand Significantly',
                    'tickets': '~287/month',
                    'detail': 'Only 3 KB entries for a topic with 72% mobile issues. Add: mobile troubleshooting (update browser, toggle Wi-Fi/data, OS requirements iOS 14+/Android 10+), blank screen fix (disable ad-blocker, JavaScript, incognito), PWA guide, recommended browsers, session timeout explanation.',
                    'ai_impact': 'Current 15% → 60% (+45% = ~129 fewer tickets/month)',
                },
            ]
        },
        {
            'priority': 'P1 — HIGH (This Week)',
            'color': BRAND_AMBER,
            'items': [
                {
                    'title': 'KYC — Country-Specific Guide',
                    'tickets': '~388/month',
                    'detail': 'Add country-specific accepted IDs (Chile: RUT/cedula, Argentina: DNI, others: passport). Photo quality guide (phone OK, full doc, good lighting). Selfie instructions. Proof of address options per country. Escalation path when verification exceeds 48h.',
                    'ai_impact': 'Current 45% → 75% (+30% = ~116 fewer tickets/month)',
                },
                {
                    'title': 'Bonus — Enhance Existing Content',
                    'tickets': '~795/month',
                    'detail': 'Make "Saldo 0.00 with active bonus" a prominent standalone entry (causes massive confusion). Add concrete rollover examples in local currency ($10,000 CLP deposit × 30 = must bet $300,000 CLP). Clarify multiple bonus policy. Explain what happens to bonus when requesting withdrawal.',
                    'ai_impact': 'Current 70% → 90% (+20% = ~159 fewer tickets/month)',
                },
            ]
        },
        {
            'priority': 'P2 — MEDIUM (Within 2 Weeks)',
            'color': BRAND_BLUE,
            'items': [
                {
                    'title': 'Casino / Games — Add Troubleshooting',
                    'tickets': '~720/month',
                    'detail': 'Game not loading: device compatibility, ad-blocker check, try another game. Result dispute process: how to file, what evidence, timeline. Live casino disconnection policy. Slot variance/volatility education.',
                    'ai_impact': 'Current 30% → 55% (+25% = ~180 fewer tickets/month)',
                },
                {
                    'title': 'Withdrawal — Make Bonus Blocking Prominent',
                    'tickets': '~108/month',
                    'detail': '46.5% of withdrawal tickets are about bonus blocking. Create dedicated, prominent FAQ entry. Add country-specific withdrawal methods. Provide escalation path for exceeded processing times.',
                    'ai_impact': 'Current 55% → 80% (+25% = ~27 fewer tickets/month)',
                },
                {
                    'title': 'Complaint Process — Document It',
                    'tickets': '~18/month',
                    'detail': 'Create formal complaint escalation path: agent → supervisor → formal complaint. Include SLA, ticket tracking, regulatory body contact. Prepare professional fraud-accusation response template (platform license, RNG certification, investigation process).',
                    'ai_impact': 'Current 5% → 30% (+25% = ~5 fewer tickets/month)',
                },
            ]
        },
        {
            'priority': 'P3 — LOW (Within Month)',
            'color': BRAND_GRAY,
            'items': [
                {
                    'title': '"Recarga" Synonym Entry',
                    'tickets': '~35/month',
                    'detail': 'Add explicit KB entry: "Recarga = Deposit. Same process, same methods." Many Latin American users use "recarga" instead of "deposito" and find nothing in KB.',
                    'ai_impact': 'Current 20% → 75%',
                },
                {
                    'title': 'Deposit Failed / Error Codes',
                    'tickets': '~28/month',
                    'detail': 'Add payment provider error codes, international card activation guide, and alternative method suggestions when one method fails.',
                    'ai_impact': 'Current 25% → 65%',
                },
                {
                    'title': 'Account Security Details',
                    'tickets': '~100/month',
                    'detail': 'Add password requirements, account block duration, session timeout explanation, device verification process.',
                    'ai_impact': 'Current 60% → 85%',
                },
            ]
        },
    ]

    for rec in recs:
        story.append(Paragraph(rec['priority'], styles['H2']))
        for item in rec['items']:
            story.append(Paragraph(f'<b>{item["title"]}</b> ({item["tickets"]})', styles['H3']))
            story.append(Paragraph(item['detail'], styles['Body']))
            story.append(Paragraph(f'<b>AI Impact:</b> {item["ai_impact"]}', styles['RecTitle']))
            story.append(spacer(3))
        story.append(hr())

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # SECTION 7: EXECUTIVE SUMMARY
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('7. Executive Summary & Key Takeaways', styles['H1']))
    story.append(hr())

    story.append(Paragraph('Top Findings:', styles['H2']))
    findings = [
        f'<b>35,963 tickets analyzed</b> across 8 months (Jul 2025 – Feb 2026), averaging {TOTAL_TICKETS//8:,}/month.',
        '<b>24.9% are greetings</b> (8,949 tickets) — users opening chat with "hola" and no question. AI handles 95% of these already.',
        '<b>Bank Transfer/Comprobante is the #2 topic</b> (4,407 tickets, 12.3%) but has ALMOST ZERO KB content. This is the biggest improvement opportunity.',
        '<b>Deposit Not Credited is rising sharply</b> — quadrupled from 76/month (Jul) to 378/month (Jan). Directly caused by shift from card to bank transfer payments.',
        '<b>Bonus questions are declining</b> — dropped 50% from Q3 to Q4 due to improved self-service and reduced promotional activity.',
        '<b>Casino/Games tickets dropped 70%</b> — from 1,322 (Jul) to 206 (Feb), likely due to platform stability improvements.',
        f'<b>Current AI coverage: ~{total_current_handled*100//TOTAL_TICKETS}%</b> of all tickets can be handled by the widget.',
        f'<b>Potential AI coverage: ~{total_potential_handled*100//TOTAL_TICKETS}%</b> after KB improvements — a +{(total_potential_handled-total_current_handled)*100//TOTAL_TICKETS}% increase.',
        f'<b>Estimated savings: ${tickets_saved//8*3:,}–${tickets_saved//8*5:,}/month</b> from ~{tickets_saved//8:,} additional automated tickets.',
    ]
    for f in findings:
        story.append(Paragraph(f'• {f}', styles['BulletItem']))
        story.append(spacer(1))

    story.append(spacer(6))
    story.append(Paragraph('Action Plan Priority:', styles['H2']))
    action_data = [
        ['Priority', 'Action', 'Tickets/mo Saved', 'Est. Savings/mo'],
        ['P0 CRITICAL', 'Bank Transfer + Deposit + Tech KB', '~492', '$1,476–$2,460'],
        ['P1 HIGH', 'KYC country guide + Bonus enhancements', '~275', '$825–$1,375'],
        ['P2 MEDIUM', 'Casino troubleshoot + Withdrawal + Complaints', '~212', '$636–$1,060'],
        ['P3 LOW', 'Recarga synonym + Error codes + Account', '~80', '$240–$400'],
        ['TOTAL', 'All improvements', '~1,059', '$3,177–$5,295'],
    ]
    story.append(make_table(action_data, col_widths=[W*0.15, W*0.35, W*0.18, W*0.20], header_color=BRAND_GREEN))

    story.append(spacer(10))
    story.append(hr())
    story.append(Paragraph(
        '<i>Report generated March 2026. Data: 35,963 Zendesk tickets (Jul 2025 – Feb 2026). '
        'Classification: keyword-based NLP with 19 categories. AI coverage estimates based on '
        'KB_FAQ_BetonWin.txt (339 lines) cross-referenced with actual ticket content.</i>',
        styles['BodySmall']
    ))

    # Build
    doc.build(story)
    print('PDF generated: BetonWin_Complete_35K_Analysis.pdf')


if __name__ == '__main__':
    build_pdf()
