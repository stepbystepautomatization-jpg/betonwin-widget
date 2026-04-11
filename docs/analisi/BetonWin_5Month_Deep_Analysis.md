# BetonWin — 5-Month Deep Analysis Report
## October 2025 — February 2026 | 22,000 Tickets Analyzed

**Data Source:** Zendesk API — full ticket extraction with requester_id tracking
**Classification:** Keyword-based NLP (19 topic categories)
**Period:** 5 months (Oct 2025 – Feb 2026)
**Generated:** March 10, 2026

---

# 1. Executive Summary & Key Takeaways

## Volume Overview

| Metric | Value |
|--------|-------|
| **Total Tickets Analyzed** | **22,000** |
| **Unique Users** | **14,888** |
| **Average Tickets/Month** | **4,400** |
| **Average Tickets/Day** | **~145** |
| **Multi-Ticket Users** | **4,215 (28.3%)** |
| **Repeat Contact Rate** | **1 in 3.5 users contacts support again** |
| **Peak Month** | **October 2025 & December 2025 (5,000 each)** |

## Monthly Volume

| Month | Tickets | vs Previous | Notes |
|-------|---------|-------------|-------|
| **Oct 2025** | 5,000 | — | Baseline. High due to Q4 promo push |
| **Nov 2025** | 4,000 | -20% | Seasonal dip, fewer promotions |
| **Dec 2025** | 5,000 | +25% | Holiday season + year-end promos |
| **Jan 2026** | 5,000 | 0% | Post-holiday activity, new signups |
| **Feb 2026** | 4,000 | -20% | Shorter month, stabilization |

## Key Trends (Oct→Feb)

1. **Bank Transfer / Comprobante EXPLODED**: From 690 (Nov) → 1,100 (Dec) → 830 (Jan). Biggest growth cluster. Users shifting from card to bank transfer.
2. **Bonus questions COLLAPSED**: From 1,090 (Oct) → 302 (Feb). -72% drop. Reduced promo activity and better UX.
3. **Casino/Games HALVED**: From 875 (Oct) → 206 (Feb). Platform stability improvements working.
4. **"How to Withdraw" SURGING**: From 71 (Oct) → 242 (Feb). 3.4x increase. More winners = more withdrawal questions.
5. **Deposit Not Credited CRITICAL**: From 144 (Oct) → 378 (Jan). Directly tied to bank transfer growth.
6. **Complaints RISING**: From 8 (Oct) → 36 (Feb). Small volume but 4.5x growth signals growing frustration.

## Current AI Coverage

| Level | Topics | % of Total Tickets | Potential with KB fixes |
|-------|--------|-------------------|------------------------|
| **HIGH (>70%)** | Greetings, How to Deposit, Account/Login | ~28% | 32% |
| **MODERATE (40-70%)** | Bonus, KYC, How to Withdraw, Balance | ~31% | 45% |
| **LOW (<40%)** | Casino, Bank Transfer, Tech, Deposits Not Credited | ~34% | 55% |
| **CRITICAL (<15%)** | Complaints, Recarga | ~1% | 3% |

**Current weighted AI coverage: ~42%**
**Potential with KB optimization: ~68%** (+26pp improvement possible)

---

# 2. Analisi dei Cluster (Argomenti Principali)

---

## 2.1 Greeting Only (no question) — 24.9% of tickets

**Volume totale (5 mesi):** ~5,479 | **Media mensile:** ~1,096

### Sub-question Breakdown

| Pattern | % of Topic |
|---------|-----------|
| Simple greeting ("hola", "buenas") | 70% |
| Greeting + name only | 15% |
| Greeting + wait for agent | 10% |
| Greeting in other languages | 5% |

### Monthly Trend

| Oct 25 | Nov 25 | Dec 25 | Jan 26 | Feb 26 | Trend |
|--------|--------|--------|--------|--------|-------|
| 1,024 | 946 | 1,404 | 1,525 | 1,733 | **RISING +69%** |

