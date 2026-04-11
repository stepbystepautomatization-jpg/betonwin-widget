#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║         BetonBot — Local Mock Server v1.1               ║
║  Simulates: n8n webhooks + Google Drive KB + S3 upload  ║
║  Usage: python3 mock_server.py                          ║
║  Then open: http://localhost:8080                       ║
╚══════════════════════════════════════════════════════════╝
"""

import json
import os
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = 8080

# ──────────────────────────────────────────────────────────────
# CONFIGURE TEST SCENARIOS HERE
# Change these values to test different deposit flows
# ──────────────────────────────────────────────────────────────
MOCK_DEPOSIT_STATUS = 'NEED_UPLOAD'
# Options:
#   'PROCESSING'    → deposit still processing (< 45 min)
#   'NEED_UPLOAD'   → needs document proof
#   'APPROVED'      → deposit approved immediately
#   'REJECTED'      → deposit rejected immediately
#   'PENDING_REVIEW'→ escalated to Zendesk

MOCK_FINAL_STATUS = 'APPROVED'
# Status returned after document analysis:
#   'APPROVED' | 'REJECTED' | 'PENDING_REVIEW'

# ──────────────────────────────────────────────────────────────
# MULTILINGUAL KNOWLEDGE BASE (EN / IT / ES / PT)
# ──────────────────────────────────────────────────────────────
KB_ARTICLES = {
    'deposit': {
        'en': {
            'name': 'Deposit Guide — FAQ',
            'content': (
                "How to make a deposit:\n\n"
                "1. Log in to your account\n"
                "2. Click on 'Deposit' in the top menu\n"
                "3. Select your preferred payment method\n"
                "4. Enter the amount (minimum €10)\n"
                "5. Confirm the transaction\n\n"
                "Payment methods available:\n"
                "• Visa / Mastercard — instant\n"
                "• Bank Transfer — 1-3 business days\n"
                "• Skrill / Neteller — instant\n"
                "• Bitcoin / USDT — 10-30 minutes\n\n"
                "Deposits are usually credited within minutes.\n"
                "If your deposit has not arrived after 30 minutes, please use the 'Check deposit status' button below to start a verification."
            )
        },
        'it': {
            'name': 'Guida ai Depositi — FAQ',
            'content': (
                "Come effettuare un deposito:\n\n"
                "1. Accedi al tuo account\n"
                "2. Clicca su 'Deposito' nel menu in alto\n"
                "3. Seleziona il metodo di pagamento preferito\n"
                "4. Inserisci l'importo (minimo €10)\n"
                "5. Conferma la transazione\n\n"
                "Metodi di pagamento disponibili:\n"
                "• Visa / Mastercard — istantaneo\n"
                "• Bonifico bancario — 1-3 giorni lavorativi\n"
                "• Skrill / Neteller — istantaneo\n"
                "• Bitcoin / USDT — 10-30 minuti\n\n"
                "I depositi vengono generalmente accreditati in pochi minuti.\n"
                "Se il tuo deposito non è arrivato dopo 30 minuti, usa il pulsante 'Verifica stato deposito' qui sotto per avviare una verifica."
            )
        },
        'es': {
            'name': 'Guía de Depósitos — FAQ',
            'content': (
                "Cómo realizar un depósito:\n\n"
                "1. Inicia sesión en tu cuenta\n"
                "2. Haz clic en 'Depósito' en el menú superior\n"
                "3. Selecciona tu método de pago preferido\n"
                "4. Introduce el importe (mínimo €10)\n"
                "5. Confirma la transacción\n\n"
                "Métodos de pago disponibles:\n"
                "• Visa / Mastercard — instantáneo\n"
                "• Transferencia bancaria — 1-3 días hábiles\n"
                "• Skrill / Neteller — instantáneo\n"
                "• Bitcoin / USDT — 10-30 minutos\n\n"
                "Los depósitos suelen acreditarse en minutos.\n"
                "Si tu depósito no ha llegado después de 30 minutos, usa el botón 'Verificar estado del depósito' para iniciar una verificación."
            )
        },
        'pt': {
            'name': 'Guia de Depósitos — FAQ',
            'content': (
                "Como fazer um depósito:\n\n"
                "1. Faça login na sua conta\n"
                "2. Clique em 'Depósito' no menu superior\n"
                "3. Selecione seu método de pagamento preferido\n"
                "4. Insira o valor (mínimo €10)\n"
                "5. Confirme a transação\n\n"
                "Métodos de pagamento disponíveis:\n"
                "• Visa / Mastercard — instantâneo\n"
                "• Transferência bancária — 1-3 dias úteis\n"
                "• Skrill / Neteller — instantâneo\n"
                "• Bitcoin / USDT — 10-30 minutos\n\n"
                "Os depósitos geralmente são creditados em minutos.\n"
                "Se o seu depósito não chegou após 30 minutos, use o botão 'Verificar status do depósito' para iniciar uma verificação."
            )
        }
    },
    'withdraw': {
        'en': {
            'name': 'Withdrawal Guide — FAQ',
            'content': (
                "How to withdraw your funds:\n\n"
                "1. Go to 'Cashier' → 'Withdraw'\n"
                "2. Choose your withdrawal method\n"
                "3. Enter the amount (minimum €20)\n"
                "4. Complete identity verification if required\n\n"
                "Processing times:\n"
                "• E-wallets (Skrill/Neteller): 0-24 hours\n"
                "• Credit/Debit card: 3-5 business days\n"
                "• Bank transfer: 3-7 business days\n\n"
                "First withdrawal requires identity verification (KYC).\n"
                "Maximum withdrawal: €10,000 per day. For higher amounts, contact support."
            )
        },
        'it': {
            'name': 'Guida ai Prelievi — FAQ',
            'content': (
                "Come prelevare i tuoi fondi:\n\n"
                "1. Vai su 'Cassa' → 'Prelievo'\n"
                "2. Scegli il metodo di prelievo\n"
                "3. Inserisci l'importo (minimo €20)\n"
                "4. Completa la verifica dell'identità se richiesta\n\n"
                "Tempi di elaborazione:\n"
                "• E-wallet (Skrill/Neteller): 0-24 ore\n"
                "• Carta di credito/debito: 3-5 giorni lavorativi\n"
                "• Bonifico bancario: 3-7 giorni lavorativi\n\n"
                "Il primo prelievo richiede la verifica dell'identità (KYC).\n"
                "Prelievo massimo: €10.000 al giorno. Per importi superiori, contatta il supporto."
            )
        },
        'es': {
            'name': 'Guía de Retiros — FAQ',
            'content': (
                "Cómo retirar tus fondos:\n\n"
                "1. Ve a 'Caja' → 'Retirar'\n"
                "2. Elige tu método de retiro\n"
                "3. Introduce el importe (mínimo €20)\n"
                "4. Completa la verificación de identidad si es necesario\n\n"
                "Tiempos de procesamiento:\n"
                "• Monederos electrónicos (Skrill/Neteller): 0-24 horas\n"
                "• Tarjeta de crédito/débito: 3-5 días hábiles\n"
                "• Transferencia bancaria: 3-7 días hábiles\n\n"
                "El primer retiro requiere verificación de identidad (KYC).\n"
                "Retiro máximo: €10.000 por día. Para importes mayores, contacta con soporte."
            )
        },
        'pt': {
            'name': 'Guia de Saques — FAQ',
            'content': (
                "Como sacar seus fundos:\n\n"
                "1. Vá para 'Caixa' → 'Saque'\n"
                "2. Escolha seu método de saque\n"
                "3. Insira o valor (mínimo €20)\n"
                "4. Complete a verificação de identidade se necessário\n\n"
                "Tempos de processamento:\n"
                "• Carteiras eletrônicas (Skrill/Neteller): 0-24 horas\n"
                "• Cartão de crédito/débito: 3-5 dias úteis\n"
                "• Transferência bancária: 3-7 dias úteis\n\n"
                "O primeiro saque requer verificação de identidade (KYC).\n"
                "Saque máximo: €10.000 por dia. Para valores maiores, contate o suporte."
            )
        }
    },
    'bonus': {
        'en': {
            'name': 'Bonus & Promotions Guide',
            'content': (
                "Available bonuses:\n\n"
                "Welcome Bonus: 100% up to €500 on first deposit\n"
                "• Minimum deposit: €20\n"
                "• Wagering requirement: 30x bonus amount\n"
                "• Valid for 30 days\n\n"
                "Reload Bonus: 50% every Monday\n"
                "• Minimum deposit: €30\n"
                "• Wagering requirement: 25x\n\n"
                "Free Spins: Available on selected slots\n"
                "• Credited automatically after qualifying deposit\n\n"
                "VIP Program: Earn points on every bet and exchange them for bonuses, free spins and cashback."
            )
        },
        'it': {
            'name': 'Guida Bonus e Promozioni',
            'content': (
                "Bonus disponibili:\n\n"
                "Bonus Benvenuto: 100% fino a €500 sul primo deposito\n"
                "• Deposito minimo: €20\n"
                "• Requisito di scommessa: 30x il bonus\n"
                "• Valido per 30 giorni\n\n"
                "Bonus Ricarica: 50% ogni lunedì\n"
                "• Deposito minimo: €30\n"
                "• Requisito di scommessa: 25x\n\n"
                "Giri Gratuiti: Disponibili su slot selezionate\n"
                "• Accreditati automaticamente dopo un deposito qualificante\n\n"
                "Programma VIP: Guadagna punti su ogni scommessa e scambiali con bonus, giri gratuiti e cashback."
            )
        },
        'es': {
            'name': 'Guía de Bonos y Promociones',
            'content': (
                "Bonos disponibles:\n\n"
                "Bono de Bienvenida: 100% hasta €500 en el primer depósito\n"
                "• Depósito mínimo: €20\n"
                "• Requisito de apuesta: 30x el bono\n"
                "• Válido por 30 días\n\n"
                "Bono de Recarga: 50% cada lunes\n"
                "• Depósito mínimo: €30\n"
                "• Requisito de apuesta: 25x\n\n"
                "Giros Gratis: Disponibles en slots seleccionados\n"
                "• Acreditados automáticamente tras depósito calificante\n\n"
                "Programa VIP: Gana puntos en cada apuesta y canjéalos por bonos, giros gratis y cashback."
            )
        },
        'pt': {
            'name': 'Guia de Bônus e Promoções',
            'content': (
                "Bônus disponíveis:\n\n"
                "Bônus de Boas-Vindas: 100% até €500 no primeiro depósito\n"
                "• Depósito mínimo: €20\n"
                "• Requisito de apostas: 30x o bônus\n"
                "• Válido por 30 dias\n\n"
                "Bônus de Recarga: 50% toda segunda-feira\n"
                "• Depósito mínimo: €30\n"
                "• Requisito de apostas: 25x\n\n"
                "Rodadas Grátis: Disponíveis em slots selecionados\n"
                "• Creditadas automaticamente após depósito qualificante\n\n"
                "Programa VIP: Ganhe pontos em cada aposta e troque por bônus, rodadas grátis e cashback."
            )
        }
    },
    'account': {
        'en': {
            'name': 'Account Management — FAQ',
            'content': (
                "Account questions:\n\n"
                "Forgot password: Click 'Forgot password' on the login page.\n"
                "You will receive a reset link via email within 5 minutes.\n\n"
                "Change email: Contact support with your new email address.\n"
                "Identity verification is required.\n\n"
                "Close account: Submit a closure request to support.\n"
                "Withdrawals must be completed before closing.\n\n"
                "2FA: Enable Two-Factor Authentication in Security Settings.\n\n"
                "Responsible gambling: Set deposit limits, loss limits or self-exclusion in your account settings."
            )
        },
        'it': {
            'name': 'Gestione Account — FAQ',
            'content': (
                "Domande sull'account:\n\n"
                "Password dimenticata: Clicca 'Password dimenticata' nella pagina di login.\n"
                "Riceverai un link di reset via email entro 5 minuti.\n\n"
                "Cambia email: Contatta il supporto con il tuo nuovo indirizzo email.\n"
                "È richiesta la verifica dell'identità.\n\n"
                "Chiudi account: Invia una richiesta di chiusura al supporto.\n"
                "I prelievi devono essere completati prima della chiusura.\n\n"
                "2FA: Attiva l'autenticazione a due fattori nelle Impostazioni di Sicurezza.\n\n"
                "Gioco responsabile: Imposta limiti di deposito, perdita o autoesclusione nelle impostazioni del tuo account."
            )
        },
        'es': {
            'name': 'Gestión de Cuenta — FAQ',
            'content': (
                "Preguntas sobre la cuenta:\n\n"
                "Contraseña olvidada: Haz clic en '¿Olvidaste tu contraseña?' en el inicio de sesión.\n"
                "Recibirás un enlace de restablecimiento por email en 5 minutos.\n\n"
                "Cambiar email: Contacta con soporte con tu nueva dirección.\n"
                "Se requiere verificación de identidad.\n\n"
                "Cerrar cuenta: Envía una solicitud de cierre al soporte.\n"
                "Los retiros deben completarse antes del cierre.\n\n"
                "2FA: Activa la Autenticación de Dos Factores en Configuración de Seguridad.\n\n"
                "Juego responsable: Establece límites de depósito, pérdida o autoexclusión en la configuración de tu cuenta."
            )
        },
        'pt': {
            'name': 'Gestão de Conta — FAQ',
            'content': (
                "Perguntas sobre a conta:\n\n"
                "Esqueci a senha: Clique em 'Esqueceu a senha?' na página de login.\n"
                "Você receberá um link de redefinição por email em 5 minutos.\n\n"
                "Mudar email: Entre em contato com o suporte com seu novo endereço.\n"
                "Verificação de identidade é necessária.\n\n"
                "Fechar conta: Envie uma solicitação de encerramento ao suporte.\n"
                "Os saques devem ser concluídos antes do encerramento.\n\n"
                "2FA: Ative a Autenticação de Dois Fatores nas Configurações de Segurança.\n\n"
                "Jogo responsável: Defina limites de depósito, perda ou autoexclusão nas configurações da sua conta."
            )
        }
    },
    'verification': {
        'en': {
            'name': 'KYC Identity Verification',
            'content': (
                "Identity verification (KYC) is required to:\n"
                "• Process your first withdrawal\n"
                "• Lift deposit limits\n"
                "• Reactivate a restricted account\n\n"
                "Documents accepted:\n"
                "• Passport or National ID (front + back)\n"
                "• Proof of address (utility bill or bank statement — last 3 months)\n"
                "• Payment method proof (card photo for card payments)\n\n"
                "Verification is usually completed within 24 hours.\n"
                "Upload your documents directly in the chat using the button below."
            )
        },
        'it': {
            'name': 'Verifica Identità KYC',
            'content': (
                "La verifica dell'identità (KYC) è richiesta per:\n"
                "• Elaborare il primo prelievo\n"
                "• Rimuovere i limiti di deposito\n"
                "• Riattivare un account limitato\n\n"
                "Documenti accettati:\n"
                "• Passaporto o Carta d'identità (fronte + retro)\n"
                "• Prova di residenza (bolletta o estratto conto — ultimi 3 mesi)\n"
                "• Prova del metodo di pagamento (foto della carta per pagamenti con carta)\n\n"
                "La verifica viene solitamente completata entro 24 ore.\n"
                "Carica i tuoi documenti direttamente nella chat usando il pulsante qui sotto."
            )
        },
        'es': {
            'name': 'Verificación de Identidad KYC',
            'content': (
                "La verificación de identidad (KYC) es necesaria para:\n"
                "• Procesar tu primer retiro\n"
                "• Eliminar límites de depósito\n"
                "• Reactivar una cuenta restringida\n\n"
                "Documentos aceptados:\n"
                "• Pasaporte o DNI (anverso + reverso)\n"
                "• Comprobante de domicilio (factura o extracto bancario — últimos 3 meses)\n"
                "• Prueba del método de pago (foto de la tarjeta para pagos con tarjeta)\n\n"
                "La verificación suele completarse en 24 horas.\n"
                "Sube tus documentos directamente en el chat usando el botón de abajo."
            )
        },
        'pt': {
            'name': 'Verificação de Identidade KYC',
            'content': (
                "A verificação de identidade (KYC) é necessária para:\n"
                "• Processar seu primeiro saque\n"
                "• Remover limites de depósito\n"
                "• Reativar uma conta restrita\n\n"
                "Documentos aceitos:\n"
                "• Passaporte ou RG/CNH (frente + verso)\n"
                "• Comprovante de residência (conta de serviços ou extrato bancário — últimos 3 meses)\n"
                "• Comprovante do método de pagamento (foto do cartão para pagamentos com cartão)\n\n"
                "A verificação geralmente é concluída em 24 horas.\n"
                "Envie seus documentos diretamente no chat usando o botão abaixo."
            )
        }
    },
    'default': {
        'en': {
            'name': 'BetonWin Support',
            'content': (
                "Welcome to BetonWin Support! 👋\n\n"
                "I can help you with:\n"
                "• Deposits and withdrawals\n"
                "• Bonuses and promotions\n"
                "• Account management\n"
                "• Technical issues\n"
                "• Identity verification (KYC)\n\n"
                "For urgent issues, reach us via:\n"
                "• Live Chat: available 24/7\n"
                "• Email: support@betonwin.com\n"
                "• Response time: within 2 hours"
            )
        },
        'it': {
            'name': 'Supporto BetonWin',
            'content': (
                "Benvenuto al Supporto BetonWin! 👋\n\n"
                "Posso aiutarti con:\n"
                "• Depositi e prelievi\n"
                "• Bonus e promozioni\n"
                "• Gestione account\n"
                "• Problemi tecnici\n"
                "• Verifica dell'identità (KYC)\n\n"
                "Per problemi urgenti, contattaci tramite:\n"
                "• Live Chat: disponibile 24/7\n"
                "• Email: support@betonwin.com\n"
                "• Tempo di risposta: entro 2 ore"
            )
        },
        'es': {
            'name': 'Soporte BetonWin',
            'content': (
                "¡Bienvenido al Soporte de BetonWin! 👋\n\n"
                "Puedo ayudarte con:\n"
                "• Depósitos y retiros\n"
                "• Bonos y promociones\n"
                "• Gestión de cuenta\n"
                "• Problemas técnicos\n"
                "• Verificación de identidad (KYC)\n\n"
                "Para problemas urgentes, contáctanos por:\n"
                "• Chat en Vivo: disponible 24/7\n"
                "• Email: support@betonwin.com\n"
                "• Tiempo de respuesta: en 2 horas"
            )
        },
        'pt': {
            'name': 'Suporte BetonWin',
            'content': (
                "Bem-vindo ao Suporte BetonWin! 👋\n\n"
                "Posso ajudá-lo com:\n"
                "• Depósitos e saques\n"
                "• Bônus e promoções\n"
                "• Gerenciamento de conta\n"
                "• Problemas técnicos\n"
                "• Verificação de identidade (KYC)\n\n"
                "Para problemas urgentes, contate-nos via:\n"
                "• Chat ao Vivo: disponível 24/7\n"
                "• Email: support@betonwin.com\n"
                "• Tempo de resposta: dentro de 2 horas"
            )
        }
    }
}

# Keywords for category detection (language-agnostic)
KB_KEYWORDS = {
    'deposit':      ['deposit', 'payment', 'fund', 'credit', 'top up', 'transfer', 'bank',
                     'deposito', 'depositar', 'pago', 'pagamento', 'ricarica', 'bonifico', 'versamento',
                     'depósito', 'recarga', 'transferencia'],
    'withdraw':     ['withdraw', 'cashout', 'cash out', 'payout', 'withdrawal',
                     'prelievo', 'prelevare', 'ritiro', 'prelevamento',
                     'retiro', 'retirar',
                     'saque', 'sacar'],
    'bonus':        ['bonus', 'promotion', 'promo', 'offer', 'free spin', 'welcome', 'reload',
                     'promozione', 'giri', 'benvenuto',
                     'bono', 'promoción', 'giros',
                     'bônus', 'promoção', 'rodadas'],
    'account':      ['account', 'password', 'login', 'email', 'register', 'profile', 'close', '2fa',
                     'account', 'passw', 'profilo', 'accesso', 'registra', 'chiudi',
                     'contraseña', 'iniciar', 'cerrar',
                     'senha', 'entrar', 'fechar'],
    'verification': ['verify', 'kyc', 'identity', 'document', 'id', 'passport', 'proof',
                     'verifica', 'identità', 'documento', 'passaporto',
                     'verificar', 'identidad', 'pasaporte',
                     'verificação', 'identidade', 'passaporte']
}


def smart_extract(content, query, max_blocks=2):
    """Extract the most relevant paragraph(s) from KB content based on query keywords."""
    import re
    clean = content.strip().replace('\r\n', '\n')
    # Split into blocks separated by blank lines
    blocks = [b.strip() for b in re.split(r'\n\n+', clean) if b.strip() and len(b.strip()) > 10]

    # Short content — return as-is
    if len(blocks) <= 2:
        return clean

    # Score each block by how many query words appear
    words = [w for w in re.split(r'[\s,.?!;:]+', query.lower()) if len(w) > 2]
    scored = []
    for block in blocks:
        lower = block.lower()
        score = sum(1 for w in words if w in lower)
        scored.append((score, block))
    scored.sort(key=lambda x: x[0], reverse=True)

    # No matches → return full content
    if scored[0][0] == 0:
        return clean

    # Return best block, optionally add second if best is short and second is substantial
    result = scored[0][1]
    if len(result) < 220 and len(scored) > 1 and scored[1][0] > 0 and len(scored[1][1]) >= 60:
        result += '\n\n' + scored[1][1]
    return result


def build_response(article_name, content, query, lang):
    """Build a natural response: intro + relevant content + closing (zero AI)."""
    extracted = smart_extract(content, query)
    name = article_name.replace('.docx', '').replace('.doc', '').strip()
    intros = {
        'en': f"Here's what I found about **{name}**:\n\n",
        'it': f"Ecco le informazioni su **{name}**:\n\n",
        'es': f"Aquí está la información sobre **{name}**:\n\n",
        'pt': f"Aqui estão as informações sobre **{name}**:\n\n"
    }
    outros = {
        'en': "\n\nIs there anything else I can help you with?",
        'it': "\n\nPosso aiutarti con qualcos'altro?",
        'es': "\n\n¿Puedo ayudarte con algo más?",
        'pt': "\n\nPosso ajudá-lo com mais alguma coisa?"
    }
    intro = intros.get(lang, intros['en'])
    outro = outros.get(lang, outros['en'])
    return intro + extracted + outro


def find_kb_article(query, lang='en'):
    """Find the most relevant KB article for query. Returns None if no keyword match."""
    q = query.lower()
    scores = {}
    for category, words in KB_KEYWORDS.items():
        for word in words:
            if word in q:
                scores[category] = scores.get(category, 0) + 1
    if not scores:
        return None  # No match → caller handles this gracefully
    category = max(scores, key=scores.get)
    article_group = KB_ARTICLES.get(category, KB_ARTICLES['default'])
    lang_code = lang if lang in article_group else 'en'
    return article_group[lang_code]


NO_MATCH_RESPONSES = {
    'en': "I'm not sure I understood your question. Could you tell me more?\n\nI can help you with:\n• Deposits and withdrawals\n• Bonuses and promotions\n• Account and password\n• Identity verification (KYC)",
    'it': "Non sono sicuro di aver capito bene. Puoi spiegarmi meglio?\n\nPosso aiutarti con:\n• Depositi e prelievi\n• Bonus e promozioni\n• Account e password\n• Verifica dell'identità (KYC)",
    'es': "No estoy seguro de haber entendido bien. ¿Puedes explicarme más?\n\nPuedo ayudarte con:\n• Depósitos y retiros\n• Bonos y promociones\n• Cuenta y contraseña\n• Verificación de identidad (KYC)",
    'pt': "Não tenho certeza que entendi bem. Pode explicar melhor?\n\nPosso ajudá-lo com:\n• Depósitos e saques\n• Bônus e promoções\n• Conta e senha\n• Verificação de identidade (KYC)"
}


class MockHandler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        status = args[0] if args else '?'
        color  = '\033[32m' if str(status).startswith('2') else '\033[33m'
        reset  = '\033[0m'
        print(f"  {color}[{self.command}]{reset} {self.path}  →  {color}{status}{reset}")

    # ── CORS helpers ──────────────────────────────────────────
    def cors_headers(self):
        self.send_header('Access-Control-Allow-Origin',  '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')

    def do_OPTIONS(self):
        self.send_response(204)
        self.cors_headers()
        self.end_headers()

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, filepath, content_type='text/html; charset=utf-8'):
        try:
            with open(filepath, 'rb') as f:
                body = f.read()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(body)))
            self.cors_headers()
            self.end_headers()
            self.wfile.write(body)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()

    def read_body(self):
        length = int(self.headers.get('Content-Length', 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw)
        except Exception:
            return {}

    # ── GET requests ──────────────────────────────────────────
    def do_GET(self):
        parsed = urlparse(self.path)
        path   = parsed.path
        qs     = parse_qs(parsed.query)

        # Static files
        if path in ('/', '/index.html'):
            self.send_file('index.html')

        elif path == '/widget.html':
            self.send_file('widget.html')

        elif path == '/widget.js':
            self.send_file('widget.js', 'application/javascript; charset=utf-8')

        # ── Mock Knowledge Base (multilingual) ─────────────────
        elif path == '/kb':
            query      = qs.get('q', [''])[0]
            lang_param = qs.get('lang', ['en'])[0]
            article    = find_kb_article(query, lang_param)
            if article is None:
                print(f"    KB query: '{query}' (lang:{lang_param}) → no match")
                self.send_json({'results': [], 'query': query, 'count': 0})
            else:
                print(f"    KB query: '{query}' (lang:{lang_param}) → '{article['name']}'")
                self.send_json({
                    'results': [{
                        'name':    article['name'],
                        'content': article['content'],
                        'type':    'application/vnd.google-apps.document',
                        'url':     'https://drive.google.com/mock',
                        'updated': '2026-02-01T10:00:00.000Z'
                    }],
                    'query': query,
                    'count': 1
                })

        # ── Mock Status polling ────────────────────────────────
        elif path.startswith('/webhook/status/'):
            job_id = path.split('/')[-1]
            print(f"    Polling job: {job_id} → {MOCK_FINAL_STATUS}")
            self.send_json({'status': MOCK_FINAL_STATUS, 'job_id': job_id})

        else:
            self.send_json({'error': 'Not found'}, 404)

    # ── POST requests ─────────────────────────────────────────
    def do_POST(self):
        path = urlparse(self.path).path
        body = self.read_body()

        # ── /webhook/chat ──────────────────────────────────────
        if path == '/webhook/chat':
            msg  = body.get('message', '')
            lang = body.get('language', 'en')
            print(f"    Chat message ({lang}): '{msg[:60]}'")
            article = find_kb_article(msg, lang)
            if article is None:
                response = NO_MATCH_RESPONSES.get(lang, NO_MATCH_RESPONSES['en'])
            else:
                response = build_response(article['name'], article['content'], msg, lang)
            self.send_json({'message': response, 'action': None})

        # ── /webhook/verify-deposit ────────────────────────────
        elif path == '/webhook/verify-deposit':
            player_id = body.get('player_id', 'unknown')
            print(f"    Verify deposit — player: {player_id}  status → {MOCK_DEPOSIT_STATUS}")
            resp = {'status': MOCK_DEPOSIT_STATUS}
            if MOCK_DEPOSIT_STATUS in ('PENDING', 'NEED_UPLOAD'):
                resp['job_id'] = f'job_{player_id}_{int(time.time())}'
            self.send_json(resp)

        # ── /webhook/presigned-url ─────────────────────────────
        elif path == '/webhook/presigned-url':
            player_id = body.get('player_id', 'user')
            file_name = body.get('file_name', 'document.jpg')
            job_id    = f'job_{player_id}_{int(time.time())}'
            print(f"    Presigned URL for: {file_name}")
            self.send_json({
                'presigned_url': f'http://localhost:{PORT}/mock-s3/{job_id}/{file_name}',
                's3_url':        f'https://betonbot-uploads.s3.amazonaws.com/{job_id}/{file_name}'
            })

        # ── /webhook/analyze ───────────────────────────────────
        elif path == '/webhook/analyze':
            s3_url    = body.get('s3_url', '')
            player_id = body.get('player_id', 'user')
            job_id    = body.get('job_id') or f'analyze_{int(time.time())}'
            print(f"    Analyze document — job: {job_id}  final → {MOCK_FINAL_STATUS}")
            self.send_json({'job_id': job_id})

        else:
            self.send_json({'error': f'Unknown endpoint: {path}'}, 404)

    # ── PUT — mock S3 upload ──────────────────────────────────
    def do_PUT(self):
        if '/mock-s3/' in self.path:
            size = int(self.headers.get('Content-Length', 0))
            self.rfile.read(size)
            fname = self.path.split('/')[-1]
            print(f"    Mock S3 upload: {fname}  ({size:,} bytes)")
            self.send_response(200)
            self.cors_headers()
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = HTTPServer(('localhost', PORT), MockHandler)

    print(f"""
\033[32m╔══════════════════════════════════════════════════╗
║         BetonBot — Local Mock Server v1.1        ║
╠══════════════════════════════════════════════════╣
║  🌐  http://localhost:{PORT}                         ║
╠══════════════════════════════════════════════════╣
║  SCENARIO ATTIVO:                                ║
║  Deposit status  →  {MOCK_DEPOSIT_STATUS:<28}║
║  Final result    →  {MOCK_FINAL_STATUS:<28}║
╠══════════════════════════════════════════════════╣
║  Lingue KB: EN / IT / ES / PT                    ║
║  Per cambiare scenario:                          ║
║  Modifica MOCK_DEPOSIT_STATUS in mock_server.py  ║
╚══════════════════════════════════════════════════╝\033[0m
Ctrl+C per fermare il server
""")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n\033[33m⏹  Server fermato.\033[0m')
