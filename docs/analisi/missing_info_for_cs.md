# BetonWin — Missing Information Request for CS Team
## Based on 35,963 Ticket Analysis (Jul 2025 – Feb 2026)

**Purpose:** This document contains questions that our AI widget CANNOT answer today. We need the CS team to provide the correct answers so we can add them to the Knowledge Base and automate these responses.

**IMPORTANT:** This document does NOT repeat the 64 questions already sent in "domande_senza_risposta.md". These are ADDITIONAL information gaps discovered after expanding the analysis from 26,963 to 35,963 tickets (adding Jan–Feb 2026 data).

**How to use this document:**
1. Read each question carefully — the "Why we need this" explains the real customer problem
2. Write the correct answer in the **"Answer"** field
3. If the answer depends on the country, specify: "Chile: X, Argentina: Y"
4. If you're unsure, write "TO VERIFY — ask [person/team]"
5. If not applicable, write "N/A" and why

---

## SECTION A — Greeting & First-Contact Handling
**Impact: 8,949 tickets (24.9% of all volume) — ~1,119/month**

These are users who open chat with just "hola" or "buenas" and no question. The AI already handles 95% of these, but we need to improve the remaining 5%.

| # | Question | Why we need this | Answer |
|---|---|---|---|
| A.1 | When a user sends only a greeting ("hola", "buenas"), what is the ideal first response? Should the bot list the main help categories or ask an open question like "How can I help you?" | Currently the bot greets back and asks "how can I help?" — but 15% of users still don't ask a question after the bot responds. We need a more proactive response that guides them. | |
| A.2 | Should the bot send a quick-action menu with buttons (e.g., "Deposit", "Withdrawal", "Bonus", "KYC", "Other") after a greeting, or just text? | 8,949 tickets are just greetings. Quick-action buttons could immediately route 70%+ of these to the right flow without waiting for the user to type a second message. | |
| A.3 | If a user sends only a greeting and then goes silent (no second message for 2+ minutes), what should the bot do? Send a follow-up? Close the chat? After how many minutes? | ~10% of greeting-only tickets end with the user abandoning the chat. Agents currently waste time waiting. | |
| A.4 | What languages should the greeting response support? Currently we have ES/EN/IT/PT. Are there other languages users write in? (e.g., German, French for European markets) | Some users write greetings in unexpected languages. | |

---

## SECTION B — Bank Transfer: Operational Details
**Impact: 4,407 tickets (12.3%) — ~551/month — RISING SHARPLY (+271% in 6 months)**

> **Note:** Questions about bank account details, comprobante requirements, and processing times are already in "domande_senza_risposta.md" (Section 1, Q1.1–1.10). The questions below are DIFFERENT — they cover operational patterns we discovered in the Jan–Feb 2026 data.

| # | Question | Why we need this | Answer |
|---|---|---|---|
| B.1 | Bank Transfer tickets exploded from 296/month (Jul 2025) to 1,100/month (Dec 2025). **Was there a change in payment provider, a promotion pushing bank transfers, or a new market launched?** We need to understand the root cause to design the right AI response. | If we know WHY transfers increased, we can proactively address the cause (e.g., if Directa24 was added, we need specific Directa24 instructions). | |
| B.2 | When a user sends a comprobante image in the chat, **does the current human workflow involve checking it manually, or is there an automated system?** Describe the exact steps an agent takes after receiving a comprobante. | We're building an automated comprobante verification flow in the widget. We need to know the current manual process to replicate it correctly. | |
| B.3 | **What are the most common reasons a bank transfer deposit is NOT credited even after sending a valid comprobante?** List the top 5 reasons in order of frequency. | Real ticket: *"Son 4 recargas de 5000 peso. Necesito una respuesta"* — Some users send multiple transfers that all get stuck. We need to explain why. | |
| B.4 | **Is there a maximum number of pending bank transfers per user?** Can a user have 3–4 unprocessed transfers at the same time? | We see users making multiple small transfers instead of one large one, creating multiple support tickets. | |
| B.5 | **What happens if a user makes a bank transfer but forgets to include the reference code?** Can the deposit still be matched? How? | Many tickets show transfers without references. The current KB doesn't explain what to do. | |
| B.6 | **Chile-specific: Does "Cuenta RUT" from Banco Estado work for both deposits AND withdrawals?** Multiple users report it doesn't appear as an option for withdrawals. | Real ticket: *"Consulta para retirar — no sale la opción de banco estado, cuenta rut"* — This is a recurring issue. | |

