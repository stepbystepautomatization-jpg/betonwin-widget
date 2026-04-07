# BetonWin Support Widget — Documentazione Completa

> Questo file è la fonte di verità per tutto il sistema BetonWin Support.
> Claude lo legge automaticamente all'inizio di ogni conversazione.
> Aggiornare questo file ad ogni modifica significativa.

---

## 1. PANORAMICA DEL SISTEMA

Il sistema BetonWin Support è un chatbot AI per il sito di gambling beton.win.
Composto da 4 componenti principali:

```
WIDGET (frontend)  →  n8n (backend AI)  →  Pinecone (KB vettoriale)  →  Google Drive (fonte dati)
     ↕                      ↕
  Zendesk              Google Apps Script
(live agent)           (KB search API)
```

**Mercati**: Chile (CLP), Argentina (ARS)
**Lingue**: Español (default), English, Italiano, Português
**Sito**: beton.win | URL alternativa: beton691.online
**Email soporte**: ayuda@beton.win

---

## 2. WIDGET (widget.js)

### File e struttura
- **widget.js** — File singolo embeddabile (~1600 righe), tutto CSS inline
- **widget.html** — Pagina demo standalone
- **test.html** — Pagina test locale

### GitHub
- **Repo**: `stepbystepautomatization-jpg/betonwin-widget`
- **Branch**: `main`
- **CDN**: `https://cdn.jsdelivr.net/gh/stepbystepautomatization-jpg/betonwin-widget@main/widget.js`
- **Purge cache dopo push**: `https://purge.jsdelivr.net/gh/stepbystepautomatization-jpg/betonwin-widget@main/widget.js`

### Configurazione (CONFIG)
```
N8N_BASE: https://n8nbeton.online
KB_URL: https://script.google.com/macros/s/AKfycbw4QH_cxD2HmW18ReyCUzo4BDPwrHeUaMwYKxXnjwSNc0yhPxCAFqZRkI6dDBD5y0ZI/exec
```

### Endpoint n8n usati dal widget
| Endpoint | Funzione |
|---|---|
| `/webhook/884acc5b-3a84-44cc-8f44-7c1b7df3df2a` | Chat principale (messaggio → AI → risposta) |
| `/webhook/verify-deposit` | Verifica deposito |
| `/webhook/status` | Status deposito |
| `/webhook/presigned-url` | URL pre-firmato per upload file |
| `/webhook/analyze` | Analisi documento caricato |
| `/webhook/escalate` | Escalation a Zendesk |
| `/webhook/agent-poll` | Polling risposte agente Zendesk |
| `/webhook/agent-reply` | Invio messaggio a agente Zendesk |

### Flussi del Widget
```
CHAT → DEPOSIT_ASK_ID → DEPOSIT_CHECKING → UPLOAD_REQUIRED → UPLOADING → ANALYZING → RESULT
CHAT → ESCALATING → LIVE_AGENT → AGENT_CLOSED
```

### Funzionalità widget
- **Chat AI** con knowledge base (ricerca Drive + n8n AI)
- **Verifica depositi** — flusso completo: Player ID → controllo stato → upload prova → analisi AI → risultato
- **Escalation intelligente**:
  - Minacce legali → escalation immediata (keyword: avvocato, denuncia, lawsuit, abogado, demanda...)
  - Richieste operatore umano → AI detection. Dopo 3 segnali → auto-escalate a Zendesk
  - `humanRequestCount` si resetta dopo escalation fallita (previene loop infinito)
- **Live agent** via Zendesk:
  - Nome reale agente da Zendesk (via `?include=users` sideload)
  - Typing indicator personalizzato ("María thinking..." / "BetonWin AI thinking...")
  - Chat si chiude SOLO su Zendesk status `closed` (non `solved` o `pending`)
- **CSAT rating** (1-5 stelle) dopo chiusura ticket
- **4 lingue** (EN/ES/IT/PT) con auto-detect da testo utente
- **Emoji picker** (24 emoji contestuali)
- **Fullscreen mode**
- **Notifiche sonore** per nuovi messaggi
- **Messaggio proattivo** dopo 30 secondi di inattività
- **Upload file** (JPG/PNG/PDF, max 10MB) con presigned URL
- **Session UUID** (v4) per analytics correlation
- **Auto-detect Player ID** da: localStorage, cookies, DOM, `window.__USER__`

### Sicurezza widget
- Rate limit: 1 msg/sec, max 1000 chars
- Max 100 messaggi per sessione
- Safety timer: auto-recovery dopo 30s se bloccato
- Sanitizzazione input

---

## 3. n8n — WORKFLOW CHAT (BetonWin AI Support v3.0 — 10 Agents)