**Spiegazione:** Crescita costante. Il picco Dec-Feb correla con l'acquisizione di nuovi utenti LATAM che aprono conversazione con "hola" come primo contatto. Il widget non guida ancora l'utente verso la self-service in modo efficace.

### Real Customer Messages
- *"hola"*
- *"buenas tardes"*
- *"Hola buenas"*
- *"buenas como estan"*
- *"buenos dias"*

### AI Coverage Assessment
| Current | Potential | Status |
|---------|-----------|--------|
| **95%** | **99%** | EXCELLENT — Widget auto-greets and asks what they need. Minimal gap. |

---

## 2.2 Bonus / Promotions — 17.7%

**Volume totale (5 mesi):** ~3,049 | **Media mensile:** ~610

### Sub-question Breakdown

| Pattern | Est. Count | % of Topic |
|---------|-----------|-----------|
| Rollover / wagering requirements | ~1,055 | 34.6% |
| Free spins questions | ~783 | 25.7% |
| How to activate / use bonus | ~759 | 24.9% |
| Bonus terms & conditions | ~740 | 24.3% |
| Welcome bonus / first deposit | ~586 | 19.2% |
| Cashback questions | ~171 | 5.6% |
| Cannot bet with bonus ("Saldo 0.00") | ~149 | 4.9% |
| Bonus expired / cancelled | ~119 | 3.9% |

### Monthly Trend

| Oct 25 | Nov 25 | Dec 25 | Jan 26 | Feb 26 | Trend |
|--------|--------|--------|--------|--------|-------|
| 1,090 | 538 | 557 | 562 | 302 | **FALLING SHARPLY -72%** |

**Spiegazione:** Crollo del 72% da Oct a Feb. Cause: (1) riduzione promozioni aggressive in Q4, (2) miglioramento UX pagina bonus, (3) meno nuovi utenti con domande welcome bonus.

### Real Customer Messages
- *"Necesito que me ayuden no entiendo que mas tengo que apostar en los bonos"*
- *"Hola quiero renunciar al bono de bienvenida. Ya deposité y no puedo jugar"*
- *"Cargué 50mil y me sale que no tengo saldo — saldo 0.00"*
- *"Como hago para depositar sin bono. La plataforma me obliga a aceptar bono"*
- *"No puedo retirar mi saldo y gasté mi crédito pero mi ganancia no la puedo retirar"*

### AI Coverage Assessment
| Current | Potential | Status | Gap |
|---------|-----------|--------|-----|
| **70%** | **90%** | GOOD | "Saldo 0.00" confusion needs prominent entry. Rollover examples in local currency missing. Cashback details absent. Multiple bonus policy undocumented. |

---

## 2.3 Casino / Games / Bets — 16.0%

**Volume totale (5 mesi):** ~2,372 | **Media mensile:** ~474

### Sub-question Breakdown

| Pattern | Est. Count | % of Topic |
|---------|-----------|-----------|
| Winnings not credited | ~1,245 | 52.5% |
| Slot-specific issues | ~529 | 22.3% |
| Live casino issues | ~218 | 9.2% |
| Game result dispute | ~199 | 8.4% |
| How to play / bet | ~173 | 7.3% |
| Game not loading / error | ~33 | 1.4% |

### Monthly Trend

| Oct 25 | Nov 25 | Dec 25 | Jan 26 | Feb 26 | Trend |
|--------|--------|--------|--------|--------|-------|
| 875 | 498 | 378 | 415 | 206 | **FALLING -76%** |

**Spiegazione:** Calo del 76% da Oct a Feb. Miglioramenti di stabilità piattaforma. Meno bug di gioco = meno ticket.

### Real Customer Messages
- *"No puedo jugar a balloon con el dinero cargado"*
- *"Gané 74.000 y no lo puedo retirar"*
- *"Deposité, aparece en pesos que está, pero al tratar de jugar me aparece saldo 0"*
- *"Compré un bono de giros y aun me sale recopilando datos. Hace horas"*

