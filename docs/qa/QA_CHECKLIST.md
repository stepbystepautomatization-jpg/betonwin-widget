# BetonBot Widget — QA Checklist

> Ultimo aggiornamento: Aprile 2026 (post-merge design + trigger)
> Widget: 2454 righe, 161KB — design premium + tutti i trigger (T-01 → T-19)

---

## 1. DESIGN & UX

### 1.1 Visual Consistency
- [x] Widget matches beton.win dark theme (#03242D background)
- [x] Primary green (#45cd98) consistent across all elements
- [x] Gold accent (#ffb64f) for ratings and agent badges
- [x] Font: Inter loads correctly, fallback to system font works
- [x] No visual glitches or overlapping elements
- [x] Widget does not cover important site elements
- [x] Z-index is highest (2147483647) — widget always on top
- [x] Border-radius 22px window, 16px bubbles, 50% avatars
- [x] CSS isolation: user-select none, tap-highlight transparent

### 1.2 FAB (Trigger Button) — Pill Design
- [x] Position: fixed bottom-right (24px from edges)
- [x] Pill shape: 44px height, border-radius 22px
- [x] Logo circolare (LOGO_FULL_B64) + label "Here to help"
- [x] Dark background with subtle green border
- [x] Float animation (bw-float 3s ease-in-out)
- [x] Ring animation (bw-ring 3s)
- [x] Hover: translateY(-2px) with enhanced shadow
- [x] Active: scale(.96) press effect
- [x] Disappears smoothly when chat opens (scale(0) + rotate)
- [x] Busy pulse animation (bw-busy-pulse)

### 1.3 Chat Window
- [x] Size: 400px wide x 620px tall (desktop)
- [x] Opens with bounce scale animation (cubic-bezier .34,1.56,.64,1)
- [x] Glass effect: backdrop-filter blur(28px) saturate(1.4)
- [x] Border: subtle green outline with green top border
- [x] Green glow shadow (120px spread)
- [x] Overscroll contained, touch-action pan-y
- [x] Closes with reverse animation

### 1.4 Header — Glass Gradient
- [x] Gradient background: rgba(4,50,62) → rgba(3,36,45)
- [x] Avatar: 40px circular with LOGO_FULL_B64
- [x] Avatar: green ring animation (bw-avatar-ring)
- [x] Avatar: hover buzz animation (bw-avatar-buzz)
- [x] Avatar: green glow shadow on hover
- [x] Bot name "BetonWin AI" (13.5px, weight 700)
- [x] Green status dot pulses (bw-pulse 2.5s)
- [x] "Online" text (10.5px, green 60% opacity)
- [x] Fullscreen button
- [x] Close button (→ triggers exit overlay)
- [x] Green gradient line at bottom (::after pseudo-element)
- [x] Header shadow for depth

### 1.5 Messages — Compact Modern
- [x] Bot messages: left-aligned, 20px circular avatar with logo
- [x] User messages: right-aligned, max 80%, green text on dark green bg
- [x] Bot bubble: rgba(255,255,255,0.04), subtle border, 16px radius
- [x] User bubble: green border + green text, no shadow
- [x] Agent bubble: gold left border accent
- [x] Message animation: bw-msg-in with bounce (cubic-bezier .34,1.56,.64,1)
- [x] Long messages wrap (word-break + overflow-wrap anywhere)
- [x] Auto-scroll to latest message
- [x] Scrollbar: 2px thin, green tint
- [x] Links: green with underline, open in new tab
- [x] Bold in bot: green color. Bold in user: white

### 1.6 Input Area — Unified Toolbar
- [x] Input wrapper: rounded 22px bar with subtle border
- [x] Textarea with auto-expand (max 100px)
- [x] Focus: green border glow
- [x] Bottom toolbar row with 4 buttons:
  - [x] Emoji button (😊)
  - [x] Attach file button (paperclip SVG)
  - [x] Language button (globe SVG)
  - [x] Send button (green circle, 34px)
- [x] Send hover: scale(1.08), darker green
- [x] Send disabled: opacity 0.1
- [x] Safe-area-inset-bottom for notch devices

### 1.7 Typing Indicator — Wave Bars
- [x] Three vertical bars with wave animation (bw-wave 1.4s)
- [x] Different heights (12px, 18px, 10px) with staggered delay
- [x] Label with animated dots (bw-ellipsis)
- [x] Shows agent name ("BetonWin AI" or real agent name)

### 1.8 Splash Screen (NEW)
- [x] Full-screen overlay on first open
- [x] Logo: 140px circular with bounce-in animation (bw-logo-in)
- [x] Green glow pulse behind logo (bw-glow-pulse)
- [x] Typewriter effect: line1 "BetonWin AI Support", line2 "24/7 Always available"
- [x] Cursor blink animation during typing
- [x] Auto-exit after 2.2s with fade-out (bw-splash-exit)
- [x] i18n: splash text in all 4 languages

### 1.9 Logo Watermark
- [x] 140px centered watermark behind messages (4% opacity)
- [x] Fades out on first message (transition 1.2s)
- [x] Restored on resetChat
- [x] Grayscale filter + brightness boost

### 1.10 Exit Overlay (NEW)
- [x] Full-screen overlay with blur backdrop (24px blur)
- [x] Title: "See you soon 👋" (i18n)
- [x] Three action cards in a row:
  - [x] New chat (💬) — green circle with orbit animation
  - [x] Rate us (⭐) — gold circle
  - [x] Exit (👋) — muted circle
- [x] Hover: cards lift 3px
- [x] CSAT stars: 5 gold stars with scale animation
- [x] Star hover: scale(1.25)
- [x] Star active: gold color + drop-shadow glow
- [x] After rating: shows "Thank you! 💚", then auto-closes
- [x] Click outside panel → back to chat
- [x] Labels update on language change

### 1.11 Footer
- [x] "Powered by BetonWin AI" — ultra-subtle (green 10% opacity)
- [x] Thin top border (green 4% opacity)

---

## 2. CONTENT & TEXT QUALITY

### 2.1 Welcome Messages (4 Languages)
- [x] ES: "¡Hola! Soy tu asistente de soporte **BetonWin** 24/7..."
- [x] EN: "Hi! I'm your **BetonWin** 24/7 support assistant..."
- [x] IT: "Ciao! Sono il tuo assistente di supporto **BetonWin** 24/7..."
- [x] PT: "Olá! Sou seu assistente de suporte **BetonWin** 24/7..."

### 2.2 AI Response Quality — Deposits
- [ ] "como depositar?" → mentions WebPay, MACH, crypto
- [ ] "deposito minimo?" → shows correct amounts
- [ ] "metodos de pago en Argentina?" → mentions Mercado Pago
- [ ] No hallucinated information
- [ ] No internal/sensitive data exposed

### 2.3 AI Response Quality — Withdrawals
- [ ] "cuanto tarda un retiro?" → 1-3 business days
- [ ] "minimo de retiro?" → correct amounts
- [ ] "regla del 70%?" → explains wagering requirement

### 2.4 AI Response Quality — Bonuses
- [ ] "como funciona el rollover?" → correct calculation
- [ ] "bono de bienvenida?" → 10 deposits, increasing bonus
- [ ] "saldo 0.00 con bono activo?" → explains real vs bonus balance

### 2.5 AI Response Quality — KYC
- [ ] "como verificar identidad?" → RUT (Chile), DNI (Argentina)
- [ ] "cuanto tarda la verificacion?" → max 72 business hours

### 2.6 AI Response Quality — Account
- [ ] "olvide contrasena" → step-by-step reset procedure
- [ ] "cuenta bloqueada" → contact support instruction

### 2.7 Response Formatting
- [x] Bold text (**text**) → `<strong>`, green in bot / white in user
- [x] Bullet lists → green dot (4px circle)
- [x] Numbered lists → green number
- [x] Links: clickable, green, underlined, target="_blank" rel="noopener"
- [x] No raw markdown visible
- [x] `<!--lang:xx-->` tags stripped before display
- [x] Language rejection → retry in Spanish as fallback

### 2.8 Error Messages (4 Languages)
- [x] Network error → "Algo salió mal..." / "Something went wrong..."
- [x] File too large → max 10MB message
- [x] Wrong file type → JPG, PNG, PDF message
- [x] Error messages match current language

---

## 3. MULTI-LANGUAGE

### 3.1 Language System
- [x] 4 languages: EN / ES / IT / PT
- [x] Default: Spanish (regardless of browser language)
- [x] Auto-detect from user text (LANG_WORDS scoring)
- [x] Short messages (< 30 chars): 1 match enough
- [x] Long messages: 2+ matches required (avoid false positives)
- [x] Tied scores → no switch (stays current)

### 3.2 Language Switching
- [x] Manual: language popup with flags (🇪🇸🇬🇧🇮🇹🇧🇷)
- [x] Auto: detected from user text
- [x] UI updates: placeholder, confirm button, exit overlay labels
- [x] Splash text in all 4 languages
- [x] Language instruction injected in AI payload: "[Reply ONLY in ...]"
- [x] AI response `<!--lang:xx-->` only applied if user didn't just set language

### 3.3 Language Rejection Handling
- [x] If n8n AI refuses non-Spanish → retry with Spanish-wrapped message
- [x] If retry also rejected → show "I can help with..." fallback
- [x] 10+ rejection patterns detected (all languages)

---

## 4. DEPOSIT VERIFICATION FLOW

- [x] Quick deposit button triggers flow
- [x] Deposit keywords auto-detect → triggers flow
- [x] Player ID form: input + confirm button
- [x] Player ID sanitized: only a-z, A-Z, 0-9, dash, underscore, max 50
- [x] Phase gate: only during DEPOSIT_ASK_ID
- [x] Status results: PROCESSING / NEED_UPLOAD / APPROVED / REJECTED / PENDING_REVIEW
- [x] Polling timeout → escalation to agent (not error)
- [x] Upload with retry (3 attempts, exponential backoff)
- [x] Quick action button reappears after result

---

## 5. FILE UPLOAD

- [x] Drag & drop zone with dashed border
- [x] Click triggers file picker
- [x] Accepted: JPG, JPEG, PNG, WebP, PDF
- [x] Max 10MB enforced
- [x] 0-byte file rejected
- [x] Progress bar (XHR progress events)
- [x] Upload to S3 via presigned URL
- [x] Upload timeout 60 seconds
- [x] Phase gate: only during UPLOAD_REQUIRED
- [x] File share in LIVE_AGENT mode via sendFileToAgent

---

## 6. SECURITY

- [x] XSS: escapeHTML on all user + bot content (&, <, >, ", ')
- [x] Links: only https:// URLs rendered as `<a>`
- [x] Player ID: alphanumeric only, max 50 chars
- [x] Job ID: sanitized for path traversal
- [x] Message length: capped at 1000 characters
- [x] Rate limit: 1s cooldown between messages
- [x] Max 100 messages per session
- [x] Safety timer: 30s auto-recover if stuck
- [x] Busy flag prevents concurrent requests
- [x] No API keys in widget source (only webhook URLs)
- [x] IIFE wrapper — no global variables

---

## 7. PERFORMANCE

- [x] KB search with timeout (Promise.race, 3.5s)
- [x] AI response timeout (18s)
- [x] KB smart search: parallel queries (original + translated + FAQ fallback)
- [x] Busy flag prevents concurrent requests
- [x] Session UUID (v4) for analytics correlation
- [x] IIFE wrapper — no globals leaked
- [x] CSS injected as single `<style>` element
- [x] Font Inter preloaded async

---

## 8. MOBILE & RESPONSIVE

- [x] Fullscreen mode: 100vw x 100vh on toggle
- [x] Overscroll contained (no page bounce)
- [x] Touch-action: pan-y
- [x] Mobile keyboard: visualViewport resize handler
- [x] Blur input after send on mobile (< 440px)
- [x] webkit-tap-highlight-color: transparent
- [x] webkit-overflow-scrolling: touch
- [x] Safe-area-inset-bottom for notch devices
- [ ] iPhone Safari tested
- [ ] Android Chrome tested

---

## 9. ESCALATION & TRIGGERS (T-01 → T-19)

### 9.1 T-01: Legal Threats → CRITICAL (Immediate Escalation)
- [x] LEGAL_KEYWORDS: 38 keywords in ES/EN/IT/PT
- [x] detectLegalThreat function
- [x] ES: abogado, demanda judicial, acción legal, denuncia
- [x] EN: lawyer, lawsuit, legal action, sue you, court, attorney
- [x] IT: avvocato, tribunale, querela, azione legale
- [x] PT: advogado, tribunal, processo judicial, ação legal
- [x] Immediate escalation: "T-01_legal_threat"
- [x] No AI response — direct to Zendesk

### 9.2 T-02: Fraud/Scam Accusations → CRITICAL (Immediate Escalation)
- [x] FRAUD_KEYWORDS: 29 keywords in ES/EN/IT/PT
- [x] detectFraudAccusation function
- [x] ES: estafa, fraude, me estafaron, empresa fraudulenta, sitio falso
- [x] EN: scam, fraud, scammed, fraudulent company, fake site
- [x] IT: truffa, frode, mi hanno truffato, azienda fraudolenta
- [x] PT: golpe, fui enganado, isso é fraude, site falso
- [x] Immediate escalation: "T-02_fraud_accusation"

### 9.3 T-03: Regulator Mentions → CRITICAL (in LEGAL_KEYWORDS)
- [x] sernac (Chile)
- [x] defensa del consumidor
- [x] agcm (Italy)
- [x] procon (Brazil)
- [x] authorities / autoridades / autorità
- [x] regulatory / regulador / órgão competente

### 9.4 Sensitive Content → CRITICAL (Immediate Escalation)
- [x] SENSITIVE_KEYWORDS: 34 keywords
- [x] detectSensitive function
- [x] Gambling addiction: adicción, ludopatía, autoexclusión, gambling problem, self-exclusion, dipendenza, vício
- [x] Fraud mentions: estafa, scam, rigged, truffa, golpe
- [x] Immediate escalation: "sensitive_content"

### 9.5 T-05/T-06: Human Request Detection (Dual-Layer)
**Layer 1 — User keywords:**
- [x] HUMAN_USER_KEYWORDS: 46 keywords in ES/EN/IT/PT
- [x] userWantsHuman function
- [x] EN: human, agent, operator, real person, talk to someone, live agent
- [x] ES: agente, operador, quiero un humano, persona real
- [x] IT: operatore, voglio parlare con, persona reale
- [x] PT: atendente, quero um humano, falar com alguém

**Layer 2 — AI response signals:**
- [x] HUMAN_RESPONSE_SIGNALS array
- [x] aiDetectsHumanRequest function
- [x] Signals: prefer to speak, human agent, frustración, etc.

**Logic:**
- [x] T-05: First request → bot tries to help (shows AI response)
- [x] T-06: HUMAN_REQUEST_THRESHOLD = 2 → escalation
- [x] No double-count: userWantsHuman check prevents AI layer from re-counting
- [x] handleWantsHuman function with urgency-based threshold
- [x] Escalation label: "T-06_human_request_x2"

### 9.6 T-07: Frustration Detection → Urgency Escalation
- [x] FRUSTRATION_KEYWORDS: 50 keywords in ES/EN/IT/PT
- [x] detectFrustration function
- [x] Detection signals:
  - [x] Keyword match (1+ = triggered)
  - [x] ALL CAPS (> 50% uppercase, length > 10) = +2 signals
  - [x] Excessive punctuation (!!! or ???) = +1 signal
- [x] Sets STATE.urgency = 'high'
- [x] Frustrated + human request → threshold drops to 1 (immediate escalation)
- [x] Escalation label: "T-07_frustrated_human_request"

### 9.7 T-17: Inactivity Timer
- [x] INACTIVITY_REMINDER_MS = 120000 (2 minutes)
- [x] INACTIVITY_CLOSE_MS = 240000 (4 minutes)
- [x] resetInactivityTimer function
- [x] Called on every user message in handleChatMessage
- [x] After 2 min: reminder message (4 languages)
  - EN: "Are you still there?"
  - ES: "¿Sigues ahí?"
  - IT: "Sei ancora lì?"
  - PT: "Você ainda está aí?"
- [x] After 4 min: chat closed, phase → AGENT_CLOSED, input disabled
- [x] Only active during CHAT and LIVE_AGENT phases
- [x] Timer cleared on resetChat

### 9.8 T-18: Client Unhappy with Bot Answer
- [x] UNHAPPY_KEYWORDS: 25 keywords in ES/EN/IT/PT
- [x] detectUnhappy function
- [x] STATE.unhappyCount tracks occurrences
- [x] After 2 unhappy messages → propose agent (4 languages)
  - EN: "I see my answer didn't help..."
  - ES: "Veo que mi respuesta no te ayudó..."
  - IT: "Vedo che la mia risposta non è stata utile..."
  - PT: "Vejo que minha resposta não ajudou..."
- [x] Reset on resetChat

### 9.9 T-19: Session Duration Monitor
- [x] SESSION_MAX_MS = 600000 (10 minutes)
- [x] checkSessionDuration function
- [x] sessionStartTime set in init() and resetChat()
- [x] After 10 min of conversation → propose agent (4 languages)
- [x] sessionStartTime reset to null after trigger (no repeat)

### 9.10 Escalation Flow
- [x] startEscalation(reason) function
- [x] Creates Zendesk ticket with conversation history
- [x] Phase transitions: ESCALATING → LIVE_AGENT → AGENT_CLOSED
- [x] Agent name from Zendesk (sideload ?include=users)
- [x] Agent polling (AGENT_POLL endpoint, 5s interval)
- [x] User can send messages and files to agent
- [x] CSAT rating (1-5 stars) after ticket close
- [x] Notify agent when user closes widget
- [x] humanRequestCount reset after failed escalation

---

## 10. KB TRANSLATION (Smart Search)

### 10.1 Translation Map
- [x] KB_TRANSLATE: 88 keyword translations
- [x] EN → ES: 42 entries (password, withdrawal, deposit, bonus, crypto, KYC, etc.)
- [x] IT → ES: 20 entries (prelievo, verifica, scommesse sportive, etc.)
- [x] PT → ES: 17 entries (saque, cadastro, apostas esportivas, etc.)
- [x] Longest match first (sorted by length descending)

### 10.2 Smart KB Search
- [x] translateQueryForKB function
- [x] searchKBRaw function (GET request to Apps Script)
- [x] Triple search: original query + translated query + FAQ fallback
- [x] Parallel Promise.all for speed
- [x] Results merged with deduplication (by filename)
- [x] Priority: translated > original > FAQ fallback
- [x] Max 5 results returned

---

## 11. LIVE AGENT & ZENDESK

- [x] Escalation via /webhook/escalate
- [x] Agent polling via /webhook/agent-poll
- [x] Agent reply via /webhook/agent-reply
- [x] Real agent name from Zendesk (sideload)
- [x] Typing indicator shows agent name
- [x] File sharing in live agent mode
- [x] CSAT rating (inline stars + exit overlay stars)
- [x] Ticket ID shown in escalation message
- [x] Chat closes only on Zendesk status "closed"
- [x] Widget close → notifies agent on Zendesk

---

## 12. RESET & STATE MANAGEMENT

- [x] resetChat clears all state:
  - [x] messages, jobId, playerId, phase → CHAT
  - [x] busy, lastSendTs → 0
  - [x] humanRequestCount → 0
  - [x] ticketId → null
  - [x] urgency → 'low'
  - [x] unhappyCount → 0
  - [x] sessionStartTime → Date.now()
  - [x] inactivityReminded → false
  - [x] inactivityTimer → cleared
- [x] Restores logo watermark
- [x] Restores bot header (name + status dot)
- [x] Re-creates quick deposit button
- [x] Re-creates typing indicator

---

## 13. RATE LIMITING & ABUSE PREVENTION

- [x] 1-second cooldown between messages
- [x] Busy flag prevents concurrent requests
- [x] Max message length: 1000 chars
- [x] Max messages per session: 100
- [x] Safety timeout: 30s auto-unlock if stuck
- [x] Phase gates: Player ID only in DEPOSIT_ASK_ID, upload only in UPLOAD_REQUIRED
- [x] New chat during loading → full state reset

---

## 14. GTM INTEGRATION

### 14.1 Tag Configuration
- [x] GTM container: BOW2 - PROD
- [x] Tag "widget cs": HTML personalizzato, All Pages
- [x] CDN URL: `@main` (NOT commit hash!) per auto-update
- [x] Duplicate guard: `getElementById('__beton_widget__')` check

### 14.2 Post-Deploy
- [ ] Widget appears on all pages
- [ ] No console errors
- [ ] No duplicate widget
- [ ] Works alongside GA4 and other tags

---

## Test Environments

| Environment | URL | Status |
|-------------|-----|--------|
| Local | http://localhost:8080/test.html | ✅ Attivo |
| CDN | cdn.jsdelivr.net/gh/.../betonwin-widget@main/widget.js | ⏳ Push pending |
| Production | beton.win | ⏳ GTM tag needs @main fix |

## Resources

| Resource | URL |
|----------|-----|
| n8n Backend | https://n8nbeton.online |
| GitHub Repo | github.com/stepbystepautomatization-jpg/betonwin-widget |
| CDN (widget.js) | cdn.jsdelivr.net/gh/stepbystepautomatization-jpg/betonwin-widget@main/widget.js |
| Purge CDN | purge.jsdelivr.net/gh/stepbystepautomatization-jpg/betonwin-widget@main/widget.js |
| GTM Container | BOW2 - PROD |
| Support Email | ayuda@beton.win |

## Automated Test Results (Aprile 2026)

| Suite | Tests | Result |
|-------|-------|--------|
| Component verification | 193/193 | ✅ ALL PASSED |
| Trigger detection (unit) | 89/89 | ✅ ALL PASSED |
| False positive checks | 6/6 | ✅ ALL PASSED |
| **Total** | **288/288** | **✅ ALL PASSED** |
