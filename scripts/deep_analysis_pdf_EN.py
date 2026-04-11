#!/usr/bin/env python3
"""
BetonWin — 5-Month Deep Analysis Report (PDF)
Oct 2025 – Feb 2026 | 22,000 Tickets | 14,888 Unique Users
Includes: Cluster Analysis, User/Churn Risk, Action Plan
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
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
styles.add(ParagraphStyle('CriticalText', parent=styles['Normal'], fontSize=9, leading=12, textColor=BRAND_RED, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('CalloutBox', parent=styles['Normal'], fontSize=9, leading=12, textColor=BRAND_DARK,
                           leftIndent=10, rightIndent=10, backColor=LIGHT_BLUE, borderPadding=6))

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

def make_highlight_table(data, col_widths=None, header_color=BRAND_RED):
    """Table with red/amber header for critical sections."""
    return make_table(data, col_widths, header_color)

# ══════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════

MONTHS_LABELS = ['Oct25', 'Nov25', 'Dec25', 'Jan26', 'Feb26']

# Cluster data: (topic, total_5mo, monthly_values, trend_label, trend_explanation, sub_questions, sample_messages, ai_current, ai_potential, ai_status, ai_gap)
CLUSTERS = [
    {
        'topic': 'Greeting Only (no question)',
        'pct': '24.9%',
        'total': 5479, 'avg': 1096,
        'monthly': [1024, 946, 1404, 1525, 1733],
        'trend': 'RISING +69%',
        'explanation': 'Crescita costante. Il picco Dec-Feb correla con l\'acquisizione di nuovi utenti LATAM che aprono conversazione con "hola" come primo contatto. Il widget non guida ancora l\'utente verso la self-service in modo efficace.',
        'subs': [
            ('Simple greeting ("hola", "buenas")', '70%'),
            ('Greeting + name only', '15%'),
            ('Greeting + wait for agent', '10%'),
            ('Greeting in other languages', '5%'),
        ],
        'samples': ['hola', 'buenas tardes', 'Hola buenas', 'buenas como estan', 'buenos dias'],
        'ai_current': 95, 'ai_potential': 99, 'ai_status': 'EXCELLENT',
        'ai_gap': 'Widget auto-greets and asks what they need. Minimal gap.',
    },
    {
        'topic': 'Bonus / Promotions',
        'pct': '17.7%',
        'total': 3049, 'avg': 610,
        'monthly': [1090, 538, 557, 562, 302],
        'trend': 'FALLING SHARPLY -72%',
        'explanation': 'Crollo del 72% da Oct a Feb. Cause: (1) riduzione promozioni aggressive in Q4, (2) miglioramento UX pagina bonus, (3) meno nuovi utenti con domande welcome bonus.',
        'subs': [
            ('Rollover / wagering requirements', '34.6%'),
            ('Free spins questions', '25.7%'),
            ('How to activate / use bonus', '24.9%'),
            ('Bonus terms &amp; conditions', '24.3%'),
            ('Welcome bonus / first deposit', '19.2%'),
            ('Cashback questions', '5.6%'),
            ('Cannot bet with bonus ("Saldo 0.00")', '4.9%'),
            ('Bonus expired / cancelled', '3.9%'),
        ],
        'samples': [
            'Necesito que me ayuden no entiendo que mas tengo que apostar en los bonos',
            'Hola quiero renunciar al bono de bienvenida. Ya deposite y no puedo jugar',
            'Cargue 50mil y me sale que no tengo saldo - saldo 0.00',
            'Como hago para depositar sin bono. La plataforma me obliga a aceptar bono',
            'No puedo retirar mi saldo y gaste mi credito pero mi ganancia no la puedo retirar',
        ],
        'ai_current': 70, 'ai_potential': 90, 'ai_status': 'GOOD',
        'ai_gap': '"Saldo 0.00" confusion needs prominent entry. Rollover examples in local currency missing. Cashback details absent. Multiple bonus policy undocumented.',
    },
    {
        'topic': 'Casino / Games / Bets',
        'pct': '16.0%',
        'total': 2372, 'avg': 474,
        'monthly': [875, 498, 378, 415, 206],
        'trend': 'FALLING -76%',
        'explanation': 'Calo del 76% da Oct a Feb. Miglioramenti di stabilita piattaforma. Meno bug di gioco = meno ticket.',
        'subs': [
            ('Winnings not credited', '52.5%'),
            ('Slot-specific issues', '22.3%'),
            ('Live casino issues', '9.2%'),
            ('Game result dispute', '8.4%'),
            ('How to play / bet', '7.3%'),
            ('Game not loading / error', '1.4%'),
        ],
        'samples': [
            'No puedo jugar a balloon con el dinero cargado',
            'Gane 74.000 y no lo puedo retirar',
            'Deposite, aparece en pesos que esta, pero al tratar de jugar me aparece saldo 0',
            'Compre un bono de giros y aun me sale recopilando datos. Hace horas',
        ],
        'ai_current': 30, 'ai_potential': 55, 'ai_status': 'POOR',
        'ai_gap': '52.5% dei ticket riguarda vincite non accreditate - richiede intervento umano. Manca troubleshooting giochi specifico. "Saldo 0.00" con bonus attivo e il punto di confusione #1.',
    },
    {
        'topic': 'Bank Transfer / Comprobante',
        'pct': '12.3%',
        'total': 3482, 'avg': 696,
        'monthly': [439, 690, 1100, 830, 423],
        'trend': 'RISING SHARPLY (peak Dec +151%)',
        'explanation': 'ESPLOSIONE in Dec (+151% vs Oct). Il mercato LATAM (Cile+Argentina) preferisce bonifici bancari. Piu utenti = piu comprobantes = piu ticket.',
        'subs': [
            ('Sending comprobante / receipt', '43.2%'),
            ('Asking for bank account details', '39.7%'),
            ('Transfer reference / tracking', '6.4%'),
            ('Transfer done, waiting confirmation', '5.9%'),
        ],
        'samples': [
            'Se puede hacer las transferencias por cuenta rut banco estado',
            'Consulta para retirar - no sale la opcion de banco estado, cuenta rut',
            'No puedo hacer ningun dep [sends screenshot]',
            'Quiero retirar mi plata',
        ],
        'ai_current': 10, 'ai_potential': 65, 'ai_status': 'CRITICAL',
        'ai_gap': 'Quasi ZERO contenuto KB. Solo 1 riga: "invia comprobante via email". Mancano: location dettagli bancari, requisiti comprobante, istruzioni upload, tempi processing, metodi per paese. MASSIMA PRIORITA.',
    },
    {
        'topic': 'KYC / Verification',
        'pct': '8.6%',
        'total': 1969, 'avg': 394,
        'monthly': [410, 372, 403, 414, 366],
        'trend': 'STABLE ~390/mo',
        'explanation': 'Costante 370-414/mese. KYC e processo obbligatorio one-time - volume proporzionale a nuove registrazioni.',
        'subs': [
            ('Phone/email verification', '67.5%'),
            ('ID types by country', '58.3%'),
            ('Selfie / photo requirements', '39.4%'),
            ('Verification status / pending', '9.5%'),
            ('Verification rejected', '4.6%'),
        ],
        'samples': [
            'Quiero verificar mi cuenta con mi cedula de identidad y cada vez que la subo me arroja error',
            'Quisiera saber por que me aparece un numero de documento que no es mio',
            'No puedo hacer la verificacion. Mi correo lo pongo y me dice que van a mandar un mensaje',
            'Subi mi cedula de identidad y no puedo verificar',
        ],
        'ai_current': 45, 'ai_potential': 75, 'ai_status': 'MODERATE',
        'ai_gap': '67.5% dei ticket riguarda verifica phone/email (non KYC documentale). Mancano: guide per paese, requisiti foto, istruzioni selfie, escalation per attese >48h.',
    },
    {
        'topic': 'Technical / App / Website',
        'pct': '6.4%',
        'total': 1574, 'avg': 315,
        'monthly': [270, 317, 350, 375, 262],
        'trend': 'RISING SLOWLY +39%',
        'explanation': 'Crescita graduale +39% (Oct-Jan), poi calo Feb. 72% dei ticket tech sono mobile - la piattaforma necessita migliore ottimizzazione mobile o app nativa.',
        'subs': [
            ('Mobile / phone issues', '72.2%'),
            ('Browser compatibility', '18.0%'),
            ('Slow performance', '14.2%'),
            ('Site not loading / down', '3.6%'),
            ('App crash / freeze', '2.4%'),
        ],
        'samples': [
            'No puedo depositar. Me salta error en la app',
            'Escribi mal mi numero de celular y no se como corregirlo',
            'Como descargar la app',
            'En las misiones me pide confirmar telefono y correo pero no se como hacerlo',
        ],
        'ai_current': 15, 'ai_potential': 60, 'ai_status': 'CRITICAL',
        'ai_gap': 'Solo 3 voci KB per un topic top-7. Mancano: troubleshooting mobile, guida PWA, error messages, VPN/ad-blocker, requisiti browser, timeout sessione.',
    },
    {
        'topic': 'Deposit Not Credited',
        'pct': '4.0%',
        'total': 1195, 'avg': 239,
        'monthly': [144, 213, 289, 378, 171],
        'trend': 'RISING SHARPLY (peak Jan +163%)',
        'explanation': 'QUADRUPLICATO Jul-Jan. Direttamente correlato alla crescita Bank Transfer - i bonifici hanno tempi piu lunghi e piu punti di failure. Feb calo potrebbe indicare miglioramenti operativi.',
        'subs': [
            ('Card payment not credited', '38.0%'),
            ('Bank transfer not credited', '27.5%'),
            ('How long to credit?', '25.1%'),
            ('Sent comprobante but not credited', '22.8%'),
            ('Mercado Pago / local not credited', '11.4%'),
        ],
        'samples': [],
        'ai_current': 35, 'ai_potential': 70, 'ai_status': 'POOR',
        'ai_gap': 'Generico "attendi 30 min poi contatta supporto". Mancano: step-by-step per metodo, timeline post-comprobante, troubleshooting specifico.',
    },
    {
        'topic': 'How to Withdraw',
        'pct': '2.4%',
        'total': 693, 'avg': 139,
        'monthly': [64, 71, 128, 146, 242],
        'trend': 'RISING SHARPLY +278%',
        'explanation': 'TRIPLICATO in 5 mesi. Piu utenti vincono = piu richieste prelievo. Il 46.5% bloccato dal bonus - pain point persistente non risolto.',
        'subs': [],
        'samples': [
            'Quiero retirar mi plata y no puedo. No entiendo que tengo que hacer',
            'Gane 74.000 y no lo puedo retirar porque ya no puedo confirmar el correo',
            'No puedo retirar lo que he ganado. Ya es segunda vez, cada vez que quiero retirar no me deja',
            'Llevo 2 dias tratando de hacer retiro y no me deja',
        ],
        'ai_current': 55, 'ai_potential': 80, 'ai_status': 'MODERATE',
        'ai_gap': 'Bonus-blocking explanation insufficiente. Mancano: metodi per paese, percorso escalation.',
    },
    {
        'topic': 'Account / Login Issues',
        'pct': '2.2%',
        'total': 425, 'avg': 85,
        'monthly': [124, 85, 65, 96, 55],
        'trend': 'FALLING -56%',
        'explanation': '',
        'subs': [],
        'samples': [],
        'ai_current': 60, 'ai_potential': 85, 'ai_status': 'GOOD',
        'ai_gap': 'KB covers password reset, blocked accounts, registration. Missing: password requirements, block duration.',
    },
    {
        'topic': 'Complaint / Dissatisfaction',
        'pct': '0.4%',
        'total': 134, 'avg': 27,
        'monthly': [8, 13, 36, 41, 36],
        'trend': 'RISING 4.5x - ALARMING',
        'explanation': 'Volume basso ma crescita ALLARMANTE. Da 8 (Oct) a 36-41. Correlato con aumento depositi non accreditati e problemi prelievo. Segnale di frustrazione crescente.',
        'subs': [],
        'samples': [
            'No son otros casino son uds los estafadores',
            'TENGO UNA QUEJA POR QUE NO CERRARON MI CUENTA COMO LO SOLICITE. SON UNOS APROVECHADORES',
            'Quiero hacer un reclamo. Solo roban el dinero',
            'Me siento estafado. Ayer jugue y supuestamente...',
            'Me cagaron de pana. Te voy a buscarte por cielo mar y tierra',
        ],
        'ai_current': 5, 'ai_potential': 30, 'ai_status': 'CRITICAL',
        'ai_gap': 'Nessun processo reclami documentato. Serve template escalation + risposta professionale ad accuse di frode.',
    },
]

# ══════════════════════════════════════════════════════════════
# BUILD PDF
# ══════════════════════════════════════════════════════════════

def build_pdf():
    doc = SimpleDocTemplate(
        '/Users/serhiykorenyev/Desktop/vs code/widget cs /Analisi /BetonWin_5Month_Deep_Analysis_EN.pdf',
        pagesize=A4,
        topMargin=1.5*cm, bottomMargin=1.5*cm,
        leftMargin=1.5*cm, rightMargin=1.5*cm,
    )
    story = []
    W = A4[0] - 3*cm

    # ── COVER ──
    story.append(Spacer(1, 35*mm))
    story.append(Paragraph('BetonWin — 5-Month Deep Analysis', styles['Title2']))
    story.append(Paragraph('October 2025 — February 2026', styles['H1']))
    story.append(hr())
    story.append(Paragraph('22,000 Tickets | 14,888 Unique Users | Cluster &amp; Churn Analysis', styles['Body']))
    story.append(spacer(4))
    story.append(Paragraph('Data Source: Zendesk API — full ticket extraction with requester_id tracking', styles['Body']))
    story.append(Paragraph('Classification: Keyword-based NLP (19 topic categories)', styles['Body']))
    story.append(Paragraph('Cross-reference: GR8 Data API (paymentOrder + paymentTransactionV2)', styles['Body']))
    story.append(Paragraph('Generated: 10 March 2026', styles['Body']))
    story.append(Spacer(1, 15*mm))

    # Key numbers
    key_data = [
        ['Metric', 'Value'],
        ['Total Tickets Analyzed', '22,000'],
        ['Unique Users', '14,888'],
        ['Average Tickets/Month', '4,400'],
        ['Average Tickets/Day', '~145'],
        ['Multi-Ticket Users', '4,215 (28.3%)'],
        ['Repeat Contact Rate', '1 in 3.5 users contacts support again'],
        ['Peak Months', 'October 2025 &amp; December 2025 (5,000 each)'],
    ]
    story.append(make_table(key_data, col_widths=[W*0.40, W*0.60], header_color=BRAND_GREEN))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # SECTION 1: EXECUTIVE SUMMARY
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('1. Executive Summary &amp; Key Takeaways', styles['H1']))
    story.append(hr())

    # Monthly volume
    story.append(Paragraph('Monthly Volume:', styles['H2']))
    vol_data = [
        ['Month', 'Tickets', 'vs Previous', 'Notes'],
        ['Oct 2025', '5,000', '—', 'Baseline. High due to Q4 promo push'],
        ['Nov 2025', '4,000', '-20%', 'Seasonal dip, fewer promotions'],
        ['Dec 2025', '5,000', '+25%', 'Holiday season + year-end promos'],
        ['Jan 2026', '5,000', '0%', 'Post-holiday activity, new signups'],
        ['Feb 2026', '4,000', '-20%', 'Shorter month, stabilization'],
    ]
    story.append(make_table(vol_data, col_widths=[W*0.15, W*0.12, W*0.12, W*0.45]))
    story.append(spacer(6))

    # Key Trends
    story.append(Paragraph('Key Trends (Oct &rarr; Feb):', styles['H2']))
    trends = [
        '<b>Bank Transfer / Comprobante EXPLODED</b>: From 690 (Nov) &rarr; 1,100 (Dec) &rarr; 830 (Jan). Biggest growth cluster.',
        '<b>Bonus questions COLLAPSED</b>: From 1,090 (Oct) &rarr; 302 (Feb). -72% drop. Reduced promo activity and better UX.',
        '<b>Casino/Games HALVED</b>: From 875 (Oct) &rarr; 206 (Feb). Platform stability improvements working.',
        '<b>"How to Withdraw" SURGING</b>: From 71 (Oct) &rarr; 242 (Feb). 3.4x increase. More winners = more withdrawal questions.',
        '<b>Deposit Not Credited CRITICAL</b>: From 144 (Oct) &rarr; 378 (Jan). Directly tied to bank transfer growth.',
        '<b>Complaints RISING</b>: From 8 (Oct) &rarr; 36 (Feb). Small volume but 4.5x growth signals growing frustration.',
    ]
    for t in trends:
        story.append(Paragraph(f'&bull; {t}', styles['BulletItem']))
        story.append(spacer(1))
    story.append(spacer(6))

    # AI Coverage summary
    story.append(Paragraph('Current AI Coverage:', styles['H2']))
    ai_summary = [
        ['Level', 'Topics', '% of Total Tickets', 'Potential with KB fixes'],
        ['HIGH (>70%)', 'Greetings, How to Deposit, Account/Login', '~28%', '32%'],
        ['MODERATE (40-70%)', 'Bonus, KYC, How to Withdraw, Balance', '~31%', '45%'],
        ['LOW (<40%)', 'Casino, Bank Transfer, Tech, Deposits Not Credited', '~34%', '55%'],
        ['CRITICAL (<15%)', 'Complaints, Recarga', '~1%', '3%'],
    ]
    story.append(make_table(ai_summary, col_widths=[W*0.15, W*0.35, W*0.18, W*0.22]))
    story.append(spacer(4))
    story.append(Paragraph('<b>Current weighted AI coverage: ~42%</b>', styles['Body']))
    story.append(Paragraph('<b>Potential with KB optimization: ~68%</b> (+26pp improvement possible)', styles['RecTitle']))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # SECTION 2: CLUSTER ANALYSIS
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('2. Cluster Analysis (Main Topics)', styles['H1']))
    story.append(hr())

    for i, c in enumerate(CLUSTERS):
        story.append(Paragraph(f'2.{i+1} {c["topic"]} — {c["pct"]}', styles['H2']))
        story.append(Paragraph(f'<b>Total volume (5 months):</b> ~{c["total"]:,} | <b>Monthly average:</b> ~{c["avg"]:,}', styles['Body']))
        story.append(spacer(2))

        # Sub-questions
        if c['subs']:
            story.append(Paragraph('Sub-question Breakdown:', styles['H3']))
            sub_data = [['Pattern', '% of Topic']]
            for name, pctv in c['subs']:
                sub_data.append([name, pctv])
            story.append(make_table(sub_data, col_widths=[W*0.70, W*0.15], header_color=BRAND_BLUE))
            story.append(spacer(3))

        # Monthly trend
        story.append(Paragraph('Monthly Trend:', styles['H3']))
        mt_data = [
            ['Month'] + MONTHS_LABELS + ['Trend'],
            ['Count'] + [str(v) for v in c['monthly']] + [c['trend']],
        ]
        cw = (W - W*0.12 - W*0.22) / 5
        story.append(make_table(mt_data, col_widths=[W*0.12] + [cw]*5 + [W*0.22], header_color=BRAND_DARK))

        if c['explanation']:
            story.append(spacer(2))
            story.append(Paragraph(c['explanation'], styles['Body']))
        story.append(spacer(3))

        # Sample messages
        if c['samples']:
            story.append(Paragraph('Real Customer Messages:', styles['H3']))
            for msg in c['samples'][:5]:
                safe = msg.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                story.append(Paragraph(f'&bull; "{safe}"', styles['Quote']))
            story.append(spacer(3))

        # AI Coverage
        status = c['ai_status']
        color_map = {'EXCELLENT': '#16a34a', 'GOOD': '#16a34a', 'MODERATE': '#d97706', 'POOR': '#dc2626', 'CRITICAL': '#dc2626'}
        sc = color_map.get(status, '#6b7280')
        story.append(Paragraph(
            f'AI Coverage: <font color="{sc}"><b>{c["ai_current"]}% current &rarr; {c["ai_potential"]}% potential ({status})</b></font>',
            styles['H3']
        ))
        story.append(Paragraph(c['ai_gap'], styles['Body']))

        story.append(hr())

        # Page breaks at logical points
        if c['topic'] in ['Casino / Games / Bets', 'Technical / App / Website', 'How to Withdraw']:
            story.append(PageBreak())

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # SECTION 3: USER ANALYSIS & CHURN RISK
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('3. Unique User Analysis & Churn Risk', styles['H1']))
    story.append(hr())
    story.append(Paragraph(
        'Data source: 22,000 tickets with requester_id extracted from Zendesk API, cross-referenced by unique user.',
        styles['BodySmall']
    ))
    story.append(spacer(6))

    # 3.1 Overview
    story.append(Paragraph('3.1 User Overview', styles['H2']))
    user_overview = [
        ['Metric', 'Value'],
        ['Total Tickets (Oct-Feb)', '22,000'],
        ['Unique Users', '14,888'],
        ['Tickets per User (average)', '1.48'],
        ['Users with 1 ticket only', '10,673 (71.7%)'],
        ['Recurring Users (2+ tickets)', '4,215 (28.3%)'],
    ]
    story.append(make_table(user_overview, col_widths=[W*0.45, W*0.40], header_color=BRAND_GREEN))
    story.append(spacer(4))
    story.append(Paragraph(
        '<b>28.3% of users generate approximately 51.5% of all tickets.</b> These recurring users are the primary target for reducing support volume.',
        styles['Body']
    ))
    story.append(spacer(6))

    # 3.2 Distribution
    story.append(Paragraph('3.2 Multi-Ticket User Distribution', styles['H2']))
    dist_data = [
        ['Tier', 'Utenti', '% of Total', 'Tickets Generated', 'Avg Tickets/User'],
        ['1 ticket', '10,673', '71.7%', '10,673', '1.0'],
        ['2 ticket', '2,660', '17.9%', '5,320', '2.0'],
        ['3-5 ticket', '1,406', '9.4%', '~4,920', '~3.5'],
        ['6-10 ticket', '135', '0.9%', '~1,013', '~7.5'],
        ['11-20 ticket', '13', '0.1%', '~195', '~15.0'],
        ['20+ ticket', '1', '<0.01%', '37', '37.0'],
        ['TOTALE', '14,888', '100%', '~22,000', '1.48'],
    ]
    story.append(make_table(dist_data, col_widths=[W*0.15, W*0.14, W*0.14, W*0.18, W*0.18]))
    story.append(spacer(6))

    # 3.3 Frustration Clusters
    story.append(Paragraph('3.3 Frustration Clusters — Users Reopening the Same Issue', styles['H2']))
    story.append(Paragraph(
        'These users open 2+ tickets on the SAME topic — a direct signal of an unresolved problem:',
        styles['Body']
    ))
    story.append(spacer(3))
    frust_data = [
        ['Topic', 'Frustrated Users', 'Total Tickets', 'Avg Tickets/User', 'Churn Risk'],
        ['Technical / App / Website', '51', '127', '2.5', 'HIGH'],
        ['How to Withdraw', '38', '103', '2.7', 'CRITICAL'],
        ['Casino / Games / Bets', '34', '80', '2.4', 'HIGH'],
        ['KYC / Verification', '33', '78', '2.4', 'HIGH'],
        ['Bank Transfer / Comprobante', '31', '74', '2.4', 'HIGH'],
        ['Bonus / Promotions', '30', '79', '2.6', 'MODERATE'],
        ['Deposit Not Credited', '27', '75', '2.8', 'CRITICAL'],
        ['Balance / Account Info', '21', '47', '2.2', 'MODERATE'],
        ['Complaint / Dissatisfaction', '3', '11', '3.7', 'CRITICAL'],
    ]
    story.append(make_highlight_table(frust_data, col_widths=[W*0.28, W*0.15, W*0.13, W*0.16, W*0.13]))
    story.append(spacer(6))

    # Critical clusters detail
    story.append(Paragraph('3.3.1 CRITICAL — "How to Withdraw" (38 utenti, 2.7 ticket ciascuno)', styles['H3']))
    story.append(Paragraph(
        '<b>Perche e critico:</b> Questi sono utenti che hanno VINTO e non riescono a prelevare. '
        'Il 46.5% e bloccato dal bonus attivo — non capiscono il rollover. Contattano supporto 2-3 volte prima di riuscire o abbandonare. '
        '<b>Impatto business:</b> Ogni utente perso qui e un vincitore attivo che depositava regolarmente. '
        'Se un vincitore non riesce a prelevare, non depositera piu.',
        styles['Body']
    ))
    story.append(spacer(3))

    story.append(Paragraph('3.3.2 CRITICAL — "Deposit Not Credited" (27 utenti, 2.8 ticket ciascuno)', styles['H3']))
    story.append(Paragraph(
        '<b>Perche e critico:</b> Questi utenti hanno PAGATO e non vedono il saldo. '
        'Media 2.8 contatti per risolvere = processo troppo lento. Direttamente correlato con crescita bank transfer. '
        '<b>Impatto business:</b> Utente con soldi "persi" e il piu probabile a lasciare la piattaforma e fare review negativa. '
        '<b>Dato GR8 API:</b> Il 90% dei depositi falliti e "Request timeout" su gateway — problema infrastrutturale.',
        styles['Body']
    ))
    story.append(spacer(3))

    story.append(Paragraph('3.3.3 HIGH — "Technical / App / Website" (51 utenti, 2.5 ticket ciascuno)', styles['H3']))
    story.append(Paragraph(
        'Gruppo piu numeroso di utenti frustrati. Problemi mobile ricorrenti non risolti al primo contatto. '
        '72% mobile-related. <b>Impatto:</b> Utente che non riesce ad accedere = zero revenue.',
        styles['Body']
    ))
    story.append(PageBreak())

    # 3.4 Top 10 users
    story.append(Paragraph('3.4 Top 10 High-Risk Users', styles['H2']))
    top_users = [
        ['#', 'User ID', 'Ticket', 'Months Active', 'Pattern', 'Risk'],
        ['1', '29547546107410', '37', '5/5', 'Persistent multi-topic', 'CRITICAL'],
        ['2', '30613096929170', '20', '4/5', 'Multi-topic + Deposit', 'CRITICAL'],
        ['3', '27922585765522', '14', '3/5', 'Multi-topic', 'HIGH'],
        ['4', '30133940804882', '14', '4/5', 'Bank Transfer recurring', 'HIGH'],
        ['5', '30683526567314', '14', '3/5', 'Multi-topic', 'HIGH'],
        ['6', '30432303606034', '13', '4/5', 'Chronic support seeker', 'MODERATE'],
        ['7', '30542650398098', '13', '3/5', 'Multi-topic', 'HIGH'],
        ['8', '28393674997138', '13', '4/5', 'Multi-topic', 'HIGH'],
        ['9', '31131560923154', '12', '2/5', 'How to Deposit (repeated)', 'HIGH'],
        ['10', '30101150841618', '11', '3/5', 'Multi-topic', 'HIGH'],
    ]
    story.append(make_highlight_table(top_users, col_widths=[W*0.04, W*0.20, W*0.08, W*0.12, W*0.28, W*0.12]))
    story.append(spacer(4))
    story.append(Paragraph(
        '<b>Il User #1 ha aperto 37 ticket in 5 mesi</b> — quasi 2 ticket a settimana per 5 mesi consecutivi. '
        'Questo utente ha bisogno di un account manager dedicato o un intervento proattivo immediato.',
        styles['CriticalText']
    ))
    story.append(spacer(8))

    # 3.5 Persistence
    story.append(Paragraph('3.5 Recurring User Persistence Over Time', styles['H2']))
    persist_data = [
        ['Months of Activity', 'Recurring Users', '% of Recurring', 'Interpretation'],
        ['1 mese (burst)', '~2,527', '60.0%', 'One-time issue, then resolved or abandoned'],
        ['2 mesi', '~1,012', '24.0%', 'Persistent problem, moderate risk'],
        ['3 mesi', '~465', '11.0%', 'Growing frustration, high risk'],
        ['4 mesi', '~169', '4.0%', 'Utente "intrappolato" — deposita ma ha problemi cronici'],
        ['5 mesi (tutti)', '~42', '1.0%', 'MAXIMUM RISK — contacting support every month'],
    ]
    story.append(make_table(persist_data, col_widths=[W*0.18, W*0.16, W*0.14, W*0.40]))
    story.append(spacer(4))
    story.append(Paragraph(
        '<b>42 utenti hanno contattato il supporto OGNI SINGOLO MESE per 5 mesi consecutivi.</b> '
        'Rappresentano i casi piu gravi di frustrazione persistente, ma anche utenti FEDELI che non hanno ancora abbandonato. '
        'Un intervento proattivo su questi 42 utenti puo trasformarli da detrattori a promotori.',
        styles['Body']
    ))
    story.append(spacer(8))

    # 3.6 Retention Recommendations
    story.append(Paragraph('3.6 Retention Recommendations by Cluster', styles['H2']))

    # How to Withdraw
    story.append(Paragraph('Per "How to Withdraw" — STOP CHURN IMMEDIATO', styles['H3']))
    ret1 = [
        ['Action', 'Detail', 'Timeline'],
        ['Pre-withdrawal popup', 'Mostrare requisiti (rollover, KYC) PRIMA che l\'utente tenti', '1 settimana'],
        ['Dedicated KB page', 'Pagina "Perche non posso prelevare" con checklist visuale', '3 giorni'],
        ['AI Widget + GR8', 'Check via API se ha bonus attivo, spiegare proattivamente', '2 settimane'],
    ]
    story.append(make_table(ret1, col_widths=[W*0.22, W*0.52, W*0.15], header_color=BRAND_RED))
    story.append(spacer(4))

    # Deposit Not Credited
    story.append(Paragraph('Per "Deposit Not Credited" — RIDURRE FRUSTRAZIONE', styles['H3']))
    ret2 = [
        ['Action', 'Detail', 'Timeline'],
        ['Real-time notification', 'Automatic deposit status after payment', '2 settimane'],
        ['KB processing times', 'Tempi per metodo (MercadoPago: 5min, BankTransfer: 2-24h)', '3 giorni'],
        ['AI Widget + GR8', 'Integrare paymentTransactionV2 per status deposito immediato', '2 settimane'],
    ]
    story.append(make_table(ret2, col_widths=[W*0.22, W*0.52, W*0.15], header_color=BRAND_AMBER))
    story.append(spacer(4))

    # 5-month users
    story.append(Paragraph('For 5-month users (42 users)', styles['H3']))
    ret3 = [
        ['Action', 'Detail', 'Timeline'],
        ['CRM Flag', 'Taggare come "VIP at risk" nel sistema', 'Immediate'],
        ['Outreach', 'Email/chiamata personalizzata per capire pain point', '1 settimana'],
        ['Compensation', 'Bonus fedelta o cashback come gesto di buona volonta', '1 settimana'],
    ]
    story.append(make_table(ret3, col_widths=[W*0.22, W*0.52, W*0.15], header_color=BRAND_GREEN))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # SECTION 4: ACTION PLAN
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph('4. Raccomandazioni per l\'Ottimizzazione (Action Plan)', styles['H1']))
    story.append(hr())

    # P0
    story.append(Paragraph('P0 — CRITICAL (Immediate — This Week)', styles['H2']))
    p0_data = [
        ['#', 'Action', 'Topic Impacted', 'Expected Impact'],
        ['P0-1', 'Creare sezione KB completa "Bank Transfer / Comprobante": dettagli bancari, requisiti comprobante, upload, tempi per paese',
         'Bank Transfer (12.3%)', '-40% tickets on this topic'],
        ['P0-2', 'Pagina "Il mio deposito non appare" con timeline per metodo e step-by-step',
         'Deposit Not Credited (4%)', '-30% ticket, meno frustrazione'],
        ['P0-3', 'Spiegare "Saldo 0.00" con bonus attivo in modo prominente — confusione #1 trasversale',
         'Bonus + Casino + Balance', '-25% across 3 clusters'],
        ['P0-4', 'Checklist pre-prelievo visuale: KYC + Rollover + Metodo bancario',
         'How to Withdraw (2.4%)', '-50% withdrawal tickets'],
    ]
    story.append(make_table(p0_data, col_widths=[W*0.06, W*0.44, W*0.22, W*0.18], header_color=BRAND_RED))
    story.append(spacer(6))

    # P1
    story.append(Paragraph('P1 — HIGH (By End of Week)', styles['H2']))
    p1_data = [
        ['#', 'Action', 'Topic Impacted', 'Expected Impact'],
        ['P1-1', 'Guida troubleshooting mobile: iOS vs Android, clear cache, PWA install',
         'Technical (6.4%)', '-35% tech tickets'],
        ['P1-2', 'Guida KYC per paese: documenti accettati Argentina (DNI), Cile (cedula), con foto esempio',
         'KYC (8.6%)', '-30% KYC tickets'],
        ['P1-3', 'Aggiungere "recarga" come sinonimo di deposito in TUTTA la KB',
         'Recarga + Deposit', '-80% recarga tickets'],
        ['P1-4', 'Rollover calculator con esempi concreti in ARS e CLP',
         'Bonus (17.7%)', '-20% rollover questions'],
        ['P1-5', 'Flag 42 utenti cronici nel CRM e assegnare priorita ai loro ticket',
         'Churn risk', 'Prevent churn'],
    ]
    story.append(make_table(p1_data, col_widths=[W*0.06, W*0.44, W*0.22, W*0.18], header_color=BRAND_AMBER))
    story.append(spacer(6))

    # P2
    story.append(Paragraph('P2 — MEDIUM (Within 2 Weeks)', styles['H2']))
    p2_data = [
        ['#', 'Action', 'Topic Impacted', 'Expected Impact'],
        ['P2-1', 'Integrare GR8 Data API nel widget: status deposito real-time, saldo, stato KYC, bonus attivo',
         'Multiple topics', '-15% overall volume'],
        ['P2-2', 'Template risposta reclami professionale con processo escalation chiaro',
         'Complaints (0.4%)', 'Better handling, less churn'],
        ['P2-3', 'Notifica proattiva post-deposito via widget con tempo stimato',
         'Deposit Not Credited', '-40% deposit tickets'],
        ['P2-4', 'Dashboard payment gateway status (90% dei fail e timeout su src_h2h/directa24)',
         'Deposit Failed', 'Proactive reduction'],
        ['P2-5', 'Auto-detect utenti ricorrenti nel widget: dopo 2o ticket sullo stesso topic, escalation automatica',
         'All clusters', '+40% first-contact resolution'],
    ]
    story.append(make_table(p2_data, col_widths=[W*0.06, W*0.44, W*0.22, W*0.18], header_color=BRAND_BLUE))
    story.append(spacer(8))

    # Impact summary
    story.append(Paragraph('Estimated Overall Impact:', styles['H2']))
    impact_data = [
        ['Metric', 'Current', 'After P0+P1', 'After P0+P1+P2'],
        ['AI Coverage (weighted)', '~42%', '~58%', '~68%'],
        ['Tickets/month requiring agent', '~2,550', '~1,700', '~1,400'],
        ['First-contact resolution', '~35%', '~50%', '~60%'],
        ['Frustrated recurring users/month', '~300', '~180', '~120'],
        ['Risk churn da supporto', 'High', 'Medium', 'Low'],
        ['Estimated agent savings', '—', '2 FTE', '3 FTE'],
    ]
    story.append(make_table(impact_data, col_widths=[W*0.32, W*0.18, W*0.18, W*0.20], header_color=BRAND_GREEN))

    story.append(spacer(12))
    story.append(hr())
    story.append(Paragraph(
        '<i>Report generated on 10 March 2026. '
        'Based on 22,000 Zendesk tickets (Oct 2025 - Feb 2026) + GR8 Data API integration. '
        '14,888 unique users tracked | 4,215 recurring users analyzed. '
        'Cross-referenced with real-time GR8 payment data (paymentOrder + paymentTransactionV2).</i>',
        styles['BodySmall']
    ))

    # Build
    doc.build(story)
    print('PDF generated: BetonWin_5Month_Deep_Analysis_EN.pdf')


if __name__ == '__main__':
    build_pdf()