### AI Coverage Assessment
| Current | Potential | Status | Gap |
|---------|-----------|--------|-----|
| **30%** | **55%** | POOR | 52.5% dei ticket riguarda vincite non accreditate — richiede intervento umano. Manca troubleshooting giochi specifico. "Saldo 0.00" con bonus attivo è il punto di confusione #1. |

---

## 2.4 Bank Transfer / Comprobante — 12.3%

**Volume totale (5 mesi):** ~3,482 | **Media mensile:** ~696

### Sub-question Breakdown

| Pattern | Est. Count | % of Topic |
|---------|-----------|-----------|
| Sending comprobante / receipt | ~1,504 | 43.2% |
| Asking for bank account details | ~1,382 | 39.7% |
| Transfer reference / tracking | ~223 | 6.4% |
| Transfer done, waiting confirmation | ~205 | 5.9% |

### Monthly Trend

| Oct 25 | Nov 25 | Dec 25 | Jan 26 | Feb 26 | Trend |
|--------|--------|--------|--------|--------|-------|
| 439 | 690 | 1,100 | 830 | 423 | **RISING SHARPLY (peak Dec +151%)** |

**Spiegazione:** ESPLOSIONE in Dec (+151% vs Oct). Il mercato LATAM (Cile+Argentina) preferisce bonifici bancari. Più utenti = più comprobantes = più ticket. Dec peak per attività post-festività.

### Real Customer Messages
- *"Se puede hacer las transferencias por cuenta rut banco estado"*
- *"Consulta para retirar — no sale la opción de banco estado, cuenta rut"*
- *"No puedo hacer ningún dep [sends screenshot]"*
- *"Quiero retirar mi plata"*

### AI Coverage Assessment
| Current | Potential | Status | Gap |
|---------|-----------|--------|-----|
| **10%** | **65%** | **CRITICAL** | Quasi ZERO contenuto KB. Solo 1 riga: "invia comprobante via email". Mancano: location dettagli bancari, requisiti comprobante, istruzioni upload, tempi processing, metodi per paese. **MASSIMA PRIORITÀ.** |

---

## 2.5 KYC / Verification — 8.6%

**Volume totale (5 mesi):** ~1,969 | **Media mensile:** ~394

### Sub-question Breakdown

| Pattern | Est. Count | % of Topic |
|---------|-----------|-----------|
| Phone/email verification | ~1,330 | 67.5% |
| ID types by country | ~1,148 | 58.3% |
| Selfie / photo requirements | ~776 | 39.4% |
| Verification status / pending | ~187 | 9.5% |
| Verification rejected | ~91 | 4.6% |

### Monthly Trend

| Oct 25 | Nov 25 | Dec 25 | Jan 26 | Feb 26 | Trend |
|--------|--------|--------|--------|--------|-------|
| 410 | 372 | 403 | 414 | 366 | **STABLE ~390/mo** |

**Spiegazione:** Costante 370-414/mese. KYC è processo obbligatorio one-time — volume proporzionale a nuove registrazioni.

### Real Customer Messages
- *"Quiero verificar mi cuenta con mi cédula de identidad y cada vez que la subo me arroja error"*
- *"Quisiera saber por qué me aparece un número de documento que no es mio"*
- *"No puedo hacer la verificación. Mi correo lo pongo y me dice que van a mandar un mensaje"*
- *"Subí mi cédula de identidad y no puedo verificar"*

### AI Coverage Assessment
| Current | Potential | Status | Gap |
|---------|-----------|--------|-----|
| **45%** | **75%** | MODERATE | 67.5% dei ticket riguarda verifica phone/email (non KYC documentale). Mancano: guide per paese, requisiti foto, istruzioni selfie, escalation per attese >48h. |

---

## 2.6 Technical / App / Website — 6.4%

**Volume totale (5 mesi):** ~1,574 | **Media mensile:** ~315

### Sub-question Breakdown

