#!/usr/bin/env python3
"""
Generate PDF: Missing Information Request for CS Team
55 new questions NOT in domande_senza_risposta.md
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)

# ── Colors ──
DARK   = colors.HexColor('#1a1a2e')
GREEN  = colors.HexColor('#16a34a')
RED    = colors.HexColor('#dc2626')
AMBER  = colors.HexColor('#d97706')
BLUE   = colors.HexColor('#2563eb')
GRAY   = colors.HexColor('#6b7280')
LGRAY  = colors.HexColor('#f3f4f6')
LGREEN = colors.HexColor('#dcfce7')
LBLUE  = colors.HexColor('#dbeafe')
LAMBER = colors.HexColor('#fef3c7')
LRED   = colors.HexColor('#fee2e2')
WHITE  = colors.white

styles = getSampleStyleSheet()
styles.add(ParagraphStyle('Title2', parent=styles['Title'], fontSize=20, textColor=DARK, spaceAfter=4))
styles.add(ParagraphStyle('Sub', parent=styles['Normal'], fontSize=12, textColor=BLUE, spaceAfter=2))
styles.add(ParagraphStyle('H1', parent=styles['Heading1'], fontSize=15, textColor=DARK, spaceBefore=12, spaceAfter=4))
styles.add(ParagraphStyle('H2', parent=styles['Heading2'], fontSize=12, textColor=BLUE, spaceBefore=8, spaceAfter=3))
styles.add(ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, leading=12, textColor=DARK, alignment=TA_JUSTIFY))
styles.add(ParagraphStyle('Small', parent=styles['Normal'], fontSize=7.5, leading=9.5, textColor=GRAY))
styles.add(ParagraphStyle('SmallI', parent=styles['Normal'], fontSize=7.5, leading=9.5, textColor=GRAY, fontName='Helvetica-Oblique'))
styles.add(ParagraphStyle('BulletX', parent=styles['Normal'], fontSize=9, leading=12, leftIndent=14, bulletIndent=4))
styles.add(ParagraphStyle('CellBody', parent=styles['Normal'], fontSize=7.5, leading=9.5, textColor=DARK))
styles.add(ParagraphStyle('CellQ', parent=styles['Normal'], fontSize=7.5, leading=9.5, textColor=DARK, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('CellWhy', parent=styles['Normal'], fontSize=7, leading=8.5, textColor=GRAY, fontName='Helvetica-Oblique'))
styles.add(ParagraphStyle('CellAns', parent=styles['Normal'], fontSize=7.5, leading=9.5, textColor=RED))

def hr():
    return HRFlowable(width='100%', thickness=0.5, color=GRAY, spaceBefore=4, spaceAfter=4)

def spacer(h=3):
    return Spacer(1, h * mm)

def section_header(letter, title, impact, color=BLUE):
    """Colored section banner."""
    data = [[Paragraph(f'<b>SECTION {letter} — {title}</b>',
             ParagraphStyle('sh', fontSize=10, textColor=WHITE, fontName='Helvetica-Bold')),
             Paragraph(f'<b>{impact}</b>',
             ParagraphStyle('sh2', fontSize=8, textColor=WHITE, alignment=TA_CENTER))]]
    t = Table(data, colWidths=['70%', '30%'])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), color),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    return t

def q_table(questions, W):
    """Build a question table. Each question = (id, question, why, real_ticket_example)."""
    header = [
        Paragraph('<b>#</b>', styles['CellBody']),
        Paragraph('<b>Question for CS Team</b>', styles['CellBody']),
        Paragraph('<b>Why We Need This</b>', styles['CellBody']),
        Paragraph('<b>Answer<br/>(to be filled)</b>', styles['CellAns']),
    ]
    rows = [header]
    for qid, question, why in questions:
        rows.append([
            Paragraph(qid, styles['CellBody']),
            Paragraph(question, styles['CellQ']),
            Paragraph(why, styles['CellWhy']),
            Paragraph('', styles['CellBody']),
        ])
    t = Table(rows, colWidths=[W*0.05, W*0.38, W*0.32, W*0.25], repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#d1d5db')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LGRAY]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('BACKGROUND', (3,1), (3,-1), colors.HexColor('#fff7ed')),
    ]))
    return t

# ══════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════

SECTIONS = [
    {
        'letter': 'A',
        'title': 'Greeting & First-Contact Handling',
        'impact': '8,949 tickets (24.9%) — ~1,119/mo',
        'color': GREEN,
        'intro': 'These are users who open chat with just "hola" or "buenas" and no question. The AI already handles 95% of these, but we need to improve the remaining 5% and reduce abandoned chats.',
        'note': None,
        'questions': [
            ('A.1', 'When a user sends only a greeting ("hola", "buenas"), what is the ideal first response? Should the bot list the main help categories or ask an open question like "How can I help you?"',
             'Currently the bot greets back and asks "how can I help?" — but 15% of users still don\'t ask a question after the bot responds. We need a more proactive response that guides them.'),
            ('A.2', 'Should the bot send a quick-action menu with buttons (e.g., "Deposit", "Withdrawal", "Bonus", "KYC", "Other") after a greeting, or just text?',
             '8,949 tickets are just greetings. Quick-action buttons could immediately route 70%+ of these to the right flow without waiting for the user to type a second message.'),
            ('A.3', 'If a user sends only a greeting and then goes silent (no second message for 2+ minutes), what should the bot do? Send a follow-up? Close the chat? After how many minutes?',
             '~10% of greeting-only tickets end with the user abandoning the chat. Agents currently waste time waiting.'),
            ('A.4', 'What languages should the greeting response support? Currently we have ES/EN/IT/PT. Are there other languages users write in? (e.g., German, French for European markets)',
             'Some users write greetings in unexpected languages. Need to know if we should add more.'),
        ]
    },
    {
        'letter': 'B',
        'title': 'Bank Transfer: Operational Details',
        'impact': '4,407 tickets (12.3%) — ~551/mo — RISING +271%',
        'color': RED,
        'intro': 'Bank transfer tickets exploded from 296/month (Jul 2025) to 1,100/month (Dec 2025). These questions cover operational patterns NOT already in "domande_senza_risposta.md" (which covers bank details, comprobante format, and processing times).',
        'note': 'Questions about bank account details, comprobante requirements, and processing times are already in "domande_senza_risposta.md" Section 1 (Q1.1–1.10). These questions are DIFFERENT.',
        'questions': [
            ('B.1', 'Bank Transfer tickets exploded +271% in 6 months. Was there a change in payment provider, a promotion pushing bank transfers, or a new market launched? We need to understand the root cause.',
             'If we know WHY transfers increased, we can proactively address the cause (e.g., if Directa24 was added, we need specific Directa24 instructions in the KB).'),
            ('B.2', 'When a user sends a comprobante image in the chat, what is the EXACT agent workflow? Manual check? Automated system? Describe the step-by-step process after receiving a comprobante.',
             'We are building an automated comprobante verification flow in the widget. We need to know the current manual process to replicate it correctly.'),
            ('B.3', 'What are the top 5 most common reasons a bank transfer deposit is NOT credited even after sending a valid comprobante?',
             'Real ticket: "Son 4 recargas de 5000 peso. Necesito una respuesta" — Multiple transfers stuck. We need to explain why.'),
            ('B.4', 'Is there a maximum number of pending bank transfers per user? Can a user have 3–4 unprocessed transfers at the same time?',
             'Users make multiple small transfers instead of one large one, creating multiple support tickets each time.'),
            ('B.5', 'What happens if a user makes a bank transfer but forgets to include the reference code? Can the deposit still be matched? How?',
             'Many tickets show transfers without references. The KB doesn\'t explain what to do in this case.'),
            ('B.6', 'Chile-specific: Does "Cuenta RUT" from Banco Estado work for both deposits AND withdrawals? Multiple users report it doesn\'t appear as an option for withdrawals.',
             'Real ticket: "Consulta para retirar — no sale la opción de banco estado, cuenta rut" — Recurring issue with no answer in KB.'),
        ]
    },
    {
        'letter': 'C',
        'title': 'Phone & Email Verification',
        'impact': '2,096 tickets (67.5% of KYC) — ~262/mo',
        'color': RED,
        'intro': '67.5% of KYC tickets are actually about phone/email verification — a completely different issue from document uploads. This is the #1 KYC problem.',
        'note': '"domande_senza_risposta.md" Section 4 covers document KYC (ID uploads, photo quality, proof of address). Phone/email verification is NOT covered there.',
        'questions': [
            ('C.1', 'Step-by-step: how does a user verify their phone number? Exact path: My Account > Settings > ...? What happens after they click "Verify"? SMS code? How many digits?',
             'Real ticket: "En las misiones me pide confirmar teléfono y correo pero no sé cómo hacerlo" — Users don\'t know the exact path.'),
            ('C.2', 'The SMS verification code doesn\'t arrive. What are the most common reasons? (Wrong number format? Carrier blocking? Country code missing?) What should the user try?',
             'This is the #1 KYC issue. Real ticket: "No puedo verificar mi número de teléfono. Cada vez que lo subo me arroja error"'),
            ('C.3', 'If a user entered the WRONG phone number during registration, can they change it themselves? Or must they contact support? What verification does support require?',
             'Real ticket: "Escribí mal mi número de celular y no sé como corregirlo" — Extremely common. Agents say "tell me your number and I\'ll fix it" but the bot can\'t do that.'),
            ('C.4', 'Same for email: if the user entered the wrong email (e.g., ".com" instead of ".cl"), can they change it themselves? What\'s the exact process?',
             'Real ticket: "Me equivoqué y puse .com y termina en .cl, entonces no puedo verificarlo" — Very frequent error.'),
            ('C.5', 'What phone number format is required? Must include country code (+56 Chile, +54 Argentina)? With or without leading zero? Provide an example for each country.',
             'Users enter numbers in different formats and get errors. We need the exact format so the bot can validate before submission.'),
            ('C.6', 'Email verification: what does the user receive? A link? A code? How long is it valid? What if it goes to spam? Can they re-send it?',
             'Real ticket: "No puedo confirmar mi correo. Lo pongo y me dice que van a mandar un mensaje" — Users don\'t know what to expect.'),
            ('C.7', 'Is phone + email verification mandatory for ALL users, or only for certain actions? (Before first withdrawal? For Hero/Loyalty program? For deposits over X amount?)',
             'Some users are blocked from playing, others play fine without verification. We need to clarify exactly when it\'s mandatory.'),
            ('C.8', 'The "secret question" — what is it? When is it set up? What if the user doesn\'t remember the answer? How does support verify identity without it?',
             'Real ticket: "No recuerdo la respuesta a mi pregunta secreta" — Agents verify via document photo. The bot needs to explain this process.'),
        ]
    },
    {
        'letter': 'D',
        'title': '"Saldo 0.00" with Active Bonus (Deep Dive)',
        'impact': '~400/mo — #1 confusion point',
        'color': AMBER,
        'intro': 'This is the SINGLE MOST CONFUSING issue for users. It appears across Bonus, Casino, and Balance tickets. Users deposit money, see a balance, but when they try to play or withdraw it shows "0.00". They think they\'ve been scammed.',
        'note': '"domande_senza_risposta.md" Q5.1 asks about this briefly. We need a MUCH more detailed explanation with concrete numerical examples.',
        'questions': [
            ('D.1', 'Explain in simple terms: why does "Saldo 0.00" appear when the user has a sports bonus active? Step-by-step example with real numbers.',
             'Real ticket: "Cargué 50mil y me sale que no tengo saldo" — User deposited $50,000 CLP, got a bonus, but can\'t play. Causes extreme frustration and fraud accusations.'),
            ('D.2', 'Concrete example: User deposits $10,000 CLP → gets 150% welcome bonus ($15,000). Total shows $25,000. They try to bet on sports → "Saldo 0.00". WHY? What should they do?',
             'We need an example so clear that anyone can understand it. The current KB explanation is too technical.'),
            ('D.3', 'Does "Saldo 0.00" also happen with casino bonuses, or only sports bonuses? If a user has a casino bonus, can they play slots normally?',
             'We see this issue across both sports and casino contexts. Need to clarify the difference.'),
            ('D.4', 'If the user doesn\'t want the bonus, how do they remove it BEFORE it\'s used? Step-by-step: My Account > Promotions > Cancel Bonus? Will they lose their deposit?',
             'Real ticket: "Hola quiero renunciar al bono de bienvenida. Ya deposité" — 248 tickets about bonus cancellation.'),
            ('D.5', 'After cancelling a bonus, does the real money (original deposit) become immediately available? Or is there a waiting period?',
             'Users cancel the bonus expecting instant access to their money. Does it work that way?'),
        ]
    },
    {
        'letter': 'E',
        'title': 'Casino Winnings Not Credited',
        'impact': '3,022 tickets (52.5% of Casino) — ~378/mo',
        'color': AMBER,
        'intro': 'Over half of all Casino tickets are about users who won but the money didn\'t appear or they can\'t withdraw their winnings. This is different from game troubleshooting (covered in domande_senza_risposta.md Section 6).',
        'note': '"domande_senza_risposta.md" Section 6 covers game loading, disputes, disconnection. These questions are about WINNINGS not appearing.',
        'questions': [
            ('E.1', 'When a user wins in a slot or casino game, how quickly should the winnings appear in their balance? Instantly? After the round ends? After a processing delay?',
             'Real ticket: "Gané 74.000 y no lo puedo retirar" — User says they won but the balance doesn\'t reflect it.'),
            ('E.2', 'If a user wins but can\'t withdraw because of an active bonus, what is the maximum amount they can withdraw? Explain the "Release Limit" with a real example in local currency.',
             'Real ticket: "No puedo retirar mi saldo. Gasté mi crédito pero mi ganancia no la puedo retirar" — Release Limit is extremely confusing.'),
            ('E.3', 'If a game crashes/freezes mid-spin or mid-round, what happens to the bet? Is the result determined server-side? Will the user see the result when they re-open the game?',
             'Real ticket: "Compré un bono de giros y aún me sale recopilando datos. Hace horas" — User stuck in unresolved game.'),
            ('E.4', 'Jackpot wins — is there a different process for large wins? Do they require additional verification? Is there a maximum payout?',
             'Users who win large amounts face unexpected delays. Need to explain why proactively.'),
            ('E.5', 'If a user believes their game result was unfair, what is the official investigation process? Who reviews it? How long? What evidence do they need?',
             'Real ticket: "Me siento estafado" — We need a professional, transparent response with RNG certification info.'),
        ]
    },
    {
        'letter': 'F',
        'title': 'Withdrawal Blocked by Bonus',
        'impact': '401 tickets (46.5% of withdrawals) — ~50/mo',
        'color': AMBER,
        'intro': 'This single issue generates HALF of all withdrawal complaints. Users try to withdraw, get blocked because of an active bonus, and don\'t understand why or what to do.',
        'note': '"domande_senza_risposta.md" Q8.1 mentions this briefly. We need the COMPLETE user flow with exact screen descriptions.',
        'questions': [
            ('F.1', 'When a user tries to withdraw with an active bonus, what EXACT error message do they see? Provide the exact text shown on screen.',
             'Users send screenshots of error messages. We need to recognize and explain each one.'),
            ('F.2', 'Step-by-step: how can a user check their current rollover/wagering progress? Exact path: My Account > Promotions > ...? What does the progress bar show?',
             'Real ticket: "No entiendo qué más tengo que apostar en los bonos" — Users don\'t know where to look.'),
            ('F.3', 'If the user decides to cancel the bonus to withdraw, what is the EXACT process? Screen by screen: where to click, what confirmation appears, what happens to balance.',
             'Real ticket: "Quiero renunciar al bono y retirar el dinero" — If the bot can guide this, we save ~200 tickets/month.'),
            ('F.4', 'After completing the wagering requirement, is the withdrawal unlocked automatically? Or does the user need to do something additional?',
             'Some users complete wagering but still can\'t withdraw. Is there an additional step?'),
            ('F.5', '"Saldo disponible" vs "Saldo total" vs "Saldo de bono" — provide exact definitions and where each appears on the platform.',
             'Real ticket: "Deposité, aparece en pesos, pero al tratar de jugar aparece saldo 0 y al retirar lo mismo" — Three balance concepts confuse users constantly.'),
        ]
    },
    {
        'letter': 'G',
        'title': 'Account Closure & Self-Exclusion',
        'impact': '~62 tickets/mo — HIGH sensitivity (compliance)',
        'color': BLUE,
        'intro': 'Account closure and self-exclusion requests are sensitive — they involve responsible gambling compliance. The bot currently cannot handle these at all.',
        'note': 'Not covered in "domande_senza_risposta.md" at all.',
        'questions': [
            ('G.1', 'What is the exact process to close an account? Must the user have zero balance? How long does it take? Is it reversible?',
             'Real ticket: "Quiero darme de baja. No pienso jugar más" — Multiple users request this daily.'),
            ('G.2', 'What is the difference between "account closure" and "self-exclusion"? Different durations? Different reversibility?',
             'Real ticket: "TENGO UNA QUEJA POR QUÉ NO CERRARON MI CUENTA" — User asked for closure but account was still active. Critical compliance issue.'),
            ('G.3', 'Self-exclusion options: what time periods are available? (24h, 1 week, 1 month, 6 months, permanent?) Can the user choose?',
             'Need specific options to list in the bot response.'),
            ('G.4', 'If a user requests account closure, what happens to their remaining balance? Must they withdraw first? What about pending bonuses?',
             'Users want to leave but have money in the account.'),
            ('G.5', 'After self-exclusion expires, does the account reopen automatically? Or does the user need to contact support to reactivate?',
             'Important for users who set temporary self-exclusion.'),
            ('G.6', 'Is there a responsible gambling helpline or organization the bot should recommend? (Local organizations in Chile, Argentina)',
             'For compliance, the bot should proactively offer this when users mention gambling problems.'),
        ]
    },
    {
        'letter': 'H',
        'title': 'Loyalty Program / Hero / Missions',
        'impact': 'Growing — part of Bonus tickets',
        'color': BLUE,
        'intro': 'The KB mentions the loyalty program but users have very specific questions about levels, rewards, and daily missions that we cannot answer.',
        'note': 'Not covered in "domande_senza_risposta.md".',
        'questions': [
            ('H.1', 'How many levels does the Hero/Loyalty program have? What are the level names? How much must a user bet (in CLP/ARS) to reach each level?',
             'Users ask "how do I level up?" — we need specific thresholds.'),
            ('H.2', 'What rewards does each level unlock? (cashback %, free spins count, free bet value, deposit bonus %). Ideally provide a table per level.',
             'Users want to know what they\'ll get at the next level.'),
            ('H.3', 'Daily Missions: what types of missions exist? (e.g., "make 5 bets", "deposit $X", "play game Y") Same for everyone or personalized?',
             'Real ticket: "En las misiones me pide confirmar teléfono" — Some missions have prerequisites users don\'t understand.'),
            ('H.4', '"Active user" = 14 days without betting = loss of benefits. Does the user lose their LEVEL or just current benefits? When they bet again, do they restart from level 1?',
             'Users who pause playing are worried about losing all their progress.'),
            ('H.5', 'Birthday bonus: is it automatic or must the user claim it? What are the requirements? (Must be active, must have deposited recently, etc.)',
             'Users expect a bonus on their birthday and get nothing. Need to explain conditions clearly.'),
        ]
    },
    {
        'letter': 'I',
        'title': 'Sports Betting Specific',
        'impact': '~200/mo — part of Casino/Games',
        'color': BLUE,
        'intro': 'The KB has basic sports info but users have operational questions about bet settlement, Cash Out, and voided bets.',
        'note': 'Not covered in "domande_senza_risposta.md".',
        'questions': [
            ('I.1', 'How quickly are sports bets settled after an event ends? (Minutes? Hours? Depends on the sport? On the league?)',
             'Users win bets but don\'t see the payout immediately and think something is wrong.'),
            ('I.2', 'Can a user cancel or edit a placed bet? Before the event starts? After it starts?',
             'Users sometimes place bets by mistake.'),
            ('I.3', 'Cash Out: is it available for all bets or only certain ones? What determines if Cash Out is offered? Can it be partial?',
             'Users see Cash Out on some bets but not others. No explanation available.'),
            ('I.4', '"My winning bet was voided" — what are the reasons a winning bet can be cancelled? (Event cancelled, odds error, suspicious activity?)',
             'Users get very angry when this happens. We need a clear, fair explanation.'),
            ('I.5', 'For accumulator/parlay bets: if one leg is cancelled, what happens to the rest? Recalculated or void?',
             'Users with multi-leg bets often face this confusion with no answer available.'),
        ]
    },
    {
        'letter': 'J',
        'title': 'Platform-Specific Issues (New Jan-Feb 2026 patterns)',
        'impact': '~150/mo — NEW patterns',
        'color': GRAY,
        'intro': 'These are new issues that emerged or grew significantly in the Jan–Feb 2026 data, particularly around registration and currency display.',
        'note': 'Not covered in "domande_senza_risposta.md".',
        'questions': [
            ('J.1', 'Chile: "Número de contribuyente" / "RUT" — during registration, what should users enter in the "document number" field? Their RUT? With or without verification digit? With dots and dash? Example.',
             'Real ticket: "Cuál es el número de contribuyente para depositar?" and "Lo pongo y dice que no es válido" — Registration blocker for Chilean users.'),
            ('J.2', 'Argentina: "DNI" or "CUIL" — which one do Argentine users enter? What format? How many digits?',
             'Same registration blocker for Argentine users.'),
            ('J.3', 'The platform shows amounts in EUR/USD but the user deposited in CLP/ARS. How is the conversion displayed? Where can they see the exchange rate used?',
             'Real ticket: "Dice que está en inglés. Yo no te entiendo" — Users confused by currency display.'),
            ('J.4', 'Can a user change their display language after registration? Where in the settings? Does it change both interface AND support language?',
             'Some users registered in the wrong language and can\'t navigate the site.'),
            ('J.5', '"Datos no válidos" error during registration — what EXACTLY does this mean? List the most common causes: name format? Special characters? Duplicate email? Age?',
             'Real ticket: "Estoy escribiendo mis datos y sale que no son válidos y son mis datos" — Registration blocker. Many users can\'t create an account.'),
            ('J.6', 'Is there a minimum age for registration? How is it verified? What happens if an underage user manages to register?',
             'Compliance question — the bot needs to mention age requirements clearly.'),
        ]
    },
]

# ══════════════════════════════════════════════════════════════
# BUILD PDF
# ══════════════════════════════════════════════════════════════

def build():
    path = '/Users/serhiykorenyev/Desktop/vs code/widget cs /BetonWin_Missing_Info_For_CS.pdf'
    doc = SimpleDocTemplate(path, pagesize=A4,
        topMargin=1.4*cm, bottomMargin=1.4*cm, leftMargin=1.4*cm, rightMargin=1.4*cm)
    story = []
    W = A4[0] - 2.8*cm

    # ── COVER ──
    story.append(Spacer(1, 30*mm))
    story.append(Paragraph('BetonWin — Missing Information', styles['Title2']))
    story.append(Paragraph('Request for Customer Support Team', styles['Sub']))
    story.append(hr())
    story.append(spacer(4))
    story.append(Paragraph(
        'This document contains <b>55 questions</b> that our AI widget <b>cannot answer today</b>. '
        'We need the CS team to provide the correct answers so we can add them to the Knowledge Base '
        'and automate these responses.',
        styles['Body']))
    story.append(spacer(4))
    story.append(Paragraph(
        '<b>IMPORTANT:</b> This document does NOT repeat the 64 questions already sent in '
        '"domande_senza_risposta.md". These are <b>ADDITIONAL</b> information gaps discovered after '
        'expanding our analysis from 26,963 to <b>35,963 tickets</b> (adding Jan–Feb 2026 data).',
        styles['Body']))
    story.append(spacer(6))

    # Key info box
    info = [
        ['Data Source', '35,963 Zendesk tickets (Jul 2025 – Feb 2026)'],
        ['New Questions', '55 (in addition to the 64 already sent)'],
        ['Total Questions', '119 combined across both documents'],
        ['Language', 'English — please answer in English'],
        ['Generated', 'March 2026'],
    ]
    t = Table(info, colWidths=[W*0.25, W*0.75])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), LBLUE),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#d1d5db')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(spacer(8))

    # How to fill
    story.append(Paragraph('<b>How to complete this document:</b>', styles['Body']))
    instructions = [
        'Read each question in the <b>"Question for CS Team"</b> column',
        'Read <b>"Why We Need This"</b> to understand the real customer problem',
        'Write the correct answer in the <b>"Answer"</b> column (orange background)',
        'If the answer depends on the country, specify: "Chile: X, Argentina: Y"',
        'If unsure, write <b>"TO VERIFY — ask [person/team]"</b>',
        'If not applicable, write <b>"N/A"</b> and the reason',
    ]
    for i, inst in enumerate(instructions, 1):
        story.append(Paragraph(f'{i}. {inst}', styles['BulletX']))
    story.append(spacer(6))

    # Summary table
    story.append(Paragraph('<b>Sections Overview:</b>', styles['Body']))
    summary = [['Section', 'Topic', 'Questions', 'Priority', 'Est. Tickets/mo']]
    priorities = ['HIGH','CRITICAL','CRITICAL','HIGH','HIGH','HIGH','MEDIUM','MEDIUM','MEDIUM','LOW']
    tickets_mo = ['1,119','551','262','400','378','50','62','—','200','150']
    for i, s in enumerate(SECTIONS):
        summary.append([
            f'Section {s["letter"]}',
            s['title'],
            str(len(s['questions'])),
            priorities[i],
            tickets_mo[i],
        ])
    summary.append(['', 'TOTAL', '55', '', '~3,172'])
    st = Table(summary, colWidths=[W*0.12, W*0.35, W*0.10, W*0.12, W*0.15], repeatRows=1)
    st.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#d1d5db')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LGRAY]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('BACKGROUND', (0,-1), (-1,-1), LGREEN),
    ]))
    story.append(st)
    story.append(PageBreak())

    # ── SECTIONS ──
    for sec in SECTIONS:
        story.append(section_header(sec['letter'], sec['title'], sec['impact'], sec['color']))
        story.append(spacer(3))
        story.append(Paragraph(sec['intro'], styles['Body']))
        if sec['note']:
            story.append(spacer(2))
            story.append(Paragraph(f'<b>Note:</b> {sec["note"]}', styles['SmallI']))
        story.append(spacer(4))
        story.append(q_table(sec['questions'], W))
        story.append(spacer(6))
        story.append(hr())
        # Page break after certain sections
        if sec['letter'] in ('B', 'D', 'F', 'H'):
            story.append(PageBreak())

    # ── CLOSING ──
    story.append(PageBreak())
    story.append(Paragraph('Summary & Next Steps', styles['H1']))
    story.append(hr())
    story.append(Paragraph(
        'Once all 55 answers are provided, combined with the 64 answers from "domande_senza_risposta.md", '
        'we will have <b>119 complete answers</b> covering virtually all customer issues seen across 35,963 tickets.',
        styles['Body']))
    story.append(spacer(4))
    story.append(Paragraph('<b>Expected impact after KB update:</b>', styles['Body']))
    impact_data = [
        ['Metric', 'Current', 'After Update'],
        ['AI ticket coverage', '~47%', '~73%'],
        ['Tickets handled by AI/month', '~2,112', '~3,280'],
        ['Additional tickets automated', '—', '~1,168/month'],
        ['Cost savings (at $3–5/ticket)', '—', '$3,504–$5,840/month'],
        ['Agent time freed', '—', '~584 hours/month'],
    ]
    it = Table(impact_data, colWidths=[W*0.40, W*0.20, W*0.25], repeatRows=1)
    it.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#d1d5db')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LGRAY]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('FONTNAME', (2,1), (2,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (2,1), (2,-1), GREEN),
    ]))
    story.append(it)
    story.append(spacer(8))

    story.append(Paragraph('<b>Priority order for answering:</b>', styles['Body']))
    story.append(Paragraph('1. <b>Sections B + C</b> (Bank Transfer + Phone Verification) — CRITICAL, highest volume', styles['BulletX']))
    story.append(Paragraph('2. <b>Sections D + E + F</b> (Saldo 0.00 + Winnings + Withdrawal) — HIGH, highest frustration', styles['BulletX']))
    story.append(Paragraph('3. <b>Sections A + G</b> (Greetings + Account Closure) — MEDIUM, operational + compliance', styles['BulletX']))
    story.append(Paragraph('4. <b>Sections H + I + J</b> (Loyalty + Sports + Platform) — LOWER, but growing', styles['BulletX']))

    story.append(spacer(10))
    story.append(hr())
    story.append(Paragraph(
        '<i>Generated: March 2026 | Data: 35,963 Zendesk tickets (Jul 2025 – Feb 2026) | '
        'Complements: domande_senza_risposta.md (64 questions)</i>',
        styles['Small']))

    doc.build(story)
    print(f'PDF generated: {path}')

if __name__ == '__main__':
    build()
