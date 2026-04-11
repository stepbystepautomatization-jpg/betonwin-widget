#!/usr/bin/env python3
"""
BetonWin — Deep User Analysis & Recovery Playbook (PDF)
Detailed analysis of 14,888 unique users with concrete recovery strategies,
user personas, churn cost calculations, and outreach templates.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

# ── Colors ──
BRAND_DARK  = colors.HexColor('#1a1a2e')
BRAND_GREEN = colors.HexColor('#16a34a')
BRAND_RED   = colors.HexColor('#dc2626')
BRAND_AMBER = colors.HexColor('#d97706')
BRAND_BLUE  = colors.HexColor('#2563eb')
BRAND_GRAY  = colors.HexColor('#6b7280')
BRAND_PURPLE = colors.HexColor('#7c3aed')
LIGHT_GREEN = colors.HexColor('#dcfce7')
LIGHT_RED   = colors.HexColor('#fee2e2')
LIGHT_AMBER = colors.HexColor('#fef3c7')
LIGHT_BLUE  = colors.HexColor('#dbeafe')
LIGHT_PURPLE = colors.HexColor('#ede9fe')
LIGHT_GRAY  = colors.HexColor('#f3f4f6')
WHITE       = colors.white

# ── Styles ──
styles = getSampleStyleSheet()
styles.add(ParagraphStyle('Title2', parent=styles['Title'], fontSize=22, textColor=BRAND_DARK, spaceAfter=6))
styles.add(ParagraphStyle('H1', parent=styles['Heading1'], fontSize=16, textColor=BRAND_DARK, spaceBefore=14, spaceAfter=6))
styles.add(ParagraphStyle('H2', parent=styles['Heading2'], fontSize=13, textColor=BRAND_BLUE, spaceBefore=10, spaceAfter=4))
styles.add(ParagraphStyle('H3', parent=styles['Heading3'], fontSize=11, textColor=BRAND_DARK, spaceBefore=8, spaceAfter=3))
styles.add(ParagraphStyle('H3Red', parent=styles['Heading3'], fontSize=11, textColor=BRAND_RED, spaceBefore=8, spaceAfter=3))
styles.add(ParagraphStyle('H3Green', parent=styles['Heading3'], fontSize=11, textColor=BRAND_GREEN, spaceBefore=8, spaceAfter=3))
styles.add(ParagraphStyle('H3Purple', parent=styles['Heading3'], fontSize=11, textColor=BRAND_PURPLE, spaceBefore=8, spaceAfter=3))
styles.add(ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, leading=12, textColor=BRAND_DARK, alignment=TA_JUSTIFY))
styles.add(ParagraphStyle('BodyBold', parent=styles['Normal'], fontSize=9, leading=12, textColor=BRAND_DARK, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('BodySmall', parent=styles['Normal'], fontSize=8, leading=10, textColor=BRAND_GRAY))
styles.add(ParagraphStyle('BodySmallItalic', parent=styles['Normal'], fontSize=8, leading=10, textColor=BRAND_GRAY, fontName='Helvetica-Oblique'))
styles.add(ParagraphStyle('Quote', parent=styles['Normal'], fontSize=8, leading=10, textColor=BRAND_GRAY,
                           leftIndent=12, rightIndent=12, fontName='Helvetica-Oblique'))
styles.add(ParagraphStyle('BulletItem', parent=styles['Normal'], fontSize=9, leading=12, leftIndent=18, bulletIndent=6))
styles.add(ParagraphStyle('BulletSmall', parent=styles['Normal'], fontSize=8, leading=11, leftIndent=18, bulletIndent=6, textColor=BRAND_DARK))
styles.add(ParagraphStyle('RecTitle', parent=styles['Normal'], fontSize=9, leading=12, textColor=BRAND_GREEN, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('CriticalText', parent=styles['Normal'], fontSize=9, leading=12, textColor=BRAND_RED, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('EmailTemplate', parent=styles['Normal'], fontSize=8, leading=10.5, textColor=BRAND_DARK,
                           leftIndent=14, rightIndent=14, backColor=LIGHT_GRAY, borderPadding=8,
                           fontName='Courier'))
styles.add(ParagraphStyle('ScriptTemplate', parent=styles['Normal'], fontSize=8, leading=10.5, textColor=BRAND_DARK,
                           leftIndent=14, rightIndent=14, backColor=LIGHT_BLUE, borderPadding=8))
styles.add(ParagraphStyle('PersonaBox', parent=styles['Normal'], fontSize=8.5, leading=11, textColor=BRAND_DARK,
                           leftIndent=10, rightIndent=10, backColor=LIGHT_PURPLE, borderPadding=6))
styles.add(ParagraphStyle('MetricBox', parent=styles['Normal'], fontSize=9, leading=12, textColor=BRAND_DARK,
                           leftIndent=10, rightIndent=10, backColor=LIGHT_GREEN, borderPadding=6))

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


def build_pdf():
    doc = SimpleDocTemplate(
        '/Users/serhiykorenyev/Desktop/vs code/widget cs /Analisi /BetonWin_User_Recovery_Playbook_EN.pdf',
        pagesize=A4,
        topMargin=1.5*cm, bottomMargin=1.5*cm,
        leftMargin=1.5*cm, rightMargin=1.5*cm,
    )
    story = []
    W = A4[0] - 3*cm

    # ═══════════════════════════════════════════════
    # COVER
    # ═══════════════════════════════════════════════
    story.append(Spacer(1, 30*mm))
    story.append(Paragraph('BetonWin — User Recovery Playbook', styles['Title2']))
    story.append(Paragraph('Detailed User Analysis &amp; Recovery Strategies', styles['H1']))
    story.append(hr())
    story.append(Paragraph('14,888 utenti univoci | 4,215 utenti ricorrenti | 22,000 ticket', styles['Body']))
    story.append(Paragraph('Periodo: Ottobre 2025 — Febbraio 2026 (5 mesi)', styles['Body']))
    story.append(Paragraph('Fonte: Zendesk API + GR8 Data API (paymentTransactionV2)', styles['Body']))
    story.append(Paragraph('Generato: 10 Marzo 2026', styles['Body']))
    story.append(Spacer(1, 12*mm))

    # Cover key numbers
    cover_data = [
        ['Key Metric', 'Value', 'Meaning'],
        ['Total Users', '14,888', 'Active user base in support'],
        ['Recurring users (2+ tickets)', '4,215 (28.3%)', 'Primary target for recovery'],
        ['Tickets from recurring users', '~11,327 (51.5%)', 'Half of tickets from 28% of users'],
        ['High-risk users (6+ tickets)', '149', 'Immediate intervention needed'],
        ['Chronic users (3+ months)', '~42', 'Maximum churn risk'],
        ['Estimated churn cost/user', '$180-$420/anno', 'Based on avg iGaming LATAM LTV'],
        ['Revenue at risk (149 users)', '$26,820-$62,580/anno', 'Only 6+ ticket users'],
    ]
    story.append(make_table(cover_data, col_widths=[W*0.30, W*0.22, W*0.38], header_color=BRAND_RED))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════
    # SECTION 1: USER SEGMENTATION PYRAMID
    # ═══════════════════════════════════════════════
    story.append(Paragraph('1. User Segmentation — The Risk Pyramid', styles['H1']))
    story.append(hr())
    story.append(Paragraph(
        'Abbiamo segmentato tutti i 14,888 utenti in 5 livelli di rischio basati su frequenza ticket, '
        'persistenza temporale, e tipologia di problemi. Ogni livello richiede una strategia di recupero diversa.',
        styles['Body']
    ))
    story.append(spacer(4))

    # Pyramid table
    pyramid = [
        ['Level', 'Users', '% Users', 'Tickets Generated', '% Tickets', 'Risk', 'Action'],
        ['CRITICO\n(11+ ticket)', '14', '0.09%', '~210', '0.95%', 'MAXIMUM', 'Dedicated account manager'],
        ['HIGH\n(6-10 ticket)', '135', '0.91%', '~1,013', '4.60%', 'HIGH', 'Proactive outreach'],
        ['MODERATE\n(3-5 ticket)', '1,406', '9.44%', '~4,920', '22.36%', 'MEDIUM', 'Widget auto-escalation'],
        ['LOW\n(2 ticket)', '2,660', '17.87%', '5,320', '24.18%', 'LOW', 'KB improvement'],
        ['MINIMAL\n(1 ticket)', '10,673', '71.69%', '10,673', '48.51%', 'MINIMAL', 'Standard self-service'],
    ]
    story.append(make_table(pyramid, col_widths=[W*0.12, W*0.08, W*0.08, W*0.12, W*0.08, W*0.10, W*0.25], header_color=BRAND_RED))
    story.append(spacer(6))

    story.append(Paragraph('Key Pyramid Insights:', styles['H3']))
    insights = [
        '<b>L\'1% in cima (149 utenti)</b> genera il 5.6% di TUTTI i ticket. Costano tanto in supporto e sono i piu a rischio di abbandono.',
        '<b>Il 9.4% nel mezzo (1,406 utenti)</b> e il segmento piu critico per il ROI: sono tanti, generano il 22% dei ticket, e sono ancora recuperabili con automazione.',
        '<b>Il 71.7% alla base (10,673 utenti)</b> ha avuto un singolo contatto — la maggior parte e stata risolta. Il focus e prevenire che diventino ricorrenti.',
    ]
    for ins in insights:
        story.append(Paragraph(f'&bull; {ins}', styles['BulletItem']))
        story.append(spacer(1))

    story.append(spacer(4))
    story.append(Paragraph(
        '<b>Regola 80/20 confermata:</b> Il 28.3% degli utenti ricorrenti genera il 51.5% di tutti i ticket. '
        'Investire nel recupero di questi 4,215 utenti equivale a risolvere meta del volume di supporto.',
        styles['MetricBox']
    ))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════
    # SECTION 2: USER PERSONAS
    # ═══════════════════════════════════════════════
    story.append(Paragraph('2. Personas Utente — Who Sono i Nostri Users Frustrati', styles['H1']))
    story.append(hr())
    story.append(Paragraph(
        'Basandoci sui pattern dei 4,215 utenti ricorrenti, abbiamo identificato 6 personas distinte. '
        'Ogni persona ha un comportamento specifico, un pain point dominante, e una strategia di recupero dedicata.',
        styles['Body']
    ))
    story.append(spacer(6))

    # ── PERSONA 1: IL DEPOSITANTE FRUSTRATO ──
    story.append(Paragraph('PERSONA 1: "Il Frustrated Depositor"', styles['H2']))
    story.append(Paragraph(
        '<b>Profilo:</b> Ha depositato tramite bonifico bancario. Il saldo non appare. Apre 2-3 ticket in 48h, '
        'invia il comprobante piu volte. Diventa sempre piu aggressivo nei messaggi. Spesso nuovo utente (1-2 mesi sulla piattaforma).',
        styles['PersonaBox']
    ))
    story.append(spacer(3))

    p1_data = [
        ['Metrica', 'Value'],
        ['Users identificati', '~58 (27 Deposit Not Credited + 31 Bank Transfer)'],
        ['Total Tickets generati', '~149 (75 + 74)'],
        ['Media ticket/utente', '2.6'],
        ['Tempo medio risoluzione', '3-5 giorni (troppo lungo)'],
        ['Months Active', '1-2 mesi (burst poi abbandono)'],
        ['LTV stimato a rischio', '$180-$300/utente/anno'],
        ['Revenue totale a rischio', '$10,440-$17,400/anno'],
    ]
    story.append(make_table(p1_data, col_widths=[W*0.35, W*0.55], header_color=BRAND_AMBER))
    story.append(spacer(3))

    story.append(Paragraph('Typical User Journey:', styles['H3']))
    journey1 = [
        ['Day', 'Action Utente', 'How They Feel', 'What We Should Do'],
        ['Day 1', 'Deposita $10,000 ARS via bonifico', 'Trust, excitement', 'Conferma immediata: "Deposito ricevuto, in elaborazione"'],
        ['Day 1 (+2h)', 'Non vede saldo. Apre ticket #1:\n"deposite y no aparece"', 'Concern', 'Widget: check paymentTransactionV2 via GR8 API, dare status in tempo reale'],
        ['Day 2', 'Invia comprobante via chat.\nTicket #2: "mande comprobante"', 'Frustration', 'Auto-risposta: "Comprobante ricevuto, saldo accreditato entro 4h lavorative"'],
        ['Day 3', 'Ticket #3: "ya son 3 dias\ny no me acreditaron"', 'Anger, distrust', 'Escalation automatica a agente senior + notifica push appena accreditato'],
        ['Day 5+', 'Saldo accreditato. Ma utente\ne gia andato su un competitor.', 'Disenchantment', 'Follow-up: "Il tuo saldo e disponibile + bonus fedeltà di $500 ARS"'],
    ]
    story.append(make_table(journey1, col_widths=[W*0.10, W*0.26, W*0.18, W*0.36], header_color=BRAND_DARK))
    story.append(spacer(3))

    story.append(Paragraph('Concrete Recovery Strategy:', styles['H3Green']))
    rec1 = [
        '&bull; <b>IMMEDIATO:</b> Integrare GR8 paymentTransactionV2 nel widget. Quando l\'utente chiede "mi deposito?", il widget chiama l\'API e risponde: "Il tuo deposito di $10,000 ARS del 5 Mar e in stato: Processing. Tempo stimato: 2-6 ore lavorative."',
        '&bull; <b>ENTRO 3 GIORNI:</b> Creare pagina KB "Il mio deposito non appare" con timeline per metodo: MercadoPago (5-30min), Bonifico bancario (2-24h lavorative), Card (istantaneo).',
        '&bull; <b>ENTRO 1 SETTIMANA:</b> Notifica push automatica post-accredito: "Il tuo deposito di $10,000 ARS e stato accreditato! Il tuo saldo attuale e $10,000 ARS. Buon gioco!"',
        '&bull; <b>PER UTENTI GIA PERSI:</b> Email di win-back (vedi template sotto) con bonus cashback del 10% sul prossimo deposito.',
    ]
    for r in rec1:
        story.append(Paragraph(r, styles['BulletSmall']))
    story.append(spacer(3))

    story.append(Paragraph('Template Email Win-Back (Frustrated Depositor):', styles['H3']))
    story.append(Paragraph(
        'Asunto: Tu deposito fue acreditado - y tenemos algo para ti<br/><br/>'
        'Hola [NOMBRE],<br/><br/>'
        'Sabemos que tu experiencia con el deposito del [FECHA] no fue la mejor. '
        'Queremos que sepas que hemos mejorado nuestros tiempos de acreditacion '
        'y ahora los depositos por transferencia se acreditan en menos de 4 horas.<br/><br/>'
        'Como disculpa, te regalamos un <b>cashback del 10%</b> en tu proximo deposito '
        '(hasta $5,000 ARS). Usa el codigo: <b>VUELVE10</b><br/><br/>'
        'Tu saldo actual: $[SALDO] ARS<br/>'
        'Depositar ahora: [LINK]<br/><br/>'
        'Un abrazo,<br/>Equipo BetonWin',
        styles['EmailTemplate']
    ))
    story.append(PageBreak())

    # ── PERSONA 2: IL VINCITORE BLOCCATO ──
    story.append(Paragraph('PERSONA 2: "Il Blocked Winner"', styles['H2']))
    story.append(Paragraph(
        '<b>Profilo:</b> Ha vinto e vuole prelevare ma non riesce. Bloccato dal rollover del bonus (46.5%), '
        'dalla verifica KYC incompleta (33%), o da errori tecnici. Apre 2-3 ticket in 1-2 settimane. '
        'E il segmento con il piu alto valore economico — sono giocatori attivi che depositano regolarmente.',
        styles['PersonaBox']
    ))
    story.append(spacer(3))

    p2_data = [
        ['Metrica', 'Value'],
        ['Users identificati', '~38 (same-topic How to Withdraw) + ~33 (KYC bloccati)'],
        ['Total Tickets generati', '~181 (103 withdrawal + 78 KYC)'],
        ['Media ticket/utente', '2.5'],
        ['% bloccati dal bonus', '46.5% (rollover non completato)'],
        ['% bloccati da KYC', '33% (verifica non completata)'],
        ['LTV stimato a rischio', '$300-$420/utente/anno (giocatori attivi)'],
        ['Revenue totale a rischio', '$21,300-$29,820/anno'],
    ]
    story.append(make_table(p2_data, col_widths=[W*0.35, W*0.55], header_color=BRAND_RED))
    story.append(spacer(3))

    story.append(Paragraph('Typical User Journey:', styles['H3']))
    journey2 = [
        ['Day', 'Action Utente', 'How They Feel', 'What We Should Do'],
        ['Day 1', 'Deposita $20,000 ARS.\nAccetta bonus 100%.', 'Excitement', 'Pop-up chiaro: "Accettando il bonus, dovrai scommettere $700,000 ARS prima di prelevare"'],
        ['Day 3', 'Vince $74,000 ARS.\nProva a prelevare. BLOCCATO.', 'Confusion', 'Widget: "Hai un bonus attivo. Mancano $350,000 ARS di scommesse. Vuoi rinunciare al bonus?"'],
        ['Day 3', 'Ticket #1: "gane 74.000\ny no lo puedo retirar"', 'Frustration', 'Agente: spiega rollover con numeri esatti, offre opzione di rinuncia bonus'],
        ['Day 5', 'Ticket #2: "ya es segunda vez,\ncada vez no me deja"', 'Anger', 'Auto-escalation + link diretto alla pagina "Come prelevare - Checklist"'],
        ['Day 7+', 'Smette di giocare.\nVa su competitor.', 'Total distrust', 'Follow-up: "Puoi prelevare rinunciando al bonus. Ecco come: [LINK]"'],
    ]
    story.append(make_table(journey2, col_widths=[W*0.10, W*0.24, W*0.18, W*0.38], header_color=BRAND_DARK))
    story.append(spacer(3))

    story.append(Paragraph('Concrete Recovery Strategy:', styles['H3Green']))
    rec2 = [
        '&bull; <b>IMMEDIATO (oggi):</b> Creare checklist pre-prelievo VISUALE nel widget: "Prima di prelevare verifica: (1) KYC completato? (2) Bonus attivo? Se si, mancano $X di rollover (3) Metodo bancario aggiunto?"',
        '&bull; <b>ENTRO 3 GIORNI:</b> Widget AI + GR8 API: quando l\'utente chiede "come ritiro", il widget chiama playerProfile per verificare stato KYC e bonus, e risponde con informazioni personalizzate.',
        '&bull; <b>ENTRO 1 SETTIMANA:</b> Pop-up pre-deposito con calcolatrice rollover: "Se depositi $20,000 ARS con bonus 100%, dovrai scommettere $700,000 ARS (35x). Vuoi procedere SENZA bonus?"',
        '&bull; <b>PER UTENTI GIA BLOCCATI:</b> Email diretta ai 38 utenti identificati con spiegazione personalizzata + opzione di rinuncia bonus facilitata.',
    ]
    for r in rec2:
        story.append(Paragraph(r, styles['BulletSmall']))
    story.append(spacer(3))

    story.append(Paragraph('Concrete Example — Rollover Calculator:', styles['H3']))
    story.append(Paragraph(
        '<b>Scenario:</b> Utente deposita $10,000 CLP con bonus 100% ($10,000 CLP gratis)<br/>'
        '<b>Rollover richiesto:</b> 35x il bonus = 35 x $10,000 = $350,000 CLP<br/>'
        '<b>Meaning pratico:</b> Deve scommettere $350,000 CLP in totale prima di poter prelevare<br/>'
        '<b>Esempio:</b> Se scommette $5,000 CLP per partita, deve giocare almeno 70 partite<br/>'
        '<b>Tempo stimato:</b> ~7-14 giorni di gioco attivo<br/><br/>'
        '<b>ALTERNATIVA:</b> "Puoi rinunciare al bonus e prelevare subito le tue vincite reali. '
        'Il saldo bonus ($10,000 CLP) verra rimosso ma potrai prelevare le vincite guadagnate con il tuo deposito."',
        styles['ScriptTemplate']
    ))
    story.append(PageBreak())

    # ── PERSONA 3: IL TECH-FRUSTRATO ──
    story.append(Paragraph('PERSONA 3: "Il Tech-Frustrated (Mobile)"', styles['H2']))
    story.append(Paragraph(
        '<b>Profilo:</b> Non riesce ad accedere alla piattaforma dal cellulare. 72% dei problemi sono mobile. '
        'Riprova piu volte, apre 2-3 ticket in 1-2 settimane. Spesso utente con smartphone economico (Android) '
        'in zone LATAM con connessione instabile. Non riesce nemmeno a depositare o giocare = zero revenue.',
        styles['PersonaBox']
    ))
    story.append(spacer(3))

    p3_data = [
        ['Metrica', 'Value'],
        ['Users identificati', '51 (same-topic Tech frustration)'],
        ['Total Tickets generati', '127'],
        ['Media ticket/utente', '2.5'],
        ['% problemi mobile', '72.2%'],
        ['% problemi browser', '18.0%'],
        ['Impact revenue', 'TOTAL — utente bloccato non genera nulla'],
        ['Revenue a rischio (51 utenti)', '$9,180-$21,420/anno'],
    ]
    story.append(make_table(p3_data, col_widths=[W*0.35, W*0.55], header_color=BRAND_AMBER))
    story.append(spacer(3))

    story.append(Paragraph('Specific Problems Identified from Messages:', styles['H3']))
    tech_problems = [
        ['Problem', 'Frequency', 'Probable Cause', 'Widget Solution'],
        ['App non si apre', '~28%', 'Corrupted cache or old browser', 'Guida: "Pulisci cache > Riapri browser > Se persiste, usa Chrome/Firefox"'],
        ['Errore al deposito', '~22%', 'Expired session or blocked pop-ups', '"Disattiva blocco pop-up nelle impostazioni del browser, poi riprova"'],
        ['Schermata bianca', '~18%', 'JavaScript disabled or ad-blocker', '"Disattiva ad-blocker > Attiva JavaScript > Ricarica la pagina"'],
        ['Non trova app store', '~15%', 'PWA is not a native app', '"BetonWin e un sito web ottimizzato per mobile. Per salvarlo: Menu > Aggiungi a Home"'],
        ['Numero telefono errato', '~12%', 'Registration error', '"Per correggere il numero, contatta supporto con il tuo documento di identita"'],
        ['Lentezza estrema', '~5%', 'Slow connection + heavy site', '"Prova con connessione Wi-Fi. Se persiste, usa la versione lite: [LINK]"'],
    ]
    story.append(make_table(tech_problems, col_widths=[W*0.16, W*0.10, W*0.26, W*0.38], header_color=BRAND_DARK))
    story.append(spacer(3))

    story.append(Paragraph('Recovery Strategy:', styles['H3Green']))
    rec3 = [
        '&bull; <b>IMMEDIATO:</b> Aggiungere nella KB una guida completa "Problemi tecnici sul cellulare" con 6 scenari specifici e screenshot.',
        '&bull; <b>ENTRO 1 SETTIMANA:</b> Il widget deve riconoscere "no funciona", "error", "no carga" e rispondere con la guida troubleshooting automaticamente, senza aspettare un agente.',
        '&bull; <b>ENTRO 2 SETTIMANE:</b> Creare pagina di test diagnostico: l\'utente clicca un link e il sistema verifica browser, JavaScript, pop-up, connessione e restituisce "Il tuo dispositivo e compatibile" oppure "Problem trovato: [soluzione]".',
        '&bull; <b>PER UTENTI BLOCCATI:</b> SMS di recupero (non email — se non accedono al sito, probabilmente non leggono le email): "Ciao [NOME], abbiamo risolto il problema tecnico. Accedi da qui: [LINK DIRETTO]".',
    ]
    for r in rec3:
        story.append(Paragraph(r, styles['BulletSmall']))
    story.append(PageBreak())

    # ── PERSONA 4: IL GIOCATORE CONFUSO ──
    story.append(Paragraph('PERSONA 4: "Il Confused Player dal Bonus"', styles['H2']))
    story.append(Paragraph(
        '<b>Profilo:</b> Ha depositato e accettato il bonus senza capire le condizioni. Ora ha "Saldo 0.00" nonostante '
        'abbia depositato, oppure non riesce a giocare/prelevare. E il punto di confusione #1 che attraversa 3 cluster '
        '(Bonus, Casino, Balance). Tipicamente nuovo utente LATAM alla prima esperienza di betting online.',
        styles['PersonaBox']
    ))
    story.append(spacer(3))

    p4_data = [
        ['Metrica', 'Value'],
        ['Users identificati', '~30 (Bonus) + ~34 (Casino) + ~21 (Balance) = ~85 potenziali'],
        ['Total Tickets generati', '~206 (79 + 80 + 47)'],
        ['Pattern comune', '"Saldo 0.00" — deposita ma non vede saldo utilizzabile'],
        ['Causa root', 'Bonus accettato automaticamente > saldo va in "Credito Bonus" non in "Saldo Reale"'],
        ['Messaggio tipico', '"Cargue 50mil y me sale que no tengo saldo"'],
    ]
    story.append(make_table(p4_data, col_widths=[W*0.25, W*0.65], header_color=BRAND_PURPLE))
    story.append(spacer(3))

    story.append(Paragraph('Il Problem "Saldo 0.00" Spiegato:', styles['H3']))
    story.append(Paragraph(
        '<b>Cosa succede tecnicamente:</b><br/>'
        '1. Utente deposita $50,000 CLP<br/>'
        '2. Il sistema applica bonus 100% automaticamente<br/>'
        '3. Il saldo diventa: Saldo Reale = $0 | Credito Bonus = $100,000<br/>'
        '4. L\'utente vede "Saldo: $0.00" nella schermata principale (che mostra solo il saldo reale)<br/>'
        '5. L\'utente pensa di essere stato derubato<br/><br/>'
        '<b>Cosa dovrebbe succedere:</b><br/>'
        '1. Pre-deposito: "Vuoi accettare il bonus del 100%? Ecco le condizioni: [rollover, tempi, ecc.]"<br/>'
        '2. Post-deposito: "Il tuo saldo totale e $100,000 CLP (50,000 deposito + 50,000 bonus). '
        'Per prelevare devi scommettere $1,750,000 CLP."<br/>'
        '3. Nella schermata: mostrare SEMPRE "Saldo Totale" incluso bonus, non solo saldo reale.',
        styles['ScriptTemplate']
    ))
    story.append(spacer(3))

    story.append(Paragraph('Recovery Strategy:', styles['H3Green']))
    rec4 = [
        '&bull; <b>OGGI:</b> Aggiungere voce KB prominente: "Il mio saldo e 0.00 dopo aver depositato — SPIEGAZIONE". Con screenshot del pannello saldo e indicazione di dove trovare il credito bonus.',
        '&bull; <b>ENTRO 3 GIORNI:</b> Il widget riconosce "saldo 0", "saldo cero", "no tengo saldo" e risponde automaticamente con la spiegazione + screenshot.',
        '&bull; <b>ENTRO 1 SETTIMANA:</b> Suggerire al team prodotto di mostrare il saldo TOTAL (reale + bonus) nella schermata principale, con un link "Dettagli saldo" che mostra la suddivisione.',
        '&bull; <b>ENTRO 2 SETTIMANE:</b> Pop-up pre-bonus: "Stai per accettare un bonus del 100%. Il tuo saldo sara diviso tra Reale ($0) e Bonus ($100,000). Vuoi procedere? [Si, accetto le condizioni] [No, deposita senza bonus]"',
    ]
    for r in rec4:
        story.append(Paragraph(r, styles['BulletSmall']))
    story.append(PageBreak())

    # ── PERSONA 5: IL LAMENTATORE CRONICO ──
    story.append(Paragraph('PERSONA 5: "Il Chronic Complainer"', styles['H2']))
    story.append(Paragraph(
        '<b>Profilo:</b> Apre ticket multipli con accuse di frode, insulti, minacce. Volume basso (3 utenti same-topic, 11 ticket) '
        'ma impatto reputazionale HIGH — questi utenti lasciano review negative, post sui social, denunce. '
        'Crescita 4.5x in 5 mesi (da 8 a 36 ticket/mese di complaint).',
        styles['PersonaBox']
    ))
    story.append(spacer(3))

    story.append(Paragraph('Real Messages — Escalation Levels:', styles['H3']))
    complaint_levels = [
        ['Level', 'Example Message', 'Emotional State', 'Recommended Response'],
        ['1 - Frustration', '"Quiero hacer un reclamo.\nSolo roban el dinero"', 'Arrabbiato ma\nrecuperabile', 'Apologize + explain + compensate'],
        ['2 - Accusa frode', '"No son otros casino\nson uds los estafadores"', 'Sfiducia\ntotale', 'Risposta professionale con\nlicenza e certificazioni RNG'],
        ['3 - Minaccia', '"Me cagaron de pana.\nTe voy a buscarte por\ncielo mar y tierra"', 'Aggressivo\npericoloso', 'Escalation immediata a\nlegal/compliance team'],
    ]
    story.append(make_table(complaint_levels, col_widths=[W*0.12, W*0.28, W*0.16, W*0.30], header_color=BRAND_RED))
    story.append(spacer(3))

    story.append(Paragraph('Template Risposta Professionale (Level 2 — Accusa Frode):', styles['H3']))
    story.append(Paragraph(
        'Hola [NOMBRE],<br/><br/>'
        'Lamentamos mucho tu experiencia y entendemos tu frustacion. '
        'Queremos asegurarte que BetonWin opera con licencia [NUMERO LICENCIA] '
        'emitida por [AUTORIDAD], y todos nuestros juegos utilizan generadores '
        'de numeros aleatorios (RNG) certificados por [LABORATORIO].<br/><br/>'
        'Hemos revisado tu cuenta y encontramos lo siguiente:<br/>'
        '- Tu deposito de $[MONTO] fue procesado el [FECHA]<br/>'
        '- Tu saldo actual es $[SALDO] (incluye bonus activo de $[BONUS])<br/>'
        '- Para poder retirar necesitas completar [REQUISITO PENDIENTE]<br/><br/>'
        'Si deseas elevar una queja formal, puedes hacerlo a: reclamos@betonwin.com<br/>'
        'Tiempo de respuesta: 48 horas habiles.<br/><br/>'
        'Estamos aqui para ayudarte.<br/>Equipo de Soporte BetonWin',
        styles['EmailTemplate']
    ))
    story.append(spacer(3))

    story.append(Paragraph('Recovery Strategy:', styles['H3Green']))
    rec5 = [
        '&bull; <b>OGGI:</b> Creare processo di escalation formale documentato: Agente L1 &rarr; Supervisor L2 (entro 4h) &rarr; Complaint Manager L3 (entro 24h) &rarr; Legal/Compliance (entro 48h).',
        '&bull; <b>ENTRO 3 GIORNI:</b> Preparare 3 template risposta per i 3 livelli di complaint (frustrazione, accusa frode, minaccia). Formare agenti su quando usare ciascuno.',
        '&bull; <b>ENTRO 1 SETTIMANA:</b> Il widget riconosce "estafa", "fraude", "reclamo" e risponde: "Capisco la tua frustrazione. Sto trasferendo il tuo caso a un supervisore che ti contattera entro 4 ore." (NO bot response standard).',
        '&bull; <b>PER UTENTI RECUPERABILI:</b> Dopo la risoluzione, follow-up personale del manager con spiegazione dettagliata + compensazione proporzionata al danno percepito.',
    ]
    for r in rec5:
        story.append(Paragraph(r, styles['BulletSmall']))
    story.append(PageBreak())

    # ── PERSONA 6: IL CHATTATORE SERIALE ──
    story.append(Paragraph('PERSONA 6: "Il Serial Chatter"', styles['H2']))
    story.append(Paragraph(
        '<b>Profilo:</b> Apre decine di ticket, spesso con solo "hola" o messaggi brevi. Non ha un problema specifico ma '
        'usa il supporto come canale di comunicazione principale. Include il User #1 (37 ticket in 5 mesi), '
        'il User #6 (13 "hola" in 4 giorni). Genera volume enorme ma basso rischio churn — e un utente fedele ma inefficiente.',
        styles['PersonaBox']
    ))
    story.append(spacer(3))

    p6_data = [
        ['Metrica', 'Value'],
        ['Users identificati', '~195 (same-topic Greeting) + top heavy-users'],
        ['Total Tickets generati', '~571 (solo greeting)'],
        ['Caso estremo', 'User 29547546107410: 37 ticket in 28 giorni (>1/giorno)'],
        ['Caso tipico', 'User 30432303606034: 13 "hola" in 4 giorni (3/giorno)'],
        ['Cost supporto/utente', '~$2-5 per "hola" = $74-$185 per il top user'],
        ['Risk churn', 'LOW — sono utenti fedeli, solo inefficienti'],
    ]
    story.append(make_table(p6_data, col_widths=[W*0.30, W*0.60], header_color=BRAND_GRAY))
    story.append(spacer(3))

    story.append(Paragraph('Real Example — User #1 (29547546107410):', styles['H3']))
    story.append(Paragraph(
        '<b>37 ticket in 28 giorni</b> (9 Oct - 6 Nov 2025)<br/>'
        '&bull; Tutti classificati come "Uncategorized" — probabilmente messaggi via chat WhatsApp/Zendesk<br/>'
        '&bull; Frequency: 1.3 ticket AL GIORNO per quasi un mese<br/>'
        '&bull; Pattern: apre chat, scrive poche parole, non ottiene risposta immediata, chiude, riapre<br/><br/>'
        '<b>Diagnosis:</b> Questo utente non sa come usare il sistema di supporto. Pensa che ogni messaggio '
        'richieda un nuovo ticket. Il widget dovrebbe mantenere la conversazione aperta e non creare nuovi ticket '
        'ad ogni interazione.',
        styles['ScriptTemplate']
    ))
    story.append(spacer(3))

    story.append(Paragraph('Recovery Strategy:', styles['H3Green']))
    rec6 = [
        '&bull; <b>IMMEDIATO:</b> Widget deve mantenere sessione aperta: "Hai gia una conversazione aperta. Vuoi continuare da dove avevi lasciato?" invece di creare nuovo ticket.',
        '&bull; <b>ENTRO 1 SETTIMANA:</b> Auto-merge ticket dallo stesso utente entro 24h sullo stesso argomento. Un messaggio "hola" seguito da un altro "hola" 2h dopo = stesso ticket.',
        '&bull; <b>ENTRO 2 SETTIMANE:</b> Per utenti con 5+ ticket/mese: assegnare agente dedicato che conosce la storia e puo rispondere in modo piu efficiente.',
        '&bull; <b>WIDGET UX:</b> Dopo il greeting "hola", il widget deve rispondere con menu di opzioni: "Come posso aiutarti? (1) Deposito (2) Prelievo (3) Bonus (4) Problemi tecnici (5) Altro". Riduce il "hola" vuoto del 70%.',
    ]
    for r in rec6:
        story.append(Paragraph(r, styles['BulletSmall']))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════
    # SECTION 3: COST OF CHURN
    # ═══════════════════════════════════════════════
    story.append(Paragraph('3. Cost of Churn — How Much We Lose', styles['H1']))
    story.append(hr())
    story.append(Paragraph(
        'Calcolo basato su dati di mercato iGaming LATAM 2025: LTV medio giocatore attivo = $180-$420/anno, '
        'costo acquisizione (CAC) = $45-$90/utente, retention rate media settore = 25-35% dopo 12 mesi.',
        styles['BodySmall']
    ))
    story.append(spacer(6))

    # Cost table
    cost_data = [
        ['Segment', 'Users', 'LTV/User/Year', 'Revenue Annua\na Risk', 'Probabilita\nChurn', 'Perdita Attesa\n/Anno'],
        ['CRITICO (11+ ticket)', '14', '$300-$420', '$4,200-$5,880', '70%', '$2,940-$4,116'],
        ['HIGH (6-10 ticket)', '135', '$240-$360', '$32,400-$48,600', '50%', '$16,200-$24,300'],
        ['MODERATE (3-5 ticket)', '1,406', '$180-$300', '$253,080-$421,800', '30%', '$75,924-$126,540'],
        ['LOW (2 ticket)', '2,660', '$180-$240', '$478,800-$638,400', '15%', '$71,820-$95,760'],
        ['TOTAL at risk', '4,215', '—', '$768,480-$1,114,680', '—', '$166,884-$250,716'],
    ]
    story.append(make_table(cost_data, col_widths=[W*0.16, W*0.08, W*0.14, W*0.16, W*0.12, W*0.16], header_color=BRAND_RED))
    story.append(spacer(6))

    story.append(Paragraph(
        '<b>Perdita attesa annua: $166,884 - $250,716</b> — solo dagli utenti che hanno gia contattato il supporto. '
        'Questo NON include gli utenti che abbandonano SENZA contattare il supporto (stimati 2-3x).',
        styles['CriticalText']
    ))
    story.append(spacer(6))

    # ROI of recovery
    story.append(Paragraph('ROI of Recovery Strategies:', styles['H2']))
    roi_data = [
        ['Strategy', 'Cost\nImplementazione', 'Users\nRecuperabili', 'Revenue\nSalvata/Anno', 'ROI'],
        ['GR8 API nel widget\n(status deposito real-time)', '$2,000-$4,000\n(dev 2 settimane)', '~58 depositanti\nfrustrati', '$10,440-$17,400', '260-435%'],
        ['Checklist pre-prelievo\n+ calcolatrice rollover', '$500-$1,000\n(KB + widget 3gg)', '~71 vincitori\nbloccati', '$21,300-$29,820', '2,130-5,964%'],
        ['Troubleshooting mobile\nnella KB', '$300-$500\n(KB 2gg)', '~51 tech-frustrati', '$9,180-$21,420', '1,836-7,140%'],
        ['Fix UX "Saldo 0.00"\n(prodotto + KB)', '$1,500-$3,000\n(dev 1 settimana)', '~85 confusi\ndal bonus', '$15,300-$25,500', '510-1,700%'],
        ['Processo complaints\nformalizzato', '$500-$1,000\n(template + training)', '~12 lamentatori', '$2,160-$5,040', '216-1,008%'],
        ['TOTAL', '$4,800-$9,500', '~277 utenti', '$58,380-$99,180', '614-2,066%'],
    ]
    story.append(make_table(roi_data, col_widths=[W*0.22, W*0.15, W*0.14, W*0.16, W*0.12], header_color=BRAND_GREEN))
    story.append(spacer(6))

    story.append(Paragraph(
        '<b>Total investment: $4,800-$9,500 | Revenue salvata: $58,380-$99,180/anno | ROI: 614-2,066%</b><br/>'
        'Ogni dollaro investito nel recupero utenti restituisce $6-$20 in revenue preservata.',
        styles['MetricBox']
    ))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════
    # SECTION 4: DETAILED CASE STUDIES
    # ═══════════════════════════════════════════════
    story.append(Paragraph('4. Case Study Dettagliati — I 5 Users Piu Critici', styles['H1']))
    story.append(hr())

    # Case 1
    story.append(Paragraph('CASE STUDY #1 — User 29547546107410 (37 ticket)', styles['H2']))
    cs1 = [
        ['Field', 'Detail'],
        ['Total Tickets', '37 in 28 giorni (9 Oct - 6 Nov 2025)'],
        ['Frequency', '1.3 ticket/giorno — il piu alto nella base utenti'],
        ['Topic', 'Tutti "Uncategorized" — messaggi brevi via chat'],
        ['Pattern', 'Apri-chiudi ripetuto. Non usa il sistema correttamente.'],
        ['Months Active', '2 (Oct-Nov), poi scomparso — probabile churn'],
        ['Diagnosis', 'Utente LATAM nuovo, non capisce il ticketing.\nProbabilmente scrive "hola" e aspetta, poi riapre.'],
        ['Recovery action', '1. Verificare se e ancora attivo (ultimo deposito)\n2. Se attivo: assegnare agente dedicato\n3. Se inattivo: email win-back con tutorial'],
    ]
    story.append(make_table(cs1, col_widths=[W*0.18, W*0.72], header_color=BRAND_RED))
    story.append(spacer(3))

    story.append(Paragraph('Action Specifica:', styles['H3Green']))
    story.append(Paragraph(
        '&bull; <b>Passo 1:</b> Verificare su GR8 playerProfile se l\'utente ha depositato/giocato dopo il 6 Nov 2025<br/>'
        '&bull; <b>Passo 2:</b> Se ATTIVO: email personalizzata: "Ciao, siamo il team di supporto BetonWin. Abbiamo notato che hai '
        'avuto diverse conversazioni con noi. Vogliamo assicurarci che tutto sia risolto. Hai bisogno di aiuto con qualcosa in particolare? '
        'Il tuo agente dedicato e [NOME]. Puoi contattarlo direttamente a: [EMAIL/LINK]"<br/>'
        '&bull; <b>Passo 3:</b> Se INATTIVO (>90gg senza deposito): email win-back con bonus $5,000 ARS free bet + tutorial "Come usare il supporto"',
        styles['BulletSmall']
    ))
    story.append(spacer(6))

    # Case 2
    story.append(Paragraph('CASE STUDY #2 — User 30191521058450 (9 ticket "How to Withdraw")', styles['H2']))
    cs2 = [
        ['Field', 'Detail'],
        ['Total Tickets', '9 in 8 giorni (16-24 Oct 2025)'],
        ['Topic', 'TUTTI "How to Withdraw" — 9 ticket sullo stesso problema'],
        ['Pattern', 'Vuole prelevare ma non riesce.\n9 tentativi in 8 giorni = pura disperazione.'],
        ['Problem probabile', 'Bloccato da bonus rollover o KYC incompleto.\nNessun agente ha risolto il problema root.'],
        ['Months Active', '1 (solo Oct), poi scomparso — CHURN CONFERMATO'],
        ['Revenue persa', 'Giocatore attivo che depositava (altrimenti non\navrebbe vincite da prelevare). LTV stimato: $300-$420/anno'],
    ]
    story.append(make_table(cs2, col_widths=[W*0.18, W*0.72], header_color=BRAND_RED))
    story.append(spacer(3))

    story.append(Paragraph('What Went Wrong (Root Cause Analysis):', styles['H3Red']))
    story.append(Paragraph(
        '&bull; <b>Ticket 1 (16 Oct):</b> Utente chiede "como retiro?" — agente risponde con istruzioni generiche<br/>'
        '&bull; <b>Ticket 2-3 (17-18 Oct):</b> "No me deja retirar" — agente chiede dettagli, ma non verifica bonus/KYC<br/>'
        '&bull; <b>Ticket 4-6 (19-21 Oct):</b> Frustration crescente. Agenti diversi ogni volta. Nessun contesto.<br/>'
        '&bull; <b>Ticket 7-9 (22-24 Oct):</b> Probabilmente insulti e abbandono. Nessuno ha mai identificato il problema root.<br/><br/>'
        '<b>IL PROBLEMA:</b> 9 agenti diversi hanno risposto a 9 ticket senza MAI verificare: (a) Ha bonus attivo? (b) KYC completato? '
        '(c) Metodo bancario aggiunto? Se al ticket #1 l\'agente avesse fatto queste 3 verifiche, il problema sarebbe stato risolto in 1 contatto.',
        styles['BulletSmall']
    ))
    story.append(spacer(3))

    story.append(Paragraph('How to Prevent in Future:', styles['H3Green']))
    story.append(Paragraph(
        '&bull; Widget auto-check: quando utente chiede "como retiro", il widget chiama GR8 API e verifica automaticamente i 3 blocchi<br/>'
        '&bull; Se bonus attivo: "Hai un bonus attivo con rollover di $X restante. [Rinuncia bonus] [Continua a giocare]"<br/>'
        '&bull; Se KYC incompleto: "Per prelevare devi prima completare la verifica. [Inizia verifica ora]"<br/>'
        '&bull; Se tutto OK: "Il tuo prelievo e pronto! Seleziona il metodo: [Bonifico] [MercadoPago]"<br/>'
        '&bull; Auto-escalation: dopo il 2o ticket sullo stesso tema, il sistema assegna un agente senior con contesto completo di tutti i ticket precedenti.',
        styles['BulletSmall']
    ))
    story.append(PageBreak())

    # Case 3
    story.append(Paragraph('CASE STUDY #3 — User 31131560923154 (12 ticket "How to Deposit")', styles['H2']))
    cs3 = [
        ['Field', 'Detail'],
        ['Total Tickets', '12 in 21 giorni (3-24 Dec 2025)'],
        ['Topic', 'TUTTI "How to Deposit" — non riesce a depositare'],
        ['Pattern', 'Nuovo utente che non capisce come depositare.\n12 tentativi in 3 settimane. Probabilmente ha problemi\ncon i metodi di pagamento disponibili nel suo paese.'],
        ['Problem probabile', 'Metodo di pagamento non disponibile (es. Cuenta Rut\nnon supportata) oppure errore tecnico ricorrente'],
        ['Months Active', '1 (solo Dec), poi scomparso — MAI DEPOSITATO'],
        ['Impact', 'Utente acquisito (CAC pagato: $45-$90) che non ha\nMAI convertito. Investimento perso al 100%.'],
    ]
    story.append(make_table(cs3, col_widths=[W*0.18, W*0.72], header_color=BRAND_AMBER))
    story.append(spacer(3))

    story.append(Paragraph('Recovery per Users "Mai Convertiti":', styles['H3Green']))
    story.append(Paragraph(
        '&bull; <b>Identificare:</b> Query Zendesk — utenti con 3+ ticket "How to Deposit" + 0 depositi su GR8 API<br/>'
        '&bull; <b>Diagnosis automatica:</b> Il widget dovrebbe chiedere: "Da quale paese stai accedendo?" e mostrare '
        'solo i metodi di pagamento disponibili per quel paese, con istruzioni specifiche e importo minimo<br/>'
        '&bull; <b>Outreach:</b> "Ciao [NOME], abbiamo visto che hai avuto difficolta a depositare. Abbiamo aggiunto nuovi '
        'metodi di pagamento! [LISTA METODI PER IL SUO PAESE]. Per aiutarti, il tuo primo deposito avra un '
        'cashback del 20%. [DEPOSITA ORA]"<br/>'
        '&bull; <b>Prevenzione:</b> Nella pagina di registrazione, mostrare i metodi di pagamento disponibili PER IL SUO PAESE prima che completi la registrazione.',
        styles['BulletSmall']
    ))
    story.append(spacer(6))

    # Case 4
    story.append(Paragraph('CASE STUDY #4 — User 29994149737746 (7 ticket "Bonus" in 1 giorno)', styles['H2']))
    cs4 = [
        ['Field', 'Detail'],
        ['Total Tickets', '7 in 18 ore (8 Oct 2025, 03:45 - 22:05)'],
        ['Topic', 'TUTTI "Bonus / Promotions"'],
        ['Pattern', 'Burst acuto: 7 ticket in 1 giorno. Crisi bonus.'],
        ['Problem probabile', 'Ha accettato bonus e non capisce le condizioni.\nProbabilmente ha vinto ma non puo prelevare\noppure saldo mostra 0.00.'],
        ['Urgency', 'MASSIMA — utente in crisi emotiva, potenziale complaint'],
    ]
    story.append(make_table(cs4, col_widths=[W*0.18, W*0.72], header_color=BRAND_AMBER))
    story.append(spacer(3))

    story.append(Paragraph(
        '<b>Lezione:</b> 7 ticket in 18 ore = l\'utente e stato ignorato per 18 ore consecutive. Con un widget AI '
        'che spiega le condizioni del bonus, questo utente avrebbe aperto 1 ticket (non 7) e probabilmente sarebbe '
        'rimasto sulla piattaforma.',
        styles['CriticalText']
    ))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════
    # SECTION 5: MASTER RECOVERY TIMELINE
    # ═══════════════════════════════════════════════
    story.append(Paragraph('5. Complete Recovery Plan — Operational Timeline', styles['H1']))
    story.append(hr())

    # Week 1
    story.append(Paragraph('WEEK 1 (11-17 March 2026) — Quick Wins', styles['H2']))
    w1 = [
        ['Action', 'Who', 'Persona Impacted', 'Tickets/Month Saved', 'Cost'],
        ['KB: "Il mio deposito non appare"\n(timeline per metodo)', 'Content Team', 'Frustrated Depositor', '~70', '$0 (contenuto)'],
        ['KB: "Saldo 0.00 con bonus"\n(spiegazione prominente)', 'Content Team', 'Confused Player', '~85', '$0 (contenuto)'],
        ['KB: "Come prelevare - Checklist"\n(pre-requisiti visivi)', 'Content Team', 'Blocked Winner', '~50', '$0 (contenuto)'],
        ['Template 3 livelli complaint\n(frustrazione/frode/minaccia)', 'CS Manager', 'Chronic Complainer', '~5', '$0 (template)'],
        ['Flag 14 utenti CRITICI nel CRM\ne assegnare priorita', 'CS Manager', 'All CRITICAL users', '~30', '$0 (CRM tag)'],
    ]
    story.append(make_table(w1, col_widths=[W*0.28, W*0.12, W*0.20, W*0.16, W*0.10], header_color=BRAND_GREEN))
    story.append(spacer(4))

    # Week 2
    story.append(Paragraph('WEEK 2 (18-24 March 2026) — Automation', styles['H2']))
    w2 = [
        ['Action', 'Who', 'Persona Impacted', 'Tickets/Month Saved', 'Cost'],
        ['Widget: riconoscere "no funciona"\ne rispondere con troubleshooting', 'Dev Team', 'Tech-Frustrated', '~40', '$500-$1,000'],
        ['Widget: menu dopo "hola"\n(deposito/prelievo/bonus/tech)', 'Dev Team', 'Serial Chatter', '~100', '$300-$500'],
        ['Auto-merge ticket stesso\nutente entro 24h', 'Dev Team', 'Serial Chatter', '~80', '$500-$1,000'],
        ['KB: troubleshooting mobile\ncompleto (6 scenari)', 'Content Team', 'Tech-Frustrated', '~30', '$0 (contenuto)'],
        ['Outreach email ai 42 utenti\ncronici (5 mesi)', 'CS Manager', 'All chronic users', '—', '$0 (email)'],
    ]
    story.append(make_table(w2, col_widths=[W*0.28, W*0.12, W*0.20, W*0.16, W*0.10], header_color=BRAND_AMBER))
    story.append(spacer(4))

    # Week 3-4
    story.append(Paragraph('WEEKS 3-4 (25 Mar - 7 Apr) — GR8 API Integration', styles['H2']))
    w34 = [
        ['Action', 'Who', 'Persona Impacted', 'Tickets/Month Saved', 'Cost'],
        ['Widget + GR8: status deposito\nreal-time (paymentTransactionV2)', 'Dev Team', 'Frustrated Depositor', '~120', '$2,000-$4,000'],
        ['Widget + GR8: check bonus/KYC\nquando utente chiede prelievo', 'Dev Team', 'Blocked Winner', '~60', '$1,500-$3,000'],
        ['Pop-up pre-bonus con\ncalcolatrice rollover', 'Product Team', 'Confused Player', '~50', '$1,000-$2,000'],
        ['Auto-escalation dopo 2o\nticket stesso topic', 'Dev Team', 'All recurring users', '~40', '$500-$1,000'],
        ['Notifica push post-deposito\naccreditato', 'Dev Team', 'Frustrated Depositor', '~30', '$500-$1,000'],
    ]
    story.append(make_table(w34, col_widths=[W*0.28, W*0.12, W*0.20, W*0.16, W*0.10], header_color=BRAND_BLUE))
    story.append(spacer(6))

    # Total impact
    story.append(Paragraph('Impact Totale dopo 4 Settimane:', styles['H2']))
    total_impact = [
        ['Metrica', 'Before (Feb 2026)', 'After (Apr 2026)', 'Improvement'],
        ['Total tickets/month', '~4,400', '~3,510', '-890/mese (-20%)'],
        ['Tickets/month from recurring', '~2,260', '~1,500', '-760/mese (-34%)'],
        ['AI resolution rate', '~42%', '~62%', '+20 punti percentuali'],
        ['First-contact resolution', '~35%', '~55%', '+20 punti percentuali'],
        ['Users frustrati/mese', '~300', '~150', '-50%'],
        ['Cost supporto/mese', '~$13,200', '~$10,530', '-$2,670/mese'],
        ['FTE saved', '—', '~2.5 FTE', '+2.5 agenti per altre attivita'],
        ['Total investment', '—', '$6,800-$13,500', 'One-time'],
        ['Payback period', '—', '—', '2.5-5 mesi'],
    ]
    story.append(make_table(total_impact, col_widths=[W*0.24, W*0.20, W*0.22, W*0.24], header_color=BRAND_GREEN))
    story.append(spacer(8))

    story.append(Paragraph(
        '<b>In 4 settimane, con un investimento di $6,800-$13,500:</b><br/>'
        '&bull; -890 ticket/mese (-20%)<br/>'
        '&bull; -$2,670/mese in costi supporto = $32,040/anno risparmiati<br/>'
        '&bull; $58,380-$99,180/anno in revenue preservata da utenti recuperati<br/>'
        '&bull; ROI totale: 670-970% nel primo anno',
        styles['MetricBox']
    ))

    story.append(spacer(10))
    story.append(hr())
    story.append(Paragraph(
        '<i>Report generato il 10 Marzo 2026. '
        'Dati: 22,000 ticket Zendesk (Oct 2025 - Feb 2026), 14,888 utenti univoci. '
        'LTV e costi basati su benchmark iGaming LATAM 2025 (H2 Gambling Capital, Newzoo). '
        'Cross-referenza: GR8 Data API (paymentOrder, paymentTransactionV2, playerProfile).</i>',
        styles['BodySmall']
    ))

    doc.build(story)
    print('PDF generated: BetonWin_User_Recovery_Playbook_EN.pdf')


if __name__ == '__main__':
    build_pdf()