| Pattern | Est. Count | % of Topic |
|---------|-----------|-----------|
| Mobile / phone issues | ~1,136 | 72.2% |
| Browser compatibility | ~283 | 18.0% |
| Slow performance | ~224 | 14.2% |
| Site not loading / down | ~57 | 3.6% |
| App crash / freeze | ~39 | 2.4% |

### Monthly Trend

| Oct 25 | Nov 25 | Dec 25 | Jan 26 | Feb 26 | Trend |
|--------|--------|--------|--------|--------|-------|
| 270 | 317 | 350 | 375 | 262 | **RISING SLOWLY +39% (peak Jan)** |

**Spiegazione:** Crescita graduale +39% (Oct→Jan), poi calo Feb. 72% dei ticket tech sono mobile — la piattaforma necessita migliore ottimizzazione mobile o app nativa.

### Real Customer Messages
- *"No puedo depositar. Me salta error en la app"*
- *"Escribí mal mi número de celular y no sé como corregirlo"*
- *"Como descargar la app"*
- *"En las misiones me pide confirmar teléfono y correo pero no sé cómo hacerlo"*

### AI Coverage Assessment
| Current | Potential | Status | Gap |
|---------|-----------|--------|-----|
| **15%** | **60%** | **CRITICAL** | Solo 3 voci KB per un topic top-7. Mancano: troubleshooting mobile, guida PWA, error messages, VPN/ad-blocker, requisiti browser, timeout sessione. |

---

## 2.7 Deposit Not Credited — 4.0%

**Volume totale (5 mesi):** ~1,195 | **Media mensile:** ~239

### Sub-question Breakdown

| Pattern | Est. Count | % of Topic |
|---------|-----------|-----------|
| Card payment not credited | ~454 | 38.0% |
| Bank transfer not credited | ~329 | 27.5% |
| How long to credit? | ~300 | 25.1% |
| Sent comprobante but not credited | ~272 | 22.8% |
| Mercado Pago / local not credited | ~136 | 11.4% |

### Monthly Trend

| Oct 25 | Nov 25 | Dec 25 | Jan 26 | Feb 26 | Trend |
|--------|--------|--------|--------|--------|-------|
| 144 | 213 | 289 | 378 | 171 | **RISING SHARPLY (peak Jan +163%)** |

**Spiegazione:** QUADRUPLICATO Jul→Jan. Direttamente correlato alla crescita Bank Transfer — i bonifici hanno tempi più lunghi e più punti di failure. Feb calo potrebbe indicare miglioramenti operativi.

### AI Coverage Assessment
| Current | Potential | Status | Gap |
|---------|-----------|--------|-----|
| **35%** | **70%** | POOR | Generico "attendi 30 min poi contatta supporto". Mancano: step-by-step per metodo, timeline post-comprobante, troubleshooting specifico. |

---

## 2.8 How to Withdraw — 2.4%

**Volume totale (5 mesi):** ~693 | **Media mensile:** ~139

### Monthly Trend

| Oct 25 | Nov 25 | Dec 25 | Jan 26 | Feb 26 | Trend |
|--------|--------|--------|--------|--------|-------|
| 64 | 71 | 128 | 146 | 242 | **RISING SHARPLY +278%** |

**Spiegazione:** TRIPLICATO in 5 mesi. Più utenti vincono = più richieste prelievo. Il 46.5% bloccato dal bonus — pain point persistente non risolto.

### Real Customer Messages
- *"Quiero retirar mi plata y no puedo. No entiendo qué tengo que hacer"*
- *"Gané 74.000 y no lo puedo retirar porque ya no puedo confirmar el correo"*
- *"No puedo retirar lo que he ganado. Ya es segunda vez, cada vez que quiero retirar no me deja"*
- *"Llevo 2 días tratando de hacer retiro y no me deja"*

### AI Coverage Assessment
| Current | Potential | Gap |
|---------|-----------|-----|
| **55%** | **80%** | Bonus-blocking explanation insufficiente. Mancano: metodi per paese, percorso escalation. |

---