---

## SECTION C — Phone & Email Verification (67.5% of KYC tickets)
**Impact: 2,096 tickets — ~262/month**

> **Note:** "domande_senza_risposta.md" Section 4 covers document KYC (ID uploads, photo quality, proof of address). But **67.5% of KYC tickets are actually about phone/email verification** — a completely different issue. These questions are NOT in the previous document.

| # | Question | Why we need this | Answer |
|---|---|---|---|
| C.1 | **Step-by-step: how does a user verify their phone number?** My Account > Settings > ...? What happens after they click "Verify"? SMS code? How many digits? | Real ticket: *"En las misiones me pide confirmar teléfono y correo pero no sé cómo hacerlo"* — Users don't know the exact path. | |
| C.2 | **The SMS verification code doesn't arrive. What are the most common reasons?** (Wrong number format? Carrier blocking? Country code missing?) What should the user try? | Real ticket: *"No puedo verificar mi número de teléfono. Cada vez que lo subo me arroja error"* — This is the #1 KYC issue. | |
| C.3 | **If a user entered the WRONG phone number during registration, can they change it themselves? Or do they need to contact support?** What verification does support require to change it? | Real ticket: *"Escribí mal mi número de celular y no sé como corregirlo"* — Extremely common. Agents say "tell me your number and I'll fix it" but the bot can't do that. | |
| C.4 | **Same question for email: if the user entered the wrong email (e.g., ".com" instead of ".cl"), can they change it themselves? What's the process?** | Real ticket: *"Me equivoqué y puse .com y termina en .cl, entonces no puedo verificarlo"* — Very frequent error. | |
| C.5 | **What phone number format is required?** Must include country code (+56 for Chile, +54 for Argentina)? With or without leading zero? Example for each country. | Users enter numbers in different formats and get errors. We need the exact format so the bot can validate before submission. | |
| C.6 | **Email verification: what does the user receive?** A link? A code? How long is it valid? What if it goes to spam? Can they re-send it? | Real ticket: *"No puedo confirmar mi correo. Lo pongo y me dice que van a mandar un mensaje"* — Users don't know what to expect. | |
| C.7 | **Is phone + email verification mandatory for ALL users, or only for certain actions?** (e.g., required before first withdrawal? Required for Hero/Loyalty program? Required for deposits over X amount?) | Some users say they're blocked from playing because they haven't verified. Others play fine without it. We need to clarify when it's mandatory. | |
| C.8 | **The "secret question" — what is it? When is it set up? What if the user doesn't remember the answer?** | Real ticket: *"No recuerdo la respuesta a mi pregunta secreta"* — Agents verify identity via document photo. The bot needs to explain this process. | |

---

## SECTION D — "Saldo 0.00" with Active Bonus (Deep Dive)
**Impact: Part of 6,358 Bonus tickets + many Casino tickets — estimated ~400/month**

> **Note:** "domande_senza_risposta.md" Q5.1 asks about this briefly. But this is the SINGLE MOST CONFUSING issue for users, appearing across Bonus, Casino, and Balance tickets. We need a much more detailed explanation.

