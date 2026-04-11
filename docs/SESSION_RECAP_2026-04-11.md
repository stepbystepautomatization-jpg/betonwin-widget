# BetonWin Widget — Session Recap (11 Aprile 2026)

## Lavoro Completato

### 1. Merge Widget (2 cartelle → 1)
Due versioni divergenti del widget unite in una sola:
- **Base design**: splash screen, exit overlay, logo base64, FAB pill, input toolbar, language popup
- **Trigger system**: T-01→T-19 (legal, fraud, regulators, frustration, unhappy, inactivity, session)
- **KB Translation**: 88 traduzioni EN/IT/PT→ES + smart search con dedup
- **Risultato**: widget unificato, 2679 righe, 170KB

### 2. Design Moderno
- Bot: testo puro senza bubble (stile ChatGPT)
- User: pill verde pieno (#45cd98) con testo scuro
- Animazioni: bot slide-up, user slide-right, typing dots pulsanti
- Exit overlay con CSAT stars

### 3. Mobile Ottimizzato
- FAB: solo logo circolare, bottom:80px (sopra nav bar sito)
- Widget: floating card 65vh, margini 8px, angoli 18px
- Tastiera iOS: overflow:hidden su body

### 4. GR8 Data API Integration
**Connessione**: Widget → n8n webhook → OAuth → `apg-s2s.com/v1/data-api/business-objects`

**Funzioni implementate**:
- `gr8Query()` — chiamata GraphQL generica
- `fetchPlayerById(id)` — profilo per Player ID
- `fetchPlayerByEmail(email)` — profilo per email  
- `fetchPlayerTransactions(id)` — ultime transazioni
- `loadPlayerData()` — auto-detect utente loggato → carica profilo gr8
- `identifyPlayer(emailOrId)` — lookup manuale per utenti non loggati
- `getPlayerContext()` — stringa dati player iniettata in ogni chiamata AI

**Dati disponibili**: playerProfile, paymentTransactionV2, paymentOrder, playerDocument, walletProxyTransaction, playerLogin, sportBet, casinoRound

### 5. Deposit Proof Screening Flow
**Flusso nel widget**:
1. User scrive "deposit not arrived" → keyword detection
2. Widget verifica se ha player data da gr8
   - SI → "Ciao [nome], valuta [CLP]. Allega prova di pagamento"
   - NO → chiede email/ID → lookup gr8 → poi chiede prova
3. User allega file → preview inline (immagine thumbnail o 📎 filename)
4. Upload a S3 via presigned URL
5. Chiama n8n `/webhook/deposit-screening`
6. Risultato torna al widget

**n8n Workflow** (`BetonWin — Deposit Proof Screening`, ID: `tD8bdjtupdJg33DS`):
```
Webhook → Get GR8 Token → Get Player Transactions → Build Result → Respond
```
- Riceve: player_id, player_name, email, s3_url, file_name, file_type, language
- Consulta gr8: ultime 5 transazioni del player
- Ritorna: status + player data + transazioni + s3_url + timestamp

### 6. File Upload & Media
- Upload funziona in tutte le fasi (CHAT, LIVE_AGENT, UPLOAD_REQUIRED)
- Preview: immagini → thumbnail inline, PDF → "📎 filename"
- Media rendering: URL immagini/video nel testo renderizzati inline
- Rimosso bottone "Verifica stato deposito"

### 7. Organizzazione Cartelle
Da 2 cartelle a 1 strutturata: `widget-cs/` con assets/, config/, docs/, scripts/

### 8. Deploy
- GitHub push + CDN purge
- GTM versione 9 pubblicata con `@main`

---

## Prossimi Step

### P0 — CRITICO (Da fare subito)

#### 1. AI Vision Screening del Payment Proof
Il workflow n8n attualmente ritorna sempre `PENDING_REVIEW`. Serve:
- **Nodo AI Vision**: scaricare il file da S3, mandarlo a LLM con vision (GPT-4o o Gemini) per estrarre dal receipt: importo, data, metodo di pagamento, nome banca
- **Nodo Compare**: confrontare i dati estratti con le transazioni gr8 del player — c'è un match di importo e data?
- **Nodo Decision**: se match → `APPROVED`, se non match → `REJECTED`, se dubbio → `PENDING_REVIEW`

#### 2. Telegram Bot Notification
Dopo lo screening, mandare i risultati a un bot Telegram:
- Player ID, nome, email
- Screenshot/PDF del proof (s3_url)
- Risultato screening (APPROVED/REJECTED/PENDING)
- Transazioni recenti da gr8
- Link diretto al ticket (se escalation)

### P1 — IMPORTANTE (Entro 1 settimana)

#### 3. Presigned URL per Upload
Attualmente il widget chiama `/webhook/presigned-url` che non esiste come workflow attivo. Serve:
- Creare workflow n8n che genera presigned URL per S3
- O usare un servizio alternativo (Cloudflare R2, Firebase Storage)

#### 4. CDN Cache Fix
jsDelivr ha cache aggressiva su `@main` — le modifiche possono metterci 5-10 minuti a propagarsi. Soluzioni:
- Usare commit hash nel tag GTM (aggiornare manualmente)
- Migrare a GitHub Pages come CDN
- Aggiungere versioning al file (`widget.js?v=XXX`)

#### 5. Widget Mobile — Tastiera
Il gap tra widget e tastiera iOS non è perfetto. Potrebbe servire testing su più dispositivi e una soluzione CSS più robusta.

### P2 — NICE TO HAVE (Entro 2 settimane)

#### 6. Deposit Flow Completo
- Verificare deposito in real-time via gr8 paymentTransactionV2
- Se deposito trovato "in processing" → dire al cliente di aspettare
- Se deposito non trovato → chiedere proof e fare screening

#### 7. Widget → GR8 Bidirezionale
- Quando utente chiede saldo → query gr8 walletProxyTransaction
- Quando utente chiede stato KYC → query gr8 playerProfile
- Quando utente chiede bonus attivo → query gr8 (se disponibile)

#### 8. Analytics Dashboard
- Trackare ogni interazione widget (messaggi, escalation, deposit flow)
- Dashboard con metriche: tempo risposta, CSAT medio, escalation rate
- Integrare con GA4 via GTM

---

## Credenziali & Endpoint

| Risorsa | Valore |
|---|---|
| GitHub Repo | `stepbystepautomatization-jpg/betonwin-widget` |
| CDN | `cdn.jsdelivr.net/.../betonwin-widget@main/widget.js` |
| n8n | `https://n8nbeton.online` |
| GR8 API | `https://apg-s2s.com/v1/data-api/business-objects` |
| GR8 Client ID | `S2S_BTH_DataAPI_GraphQL_DC0_Prod_Client` |
| GR8 Brand | BOW (operator BTH) |
| GTM | BOW2-PROD, versione 9 |

## Workflow n8n Attivi

| Workflow | Webhook | Funzione |
|---|---|---|
| BetonWin AI Support v3.0 | `/webhook/884acc5b-...` | Chat AI (10 agenti) |
| BetonBot — Zendesk Escalation | `/webhook/escalate`, `agent-poll`, `agent-reply` | Live agent |
| webhook GR8 | `/webhook/99a8f6ae-...` | Proxy GraphQL generico |
| Deposit Proof Screening | `/webhook/deposit-screening` | Screening deposito |
| Sync Google Drive → Pinecone | `/webhook/sync-pinecone` | KB sync |