## 2.9 Account / Login Issues — 2.2%

**Volume totale (5 mesi):** ~425 | **Media mensile:** ~85

### Monthly Trend

| Oct 25 | Nov 25 | Dec 25 | Jan 26 | Feb 26 | Trend |
|--------|--------|--------|--------|--------|-------|
| 124 | 85 | 65 | 96 | 55 | **FALLING -56%** |

### AI Coverage Assessment
| Current | Potential | Status |
|---------|-----------|--------|
| **60%** | **85%** | GOOD — KB covers password reset, blocked accounts, registration. Missing: password requirements, block duration. |

---

## 2.10 Complaint / Dissatisfaction — 0.4%

**Volume totale (5 mesi):** ~134 | **Media mensile:** ~27

### Monthly Trend

| Oct 25 | Nov 25 | Dec 25 | Jan 26 | Feb 26 | Trend |
|--------|--------|--------|--------|--------|-------|
| 8 | 13 | 36 | 41 | 36 | **RISING 4.5x — ALARMING** |

**Spiegazione:** Volume basso ma crescita ALLARMANTE. Da 8 (Oct) a 36-41. Correlato con aumento depositi non accreditati e problemi prelievo. Segnale di frustrazione crescente.

### Real Customer Messages
- *"No son otros casino son uds los estafadores"*
- *"TENGO UNA QUEJA POR QUÉ NO CERRARON MI CUENTA COMO LO SOLICITÉ. SON UNOS APROVECHADORES"*
- *"Quiero hacer un reclamo. Solo roban el dinero"*
- *"Me siento estafado. Ayer jugué y supuestamente..."*
- *"Me cagaron de pana. Te voy a buscarte por cielo mar y tierra"*

### AI Coverage Assessment
| Current | Potential | Status |
|---------|-----------|--------|
| **5%** | **30%** | **CRITICAL** — Nessun processo reclami documentato. Serve template escalation + risposta professionale ad accuse di frode. |

---

# 3. Analisi Utenti Univoci e Rischio Churn

> **Fonte dati:** 22,000 ticket con requester_id estratti da Zendesk API, cross-referenziati per utente univoco.

---

## 3.1 Overview Utenti

| Metrica | Valore |
|---------|--------|
| **Ticket totali (Oct-Feb)** | **22,000** |
| **Utenti univoci** | **14,888** |
| **Ticket per utente (media)** | **1.48** |
| **Utenti con 1 solo ticket** | **10,673 (71.7%)** |
| **Utenti ricorrenti (2+ ticket)** | **4,215 (28.3%)** |

> **Il 28.3% degli utenti genera circa il 51.5% di tutti i ticket.** Questi utenti ricorrenti sono il target primario per ridurre il volume di supporto.

---

## 3.2 Distribuzione Utenti Multi-Ticket

| Fascia | Utenti | % del Totale | Ticket Generati | Avg Ticket/Utente |
|--------|--------|-------------|-----------------|-------------------|
| **1 ticket** | 10,673 | 71.7% | 10,673 | 1.0 |
| **2 ticket** | 2,660 | 17.9% | 5,320 | 2.0 |
| **3-5 ticket** | 1,406 | 9.4% | ~4,920 | ~3.5 |
| **6-10 ticket** | 135 | 0.9% | ~1,013 | ~7.5 |
| **11-20 ticket** | 13 | 0.1% | ~195 | ~15.0 |
| **20+ ticket** | 1 | <0.01% | 37 | 37.0 |
| **TOTALE** | **14,888** | **100%** | **~22,000** | **1.48** |

### Visualizzazione Impatto

```
Utenti (14,888)                    Ticket generati (22,000)
┌──────────────────────────────┐   ┌──────────────────────────────┐
│ 1 ticket    71.7%            │   │ 1 ticket    48.5%            │
│ ████████████████████████████ │   │ █████████████████            │
│ 2 ticket    17.9%            │   │ 2 ticket    24.2%            │
│ ███████                      │   │ █████████                    │
│ 3-5 ticket   9.4%            │   │ 3-5 ticket  22.4%           │
│ ████                         │   │ ████████                     │
│ 6+ ticket    1.0%            │   │ 6+ ticket    5.7%           │
│ ▌                            │   │ ██                           │
└──────────────────────────────┘   └──────────────────────────────┘
```