**Workflow ID**: `CfS-ypkrpmP5fq-SB1qKN`
**URL**: `https://n8nbeton.online`
**API Key**: configurata nel progetto

### Architettura
```
Webhook → Extract Query → Router (categorizza + rileva lingua) → Category Switch → Agente specializzato → Format Response → Respond
```

### Router
Il Router analizza il messaggio e determina:
1. **Lingua** (en/es/it/pt) — basato su phrase matching
2. **Categoria** — basato su keyword scoring con priority rules

### 10 Agenti specializzati
Ogni agente ha: LLM (OpenRouter), Memory (buffer window), Pinecone KB (namespace specifico), System Prompt con REGLAS.

| Agente | Namespace Pinecone | Ambito |
|---|---|---|
| Deposits Agent | `kb_deposit` | Depositi, metodi, problemi deposito |
| Withdrawals Agent | `kb_withdrawal` | Retiri, stati, problemi retiro |
| Bonuses Agent | `kb_bonos` | Bonus, promozioni, rollover, fidelidad |
| Verification Agent | `kb_verification` | KYC, telefono, email, documenti |
| Account Agent | `kb_account` | Cuenta, accesso, dati personali, saldo, juego responsable |
| Technical Agent | `kb_issues` | Problemi tecnici, errori, troubleshooting |
| Sports Agent | `apuestas_deportivas` | Scommesse sportive, cuotas, eventi |
| Casino Agent | `kb_casino` | Casino, slots, live casino, RNG |
| Balance Agent | `kb_account` | Saldo, balance locked (condivide namespace con Account) |
| General Agent | `guias` | Piattaforma, app, lingue, collaborazioni, soporte |

### REGLAS DE COMPORTAMIENTO (iniettate in tutti i 10 agenti)
1. **IDIOMA**: Rispondere SEMPRE nella lingua del cliente
2. **BREVEDAD**: Max 150 parole, non ripetere info già date
3. **PAÍS**: Chiedere paese prima di dare info depositi/retiri
4. **CANALES**: Chat en vivo come prima opzione, email come seconda
5. **TRANQUILIZAR**: Quando si parla di soldi → "Tu dinero está seguro" prima di tutto
6. **TROUBLESHOOTING**: Sempre troubleshooting base prima di escalare
7. **CONSISTENCIA**: Stesso livello di dettaglio loggato o non loggato
8. **NO ASUMIR**: Chiedere chiarimenti se manca info
9. **EMPATÍA**: Se frustrazione → empatia prima di info tecnica
10. **VIP**: Se VIP → contatto agente personale WhatsApp/email

### Dati critici nei system prompt degli agenti
- **Account Agent**: Nome/DOB/paese NON modificabili. Dispositivi condivisi: T&C 61.4
- **Bonuses Agent**: Cancellazione bonus solo se NON usato. Notifiche ≠ bonus disponibili
- **Technical Agent**: 1 solo gioco funzionante = problema server, NON cache
- **General Agent**: Collaborazioni → Telegram @Sh0kunin

---

## 4. n8n — WORKFLOW SYNC (Sync Google Drive → Pinecone)

**Workflow ID**: `jgWqM7M7U24IVw_gspQUZ`
**Trigger**: Ogni 6 ore automatico + webhook manuale `POST /webhook/sync-pinecone`

### Flusso
```
Trigger → Define Folders (root ID) → Web App (legge Drive) → Extract Files → Code Chunking (paragrafi, max 1500 chars) → OpenAI Embeddings → Prepare Pinecone Body → Upsert Pinecone
```

### Parametri chunking
- **Max chunk**: 1500 chars
- **Min chunk**: 200 chars
- **Split**: per paragrafo (\\n\\n) — MAI a metà frase
- **No _global duplication**: le REGLAS sono nei system prompt, non duplicati in Pinecone

---

## 5. PINECONE (Knowledge Base vettoriale)

**Index**: `kb-betonwin-prod`
**URL**: `https://kb-betonwin-prod-g67tsy0.svc.aped-4627-b74a.pinecone.io`
**Dimensione embedding**: 1536 (OpenAI text-embedding-3-small)
**Vettori totali**: ~112

### Namespace e contenuto
| Namespace | Vettori | File | Chars |
|---|---|---|---|
| `kb_bonos` | 41 | 12 | 76K |
| `kb_account` | 17 | 13 | 21K |
| `kb_deposit` | 14 | 9 | 19K |
| `kb_withdrawal` | 12 | 9 | 14K |
| `kb_verification` | 11 | 9 | 12K |
| `apuestas_deportivas` | 4 | 3 | 11K |
| `kb_issues` | 7 | 4 | 6K |
| `kb_casino` | 3 | 2 | 10K |
| `guias` | 3 | 2 | 3K |