| # | Question | Why we need this | Answer |
|---|---|---|---|
| D.1 | **Explain in simple terms: why does "Saldo 0.00" appear when the user has a sports bonus active?** The KB says "sports bonuses require 50% real money + 50% bonus per bet" — but users don't understand this. We need a step-by-step example. | Real ticket: *"Cargué 50mil y me sale que no tengo saldo"* — User deposited $50,000 CLP, got a bonus, but can't play. This causes extreme frustration and fraud accusations. | |
| D.2 | **Concrete example with numbers:** If a user deposits $10,000 CLP and gets a 150% welcome bonus ($15,000 CLP), their total balance shows $25,000. But when they try to bet on sports, it shows "Saldo 0.00". WHY? And what should they do? | We need an example so clear that a 5th grader could understand it. The current KB explanation is too technical. | |
| D.3 | **Does "Saldo 0.00" also happen with casino bonuses, or only sports bonuses?** If a user has a casino bonus, can they play slots normally? | We see this issue across both sports and casino contexts. Need to clarify the difference. | |
| D.4 | **If the user doesn't want the bonus, how do they remove it BEFORE it's used?** Step-by-step: My Account > Promotions > Cancel Bonus? Will they lose their deposit? | Real ticket: *"Hola quiero renunciar al bono de bienvenida. Ya deposité"* — Users want to remove the bonus to access their real money. 248 tickets about bonus cancellation. | |
| D.5 | **After cancelling a bonus, does the real money (original deposit) become immediately available? Or is there a waiting period?** | Users cancel the bonus expecting instant access to their money. Does it work that way? | |

---

## SECTION E — Casino Winnings Not Credited
**Impact: 3,022 tickets (52.5% of Casino topic) — ~378/month**

> **Note:** "domande_senza_risposta.md" Section 6 covers game troubleshooting (loading, disputes, disconnection). These questions are about a DIFFERENT issue: users who won but the money didn't appear or they can't withdraw their winnings.

| # | Question | Why we need this | Answer |
|---|---|---|---|
| E.1 | **When a user wins in a slot or casino game, how quickly should the winnings appear in their balance?** Instantly? After the round ends? After a processing delay? | Real ticket: *"Gané 74.000 y no lo puedo retirar"* — User says they won but the balance doesn't reflect it. | |
| E.2 | **If a user wins but can't withdraw because of an active bonus, what is the maximum amount they can withdraw?** Explain the "Release Limit" calculation with a real example in local currency. | Real ticket: *"No puedo retirar mi saldo. Gasté mi crédito pero mi ganancia no la puedo retirar"* — The release limit concept is extremely confusing. | |
| E.3 | **If a game crashes/freezes mid-spin or mid-round, what happens to the bet?** Is the result determined server-side? Will the user see the result when they re-open the game? | Real ticket: *"Compré un bono de giros y aún me sale recopilando datos. Hace horas"* — User is stuck in a game that won't resolve. | |
| E.4 | **Jackpot wins — is there a different process for large wins?** Do they require additional verification? Is there a maximum payout? | Users who win large amounts face unexpected delays. Need to explain why. | |
| E.5 | **If a user believes their game result was unfair or rigged, what is the official investigation process?** Who reviews it? How long does it take? What evidence do they need to provide? | Real ticket: *"Me siento estafado. Ayer jugué y supuestamente..."* — We need a professional, transparent response. | |

---

## SECTION F — Withdrawal Blocked by Bonus (46.5% of withdrawal tickets)
**Impact: 401 tickets — ~50/month — but causes HIGH frustration**

> **Note:** "domande_senza_risposta.md" Q8.1 mentions this briefly. We need a COMPLETE flow because this single issue generates half of all withdrawal complaints.