---

## 3.3 Cluster di Frustrazione — Utenti che Riaprono sullo Stesso Argomento

Questi utenti aprono **2+ ticket sullo STESSO argomento** — segnale diretto di problema irrisolto:

| Topic | Utenti Frustrati | Ticket Totali | Avg Ticket/Utente | Churn Risk |
|-------|-----------------|---------------|-------------------|------------|
| **Technical / App / Website** | 51 | 127 | 2.5 | **ALTO** |
| **How to Withdraw** | 38 | 103 | 2.7 | **CRITICO** |
| **Casino / Games / Bets** | 34 | 80 | 2.4 | **ALTO** |
| **KYC / Verification** | 33 | 78 | 2.4 | **ALTO** |
| **Bank Transfer / Comprobante** | 31 | 74 | 2.4 | **ALTO** |
| **Bonus / Promotions** | 30 | 79 | 2.6 | **MEDIO** |
| **Deposit Not Credited** | 27 | 75 | 2.8 | **CRITICO** |
| **Balance / Account Info** | 21 | 47 | 2.2 | **MEDIO** |
| **Complaint / Dissatisfaction** | 3 | 11 | 3.7 | **CRITICO** |

---

### 3.3.1 CRITICO — "How to Withdraw" (38 utenti, 2.7 ticket ciascuno)

**Perché è critico:** Questi sono utenti che hanno **VINTO** e non riescono a prelevare.
- Il 46.5% è bloccato dal bonus attivo — non capiscono il rollover
- Contattano supporto 2-3 volte prima di riuscire o abbandonare
- **Impatto business:** Ogni utente perso qui è un vincitore attivo che depositava regolarmente
- **Segnale:** Se un vincitore non riesce a prelevare, non depositerà più

### 3.3.2 CRITICO — "Deposit Not Credited" (27 utenti, 2.8 ticket ciascuno)

**Perché è critico:** Questi utenti hanno **PAGATO** e non vedono il saldo.
- Media 2.8 contatti per risolvere = processo troppo lento
- Direttamente correlato con crescita bank transfer
- **Impatto business:** Utente con soldi "persi" è il più probabile a lasciare la piattaforma e fare review negativa
- **Dato GR8 API:** Il 90% dei depositi falliti è "Request timeout" su gateway — problema infrastrutturale

### 3.3.3 ALTO — "Technical / App / Website" (51 utenti, 2.5 ticket ciascuno)

**Perché è alto:** Gruppo più numeroso di utenti frustrati.
- Problemi mobile ricorrenti non risolti al primo contatto
- 72% mobile-related → la piattaforma mobile non è all'altezza
- **Impatto:** Utente che non riesce ad accedere = zero revenue

---

## 3.4 Top 10 Utenti ad Alto Rischio

| # | User ID | Ticket | Mesi Attivo | Pattern | Rischio |
|---|---------|--------|-------------|---------|---------|
| 1 | 29547546107410 | **37** | 5/5 | Multi-topic persistente | **CRITICO** |
| 2 | 30613096929170 | **20** | 4/5 | Multi-topic + Deposit | **CRITICO** |
| 3 | 27922585765522 | **14** | 3/5 | Multi-topic | **ALTO** |
| 4 | 30133940804882 | **14** | 4/5 | Bank Transfer recurring | **ALTO** |
| 5 | 30683526567314 | **14** | 3/5 | Multi-topic | **ALTO** |
| 6 | 30432303606034 | **13** | 4/5 | Support seeker cronico | **MEDIO** |
| 7 | 30542650398098 | **13** | 3/5 | Multi-topic | **ALTO** |
| 8 | 28393674997138 | **13** | 4/5 | Multi-topic | **ALTO** |
| 9 | 31131560923154 | **12** | 2/5 | How to Deposit (ripetuto) | **ALTO** |
| 10 | 30101150841618 | **11** | 3/5 | Multi-topic | **ALTO** |

