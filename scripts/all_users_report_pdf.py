#!/usr/bin/env python3
"""
BetonWin — Complete User Registry & Analysis (PDF)
All 14,888 users with IDs, ticket counts, topics, and recovery actions.
English version.
"""

import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

# Load data
with open('/Users/serhiykorenyev/Desktop/vs code/widget cs /Analisi /all_users_detail.json') as f:
    DATA = json.load(f)

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

styles = getSampleStyleSheet()
styles.add(ParagraphStyle('Title2', parent=styles['Title'], fontSize=22, textColor=BRAND_DARK, spaceAfter=6))
styles.add(ParagraphStyle('H1', parent=styles['Heading1'], fontSize=16, textColor=BRAND_DARK, spaceBefore=14, spaceAfter=6))
styles.add(ParagraphStyle('H2', parent=styles['Heading2'], fontSize=13, textColor=BRAND_BLUE, spaceBefore=10, spaceAfter=4))
styles.add(ParagraphStyle('H3', parent=styles['Heading3'], fontSize=11, textColor=BRAND_DARK, spaceBefore=8, spaceAfter=3))
styles.add(ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, leading=12, textColor=BRAND_DARK, alignment=TA_JUSTIFY))
styles.add(ParagraphStyle('BodySmall', parent=styles['Normal'], fontSize=8, leading=10, textColor=BRAND_GRAY))
styles.add(ParagraphStyle('BulletItem', parent=styles['Normal'], fontSize=9, leading=12, leftIndent=18, bulletIndent=6))
styles.add(ParagraphStyle('CriticalText', parent=styles['Normal'], fontSize=9, leading=12, textColor=BRAND_RED, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('GreenText', parent=styles['Normal'], fontSize=9, leading=12, textColor=BRAND_GREEN, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('MetricBox', parent=styles['Normal'], fontSize=9, leading=12, textColor=BRAND_DARK,
                           leftIndent=10, rightIndent=10, backColor=LIGHT_GREEN, borderPadding=6))
styles.add(ParagraphStyle('AlertBox', parent=styles['Normal'], fontSize=9, leading=12, textColor=BRAND_DARK,
                           leftIndent=10, rightIndent=10, backColor=LIGHT_RED, borderPadding=6))
styles.add(ParagraphStyle('InfoBox', parent=styles['Normal'], fontSize=9, leading=12, textColor=BRAND_DARK,
                           leftIndent=10, rightIndent=10, backColor=LIGHT_BLUE, borderPadding=6))
styles.add(ParagraphStyle('TinyText', parent=styles['Normal'], fontSize=6.5, leading=8.5, textColor=BRAND_DARK))

def hr():
    return HRFlowable(width='100%', thickness=0.5, color=BRAND_GRAY, spaceBefore=6, spaceAfter=6)

def spacer(h=4):
    return Spacer(1, h*mm)

def make_table(data, col_widths=None, header_color=BRAND_DARK, font_size=7.5):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ('BACKGROUND', (0,0), (-1,0), header_color),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 7.5),
        ('FONTSIZE', (0,1), (-1,-1), font_size),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#d1d5db')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT_GRAY]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]
    t.setStyle(TableStyle(style))
    return t

def make_small_table(data, col_widths=None, header_color=BRAND_DARK):
    return make_table(data, col_widths, header_color, font_size=6.5)


def build_pdf():
    doc = SimpleDocTemplate(
        '/Users/serhiykorenyev/Desktop/vs code/widget cs /Analisi /BetonWin_All_Users_Registry.pdf',
        pagesize=A4,
        topMargin=1.2*cm, bottomMargin=1.2*cm,
        leftMargin=1.2*cm, rightMargin=1.2*cm,
    )
    story = []
    W = A4[0] - 2.4*cm

    meta = DATA['meta']
    users_6plus = DATA['users_6plus']
    users_3to5 = DATA['users_3to5']
    users_2 = DATA['users_2tickets']
    single_by_topic = DATA['users_1ticket_by_topic']
    frustration = DATA['same_topic_frustration']

    # ═══════════════════════════════════════════════
    # COVER
    # ═══════════════════════════════════════════════
    story.append(Spacer(1, 25*mm))
    story.append(Paragraph('BetonWin — Complete User Registry', styles['Title2']))
    story.append(Paragraph('14,888 Users | Full ID Mapping | Ticket Analysis', styles['H1']))
    story.append(hr())
    story.append(Paragraph(f'Total Tickets: {meta["total_tickets"]:,} | Period: {meta["period"]}', styles['Body']))
    story.append(Paragraph('Source: Zendesk API — all tickets with requester_id extraction', styles['Body']))
    story.append(Paragraph('Generated: 10 March 2026', styles['Body']))
    story.append(Spacer(1, 12*mm))

    cover_data = [
        ['Segment', 'Users', '% of Total', 'Tickets Generated', 'Avg Tickets/User', 'Risk Level'],
        ['20+ tickets', str(DATA['user_buckets']['20_plus']), '<0.01%',
         str(sum(u['ticket_count'] for u in users_6plus if u['ticket_count'] > 20)), '37.0', 'CRITICAL'],
        ['11-20 tickets', str(DATA['user_buckets']['11_to_20']), '0.09%',
         str(sum(u['ticket_count'] for u in users_6plus if 11 <= u['ticket_count'] <= 20)), '~12.5', 'CRITICAL'],
        ['6-10 tickets', str(DATA['user_buckets']['6_to_10']), '0.91%',
         str(sum(u['ticket_count'] for u in users_6plus if 6 <= u['ticket_count'] <= 10)), '~7.5', 'HIGH'],
        ['3-5 tickets', str(DATA['user_buckets']['3_to_5']), '9.44%', '~4,920', '~3.5', 'MODERATE'],
        ['2 tickets', str(DATA['user_buckets']['2_tickets']), '17.87%', '5,320', '2.0', 'LOW'],
        ['1 ticket', str(DATA['user_buckets']['1_ticket']), '71.69%',
         str(DATA['user_buckets']['1_ticket']), '1.0', 'MINIMAL'],
        ['TOTAL', f'{meta["total_unique_users"]:,}', '100%', f'{meta["total_tickets"]:,}', '1.48', '—'],
    ]
    story.append(make_table(cover_data, col_widths=[W*0.14, W*0.10, W*0.10, W*0.16, W*0.14, W*0.12]))
    story.append(spacer(6))

    story.append(Paragraph(
        '<b>Key insight:</b> 28.3% of users (4,215 recurring) generate 51.5% of all tickets. '
        'The top 149 users (1%) alone generate 5.6% of total volume. These are the primary targets for recovery.',
        styles['MetricBox']
    ))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════
    # SECTION 1: MONTHLY VOLUME & TOPIC BREAKDOWN
    # ═══════════════════════════════════════════════
    story.append(Paragraph('1. Monthly Volume &amp; Topic Distribution', styles['H1']))
    story.append(hr())

    story.append(Paragraph('Monthly Ticket Volume:', styles['H2']))
    vol_data = [['Month'] + list(DATA['monthly_volume'].keys()),
                ['Tickets'] + [f'{v:,}' for v in DATA['monthly_volume'].values()]]
    story.append(make_table(vol_data, col_widths=[W*0.12] + [(W-W*0.12)/len(DATA['monthly_volume'])]*len(DATA['monthly_volume']),
                           header_color=BRAND_GREEN))
    story.append(spacer(6))

    story.append(Paragraph('Overall Topic Distribution:', styles['H2']))
    topic_data = [['#', 'Topic', 'Tickets', '% of Total']]
    total_t = meta['total_tickets']
    for i, (topic, cnt) in enumerate(DATA['topic_totals'].items(), 1):
        topic_data.append([str(i), topic, f'{cnt:,}', f'{cnt/total_t*100:.1f}%'])
    story.append(make_table(topic_data, col_widths=[W*0.04, W*0.36, W*0.12, W*0.10]))
    story.append(spacer(6))

    # Monthly by topic
    story.append(Paragraph('Monthly Topic Breakdown:', styles['H2']))
    months = sorted(DATA['monthly_topic'].keys())
    mt_header = ['Topic'] + [m[2:] for m in months]  # '25-10' etc
    mt_data = [mt_header]
    for topic in list(DATA['topic_totals'].keys())[:12]:  # top 12 topics
        row = [topic[:30]]
        for m in months:
            row.append(str(DATA['monthly_topic'].get(m, {}).get(topic, 0)))
        mt_data.append(row)
    cw = (W - W*0.28) / len(months)
    story.append(make_table(mt_data, col_widths=[W*0.28] + [cw]*len(months)))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════
    # SECTION 2: CRITICAL USERS (11+ TICKETS)
    # ═══════════════════════════════════════════════
    critical_users = [u for u in users_6plus if u['ticket_count'] >= 11]
    story.append(Paragraph(f'2. CRITICAL Users — 11+ Tickets ({len(critical_users)} users)', styles['H1']))
    story.append(hr())
    story.append(Paragraph(
        'These users have opened 11 or more tickets in 5 months. Each one represents a severe service failure '
        'and immediate churn risk. Every user is listed with full details.',
        styles['AlertBox']
    ))
    story.append(spacer(4))

    for i, u in enumerate(critical_users, 1):
        topics_str = ', '.join(f'{t}: {c}' for t, c in u['all_topics'].items())
        months_str = ', '.join(u['months_active'])
        subjects = u.get('sample_subjects', [])
        subj_str = ' | '.join(s[:60] for s in subjects[:3]) if subjects else '(no subject captured)'

        story.append(Paragraph(f'#{i} — User ID: {u["user_id"]}', styles['H3']))
        user_detail = [
            ['Field', 'Value'],
            ['User ID', str(u['user_id'])],
            ['Total Tickets', str(u['ticket_count'])],
            ['Months Active', f'{u["month_span"]} months ({months_str})'],
            ['First Ticket', u['first_ticket']],
            ['Last Ticket', u['last_ticket']],
            ['Topics', topics_str],
            ['Sample Subjects', subj_str],
            ['Risk Level', 'CRITICAL' if u['ticket_count'] >= 20 else 'HIGH'],
            ['Recommended Action', 'Dedicated account manager + proactive outreach' if u['ticket_count'] >= 20
             else 'Priority flag in CRM + senior agent assignment'],
        ]
        story.append(make_table(user_detail, col_widths=[W*0.20, W*0.70], header_color=BRAND_RED))
        story.append(spacer(4))

    story.append(Paragraph(
        f'<b>Action Required:</b> All {len(critical_users)} users above must be flagged in the CRM immediately. '
        f'For users with 20+ tickets, assign a dedicated account manager. For 11-20 ticket users, '
        f'route all future tickets to senior agents with full conversation history.',
        styles['CriticalText']
    ))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════
    # SECTION 3: HIGH-RISK USERS (6-10 TICKETS)
    # ═══════════════════════════════════════════════
    high_users = [u for u in users_6plus if 6 <= u['ticket_count'] <= 10]
    story.append(Paragraph(f'3. HIGH-Risk Users — 6-10 Tickets ({len(high_users)} users)', styles['H1']))
    story.append(hr())
    story.append(Paragraph(
        f'These {len(high_users)} users have opened 6-10 tickets each. They are actively frustrated but still '
        'engaging with the platform — making them the highest-ROI recovery targets.',
        styles['Body']
    ))
    story.append(spacer(4))

    # Full table of all 6-10 ticket users
    high_data = [['#', 'User ID', 'Tickets', 'Months', 'Primary Topic', 'Other Topics', 'First', 'Last']]
    for i, u in enumerate(high_users, 1):
        topics = u['all_topics']
        primary = list(topics.keys())[0] if topics else '—'
        others = ', '.join(f'{t}:{c}' for t, c in list(topics.items())[1:3]) if len(topics) > 1 else '—'
        high_data.append([
            str(i),
            str(u['user_id']),
            str(u['ticket_count']),
            str(u['month_span']),
            primary[:25],
            others[:35],
            u['first_ticket'][:10],
            u['last_ticket'][:10],
        ])

    # Split into pages of ~40 rows
    page_size = 38
    for start in range(0, len(high_data)-1, page_size):
        chunk = [high_data[0]] + high_data[1+start:1+start+page_size]
        story.append(make_small_table(chunk,
            col_widths=[W*0.04, W*0.16, W*0.06, W*0.06, W*0.20, W*0.22, W*0.10, W*0.10]))
        if start + page_size < len(high_data)-1:
            story.append(PageBreak())

    story.append(spacer(4))
    story.append(Paragraph(
        f'<b>Recovery strategy for all {len(high_users)} users:</b> Auto-escalation after 2nd ticket on same topic. '
        f'Widget should detect returning user and greet with: "Welcome back! I see you contacted us before about [TOPIC]. '
        f'Let me connect you with a senior agent who has your full history."',
        styles['GreenText']
    ))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════
    # SECTION 4: SAME-TOPIC FRUSTRATION WITH USER IDS
    # ═══════════════════════════════════════════════
    story.append(Paragraph('4. Same-Topic Frustration — Users Opening 2+ Tickets on Same Issue', styles['H1']))
    story.append(hr())
    story.append(Paragraph(
        'These users opened multiple tickets about the SAME problem — the clearest signal that '
        'the issue was NOT resolved on first contact. Listed by topic with user IDs.',
        styles['Body']
    ))
    story.append(spacer(6))

    for topic, info in frustration.items():
        user_count = info['user_count']
        total_tix = info['total_tickets']
        users_list = info['users']

        story.append(Paragraph(
            f'{topic} — {user_count} frustrated users, {total_tix} tickets',
            styles['H2']
        ))

        # Why they're frustrated + what to do
        reasons = {
            'Greeting Only (no question)': ('Users open chat with "hola" repeatedly because the widget doesn\'t guide them. They don\'t know how to ask their actual question.',
                'Widget should auto-respond with topic menu after greeting. Auto-merge repeat "hola" tickets from same user within 24h.'),
            'Technical / App / Website': ('Recurring mobile/browser issues not resolved on first contact. 72% are mobile problems — the platform needs better mobile optimization.',
                'Add comprehensive mobile troubleshooting to KB. Widget should recognize "no funciona"/"error" and auto-respond with diagnostic steps.'),
            'How to Withdraw': ('Users who WON but can\'t withdraw. 46.5% blocked by bonus rollover. They contact support 2-3 times before giving up.',
                'Widget + GR8 API: auto-check bonus/KYC status when user asks about withdrawal. Show personalized checklist. Biggest churn risk — these are PAYING users.'),
            'Casino / Games / Bets': ('52.5% about winnings not credited. Game errors and "Saldo 0.00" confusion. Requires human investigation for winnings issues.',
                'Add "Saldo 0.00 with active bonus" explanation prominently. Game troubleshooting guide in KB. Escalate winnings disputes to senior agents.'),
            'Bonus / Promotions': ('Rollover confusion, "Saldo 0.00", bonus blocking withdrawals. Users don\'t understand bonus terms.',
                'Pre-bonus popup with rollover calculator in local currency. Prominent "How bonus affects your balance" KB entry. Option to decline bonus.'),
            'KYC / Verification': ('67.5% are phone/email verification issues (not document KYC). Users can\'t verify because of wrong email/phone during registration.',
                'Country-specific ID guide. Step-by-step verification flow in widget. Escalation path for verification stuck >48h.'),
            'Bank Transfer / Comprobante': ('Users sending bank receipts and asking for bank details. Almost ZERO KB content for the #2 volume topic.',
                'URGENT: Create complete bank transfer guide with country-specific details, comprobante requirements, and processing times.'),
            'Deposit Not Credited': ('Users paid but balance not updated. Average 2.8 contacts to resolve. Directly correlated with bank transfer growth.',
                'Integrate GR8 paymentTransactionV2 for real-time deposit status in widget. Add timeline per payment method to KB.'),
            'Balance / Account Info': ('"Saldo 0.00" confusion and account data change requests.',
                'Show total balance (real + bonus) prominently. Add self-service account data change flow.'),
            'Recarga / Top-up': ('"Recarga" is LATAM synonym for deposit — not recognized in KB. Users search "recarga" and find nothing.',
                'Add "recarga" as explicit synonym throughout KB. Map to deposit flow in widget.'),
        }

        reason, action = reasons.get(topic, ('Multiple unresolved contacts.', 'Investigate and create dedicated KB content.'))
        story.append(Paragraph(f'<b>Why they\'re frustrated:</b> {reason}', styles['Body']))
        story.append(Paragraph(f'<b>Recovery action:</b> {action}', styles['GreenText']))
        story.append(spacer(3))

        # User table
        u_data = [['#', 'User ID', 'Tickets\n(this topic)', 'Total\nTickets', 'Months Active']]
        for j, u in enumerate(users_list[:25], 1):
            u_data.append([
                str(j),
                str(u['user_id']),
                str(u['tickets_on_topic']),
                str(u['total_tickets']),
                ', '.join(u['months']),
            ])
        if len(users_list) > 25:
            u_data.append(['...', f'+{len(users_list)-25} more', '—', '—', '—'])

        story.append(make_small_table(u_data,
            col_widths=[W*0.04, W*0.22, W*0.12, W*0.10, W*0.30]))
        story.append(hr())

        # Page break every 2 topics
        if topic in ['How to Withdraw', 'KYC / Verification', 'Deposit Not Credited']:
            story.append(PageBreak())

    story.append(PageBreak())

    # ═══════════════════════════════════════════════
    # SECTION 5: MODERATE RISK (3-5 TICKETS) SUMMARY
    # ═══════════════════════════════════════════════
    story.append(Paragraph(f'5. MODERATE-Risk Users — 3-5 Tickets ({len(users_3to5):,} users)', styles['H1']))
    story.append(hr())
    story.append(Paragraph(
        f'These {len(users_3to5):,} users have opened 3-5 tickets. They are the largest recoverable segment — '
        f'too many to handle individually, but automating their resolution would eliminate ~22% of all support volume.',
        styles['Body']
    ))
    story.append(spacer(4))

    # Group by primary topic
    topic_groups = {}
    for u in users_3to5:
        t = u['primary_topic']
        if t not in topic_groups:
            topic_groups[t] = {'count': 0, 'sample_ids': []}
        topic_groups[t]['count'] += 1
        if len(topic_groups[t]['sample_ids']) < 10:
            topic_groups[t]['sample_ids'].append(u['user_id'])

    topic_groups_sorted = sorted(topic_groups.items(), key=lambda x: -x[1]['count'])

    grp_data = [['Primary Topic', 'Users (3-5 tickets)', '% of Segment', 'Sample User IDs']]
    for topic, info in topic_groups_sorted:
        ids_str = ', '.join(str(uid) for uid in info['sample_ids'][:5])
        if info['count'] > 5:
            ids_str += f' ... +{info["count"]-5} more'
        grp_data.append([
            topic[:30],
            str(info['count']),
            f'{info["count"]/len(users_3to5)*100:.1f}%',
            ids_str,
        ])
    story.append(make_small_table(grp_data, col_widths=[W*0.24, W*0.12, W*0.10, W*0.44]))
    story.append(spacer(6))

    # Full list pages (compact)
    story.append(Paragraph('Complete User List (3-5 Tickets):', styles['H3']))
    story.append(Paragraph(
        'Below is the complete list of all 1,406 users with 3-5 tickets. '
        'Use this for CRM bulk-tagging and targeted outreach campaigns.',
        styles['BodySmall']
    ))
    story.append(spacer(3))

    list_data = [['#', 'User ID', 'Tix', 'Topic', 'Months', 'First Ticket', 'Last Ticket']]
    for i, u in enumerate(users_3to5, 1):
        topics = u['all_topics']
        primary = list(topics.keys())[0][:22] if topics else '—'
        list_data.append([
            str(i),
            str(u['user_id']),
            str(u['ticket_count']),
            primary,
            str(u['month_span']),
            u['first_ticket'][:10],
            u['last_ticket'][:10],
        ])

    page_size = 50
    for start in range(0, len(list_data)-1, page_size):
        chunk = [list_data[0]] + list_data[1+start:1+start+page_size]
        story.append(make_small_table(chunk,
            col_widths=[W*0.04, W*0.18, W*0.04, W*0.22, W*0.06, W*0.12, W*0.12]))
        if start + page_size < len(list_data)-1:
            story.append(PageBreak())

    story.append(PageBreak())

    # ═══════════════════════════════════════════════
    # SECTION 6: LOW RISK (2 TICKETS) SUMMARY
    # ═══════════════════════════════════════════════
    story.append(Paragraph(f'6. LOW-Risk Users — 2 Tickets ({len(users_2):,} users)', styles['H1']))
    story.append(hr())
    story.append(Paragraph(
        f'These {len(users_2):,} users have opened exactly 2 tickets. Most had a single issue that required '
        f'a follow-up. The focus is preventing them from becoming 3+ ticket users through better first-contact resolution.',
        styles['Body']
    ))
    story.append(spacer(4))

    # Group by primary topic
    topic_2 = {}
    for u in users_2:
        t = u['primary_topic']
        if t not in topic_2:
            topic_2[t] = {'count': 0, 'sample_ids': []}
        topic_2[t]['count'] += 1
        if len(topic_2[t]['sample_ids']) < 8:
            topic_2[t]['sample_ids'].append(u['user_id'])

    grp2_data = [['Primary Topic', 'Users', '% of Segment', 'Sample User IDs']]
    for topic, info in sorted(topic_2.items(), key=lambda x: -x[1]['count']):
        ids_str = ', '.join(str(uid) for uid in info['sample_ids'][:4])
        if info['count'] > 4:
            ids_str += f' +{info["count"]-4} more'
        grp2_data.append([topic[:30], str(info['count']), f'{info["count"]/len(users_2)*100:.1f}%', ids_str])
    story.append(make_small_table(grp2_data, col_widths=[W*0.24, W*0.10, W*0.10, W*0.46]))
    story.append(spacer(6))

    # Full list (compact, 6 per line)
    story.append(Paragraph('Complete User ID List (2 Tickets) — for CRM Bulk Import:', styles['H3']))
    # Print in dense format, 4 users per row
    dense_data = [['User ID', 'Topic', 'User ID', 'Topic', 'User ID', 'Topic']]
    row = []
    for u in users_2:
        row.extend([str(u['user_id']), u['primary_topic'][:18]])
        if len(row) == 6:
            dense_data.append(row)
            row = []
    if row:
        while len(row) < 6:
            row.append('')
        dense_data.append(row)

    page_size = 55
    for start in range(0, len(dense_data)-1, page_size):
        chunk = [dense_data[0]] + dense_data[1+start:1+start+page_size]
        cw = W / 6
        story.append(make_small_table(chunk, col_widths=[cw*1.1, cw*0.9]*3))
        if start + page_size < len(dense_data)-1:
            story.append(PageBreak())

    story.append(PageBreak())

    # ═══════════════════════════════════════════════
    # SECTION 7: SINGLE-TICKET USERS SUMMARY
    # ═══════════════════════════════════════════════
    story.append(Paragraph(f'7. Single-Ticket Users — Topic Distribution ({DATA["user_buckets"]["1_ticket"]:,} users)', styles['H1']))
    story.append(hr())
    story.append(Paragraph(
        'These users contacted support once. Most had their issue resolved or abandoned the platform. '
        'The topic distribution reveals which issues are most common for first-time support contacts.',
        styles['Body']
    ))
    story.append(spacer(4))

    single_data = [['Topic', 'Users', '% of Single-Ticket', 'Insight']]
    insights_map = {
        'Uncategorized': 'Chat-based conversations classified as uncategorized (no subject/description match)',
        'Greeting Only (no question)': 'Users who said "hola" and either got help or left',
        'Bank Transfer / Comprobante': 'Sending comprobante — usually resolved in 1 contact',
        'Technical / App / Website': 'One-time tech issue, likely resolved',
        'KYC / Verification': 'One-time verification process',
        'Casino / Games / Bets': 'Game question or issue, resolved',
        'Bonus / Promotions': 'Bonus question, usually answered',
        'How to Withdraw': 'Withdrawal question — monitor for return',
        'Deposit Not Credited': 'Deposit issue — HIGH risk of return if not properly resolved',
        'Balance / Account Info': 'Balance inquiry',
        'Account / Login Issues': 'Login/password issue, resolved',
        'Recarga / Top-up': 'Top-up question',
        'How to Deposit': 'Deposit instructions needed',
        'Complaint / Dissatisfaction': 'ALERT: single complaint = user likely already churned',
    }
    total_single = sum(single_by_topic.values())
    for topic, cnt in single_by_topic.items():
        insight = insights_map.get(topic, '—')
        single_data.append([topic[:30], f'{cnt:,}', f'{cnt/total_single*100:.1f}%', insight[:65]])
    story.append(make_small_table(single_data, col_widths=[W*0.24, W*0.08, W*0.12, W*0.46]))
    story.append(spacer(6))

    story.append(Paragraph(
        '<b>Key finding:</b> 8,788 single-ticket users (82.4%) are "Uncategorized" — these are chat-based '
        'conversations where the subject/description didn\'t match any keyword. To improve classification, '
        'the system needs to analyze chat comments (not just the initial ticket text).',
        styles['InfoBox']
    ))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════
    # SECTION 8: EXECUTIVE SUMMARY & ACTION PLAN
    # ═══════════════════════════════════════════════
    story.append(Paragraph('8. Executive Summary &amp; Recommended Actions', styles['H1']))
    story.append(hr())

    story.append(Paragraph('Key Findings:', styles['H2']))
    findings = [
        f'<b>{meta["total_unique_users"]:,} unique users</b> contacted support over 5 months, generating {meta["total_tickets"]:,} tickets.',
        '<b>28.3% of users are recurring</b> (4,215 users with 2+ tickets) — they generate 51.5% of all ticket volume.',
        f'<b>{len(critical_users)} CRITICAL users</b> (11+ tickets) need immediate intervention — each represents a severe service failure.',
        f'<b>{len(high_users)} HIGH-risk users</b> (6-10 tickets) are the best ROI targets for recovery investment.',
        '<b>Same-topic frustration</b> affects 490+ users across 10 topics — clear signal of first-contact resolution failure.',
        '<b>"How to Withdraw"</b> has the highest churn risk: 40 users averaging 2.7 tickets each, all potentially paying users who can\'t cash out.',
        '<b>"Deposit Not Credited"</b> directly correlates with bank transfer growth — 28 users averaging 2.8 tickets with money "lost".',
        '<b>82.4% of single-ticket users</b> are "Uncategorized" — improving classification requires comment-level analysis.',
    ]
    for f in findings:
        story.append(Paragraph(f'&bull; {f}', styles['BulletItem']))
        story.append(spacer(1))
    story.append(spacer(6))

    story.append(Paragraph('Immediate Actions (This Week):', styles['H2']))
    actions = [
        ['Priority', 'Action', 'Target Users', 'Expected Impact'],
        ['P0', f'Flag all {len(critical_users)} CRITICAL users in CRM', f'{len(critical_users)} users', 'Prevent churn of highest-value users'],
        ['P0', f'Flag all {len(high_users)} HIGH-risk users in CRM', f'{len(high_users)} users', 'Enable proactive support routing'],
        ['P0', 'Create "Why can\'t I withdraw" KB page', '40 frustrated withdrawal users', '-50% withdrawal tickets'],
        ['P0', 'Create "My deposit isn\'t showing" KB page', '28 frustrated deposit users', '-30% deposit-not-credited tickets'],
        ['P1', 'Add "recarga" synonym throughout KB', '7 frustrated + 19 single-ticket', '-80% recarga tickets'],
        ['P1', 'Mobile troubleshooting guide in KB', '50 frustrated tech users', '-35% tech tickets'],
        ['P1', 'Auto-escalation after 2nd same-topic ticket', 'All 490+ frustrated users', '+40% first-contact resolution'],
        ['P2', 'Integrate GR8 API for real-time deposit status', '28 deposit + 31 bank transfer', '-40% deposit tickets'],
        ['P2', 'Widget greeting menu (after "hola")', '194 serial greeters', '-70% empty greeting tickets'],
    ]
    story.append(make_table(actions, col_widths=[W*0.06, W*0.36, W*0.24, W*0.24], header_color=BRAND_GREEN))
    story.append(spacer(6))

    story.append(Paragraph(
        '<b>Estimated total impact:</b> -890 tickets/month (-20%), AI coverage from 42% to 62%, '
        '$58K-$99K/year in preserved revenue from recovered users, 2.5 FTE equivalent saved.',
        styles['MetricBox']
    ))

    story.append(spacer(10))
    story.append(hr())
    story.append(Paragraph(
        f'<i>Report generated 10 March 2026. Data: {meta["total_tickets"]:,} Zendesk tickets ({meta["period"]}). '
        f'{meta["total_unique_users"]:,} unique users tracked via requester_id. '
        f'Cross-reference: GR8 Data API (paymentOrder, paymentTransactionV2, playerProfile). '
        f'All user IDs are Zendesk requester_ids — can be used for CRM lookup and GR8 API player matching.</i>',
        styles['BodySmall']
    ))

    doc.build(story)
    print('PDF generated: BetonWin_All_Users_Registry.pdf')


if __name__ == '__main__':
    build_pdf()
