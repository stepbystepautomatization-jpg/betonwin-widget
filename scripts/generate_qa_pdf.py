#!/usr/bin/env python3
"""Generate BetonWin Widget QA Checklist PDF"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus.flowables import KeepTogether
import os

OUTPUT = os.path.join(os.path.dirname(__file__), 'QA_Checklist_BetonWin_Widget.pdf')

# Brand colors
TEAL = HexColor('#03242D')
GREEN = HexColor('#45cd98')
GREEN_LIGHT = HexColor('#e8f7f0')
GOLD = HexColor('#ffc572')
DARK = HexColor('#1a1a2e')
GRAY = HexColor('#666666')
LIGHT_BG = HexColor('#f8f9fa')
RED = HexColor('#e74c3c')
ORANGE = HexColor('#f39c12')

styles = getSampleStyleSheet()

# Custom styles
styles.add(ParagraphStyle(name='DocTitle', fontName='Helvetica-Bold', fontSize=22, textColor=TEAL, spaceAfter=4*mm, alignment=TA_CENTER))
styles.add(ParagraphStyle(name='DocSubtitle', fontName='Helvetica', fontSize=11, textColor=GRAY, spaceAfter=8*mm, alignment=TA_CENTER))
styles.add(ParagraphStyle(name='SectionTitle', fontName='Helvetica-Bold', fontSize=14, textColor=TEAL, spaceBefore=8*mm, spaceAfter=4*mm))
styles.add(ParagraphStyle(name='SubSection', fontName='Helvetica-Bold', fontSize=11, textColor=HexColor('#2c3e50'), spaceBefore=5*mm, spaceAfter=2*mm))
styles.add(ParagraphStyle(name='Body', fontName='Helvetica', fontSize=9.5, textColor=HexColor('#333333'), spaceAfter=2*mm, leading=13))
styles.add(ParagraphStyle(name='BulletItem', fontName='Helvetica', fontSize=9.5, textColor=HexColor('#333333'), leftIndent=12*mm, bulletIndent=6*mm, spaceAfter=1.5*mm, leading=13))
styles.add(ParagraphStyle(name='CheckItem', fontName='Helvetica', fontSize=9.5, textColor=HexColor('#333333'), leftIndent=14*mm, bulletIndent=6*mm, spaceAfter=2*mm, leading=13))
styles.add(ParagraphStyle(name='Note', fontName='Helvetica-Oblique', fontSize=9, textColor=GRAY, leftIndent=6*mm, spaceAfter=2*mm, leading=12))
styles.add(ParagraphStyle(name='StatusPending', fontName='Helvetica-Bold', fontSize=9, textColor=ORANGE))
styles.add(ParagraphStyle(name='Footer', fontName='Helvetica', fontSize=8, textColor=GRAY, alignment=TA_CENTER))

def checkbox(text, status=''):
    """Create a checkbox item: ☐ text"""
    s = status
    prefix = '☐'
    return Paragraph(f'{prefix}  {text}  <font color="#999999">{s}</font>', styles['CheckItem'])

def section(title):
    return Paragraph(title, styles['SectionTitle'])

def sub(title):
    return Paragraph(title, styles['SubSection'])

def body(text):
    return Paragraph(text, styles['Body'])

def note(text):
    return Paragraph(f'<i>Note: {text}</i>', styles['Note'])

def bullet(text):
    return Paragraph(f'•  {text}', styles['BulletItem'])

def hr():
    return HRFlowable(width='100%', thickness=0.5, color=HexColor('#e0e0e0'), spaceAfter=3*mm, spaceBefore=3*mm)

def build():
    doc = SimpleDocTemplate(OUTPUT, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=20*mm, bottomMargin=20*mm)
    story = []

    # ==================== COVER ====================
    story.append(Spacer(1, 30*mm))
    story.append(Paragraph('BetonWin AI Support Widget', styles['DocTitle']))
    story.append(Paragraph('QA Checklist & Verification Document', styles['DocSubtitle']))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph('Version 1.0  —  March 2026', styles['Footer']))
    story.append(Paragraph('Prepared for QA Team', styles['Footer']))
    story.append(Spacer(1, 10*mm))
    story.append(hr())
    story.append(Spacer(1, 5*mm))

    # Summary table
    summary_data = [
        ['Component', 'Details'],
        ['File', 'widget.js (~2000 lines, single embeddable file)'],
        ['Deployment', 'GitHub → jsDelivr CDN'],
        ['Backend', 'n8n webhooks (https://n8nbeton.online)'],
        ['KB', 'Google Apps Script (FAQ search)'],
        ['Ticketing', 'Zendesk (escalation + live agent)'],
        ['Storage', 'S3 (file uploads via presigned URLs)'],
        ['Languages', 'EN, ES, IT, PT (auto-detect + manual switch)'],
        ['Target Site', 'https://beton.win'],
    ]
    t = Table(summary_data, colWidths=[40*mm, 120*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(PageBreak())

    # ==================== 1. VISUAL / UI DESIGN ====================
    story.append(section('1. Visual & UI Design Verification'))
    story.append(body('Verify the widget\'s visual appearance, animations, and design consistency across all states.'))

    story.append(sub('1.1 Splash Screen'))
    story.append(checkbox('Logo (BET ON WIN, 160px PNG) appears with coin-spin animation'))
    story.append(checkbox('Logo is NOT cropped — full circle visible, no dark border'))
    story.append(checkbox('Typewriter text "BetonWin AI Support" types character by character'))
    story.append(checkbox('Second line "24/7 Siempre disponible" types after first line'))
    story.append(checkbox('Cursor blinks green during typing'))
    story.append(checkbox('Splash fades out after ~2.2s — transition is smooth'))
    story.append(checkbox('Splash only plays on FIRST open — reopening widget skips splash'))
    story.append(checkbox('Chat is NOT visible behind splash (solid background)'))

    story.append(sub('1.2 FAB Trigger Button'))
    story.append(checkbox('Shows BET ON WIN logo (36px circle) + "Here to help" label'))
    story.append(checkbox('Pill shape with dark teal background + green border'))
    story.append(checkbox('Float animation (3s, subtle 4px vertical movement)'))
    story.append(checkbox('Hover: lift -2px, glow intensifies'))
    story.append(checkbox('Busy state: green pulse glow when bot is processing'))
    story.append(checkbox('Disappears (scale to 0) when widget is open'))

    story.append(sub('1.3 Header'))
    story.append(checkbox('Avatar: 40px circle with BET ON WIN logo, green ring animation'))
    story.append(checkbox('Avatar hover: vibration buzz (0.2s)'))
    story.append(checkbox('Bot name: "BetonWin AI" — correct font weight and size'))
    story.append(checkbox('Status dot: green, pulsing animation'))
    story.append(checkbox('Status text: "Online" / "En línea" etc. — matches current language'))
    story.append(checkbox('Fullscreen button: works, icon switches between expand/collapse'))
    story.append(checkbox('Close (X) button: opens exit overlay (does NOT close directly)'))
    story.append(checkbox('Green glow line at bottom of header'))

    story.append(sub('1.4 Message Bubbles'))
    story.append(checkbox('Bot bubble: subtle dark bg rgba(255,255,255,0.04), visible on #03242D'))
    story.append(checkbox('User bubble: dark bg with green text, green border, green right accent'))
    story.append(checkbox('Agent (human) bubble: dark card + gold top border, distinct from bot'))
    story.append(checkbox('Font size 13px, line-height 1.55 — readable and compact'))
    story.append(checkbox('Bold text: green in bot bubbles, white in user'))
    story.append(checkbox('Bullet lists: green dots (4px) aligned properly'))
    story.append(checkbox('Numbered lists: green numbers aligned'))
    story.append(checkbox('Links: green with subtle underline'))
    story.append(checkbox('Long text wraps correctly — NO overflow outside bubble'))
    story.append(checkbox('Long URLs break properly — no horizontal scroll'))
    story.append(checkbox('Spring bounce animation on new messages'))
    story.append(checkbox('Bot avatar (22px circle) hidden — concierge style'))
    story.append(note('Test with very long messages, URLs, and mixed languages'))

    story.append(sub('1.5 Input Area'))
    story.append(checkbox('Unified input bar: textarea + toolbar in one rounded container'))
    story.append(checkbox('Toolbar buttons: 😊 Emoji, 📎 Attach, 🌐 Language, ▶ Send'))
    story.append(checkbox('Send button: 34px green circle, paper plane icon'))
    story.append(checkbox('Emoji picker opens above input, 8-column grid'))
    story.append(checkbox('Attach button: opens file picker'))
    story.append(checkbox('Language button: opens popup with 4 flags (🇪🇸 🇬🇧 🇮🇹 🇧🇷)'))
    story.append(checkbox('Input focus: border turns green'))
    story.append(checkbox('Textarea auto-grows with content (max 100px height)'))
    story.append(checkbox('Keyboard hides on mobile after send'))

    story.append(sub('1.6 Exit Overlay'))
    story.append(checkbox('3 circular buttons in a row: 💬 New chat, ⭐ Rate, 👋 Exit'))
    story.append(checkbox('Title: "¡Hasta pronto! 👋" — 20px, bold, white'))
    story.append(checkbox('New chat circle: green orbit animation on border'))
    story.append(checkbox('Rate circle: gold shimmer effect'))
    story.append(checkbox('Exit circle: muted, neutral'))
    story.append(checkbox('Labels change with language switch'))
    story.append(checkbox('Click Rate → stars appear (5 gold stars, 34px)'))
    story.append(checkbox('Star hover: scale 1.25'))
    story.append(checkbox('Star click: locks rating, sends to Zendesk if ticket exists'))
    story.append(checkbox('"Thanks" message appears, widget closes after 1.2s'))
    story.append(checkbox('Click outside overlay → returns to chat'))

    story.append(sub('1.7 Logo Watermark Background'))
    story.append(checkbox('Logo visible at 4% opacity behind messages'))
    story.append(checkbox('Grayscale + brightness filter — not distracting'))
    story.append(checkbox('Fades out (1.2s transition) when first message is sent'))
    story.append(checkbox('Reappears on "New chat" reset'))

    story.append(PageBreak())

    # ==================== 2. FUNCTIONAL ====================
    story.append(section('2. Functional Verification'))
    story.append(body('Verify all widget features work correctly end-to-end.'))

    story.append(sub('2.1 Chat Flow'))
    story.append(checkbox('Send message → typing indicator appears'))
    story.append(checkbox('Typing indicator: 3 green bars waving + "BetonWin AI Thinking..."'))
    story.append(checkbox('FAB shows busy state (pulse) while bot is typing'))
    story.append(checkbox('Bot responds within 18s timeout'))
    story.append(checkbox('If timeout → shows error message, input re-enabled'))
    story.append(checkbox('Safety timer: if stuck for 30s, auto-recovers input'))
    story.append(checkbox('Rate limit: can\'t send more than 1 msg/second'))
    story.append(checkbox('Max message length: 1000 characters'))
    story.append(checkbox('KB search: queries Google Apps Script (3.5s timeout)'))
    story.append(checkbox('KB results passed to AI as context'))
    story.append(checkbox('Conversation history: last 12 messages sent to AI'))
    story.append(checkbox('Enter key sends message, Shift+Enter adds new line'))
    story.append(checkbox('Emoji picker inserts emoji at cursor position'))
    story.append(checkbox('Proactive message appears after 30s if user hasn\'t interacted'))

    story.append(sub('2.2 Language System'))
    story.append(checkbox('Default language: Spanish (ES)'))
    story.append(checkbox('Auto-detect from text: "ciao" → Italian, "hello" → English'))
    story.append(checkbox('Short messages (<30 chars): 1 keyword match is enough'))
    story.append(checkbox('Long messages: require 2+ keyword matches'))
    story.append(checkbox('Manual switch via 🌐 popup: ES, EN, IT, PT'))
    story.append(checkbox('All UI updates on language change: placeholder, buttons, exit labels'))
    story.append(checkbox('AI receives language instruction: "[Reply ONLY in Italian] ..."'))
    story.append(checkbox('AI response <!--lang:XX--> tag does NOT override user\'s choice'))
    story.append(checkbox('Rejection retry: if AI refuses language, retries in Spanish'))
    story.append(note('Test: write "ciao", then "hello", then "hola" — language should switch each time'))

    story.append(sub('2.3 Escalation to Live Agent'))
    story.append(checkbox('Legal threat keywords → immediate escalation (no AI call)'))
    story.append(checkbox('Human request detected 3x → auto escalation'))
    story.append(checkbox('Escalation sends: reason, language, history, player_id, name, email'))
    story.append(checkbox('Zendesk ticket created → ticket ID shown'))
    story.append(checkbox('Header changes: "Live Agent" + orange status dot'))
    story.append(checkbox('User can type messages → sent to Zendesk as comments'))
    story.append(checkbox('User can send files → uploaded to S3, URL sent to agent'))
    story.append(checkbox('Agent replies appear in real-time (polling)'))
    story.append(checkbox('Agent name shown in header + message bubbles'))
    story.append(checkbox('Ticket "closed" OR "solved" → stops polling, shows CSAT'))
    story.append(checkbox('If escalation fails → shows email fallback (ayuda@beton.win)'))

    story.append(sub('2.4 Agent Polling (Technical)'))
    story.append(checkbox('Uses `since` parameter (not always 0) — fetches only new comments'))
    story.append(checkbox('Dedup via object keys (O(1) lookup)'))
    story.append(checkbox('Backoff: starts at 5s, increases to max 20s after 6 idle polls'))
    story.append(checkbox('Resets to 5s when new comment arrives'))
    story.append(checkbox('Max 360 polls (30 min) before timeout'))
    story.append(checkbox('Timeout message shown (not silent failure)'))

    story.append(sub('2.5 File Upload'))
    story.append(checkbox('Accepted types: JPG, PNG, WebP, PDF'))
    story.append(checkbox('Max file size: 10MB — error message if exceeded'))
    story.append(checkbox('Wrong file type → error message'))
    story.append(checkbox('Upload flow: presigned URL → S3 PUT → analyze'))
    story.append(checkbox('Progress bar updates during upload'))
    story.append(checkbox('Upload retry: 3 attempts with backoff (2s, 4s, 6s)'))
    story.append(checkbox('If all retries fail → returns to upload form, user can retry'))
    story.append(checkbox('S3 upload timeout: 60s'))

    story.append(sub('2.6 Deposit Verification Flow'))
    story.append(body('<font color="#f39c12"><b>⚠ PENDING — Awaiting deposit endpoint specifications</b></font>'))
    story.append(checkbox('Player ID form: alphanumeric + dash/underscore, max 50 chars'))
    story.append(checkbox('VERIFY endpoint returns correct status'))
    story.append(checkbox('PROCESSING → back to chat with message'))
    story.append(checkbox('NEED_UPLOAD → upload form shown'))
    story.append(checkbox('PENDING → starts polling'))
    story.append(checkbox('Polling: 3s interval, max 80 polls (4 min)'))
    story.append(checkbox('Feedback at poll 10 (30s): "Still analyzing..."'))
    story.append(checkbox('Feedback at poll 30 (90s): "Almost done..."'))
    story.append(checkbox('If polling timeout → auto-escalation to human agent'))
    story.append(checkbox('Final results: APPROVED / REJECTED / PENDING_REVIEW'))
    story.append(note('Full deposit flow testing blocked until backend endpoints are confirmed'))

    story.append(PageBreak())

    # ==================== 3. RESPONSIVE / MOBILE ====================
    story.append(section('3. Responsive & Mobile Verification'))

    story.append(sub('3.1 Desktop (1440px+)'))
    story.append(checkbox('Widget: 400px wide, 620px tall, positioned bottom-right'))
    story.append(checkbox('FAB: bottom 24px, right 24px'))
    story.append(checkbox('All animations smooth (60fps)'))
    story.append(checkbox('Fullscreen mode works correctly'))

    story.append(sub('3.2 Tablet (768px)'))
    story.append(checkbox('Widget renders correctly'))
    story.append(checkbox('Touch targets: all buttons ≥ 44x44px'))
    story.append(checkbox('Emoji picker: 8-column grid'))

    story.append(sub('3.3 Mobile (375px — iPhone SE)'))
    story.append(checkbox('FAB: bottom 80px (above nav bar), right 16px'))
    story.append(checkbox('Widget: nearly fullscreen (100dvh - 16px)'))
    story.append(checkbox('Border-radius 18px on widget window'))
    story.append(checkbox('Text readable without zooming'))
    story.append(checkbox('Input area: keyboard doesn\'t cover messages'))
    story.append(checkbox('Keyboard hides after sending message'))
    story.append(checkbox('Emoji picker: 7-column grid'))
    story.append(checkbox('Exit overlay circles: touch-friendly'))
    story.append(checkbox('Splash screen: logo scales correctly'))
    story.append(checkbox('Avatar hover expand disabled on mobile'))

    story.append(sub('3.4 Network Conditions'))
    story.append(checkbox('3G (slow): widget loads, splash plays, chat works'))
    story.append(checkbox('3G: KB search likely times out (3.5s) — AI still responds'))
    story.append(checkbox('4G: all features work within timeouts'))
    story.append(checkbox('Offline → Online: widget recovers gracefully'))
    story.append(checkbox('Slow connection: upload progress bar updates correctly'))
    story.append(checkbox('Network drop during upload → retry mechanism activates'))
    story.append(note('Use Chrome DevTools Network throttling to simulate 3G/4G'))

    story.append(PageBreak())

    # ==================== 4. SECURITY ====================
    story.append(section('4. Security Verification'))

    story.append(sub('4.1 Input Sanitization'))
    story.append(checkbox('HTML escaping: script tags escaped in messages'))
    story.append(checkbox('XSS test: send img/script injection attempts — must be escaped'))
    story.append(checkbox('Link sanitization: URLs quoted properly in href attributes'))
    story.append(checkbox('Player ID sanitization: only alphanumeric + dash/underscore'))
    story.append(checkbox('Job ID sanitization: only alphanumeric + dash/underscore'))
    story.append(checkbox('Message length cap: 1000 characters enforced'))

    story.append(sub('4.2 API Security'))
    story.append(checkbox('No API keys exposed in client-side code'))
    story.append(checkbox('n8n endpoints use webhook URLs (not API key auth)'))
    story.append(checkbox('S3 presigned URLs: time-limited, single-use'))
    story.append(checkbox('File type validation: server-side + client-side'))
    story.append(checkbox('Session ID: UUID v4, unique per widget instance'))
    story.append(checkbox('No sensitive data stored in localStorage'))

    story.append(sub('4.3 Content Security'))
    story.append(checkbox('Widget runs in IIFE — no global variable pollution'))
    story.append(checkbox('Links open with rel="noopener" — prevents tab hijacking'))
    story.append(checkbox('No eval() or innerHTML with unsanitized input'))
    story.append(checkbox('Markdown parser: only safe HTML tags (strong, em, a, hr, span)'))

    story.append(PageBreak())

    # ==================== 5. PERFORMANCE ====================
    story.append(section('5. Performance Verification'))

    story.append(sub('5.1 Load Performance'))
    story.append(checkbox('Widget JS file size: check gzipped size (target: < 100KB)'))
    story.append(checkbox('Font (Inter): loaded via preload, non-render-blocking'))
    story.append(checkbox('Logo images: base64 embedded (no extra HTTP requests)'))
    story.append(checkbox('No external dependencies (zero third-party libraries)'))
    story.append(checkbox('Widget initializes < 500ms on 4G'))

    story.append(sub('5.2 Runtime Performance'))
    story.append(checkbox('Animations: only transform + opacity (GPU composited)'))
    story.append(checkbox('No memory leaks in agent polling (timeout-based, not interval)'))
    story.append(checkbox('Agent polling backoff: reduces from 12 req/min to 3 req/min when idle'))
    story.append(checkbox('Message history capped at 100 messages'))
    story.append(checkbox('Emoji picker: lazy-loaded on first click'))
    story.append(checkbox('Scroll performance: overscroll-behavior:contain prevents page scroll'))

    story.append(sub('5.3 API Performance'))

    api_data = [
        ['Endpoint', 'Timeout', 'Polling', 'Notes'],
        ['KB Search', '3.5s', 'N/A', 'Falls back to no-context if timeout'],
        ['AI Chat', '18s', 'N/A', 'Safety timer at 30s auto-recovers'],
        ['Verify Deposit', '18s', 'N/A', 'Returns status + job_id'],
        ['Presigned URL', '18s', 'N/A', 'Returns S3 upload URL'],
        ['S3 Upload', '60s', 'N/A', '3 retries with backoff'],
        ['Analyze', '18s', 'N/A', 'Starts polling if job_id returned'],
        ['Status Poll', '3s/call', '3s × 80 = 4min', 'Escalates on timeout'],
        ['Agent Poll', '5-20s', '5s → 20s backoff', 'since-based, 30min max'],
        ['Agent Reply', '18s', 'N/A', 'Sends user message to Zendesk'],
        ['Escalate', '18s', 'N/A', 'Creates Zendesk ticket'],
    ]
    t = Table(api_data, colWidths=[35*mm, 20*mm, 35*mm, 70*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t)

    story.append(PageBreak())

    # ==================== 6. BROWSER COMPAT ====================
    story.append(section('6. Browser Compatibility'))

    browsers = [
        ['Browser', 'Desktop', 'Mobile', 'Priority'],
        ['Chrome 90+', '☐ Test', '☐ Test', 'HIGH'],
        ['Safari 15+', '☐ Test', '☐ Test (iOS)', 'HIGH'],
        ['Firefox 90+', '☐ Test', '☐ Test', 'MEDIUM'],
        ['Edge 90+', '☐ Test', '—', 'MEDIUM'],
        ['Samsung Internet', '—', '☐ Test', 'LOW'],
    ]
    t = Table(browsers, colWidths=[40*mm, 35*mm, 35*mm, 30*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 5*mm))

    story.append(sub('Key Features to Verify per Browser'))
    story.append(checkbox('CSS backdrop-filter (frosted glass) — Safari + Chrome'))
    story.append(checkbox('CSS clip-path — all modern browsers'))
    story.append(checkbox('CSS animation (keyframes) — all browsers'))
    story.append(checkbox('Fetch API — all modern browsers'))
    story.append(checkbox('TextArea auto-resize — all browsers'))
    story.append(checkbox('File input with capture attribute — mobile only'))
    story.append(checkbox('100dvh unit — check Safari iOS (known quirks)'))

    story.append(PageBreak())

    # ==================== 7. ACCESSIBILITY ====================
    story.append(section('7. Accessibility (a11y)'))

    story.append(checkbox('Widget dialog: role="dialog", aria-label="BetonWin Support"'))
    story.append(checkbox('FAB trigger: aria-label="Support Chat"'))
    story.append(checkbox('Send button: aria-label="Send message"'))
    story.append(checkbox('Emoji button: aria-label="Emoji"'))
    story.append(checkbox('Attach button: aria-label="Attach file"'))
    story.append(checkbox('Language button: aria-label="Change language"'))
    story.append(checkbox('Messages area: aria-live="polite", aria-relevant="additions"'))
    story.append(checkbox('Keyboard navigation: Tab cycles through interactive elements'))
    story.append(checkbox('Enter key sends message from textarea'))
    story.append(checkbox('Escape key should close exit overlay'))
    story.append(checkbox('Color contrast: text on dark bg meets WCAG AA (4.5:1)'))
    story.append(checkbox('Green text (#45cd98) on #03242D: contrast ratio ≥ 4.5:1'))

    story.append(PageBreak())

    # ==================== 8. INTEGRATION ====================
    story.append(section('8. Integration Verification'))

    story.append(sub('8.1 Embed on Target Site'))
    story.append(checkbox('Widget loads correctly on https://beton.win'))
    story.append(checkbox('No CSS conflicts with site styles'))
    story.append(checkbox('z-index 2147483647: widget stays on top of all site elements'))
    story.append(checkbox('FAB doesn\'t overlap site navigation on mobile'))
    story.append(checkbox('Widget doesn\'t break site scrolling'))
    story.append(checkbox('Font Inter loads correctly'))

    story.append(sub('8.2 CDN Deployment'))
    story.append(checkbox('Push to GitHub main branch'))
    story.append(checkbox('Purge jsDelivr cache: https://purge.jsdelivr.net/gh/...'))
    story.append(checkbox('Verify CDN serves updated file'))
    story.append(checkbox('Check file size after minification'))

    story.append(sub('8.3 n8n Backend'))
    story.append(checkbox('All 8 webhook endpoints responding'))
    story.append(checkbox('AI agents routing correctly (10 categories)'))
    story.append(checkbox('Zendesk ticket creation working'))
    story.append(checkbox('Agent polling returns comments with authors'))
    story.append(checkbox('KB search returns relevant results'))

    story.append(PageBreak())

    # ==================== 9. NEXT STEPS ====================
    story.append(section('9. Next Steps (Upcoming Verification Rounds)'))
    story.append(body('The following items are planned for future QA rounds after backend specifications are finalized.'))

    story.append(Spacer(1, 3*mm))

    next_data = [
        ['Item', 'Status', 'Dependency'],
        ['Deposit verification (full flow)', 'PENDING', 'Backend endpoint specs'],
        ['Payment proof upload + AI analysis', 'PENDING', 'S3 + Analyze endpoint config'],
        ['Zendesk ticket fields mapping', 'PENDING', 'Zendesk admin config'],
        ['CSAT rating → Zendesk sync', 'PENDING', 'Agent reply endpoint'],
        ['Player ID auto-detection on live site', 'PENDING', 'beton.win DOM structure'],
        ['Push notifications (browser)', 'PLANNED', 'Service worker setup'],
        ['Chat persistence (localStorage)', 'PLANNED', 'Privacy review'],
        ['Analytics / event tracking', 'PLANNED', 'Analytics platform choice'],
        ['Load testing (100+ concurrent users)', 'PLANNED', 'n8n server capacity'],
        ['A/B testing (widget styles)', 'PLANNED', 'Feature flag system'],
    ]
    t = Table(next_data, colWidths=[65*mm, 25*mm, 70*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_BG),
        ('TEXTCOLOR', (1, 1), (1, -1), ORANGE),
        ('FONTNAME', (1, 1), (1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t)

    story.append(Spacer(1, 10*mm))
    story.append(hr())
    story.append(Paragraph('End of QA Checklist — BetonWin AI Support Widget v1.0', styles['Footer']))
    story.append(Paragraph('Document generated March 31, 2026', styles['Footer']))

    doc.build(story)
    print(f'PDF generated: {OUTPUT}')

if __name__ == '__main__':
    build()