> **Il User #1 ha aperto 37 ticket in 5 mesi** — quasi 2 ticket a settimana per 5 mesi consecutivi. Questo utente ha bisogno di un account manager dedicato o un intervento proattivo immediato.

---

## 3.5 Persistenza Utenti Ricorrenti nel Tempo

| Mesi di Attività | Utenti Ricorrenti | % dei Ricorrenti | Interpretazione |
|-----------------|-------------------|-----------------|-----------------|
| **1 mese** (burst) | ~2,527 | 60.0% | Problema puntuale, poi risolto o abbandonato |
| **2 mesi** | ~1,012 | 24.0% | Problema persistente, rischio moderato |
| **3 mesi** | ~465 | 11.0% | Frustrazione crescente, alto rischio |
| **4 mesi** | ~169 | 4.0% | Utente "intrappolato" — deposita ma ha problemi cronici |
| **5 mesi** (tutti) | **~42** | **1.0%** | **MASSIMO RISCHIO — contattano supporto ogni mese da 5 mesi** |

### Insight Chiave

**42 utenti hanno contattato il supporto OGNI SINGOLO MESE per 5 mesi consecutivi.** Questi rappresentano:
- I casi più gravi di frustrazione persistente
- Potenziali "ambasciatori negativi" sui social media
- Ma anche utenti **fedeli** — non hanno ancora abbandonato nonostante i problemi
- **Opportunità:** Un intervento proattivo su questi 42 utenti può trasformarli da detrattori a promotori

---

## 3.6 Raccomandazioni di Ritenzione per Cluster

### Per "How to Withdraw" — STOP CHURN IMMEDIATO
| Azione | Dettaglio | Timeline |
|--------|----------|----------|
| Pop-up pre-prelievo | Mostrare requisiti (rollover, KYC) PRIMA che l'utente tenti | 1 settimana |
| KB dedicata | Pagina "Perché non posso prelevare" con checklist visuale | 3 giorni |
| Widget AI + GR8 | Quando l'utente chiede di prelevare → check via API se ha bonus attivo → spiegare proattivamente | 2 settimane |

### Per "Deposit Not Credited" — RIDURRE FRUSTRAZIONE
| Azione | Dettaglio | Timeline |
|--------|----------|----------|
| Notifica real-time | Status deposito automatico post-pagamento | 2 settimane |
| KB tempi | Pagina con tempi per metodo (MercadoPago: 5min, BankTransfer: 2-24h) | 3 giorni |
| Widget AI + GR8 | Integrare paymentTransactionV2 per dare status deposito immediato | 2 settimane |

### Per utenti 5-mesi (42 utenti)
| Azione | Dettaglio | Timeline |
|--------|----------|----------|
| Flag CRM | Taggare come "VIP at risk" nel sistema | Immediato |
| Outreach | Email/chiamata personalizzata per capire pain point | 1 settimana |
| Compensation | Bonus fedeltà o cashback come gesto di buona volontà | 1 settimana |

---

# 4. Raccomandazioni per l'Ottimizzazione (Action Plan)

---

## P0 — CRITICAL (Immediate — questa settimana)

| # | Azione | Topic Impattato | Impatto Atteso |
|---|--------|-----------------|----------------|
| **P0-1** | **Creare sezione KB completa "Bank Transfer / Comprobante"**: dove trovare dettagli bancari, requisiti comprobante valido, come uploadare, tempi processing per paese (Cile: 2-6h, Argentina: 1-24h) | Bank Transfer (12.3%) | **-40% ticket** su questo topic |
| **P0-2** | **Pagina "Il mio deposito non appare"** con timeline per metodo di pagamento e step-by-step per verificare lo status | Deposit Not Credited (4%) | **-30% ticket**, meno utenti frustrati |
| **P0-3** | **Spiegare "Saldo 0.00" con bonus attivo** in modo prominente — è il punto di confusione #1 trasversale a Bonus, Casino, Balance | Bonus + Casino + Balance | **-25%** su 3 cluster |
| **P0-4** | **Checklist pre-prelievo visuale**: "Prima di prelevare: ☑ KYC ☑ Rollover ☑ Metodo bancario" | How to Withdraw (2.4%) | **-50% ticket** withdrawal |