---

## 6. GOOGLE DRIVE — Struttura KB

**Root folder ID**: `1wgj11oLcZ6WXPluSoUksQ8vX8wCZhRVy`

```
BetonWin KB/
├── _global/                     → REGLAS + SOPORTE (non duplicato in Pinecone)
│   ├── reglas_bot
│   └── soporte
├── _archive/                    → FAQ monolitica originale (backup)
├── kb_deposit/        (9 file)  → Depositi: how-to, metodi, delay Chile/AR, fallidi, issues AR
├── kb_withdrawal/     (9 file)  → Retiri: how-to, status, delay, limiti, cancel
├── kb_bonos/         (12 file)  → Bonos: FAQ, escenarios, loyalty, abusers, deportivos, release limit
├── kb_verification/   (9 file)  → KYC: how-to, telefono, email, risk verification
├── kb_account/       (13 file)  → Account: cierre, duplicati, cambio dati, balance, password, bloqueo
├── kb_issues/         (4 file)  → Problemi: tecnici, non-tecnici, troubleshooting
├── apuestas_deportivas/ (3 file) → Sport: guía completa, revisione apuestas
├── kb_casino/         (2 file)  → Casino: FAQ, guía casino online
└── guias/             (2 file)  → General: app móvil, colaboraciones
```

**Totale**: 63 file, 172K chars di contenuto

### Cartelle sorgente operative (documenti di training agenti)
Queste cartelle contengono i documenti operativi originali. Lo script `integrate_kb.gs` li filtra (rimuove dati sensibili) e li copia nella KB.

| ID Cartella | Nome | Namespace |
|---|---|---|
| `1247LFqi5TzaK8f6Jra-8P-awuQuCgLfg` | 02_KB_Account | kb_account |
| `1jW_LRG6Sn5Ky_51WlDl67CAm9PGXuj2O` | 03_KB_Deposits | kb_deposit |
| `1a-_NdQfZ4g7hfYpek8zon1OqtNkrEOfG` | 04_KB_Withdrawal | kb_withdrawal |
| `1FzPeQm4ReY16BH1wSlsQkpOfbBPI4Dvz` | 05_KB_Verification | kb_verification |
| `1WltePG7_jajQ0TyptP-U9LU3OulhpCzF` | 06_KB_Bonos | kb_bonos |
| `1rPlaiaqMVkSERSFP0CcjYg0zeggQKH9A` | 09_KB_Issues | kb_issues |
| `12xDA0wjsGrhkXQdcy6fVFsZCkAG8suMM` | 10_Apuestas_Deportivas | apuestas_deportivas |

Cartelle NON integrate (solo processi interni/credenziali):
- 07_Categorizacion_SOP, 08_QA_Information, 11_Escalaciones, 12_Escalacion_CRM, 13_Additional_Tasks

---

## 7. GOOGLE APPS SCRIPT

### 7.1 KB Search API (usata dal widget)
- **URL**: `https://script.google.com/macros/s/AKfycbw4QH_cxD2HmW18ReyCUzo4BDPwrHeUaMwYKxXnjwSNc0yhPxCAFqZRkI6dDBD5y0ZI/exec`
- **Funzione**: Cerca nel Drive per fullText, ritorna risultati con contenuto
- **Usata da**: widget.js (ricerca KB prima di mandare a n8n)
- **NON TOCCARE** — il widget la usa in produzione

### 7.2 Sync Export Web App (usata dal sync workflow n8n)
- **URL**: `https://script.google.com/macros/s/AKfycbzvcodD0C4-zr5mcqEeuQA5ife62lhcx0-AoF_N2EgWOl_p-2i4Ur6C0ZtGg8fjd-8YBg/exec`
- **Funzione**: Legge sottocartelle del Drive, ritorna file organizzati per namespace con _global prepended
- **Parametri**: `?folderId=ROOT_ID` (tutti) o `?folderId=ROOT_ID&ns=kb_bonos` (specifico)
- **Usata da**: n8n sync workflow

### 7.3 Script di utilità (sul Desktop, NON deployati)
- **restructure_kb.gs** — Crea struttura cartelle + splitta FAQ per sezione
- **integrate_kb.gs** — Copia documenti dalle cartelle operative alla KB, filtra dati sensibili
- **scan_folders.gs** — Scansiona cartelle e mostra contenuto

---

## 8. ZENDESK — Escalation e Live Agent