| # | Question | Why we need this | Answer |
|---|---|---|---|
| F.1 | **When a user tries to withdraw with an active bonus, what EXACT error message do they see?** Provide the exact text shown on screen. | Users send screenshots of error messages. We need to recognize and explain each one. | |
| F.2 | **Step-by-step: how can a user check their current rollover/wagering progress?** My Account > Promotions > ...? What does the progress bar show? | Real ticket: *"Necesito que me ayuden. No entiendo qué más tengo que apostar en los bonos"* — Users don't know where to look. | |
| F.3 | **If the user decides to cancel the bonus to withdraw their real money, what is the EXACT process?** Screen by screen: where to click, what confirmation appears, what happens to their balance. | Real ticket: *"Hola necesito retirar dinero y no puedo. Quiero renunciar al bono"* — This is a critical self-service flow. If the bot can guide users through it, we save ~200 tickets/month. | |
| F.4 | **After completing the wagering requirement, is the withdrawal unlocked automatically? Or does the user need to do something?** | Some users complete wagering but still can't withdraw. Is there an additional step? | |
| F.5 | **"Saldo disponible" vs "Saldo total" vs "Saldo de bono" — provide the exact definitions and where each appears on the platform.** | Real ticket: *"Deposité, aparece en pesos que está, pero al tratar de jugar me aparece saldo 0 y al tratar de retirar lo mismo"* — Three different balance concepts confuse users constantly. | |

---

## SECTION G — Account Closure & Self-Exclusion
**Impact: 62 tickets/month — but HIGH sensitivity (responsible gambling compliance)**

> **Note:** Not covered in "domande_senza_risposta.md" at all.

| # | Question | Why we need this | Answer |
|---|---|---|---|
| G.1 | **What is the exact process to close an account?** Does the user need to have zero balance? How long does it take? Is it reversible? | Real ticket: *"Quiero darme de baja. No pienso jugar más en la página"* — Multiple users request this daily. | |
| G.2 | **What is the difference between "account closure" and "self-exclusion"?** Are they the same? Different durations? | Real ticket: *"TENGO UNA QUEJA POR QUÉ NO CERRARON MI CUENTA COMO LO SOLICITÉ"* — This user had asked for closure but the account was still active. Critical compliance issue. | |
| G.3 | **Self-exclusion options: what time periods are available?** (24h, 1 week, 1 month, 6 months, permanent?) Can the user choose? | Need specific options to list in the bot response. | |
| G.4 | **If a user requests account closure, what happens to their remaining balance?** Must they withdraw first? What if they have a pending bonus? | Users want to leave but have money in the account. | |
| G.5 | **After self-exclusion expires, does the account reopen automatically? Or does the user need to contact support?** | Important for users who set temporary limits. | |
| G.6 | **Is there a responsible gambling helpline or organization the bot should recommend?** (e.g., local organizations in Chile, Argentina) | For compliance, the bot should proactively offer this information when users mention gambling problems. | |

---

## SECTION H — Loyalty Program / Hero / Missions
**Impact: Part of Bonus tickets — growing as program expands**

> **Note:** Not covered in "domande_senza_risposta.md". The KB mentions the loyalty program but users have very specific questions.

| # | Question | Why we need this | Answer |
|---|---|---|---|
| H.1 | **How many levels does the Hero/Loyalty program have?** What are the level names? How much do you need to bet to reach each level? | Users ask "how do I level up?" — we need specific thresholds. | |
| H.2 | **What rewards does each level unlock?** (cashback %, free spins count, free bet value, deposit bonus %) | Users want to know what they'll get. A table per level would be ideal. | |
| H.3 | **Daily Missions: what types of missions exist?** (e.g., "make 5 bets", "deposit $X", "play game Y") Are they the same for everyone or personalized? | Real ticket: *"En las misiones me pide confirmar teléfono y correo"* — Some missions have prerequisites users don't understand. | |
| H.4 | **"Active user" requirement: the KB says 14 days without betting = loss of benefits. Does the user lose their LEVEL or just access to current benefits?** When they bet again, do they restart from level 1 or return to their previous level? | This distinction matters a lot. Users who pause are worried about losing progress. | |
| H.5 | **Birthday bonus: is it automatic or does the user need to claim it? What are the requirements?** (Must be active, must have deposited recently, etc.) | Users expect a bonus on their birthday and get nothing. Need to explain conditions. | |

---

