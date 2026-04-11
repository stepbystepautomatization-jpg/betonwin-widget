# BetonWin — Zendesk Custom Fields Map
## Bot Escalation Auto-Classification

> Questo documento descrive come il bot classifica automaticamente i ticket
> quando scala la conversazione a un agente su Zendesk.
> I custom fields vengono compilati in base alle keyword trovate nei messaggi dell'utente.

---

## Field IDs Reference

| Field | Zendesk ID | Descrizione |
|-------|-----------|-------------|
| Topic | 27822230404498 | Categoria principale del ticket |
| Type of Contact | 29374195005842 | Tipo di contatto |
| User Level | 29328409050002 | Livello utente (sempre "regular") |
| Player ID | 31755319126162 | ID giocatore |
| Comments | 29328398594194 | Note interne |
| User Description | 31755504800274 | Descrizione utente |
| Payment Gateway | 31755408615186 | Gateway pagamento |
| Bonus Type | 30077296748690 | Tipo bonus |

---

## L1 Fields (uno per categoria)

| Categoria | Field Name | Zendesk ID |
|-----------|-----------|-----------|
| General | l1_general | 29325850558226 |
| Account | l1_account | 29326311046674 |
| Issues (Tech) | l1_issues | 29328446391826 |
| Verification | l1_verification | 29328650807698 |
| Product | l1_product | 29328730258578 |
| Promotions | l1_promotions | 29328737528210 |
| Withdrawal | l1_withdrawal | 29342186376978 |
| Deposits | l1_deposits | 29343098504722 |
| VIP | l1_vip | 29355517674514 |

## L2 Fields

| Field Name | Zendesk ID | Usato quando |
|-----------|-----------|-------------|
| l2_generic | 29328460161170 | Generico |
| l2_close_account | 29409342498962 | Chiusura account |
| l2_technical | 29409525919122 | Problemi tecnici |
| l2_deposit_status | 29409941644946 | Stato deposito |
| l2_withdrawal_st | 29409875818514 | Stato prelievo |
| l2_retracted | 29409706402578 | Bonus ritirato |
| l2_general_info | 30077324458770 | Info generali |
| l2_sport_bonus | 30415840160402 | Bonus sportivo |
| l2_unable_wd | 30507848552978 | Non riesce a prelevare |
| l2_vip_perks | 29409981824146 | Perks VIP |
| l2_vip_follow | 29409918499986 | Follow-up VIP |
| l2_non_technical | 29971583191058 | Non tecnico |
| l2_verification | 29409640707474 | Verifica |

## L3 Fields

| Field Name | Zendesk ID | Usato quando |
|-----------|-----------|-------------|
| l3_generic | 29343027897362 | Generico |
| l3_deposit_decl | 30079878798994 | Deposito rifiutato |
| l3_ws_declined | 29409820641682 | Prelievo rifiutato |
| l3_ws_pending | 29409846114066 | Prelievo pendente |

---

## Classificazione per Categoria

### 1. DEPOSITS
**Topic:** `deposit` | **Priority:** high/medium

| L1 Value | Trigger Keywords | Type of Contact | Priority |
|----------|-----------------|-----------------|----------|
| `deposit_not_reflected` | no acreditado, not reflected, no aparece, not showing, non arrivato, não chegou | non_technical_issue | high |
| `deposit_delay` | delay, tarda, demora, ritardo | non_technical_issue | high |
| `deposit_status` | status, estado, pending | question | medium |
| `payment_methods_offered` | method, metodo | question | medium |
| `how_to_deposit` | como, how | question | medium |
| `general_info___` | (default) | question | medium |

**L2 (solo se L1 = deposit_status):**

| L2 Value | Trigger Keywords |
|----------|-----------------|
| `declined4` | rechazado, declined, rejected |
| `pending4` | pendiente, pending |
| `approved4` | (default) |

---

### 2. WITHDRAWAL
**Topic:** `withdrawal` | **Type:** non_technical_issue

| L1 Value | Trigger Keywords |
|----------|-----------------|
| `withdrawal_satus` | rechazado, rejected, declined, status, estado, pending |
| `cancel_request2` | cancelar, cancel |
| `withdrawal_limit_` | limite, limit |
| `unable_to_withdraw` | verificar, verify, unable, no puedo |
| `how_to_withdrawal` | como, how |
| `general_info___3` | (default) |

**L2 (se L1 = withdrawal_satus):**

| L2 Value | Trigger Keywords |
|----------|-----------------|
| `declined12` | rechazado, declined |
| `pending12` | pendiente, pending |
| `approved12` | (default) |

**L2 (se L1 = unable_to_withdraw):**
→ `incomplete_verification` (field: l2_unable_wd)

---

### 3. PROMOTIONS
**Topic:** `promotions` | **Type:** lack_of_customer_knowledge | **Priority:** low

| L1 Value | Trigger Keywords |
|----------|-----------------|
| `cashback_bonus` | rollover, wagering, terms, condiciones |
| `retracted_bonus` | expired, expirado, retracted |
| `deposit_bonus__` | locked, bloqueado |
| `free_bet_bonus` | cancel, cancelar |
| `daily_bonus_info` | loyalty, hero, fidelidad |
| `sport_bonus_` | sport, deportivo |
| `promo_code_` | codigo, code, promo code |
| `bonus_request2` | request, solicitar, pedir |
| `other5` | (default) |

---

### 4. VERIFICATION
**Topic:** `verification` | **Type:** question