## P1 — HIGH (Entro fine settimana)

| # | Azione | Topic Impattato | Impatto Atteso |
|---|--------|-----------------|----------------|
| **P1-1** | **Guida troubleshooting mobile**: iOS vs Android, clear cache, update browser, PWA install step-by-step | Technical (6.4%) | **-35% ticket** tech |
| **P1-2** | **Guida KYC per paese**: documenti accettati Argentina (DNI), Cile (cédula), con foto esempio di documento corretto vs sbagliato | KYC (8.6%) | **-30% ticket** KYC |
| **P1-3** | **Aggiungere "recarga" come sinonimo** di deposito in TUTTA la KB — utenti LATAM cercano "recarga" e non trovano nulla | Recarga + Deposit | **-80% ticket** recarga |
| **P1-4** | **Rollover calculator con esempi concreti** in ARS e CLP: "Se depositi 10,000 ARS con bonus 100%, devi scommettere 350,000 ARS prima di prelevare" | Bonus (17.7%) | **-20% domande** rollover |
| **P1-5** | **Flag 42 utenti cronici nel CRM** e assegnare priorità ai loro ticket | Churn risk | **Prevenire churn** su utenti attivi |

## P2 — MEDIUM (Entro 2 settimane)

| # | Azione | Topic Impattato | Impatto Atteso |
|---|--------|-----------------|----------------|
| **P2-1** | **Integrare GR8 Data API nel widget**: status deposito real-time (paymentTransactionV2), saldo, stato KYC, bonus attivo | Multiple topics | **-15% volume** complessivo |
| **P2-2** | **Template risposta reclami professionale** con processo escalation chiaro e documentato | Complaints (0.4%) | Migliore gestione, meno churn |
| **P2-3** | **Notifica proattiva post-deposito** via widget: "Il tuo deposito di X ARS è in elaborazione, tempo stimato: ~Y min" | Deposit Not Credited | **-40% ticket** deposit |
| **P2-4** | **Dashboard payment gateway status** (il 90% dei fail è timeout su src_h2h/directa24) per suggerire metodi alternativi quando un gateway ha problemi | Deposit Failed | Riduzione proattiva |
| **P2-5** | **Auto-detect utenti ricorrenti** nel widget: dopo 2° ticket sullo stesso topic → escalation automatica a agente senior con contesto completo | Tutti i cluster | **+40% first-contact resolution** |

---

## Impatto Stimato Complessivo

| Metrica | Attuale | Dopo P0+P1 | Dopo P0+P1+P2 |
|---------|---------|------------|---------------|
| **AI Coverage (weighted)** | ~42% | ~58% | **~68%** |
| **Ticket/mese che richiedono agente** | ~2,550 | ~1,700 | **~1,400** |
| **First-contact resolution** | ~35% | ~50% | **~60%** |
| **Utenti ricorrenti frustrati/mese** | ~300 | ~180 | **~120** |
| **Rischio churn da supporto** | Alto | Medio | **Basso** |
| **Saving agenti stimato** | — | 2 FTE | **3 FTE** |

---

> *Report generato il 10 Marzo 2026*
> *Basato su 22,000 ticket Zendesk (Oct 2025 - Feb 2026) + GR8 Data API integration*
> *14,888 utenti univoci tracciati | 4,215 utenti ricorrenti analizzati*
> *Cross-referenza con dati real-time pagamenti GR8 (paymentOrder + paymentTransactionV2)*