## SECTION I — Sports Betting Specific
**Impact: Part of Casino/Games tickets — ~200/month**

> **Note:** Not covered in "domande_senza_risposta.md". The KB has basic sports info but users have operational questions.

| # | Question | Why we need this | Answer |
|---|---|---|---|
| I.1 | **How quickly are sports bets settled after an event ends?** (Minutes? Hours? Depends on the sport?) | Users win bets but don't see the payout immediately. | |
| I.2 | **Can a user cancel or edit a placed bet?** Before the event starts? After? | Users sometimes place bets by mistake. | |
| I.3 | **Cash Out: is it available for all bets or only certain ones?** What determines if Cash Out is offered? Can it be partial? | Real ticket: User tried Cash Out but option wasn't available. | |
| I.4 | **"My winning bet was voided" — what are the reasons a winning bet can be cancelled?** (Event cancelled, odds error, suspicious activity?) | Users get very angry when this happens. We need a clear, fair explanation. | |
| I.5 | **For accumulator/parlay bets: if one leg is cancelled, what happens to the rest?** Is the bet recalculated or void? | Users with multi-leg bets often face this confusion. | |

---

## SECTION J — Platform-Specific Issues (New patterns from Jan-Feb 2026)
**Impact: ~150/month — NEW patterns not seen before**

| # | Question | Why we need this | Answer |
|---|---|---|---|
| J.1 | **"Número de contribuyente" / "RUT" — during registration, what should Chilean users enter in the "document number" field?** Their RUT? With or without the verification digit? With dots and dash? | Real ticket: *"Cuál es el número de contribuyente para depositar?"* and *"Número de contribuyente, cuando lo pongo dice q no es válido"* — Registration blocker for Chilean users. | |
| J.2 | **Argentina: "DNI" or "CUIL" — which one do Argentine users need?** Format? | Same issue for Argentine users. | |
| J.3 | **The platform shows amounts in EUR/USD but the user deposited in CLP/ARS. How is the conversion displayed?** Where can they see the exchange rate? | Real ticket: *"Dice que está en inglés. Yo no te entiendo"* — Users confused by currency display. | |
| J.4 | **Can a user change their display language after registration?** Where? Does it change the interface AND support language? | Some users registered in the wrong language. | |
| J.5 | **"Datos no válidos" — what EXACTLY does this error mean during registration?** List the most common causes (name format, special characters, duplicate email, age restriction). | Real ticket: *"Estoy escribiendo mis datos y sale que no son válidos y son mis datos"* — Registration blocker. Many users can't even create an account. | |
| J.6 | **Is there a minimum age for registration? How is it verified?** What if an underage user manages to register? | Compliance question — the bot needs to mention this. | |

---

## Summary

| Section | Topic | New Questions | Est. Tickets/month |
|---|---|---|---|
| A | Greeting Handling Strategy | 4 | 1,119 |
| B | Bank Transfer Operations | 6 | 551 |
| C | Phone & Email Verification | 8 | 262 |
| D | "Saldo 0.00" Deep Dive | 5 | 400 |
| E | Casino Winnings Not Credited | 5 | 378 |
| F | Withdrawal Blocked by Bonus | 5 | 50 |
| G | Account Closure & Self-Exclusion | 6 | 62 |
| H | Loyalty Program / Hero | 5 | — |
| I | Sports Betting Specific | 5 | 200 |
| J | Platform-Specific Issues | 6 | 150 |
| **TOTAL** | | **55 new questions** | **~3,172/month** |

Combined with the 64 questions from "domande_senza_risposta.md", this gives us **119 total questions** covering virtually all customer issues seen across 35,963 tickets.

**Once both documents are completed, the AI widget could handle an estimated 70–75% of all incoming tickets autonomously.**

---

*Generated: 10 March 2026*
*Based on: 35,963 Zendesk tickets (Jul 2025 – Feb 2026)*
*Complements: domande_senza_risposta.md (64 questions from 26,963-ticket analysis)*