### Flusso escalation
1. Widget rileva necessità di escalation (minaccia legale O 3+ richieste operatore)
2. Widget chiama `/webhook/escalate` con conversazione
3. n8n crea ticket Zendesk
4. Widget passa in modalità LIVE_AGENT
5. Widget fa polling su `/webhook/agent-poll` per risposte agente
6. Utente può mandare messaggi e file all'agente via `/webhook/agent-reply`
7. Ticket si chiude SOLO quando Zendesk status = `closed`

### Escalation triggers
- **Minacce legali** (immediato): keyword locali in tutte le lingue
  - ES: abogado, demanda, denuncia, tribunal, fiscal
  - IT: avvocato, denuncia, tribunale, causa legale
  - EN: lawyer, lawsuit, legal action, sue
  - PT: advogado, processo, denúncia
- **Richiesta umano** (dopo 3 detection): AI-based, analizza risposta dell'agente per segnali di "il cliente vuole parlare con una persona"

### Zendesk config
- Agent name reale mostrato nel widget (sideload `?include=users`)
- CSAT (1-5 stelle) dopo chiusura ticket
- Custom fields: vedi `ZENDESK_CUSTOM_FIELDS_MAP.md`

---

## 9. ESCALATION — MINACCE LEGALI

Quando un utente usa parole che indicano intenzione di azione legale, il widget bypassa completamente l'AI e scala immediatamente a un agente umano via Zendesk. Questo è un meccanismo di sicurezza critico.

### Keyword monitorate (funzione `detectLegalThreat` in widget.js)
Le keyword sono hardcoded nel widget e copono ES, IT, EN, PT.

---

## 10. COMANDI OPERATIVI

### Sync Pinecone manuale
```bash
curl -X POST "https://n8nbeton.online/webhook/sync-pinecone" -H "Content-Type: application/json" -d '{}'
```

### Purge CDN dopo push widget
```bash
curl "https://purge.jsdelivr.net/gh/stepbystepautomatization-jpg/betonwin-widget@main/widget.js"
```

### Check stato Pinecone
```bash
curl "https://kb-betonwin-prod-g67tsy0.svc.aped-4627-b74a.pinecone.io/describe_index_stats" \
  -H "Api-Key: [API_KEY]" -d '{}'
```

### n8n API
```bash
# Lista workflow
curl "https://n8nbeton.online/api/v1/workflows" -H "X-N8N-API-KEY: [API_KEY]"

# Dettagli workflow
curl "https://n8nbeton.online/api/v1/workflows/[WORKFLOW_ID]" -H "X-N8N-API-KEY: [API_KEY]"
```

---

## 11. PROBLEMI NOTI E LIMITAZIONI

- **I6 (1 solo gioco)**: L'agente Technical suggerisce ancora cache come prima soluzione invece di problema server — il contenuto giusto è nella KB ma non sempre viene recuperato
- **W7 (perché prima potevo retirare)**: Menziona "cambios en T&C" genericamente — dovrebbe dire "nuovo deposito con bonus resetta wagering"
- **Widget kb_content ignorato da n8n**: Il widget manda `kb_content` dalla ricerca Drive, ma n8n lo ignora completamente (usa solo Pinecone). Il campo esiste nel payload ma non viene usato
- **Sync upsertedCount**: Il webhook ritorna sempre il count dell'ultimo batch, non il totale. Non è un errore, i vettori vengono tutti caricati

---

## 12. STORICO MODIFICHE

### v4.0 (Aprile 2026)
- Ristrutturazione completa KB: da 1 file monolitico a 63 file in 9 cartelle
- Fix namespace: Casino (`apuestas_deportivas` → `kb_casino`), Balance (`guias` → `kb_account`)
- REGLAS DE COMPORTAMIENTO iniettate nei 10 agenti
- Smart chunking: paragrafi, max 1500 chars, no split a metà frase
- Integrazione 44 documenti dalle cartelle operative (filtrati dati sensibili)
- Fix Router: +30 frasi inglesi per detection lingua
- Fix system prompt: dati critici Account, Bonuses, Technical, General (@Sh0kunin)
- Web App Sync aggiornata: supporto multi-folder con _global
- KB: 172K chars, 112 vettori, 9 namespace

### v3.0 (Marzo 2026)
- UI premium redesign, ottimizzazione mobile
- Agent polling fix (since=0 + dedup)
- Session UUID per analytics
- AI-based human escalation detection
- Emoji picker, fullscreen, typing indicator
- CSAT rating dopo chiusura ticket

### v2.0 (Marzo 2026)
- Live agent via Zendesk con nome reale
- Auto-detect Player ID
- 4 lingue (EN/ES/IT/PT)
- Security hardening