| L1 Value | Trigger Keywords | Priority |
|----------|-----------------|----------|
| `email_verification` | email, correo | medium |
| `phone_verification` | phone, telefono, sms | medium |
| `verification3` | status, estado, declined, rechazado | medium |
| `user_unable_to_verify_account` | unable, no puedo, non riesco | **urgent** |
| `risk_verification` | risk | medium |
| `how_to_verify` | como, how | medium |
| `other19` | (default) | medium |

**L2 (se L1 = verification3):**

| L2 Value | Trigger Keywords |
|----------|-----------------|
| `declined1` | declined, rechazado |
| `completed1` | (default) |

---

### 5. ACCOUNT
**Topic:** `customer_support` | **Type:** request

| L1 Value | Trigger Keywords | Priority |
|----------|-----------------|----------|
| `password_reset` | contraseña, password | medium |
| `request_to_close_account` | cerrar, close | medium |
| `duplicated_account_` | duplicada, duplicate | **urgent** |
| `account_restrictions` | bloqueada, blocked, restricted | **urgent** |
| `update_email` | email | medium |
| `update_phone_number` | telefono, phone | medium |
| `change_personal_details` | datos, personal | medium |
| `balance_info` | saldo, balance | medium |
| `general_questions2` | (default) | medium |

---

### 6. ISSUES (Technical)
**Topic:** `website_complaints` | **Type:** technical_issue | **Priority:** urgent

| L1 Value | L2 Field | L2 Value | Trigger Keywords |
|----------|----------|----------|-----------------|
| `technical` | l2_technical | `troubleshooting` | login, iniciar sesion, accedere |
| `technical` | l2_technical | `client_cant_log_in1` | crash, congelado, frozen |
| `technical` | l2_technical | `unknown_error1` | lento, slow |
| `technical` | l2_technical | `blocked_game1` | error |
| `technical` | l2_technical | `troubleshooting` | (default) |

---

### 7. PRODUCT (Casino / Sports)
**Topic:** `casino` o `bets` | **Type:** question | **Priority:** low

| L1 Value | Trigger Keywords |
|----------|-----------------|
| `slot_general_info` | slot |
| `live_casino_info` | live |
| `casino_general_info` | casino |
| `sportbet_general_info` | apuesta, bet |

---

### 8. VIP
**Topic:** `vip` | **Type:** request | **Priority:** medium

| L1 Value | Trigger Keywords |
|----------|-----------------|
| `vip_follow_up_1` | missed, follow |
| `vip_perks1` | (default) |

---

### 9. GENERAL (default)
**Topic:** `general_questions` | **Type:** question | **Priority:** low

| L1 Value | Trigger Keywords |
|----------|-----------------|
| `how_to_register` | register, registrar |
| `how_to_play` | play, jugar |
| `refund_request` | refund, reembolso |
| `terms_and_conditions_` | terms, terminos |
| `privacy_policy` | privacy, privacidad |
| `general_questions1` | (default) |

---

### LEGAL THREAT (override)
**Topic:** `legal_questions` | **Type:** request | **Priority:** urgent
> Sovrascrive qualsiasi altra categoria. Trigger: keyword legali nel messaggio.

---

## Type of Contact Values

| Value | Quando |
|-------|--------|
| `question` | Domande informative |
| `request` | Richieste di azione (chiusura account, VIP, ecc.) |
| `non_technical_issue` | Problemi non tecnici (deposito mancante, prelievo) |
| `technical_issue` | Problemi tecnici (crash, errori, login) |
| `lack_of_customer_knowledge` | Il cliente non sa come funziona (bonus, promo) |

## Priority Values

| Value | Quando |
|-------|--------|
| `urgent` | Minacce legali, account bloccato, verifica impossibile, problemi tecnici |
| `high` | Deposito non arrivato, deposito in ritardo, escalation umana |
| `medium` | Account, verifiche, prelievi, VIP |
| `low` | Promozioni, prodotto, domande generali |

---

## Come funziona la classificazione

1. Il bot raccoglie tutti i messaggi dell'utente dalla conversazione
2. Conta le keyword per ogni categoria (deposits, withdrawal, promotions, ecc.)
3. La categoria con più match vince
4. In base alla categoria, seleziona il valore L1 più specifico
5. Se applicabile, seleziona anche L2 e L3
6. Compila i custom fields di Zendesk automaticamente

## Keywords di classificazione

### Deposits
`deposit, deposito, depositar, depósito, webpay, mach, mercado pago, recarga, acreditar, payment method, metodo de pago`

### Withdrawal
`retiro, retirar, withdrawal, withdraw, cobrar, sacar plata, sacar dinero, saque, prelievo, prelevare`

### Promotions
`bono, bonus, promo, rollover, wagering, giro gratis, free spin, cashback, fidelidad, hero, codigo promo`

### Verification (KYC)
`verificacion, verificación, kyc, documento, dni, pasaporte, identidad, selfie, verificar, verify`

### Account
`cuenta, contraseña, password, registro, login, bloqueada, duplicada, cerrar cuenta, close account, password reset`

### Technical Issues
`error, bug, no funciona, no carga, lento, crash, congelado, frozen, not working, not loading, pantalla`

### Product
`casino, slot, ruleta, blackjack, rtp, juego, poker, roulette, tragamoneda, apuesta, bet, parlay, cash out`

### VIP
`vip, exclusive, cumpleaños, birthday, anniversary`
