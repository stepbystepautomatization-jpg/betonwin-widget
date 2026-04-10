(function () {
  'use strict';

  // ============================================================
  // 1. CONFIGURATION
  // ============================================================
  var CONFIG = {
    N8N_BASE: 'https://n8nbeton.online',
    KB_URL:   'https://script.google.com/macros/s/AKfycbw4QH_cxD2HmW18ReyCUzo4BDPwrHeUaMwYKxXnjwSNc0yhPxCAFqZRkI6dDBD5y0ZI/exec',
    ENDPOINTS: {
      CHAT:        '/webhook/884acc5b-3a84-44cc-8f44-7c1b7df3df2a',
      VERIFY:      '/webhook/verify-deposit',
      STATUS:      '/webhook/status',
      PRESIGNED:   '/webhook/presigned-url',
      ANALYZE:     '/webhook/analyze',
      ESCALATE:    '/webhook/escalate',
      AGENT_POLL:  '/webhook/agent-poll',
      AGENT_REPLY: '/webhook/agent-reply'
    },
    POLL_INTERVAL_MS: 3000,
    POLL_MAX:         40,
    BOT_NAME:         'BetonWin Support',
    MAX_FILE_MB:      10,
    ACCEPTED_TYPES:   ['image/jpeg', 'image/png', 'image/webp', 'application/pdf']
  };

  // ============================================================
  // 2. COLORS — BetonWin Brand Palette
  // ============================================================
  var C = {
    bg:            '#03242D',
    widget:        '#042a33',
    header:        '#03242D',
    green:         '#2DEC76',
    greenDark:     '#25cc65',
    greenGlow:     'rgba(45,236,118,0.08)',
    greenGlowB:    'rgba(45,236,118,0.18)',
    text:          '#e8f0f2',
    textMuted:     '#6b8f9a',
    border:        'rgba(45,236,118,0.06)',
    headerBorder:  'rgba(45,236,118,0.08)',
    userBubble:    '#0a3d2a',
    botBubble:     '#042e38',
    input:         '#042a33',
    inputBorder:   'rgba(45,236,118,0.1)',
    scrollbar:     'rgba(45,236,118,0.08)',
    danger:        '#f87171',
    warning:       '#fbbf24',
    shadow:        '0 0 0 1px rgba(45,236,118,0.06),0 24px 80px rgba(0,0,0,0.7),0 0 60px rgba(45,236,118,0.04)',
    triggerShadow: '0 0 0 0 rgba(45,236,118,0.35),0 8px 32px rgba(0,0,0,0.5)'
  };

  // ============================================================
  // 3. TRANSLATIONS (i18n) — EN / ES / IT / PT
  // ============================================================
  var LANG = {
    en: {
      welcome:          "Hi! I'm your **BetonWin** 24/7 support assistant. How can I help you today?",
      placeholder:      'Type your message...',
      send:             'Send',
      typing:           'Thinking',
      online:           'Online',
      quick_deposit:    'Check deposit status',
      deposit_ask_id:   'Sure! Please enter your **Player ID** to check your deposit:',
      player_id_ph:     'Enter Player ID',
      confirm:          'Confirm',
      deposit_checking: 'Checking your deposit... ⏳',
      deposit_proc:     'Your deposit is still **processing**. This usually takes a few minutes. Please check again shortly.',
      upload_required:  'Your deposit needs additional verification.\nPlease **upload your payment proof** (screenshot or bank receipt):',
      upload_drag:      'Drag & drop or click to upload',
      upload_hint:      'JPG · PNG · PDF — max 10MB',
      uploading:        'Uploading your document...',
      analyzing:        'AI is analyzing your document... 🤖',
      result_approved:  '✅ Your deposit has been **APPROVED**!\nFunds will appear in your account shortly.',
      result_rejected:  '❌ Your deposit has been **REJECTED**.\nPlease contact support for more details.',
      result_pending:   '⏳ Your case has been **escalated** to our support team.\nA ticket has been created — we will contact you soon.',
      kb_searching:     'Let me check our knowledge base... 🔍',
      no_results:       "I'm not sure I understood your question. Could you tell me more?\n\nI can help you with:\n• Deposits and withdrawals\n• Bonuses and promotions\n• Account and password\n• Identity verification (KYC)",
      deposit_intent:   "It looks like you have a question about a deposit. Let me help you check its status!",
      err_generic:      'Something went wrong. Please try again.',
      err_file_size:    'File is too large. Maximum size is 10MB.',
      err_file_type:    'File type not supported. Please upload JPG, PNG, or PDF.',
      new_chat:         'New chat',
      close:            'Close',
      escalating:       'Connecting you to a live agent... 🔄',
      escalated:        '🧑‍💼 You are now connected with our support team.\nAn agent will review your conversation and reply here shortly.',
      escalate_ticket:  'Ticket **#{{id}}** created.',
      live_agent:       'Live Agent',
      agent_closed:     'The agent has closed this conversation.\nClick **New chat** to start a new one.',
      human_noted:      "I understand you'd like to speak with a human agent. Let me try to help you first — if I can't resolve your issue, I'll connect you with an agent.",
      human_escalate:   "I'm connecting you with a live agent now.",
      proactive:        'Hi! Need any help? I can assist you with deposits, withdrawals, bonuses, and more.',
      csat_ask:         'How was your experience?',
      csat_thanks:      'Thank you for your feedback!',
      send_file_agent:  'Send a file to the agent',
      file_sent:        'File sent to agent.'
    },
    es: {
      welcome:          '¡Hola! Soy tu asistente de soporte **BetonWin** 24/7. ¿En qué puedo ayudarte hoy?',
      placeholder:      'Escribe tu mensaje...',
      send:             'Enviar',
      typing:           'Pensando',
      online:           'En línea',
      quick_deposit:    'Verificar estado del depósito',
      deposit_ask_id:   '¡Claro! Por favor, introduce tu **ID de jugador** para verificar tu depósito:',
      player_id_ph:     'Introduce tu ID de jugador',
      confirm:          'Confirmar',
      deposit_checking: 'Verificando tu depósito... ⏳',
      deposit_proc:     'Tu depósito todavía está **procesando**. Esto suele tardar unos minutos.',
      upload_required:  'Tu depósito necesita verificación adicional.\nPor favor, **sube tu comprobante de pago** (captura o recibo bancario):',
      upload_drag:      'Arrastra aquí o haz clic para subir',
      upload_hint:      'JPG · PNG · PDF — máx 10MB',
      uploading:        'Subiendo tu documento...',
      analyzing:        'La IA está analizando tu documento... 🤖',
      result_approved:  '✅ ¡Tu depósito ha sido **APROBADO**!\nLos fondos aparecerán en tu cuenta en breve.',
      result_rejected:  '❌ Tu depósito ha sido **RECHAZADO**.\nPor favor, contacta con soporte para más detalles.',
      result_pending:   '⏳ Tu caso ha sido **escalado** a nuestro equipo de soporte.\nSe ha creado un ticket — nos pondremos en contacto contigo pronto.',
      kb_searching:     'Déjame consultar nuestra base de conocimiento... 🔍',
      no_results:       'No estoy seguro de haber entendido bien. ¿Puedes explicarme más?\n\nPuedo ayudarte con:\n• Depósitos y retiros\n• Bonos y promociones\n• Cuenta y contraseña\n• Verificación de identidad (KYC)',
      deposit_intent:   '¡Parece que tienes una pregunta sobre un depósito! Déjame ayudarte a verificar su estado.',
      err_generic:      'Algo salió mal. Por favor, inténtalo de nuevo.',
      err_file_size:    'El archivo es demasiado grande. El tamaño máximo es 10MB.',
      err_file_type:    'Tipo de archivo no compatible. Sube JPG, PNG o PDF.',
      new_chat:         'Nueva conversación',
      close:            'Cerrar',
      escalating:       'Conectándote con un agente... 🔄',
      escalated:        '🧑‍💼 Estás conectado con nuestro equipo de soporte.\nUn agente revisará tu conversación y te responderá aquí en breve.',
      escalate_ticket:  'Ticket **#{{id}}** creado.',
      live_agent:       'Agente',
      agent_closed:     'El agente ha cerrado esta conversación.\nHaz clic en **Nueva conversación** para iniciar una nueva.',
      human_noted:      'Entiendo que quieres hablar con un agente. Déjame intentar ayudarte primero — si no puedo resolver tu problema, te conecto con un agente.',
      human_escalate:   'Te estoy conectando con un agente ahora.',
      proactive:        '¡Hola! ¿Necesitas ayuda? Puedo ayudarte con depósitos, retiros, bonos y más.',
      csat_ask:         '¿Cómo fue tu experiencia?',
      csat_thanks:      '¡Gracias por tu opinión!',
      send_file_agent:  'Enviar archivo al agente',
      file_sent:        'Archivo enviado al agente.'
    },
    it: {
      welcome:          'Ciao! Sono il tuo assistente di supporto **BetonWin** 24/7. Come posso aiutarti oggi?',
      placeholder:      'Scrivi il tuo messaggio...',
      send:             'Invia',
      typing:           'Pensando',
      online:           'Online',
      quick_deposit:    'Verifica stato deposito',
      deposit_ask_id:   'Certo! Inserisci il tuo **Player ID** per verificare il deposito:',
      player_id_ph:     'Inserisci Player ID',
      confirm:          'Conferma',
      deposit_checking: 'Verifica deposito in corso... ⏳',
      deposit_proc:     'Il tuo deposito è ancora in **elaborazione**. Richiede qualche minuto.',
      upload_required:  'Il deposito richiede verifica aggiuntiva.\nCarica la tua **prova di pagamento** (screenshot o ricevuta bancaria):',
      upload_drag:      'Trascina qui o clicca per caricare',
      upload_hint:      'JPG · PNG · PDF — max 10MB',
      uploading:        'Caricamento documento...',
      analyzing:        "L'AI sta analizzando il documento... 🤖",
      result_approved:  '✅ Il tuo deposito è stato **APPROVATO**!\nI fondi appariranno presto nel tuo account.',
      result_rejected:  '❌ Il tuo deposito è stato **RIFIUTATO**.\nContatta il supporto per maggiori dettagli.',
      result_pending:   '⏳ Il tuo caso è stato **inoltrato** al team di supporto.\nÈ stato creato un ticket — ti contatteremo a breve.',
      kb_searching:     'Consulto la nostra knowledge base... 🔍',
      no_results:       "Non sono sicuro di aver capito bene. Puoi spiegarmi meglio?\n\nPosso aiutarti con:\n• Depositi e prelievi\n• Bonus e promozioni\n• Account e password\n• Verifica dell'identità (KYC)",
      deposit_intent:   'Sembra che tu abbia una domanda su un deposito. Lascia che ti aiuti a verificarne lo stato!',
      err_generic:      'Si è verificato un errore. Riprova.',
      err_file_size:    'File troppo grande. Massimo 10MB.',
      err_file_type:    'Tipo file non supportato. Carica JPG, PNG o PDF.',
      new_chat:         'Nuova conversazione',
      close:            'Chiudi',
      escalating:       'Ti sto collegando con un agente... 🔄',
      escalated:        '🧑‍💼 Sei connesso con il nostro team di supporto.\nUn agente esaminerà la conversazione e ti risponderà qui a breve.',
      escalate_ticket:  'Ticket **#{{id}}** creato.',
      live_agent:       'Agente',
      agent_closed:     "L'agente ha chiuso questa conversazione.\nClicca su **Nuova conversazione** per iniziarne una nuova.",
      human_noted:      'Capisco che vorresti parlare con un operatore. Lasciami provare ad aiutarti prima — se non riesco a risolvere, ti collego con un agente.',
      human_escalate:   'Ti sto collegando con un agente ora.',
      proactive:        'Ciao! Hai bisogno di aiuto? Posso assisterti con depositi, prelievi, bonus e altro.',
      csat_ask:         "Com'è stata la tua esperienza?",
      csat_thanks:      'Grazie per il tuo feedback!',
      send_file_agent:  "Invia file all'agente",
      file_sent:        "File inviato all'agente."
    },
    pt: {
      welcome:          'Olá! Sou seu assistente de suporte **BetonWin** 24/7. Como posso ajudá-lo hoje?',
      placeholder:      'Digite sua mensagem...',
      send:             'Enviar',
      typing:           'Pensando',
      online:           'Online',
      quick_deposit:    'Verificar status do depósito',
      deposit_ask_id:   'Claro! Por favor, insira seu **ID de jogador** para verificar seu depósito:',
      player_id_ph:     'Insira seu ID de jogador',
      confirm:          'Confirmar',
      deposit_checking: 'Verificando seu depósito... ⏳',
      deposit_proc:     'Seu depósito ainda está **processando**. Isso geralmente leva alguns minutos.',
      upload_required:  'Seu depósito precisa de verificação adicional.\nPor favor, **envie seu comprovante de pagamento** (captura ou recibo bancário):',
      upload_drag:      'Arraste aqui ou clique para enviar',
      upload_hint:      'JPG · PNG · PDF — máx 10MB',
      uploading:        'Enviando seu documento...',
      analyzing:        'A IA está analisando seu documento... 🤖',
      result_approved:  '✅ Seu depósito foi **APROVADO**!\nOs fundos aparecerão em sua conta em breve.',
      result_rejected:  '❌ Seu depósito foi **RECUSADO**.\nEntre em contato com o suporte para mais detalhes.',
      result_pending:   '⏳ Seu caso foi **escalado** para nossa equipe de suporte.\nUm ticket foi criado — entraremos em contato em breve.',
      kb_searching:     'Deixa-me consultar nossa base de conhecimento... 🔍',
      no_results:       'Não tenho certeza que entendi bem. Pode explicar melhor?\n\nPosso ajudá-lo com:\n• Depósitos e saques\n• Bônus e promoções\n• Conta e senha\n• Verificação de identidade (KYC)',
      deposit_intent:   'Parece que você tem uma pergunta sobre um depósito. Deixa-me ajudar a verificar o status!',
      err_generic:      'Algo deu errado. Por favor, tente novamente.',
      err_file_size:    'Arquivo muito grande. Tamanho máximo é 10MB.',
      err_file_type:    'Tipo de arquivo não suportado. Envie JPG, PNG ou PDF.',
      new_chat:         'Nova conversa',
      close:            'Fechar',
      escalating:       'Conectando você com um agente... 🔄',
      escalated:        '🧑‍💼 Você está conectado com nossa equipe de suporte.\nUm agente revisará sua conversa e responderá aqui em breve.',
      escalate_ticket:  'Ticket **#{{id}}** criado.',
      live_agent:       'Agente',
      agent_closed:     'O agente encerrou esta conversa.\nClique em **Nova conversa** para iniciar uma nova.',
      human_noted:      'Entendo que você quer falar com um agente. Deixa-me tentar ajudar primeiro — se não conseguir resolver, te conecto com um agente.',
      human_escalate:   'Estou conectando você com um agente agora.',
      proactive:        'Olá! Precisa de ajuda? Posso ajudá-lo com depósitos, saques, bônus e mais.',
      csat_ask:         'Como foi sua experiência?',
      csat_thanks:      'Obrigado pelo seu feedback!',
      send_file_agent:  'Enviar arquivo ao agente',
      file_sent:        'Arquivo enviado ao agente.'
    }
  };

  // Always start in Spanish (site is for Chile/Argentina)
  // Language switches only when user types in another language
  var lang = 'es';
  function t(k) { return (LANG[lang] || LANG.en)[k] || k; }

  // ============================================================
  // 4. STATE
  // ============================================================
  var STATE = {
    isOpen:     false,
    phase:      'CHAT',       // CHAT | DEPOSIT_ASK_ID | ... | LIVE_AGENT | AGENT_CLOSED
    playerId:   null,
    jobId:      null,
    pollTimer:  null,
    pollCount:  0,
    messages:   [],
    busy:       false,
    lastSendTs: 0,
    humanRequestCount: 0,     // T-05/T-06: track "talk to human" requests
    ticketId:   null,         // Zendesk ticket ID for live agent
    agentPollTimer: null,     // polling for agent replies
    sessionId: null,          // UUID for analytics correlation
    sessionStartTime: null,   // T-19: session start timestamp
    urgency: 'low',           // T-07: sentiment urgency (low/high)
    inactivityTimer: null,    // T-17: inactivity timeout
    inactivityReminded: false, // T-17: already sent reminder
    unhappyCount: 0           // T-18: "wrong answer" counter
  };

  function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      var r = Math.random() * 16 | 0;
      return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
  }

  var MAX_MSG_LENGTH = 1000;
  var MAX_MESSAGES   = 100;
  var SEND_COOLDOWN  = 1000;
  var HUMAN_REQUEST_THRESHOLD = 2;    // T-06: escalate after 2 requests (was 3)
  var AGENT_POLL_INTERVAL = 5000;
  var AGENT_POLL_MAX = 360;
  var PROACTIVE_DELAY = 30000;    // show proactive message after 30s
  var INACTIVITY_REMINDER_MS = 120000;  // T-17: remind after 120s
  var INACTIVITY_CLOSE_MS = 240000;     // T-17: close after 240s
  var SESSION_MAX_MS = 600000;          // T-19: 10 minutes max session
  var NOTIF_SOUND_URL = 'data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1bZ3N9gnqEi46Oj4uFfnRoW1BFQkVOXG53goqRlZeSjIOAd21kXFhYXWRveoaOk5aXlI6HgXpya2VfXWBka3aBipKXmZiVkIqEfnhybGhjY2dsdoGKkpiamJaTjoiCfHZwamZlZ2tygIqSmJqYlpKNh4F8dnBqZmVnaHCBi5OYmpeTkI2Kh4N+eXRua2lrbXN+iJCWmJaTkI2KiIWBfHdybm1sb3R7hIySlZaTkI6MioiFgnx4dHFvcHJ2fIWNkpWUk5COjIqIhYJ/e3d0cnF0eH2EjJGUlJKQjouKiIaEgn55dnRzdHd7gIaPk5WUkpCOjIqJh4WCf3x5d3Z2eXyBh42Sk5OSkI6MioiGhIF+e3l3dnd5fIKHjZGTkpKQjo2LiYeFgn98enl4eXt+goiNkZOSkI+NjIuJh4WDgH17enl5e32Bg4iNkJKRkI6NjIuJh4WDgH58e3p6e32AhIiNkJGRj46NjIqJh4aDgX98fHt7fH6BhYmNkJGQj46NjIqIh4WDgX9+fHx8fX+ChomMj5CQj46NjIqIhoWDgYB+fXx9fn+ChomMj5CQj46Mi4qIhoWDgX9+fXx9fn+Bg4eLjo+Pj46NjIqIhoWDgX9+fXx8fX6AgoWIi46Pj4+OjYuKiIaFg4GAfn18fH1+gIKFiIuOj4+Pjo2LioiGhYOBgH5+fX1+f4GDhomLjo+Pj46Ni4qIhoWDgYB+fn19fn+BgoWIi42Oj4+OjYuKiIaFg4F/fn19fX5/gYOFiIuNjo6Ojo2LioiGhIOBf35+fX1+f4GDhYiLjY6Ojo2Mi4mIhoSDgX9+fn19fn+BgoSHioyNjo6NjYuKiIaEg4F/fn59fX5/gIKEh4qMjY6OjY2LioiGhIOBf35+fX1+f4CCBIeKjI2NjY2Ni4qIhoSDgX9+fn19fn+AgoSHioyNjY2NjIuJiIaEg4GAf35+fX5/gIKEh4qMjY2NjIyLiYiGhIOBgH9+fn1+f4CCBIeKjI2NjYyMi4mIhoSDgYB/fn5+fn+AgoSHiouNjY2MjIuJiIaEg4GAfn5+fn5/gIKEhomLjI2NjIyLiYiGhIOBgH5+fn5+f4CChIaJi4yNjYyMi4mIhoSDgYB+fn5+fn+AgoSGiYuMjI2MjIuJiIaEg4GAfn5+fn5/gIKEhomLjIyNjIuLiYiGhIOBgH5+fn5+f4CChIaJi4yMjIyLi4mIhoSEgYB/fn5+fn+AgoSGiYuMjIyMi4uJiIaEg4GAfn5+fn5/gIKEhomLjIyMi4uLiYiGhISDgYB/fn5+f3+AgoSGiYuMjIyLi4uJiIaFhIKBf35+fn5/gIGDhYiKi4yMjIuLi4mIhoWEgoF/fn5+fn9/gYOFiIqLjIyMi4uLiYiHhYSCgX9+fn5+f4CBg4WIiouMjIyLi4qJiIeFhIKBf35+fn5/f4GDhYeKi4uMjIuLi4mIh4WEgoF/fn5+fn9/gYOFh4qLi4yLi4uKiYeGhYSCgX9+fn5+f3+Bg4WHiouLjIuLi4qJh4aFhIKBf39+fn5/f4GDhYeJi4uLi4uLiomHhoWEgoGAf35+fn9/gIKDhYeJi4uLi4uLiomHhoWEgoGAf35+fn9/gIKDhYeJi4uLi4uLiomIhoWEgoGAf39+fn9/gIKDhYeJiouLi4uKiomIhoWEgoGAf39+fn9/gIKDhYeJiouLi4uKiomIhoWEg4KBf39+fn9/gIKDhYeJiouLi4uKiomIhoaFg4KBf39+fn9/gIGDBQ==';

  // Stubs for removed features (persistence/analytics)
  function saveChat() {}
  function loadChat() { return null; }
  function clearSavedChat() {}
  function trackEvent() {}

  // ============================================================
  // NOTIFICATION SOUND
  // ============================================================
  var notifAudio = null;
  var audioUnlocked = false;
  function unlockAudio() {
    if (audioUnlocked) return;
    try {
      notifAudio = new Audio(NOTIF_SOUND_URL);
      notifAudio.volume = 0.3;
      notifAudio.play().then(function () {
        notifAudio.pause();
        notifAudio.currentTime = 0;
        audioUnlocked = true;
      }).catch(function () {});
    } catch (e) {}
  }
  function playNotifSound() {
    try {
      if (!notifAudio) { notifAudio = new Audio(NOTIF_SOUND_URL); notifAudio.volume = 0.3; }
      notifAudio.currentTime = 0;
      notifAudio.play().catch(function () {});
    } catch (e) {}
  }

  // ============================================================
  // UNREAD BADGE
  // ============================================================
  var unreadCount = 0;
  function updateBadge() {
    var badge = document.getElementById('bw-notif');
    if (!badge) return;
    if (unreadCount > 0 && !STATE.isOpen) {
      badge.style.display = 'block';
      badge.textContent = unreadCount > 9 ? '9+' : unreadCount;
      badge.style.fontSize = '9px';
      badge.style.color = '#fff';
      badge.style.lineHeight = '16px';
      badge.style.textAlign = 'center';
      badge.style.fontWeight = '700';
    } else {
      badge.style.display = 'none';
      unreadCount = 0;
    }
  }

  function notifyNewMessage() {
    if (!STATE.isOpen) {
      unreadCount++;
      updateBadge();
      playNotifSound();
    }
  }

  // ============================================================
  // ESCALATION — Multi-trigger system (T-01 to T-19)
  // ============================================================

  // T-01: Legal threats → CRITICAL (immediate escalation)
  var LEGAL_KEYWORDS = [
    'denuncio','denunciar','denuncia','vie legali','abogado','abogados','demanda judicial',
    'demanda legal','accion legal','acción legal','los voy a demandar',
    'lawyer','legal action','sue you','take legal','court','lawsuit','attorney',
    'avvocato','tribunale','querela','azione legale','vi denuncio',
    'advogado','tribunal','processo judicial','ação legal','vou processar',
    // T-03: Regulator mentions → CRITICAL
    'sernac','defensa del consumidor','regulador','authorities','autorità',
    'agcm','procon','órgão competente','regulatory','autoridades'
  ];

  // T-02: Fraud/scam accusations → CRITICAL (immediate escalation)
  var FRAUD_KEYWORDS = [
    'fraude','estafa','me estafaron','esto es un fraude','están estafando','empresa fraudulenta','sitio falso',
    'fraud','scam','i\'ve been scammed','this is fraud','you\'re scamming','fraudulent company','fake site',
    'frode','truffa','mi hanno truffato','questa è una frode','state truffando','azienda fraudolenta','sito falso',
    'golpe','fui enganado','isso é fraude','estão enganando','empresa fraudulenta','site falso'
  ];

  // T-07: Frustration/negative sentiment keywords
  var FRUSTRATION_KEYWORDS = [
    // ES
    'inútil','no sirve','basura','robo','ladrones','mentirosos','ridículo','una mierda',
    'están robando','vergüenza','peor servicio','nunca más','quiero mi dinero',
    // EN
    'useless','garbage','theft','thieves','liars','ridiculous','bullshit',
    'you\'re stealing','shame','worst service','never again','i want my money','terrible','pathetic',
    // IT
    'inutile','spazzatura','furto','ladri','bugiardi','ridicolo','schifezza',
    'state rubando','vergogna','peggior servizio','mai più','rivoglio i miei soldi',
    // PT
    'lixo','roubo','ladrões','mentirosos','ridículo','uma merda',
    'estão roubando','vergonha','pior serviço','nunca mais','quero meu dinheiro'
  ];

  // T-18: Client unhappy with bot answer
  var UNHAPPY_KEYWORDS = [
    'esto no es correcto','no es correcto','estás equivocado','respuesta incorrecta','eso no es verdad','no me sirve',
    'this is wrong','you\'re wrong','you are wrong','that\'s incorrect','that is incorrect','not correct','doesn\'t help','does not help','useless answer',
    'non è corretto','è sbagliato','risposta sbagliata','non è vero','non mi serve',
    'isso não está certo','está errado','resposta errada','não está correto','não me ajuda'
  ];

  // T-01 + T-03: Detect legal threats and regulator mentions
  function detectLegalThreat(text) {
    var lower = text.toLowerCase();
    for (var i = 0; i < LEGAL_KEYWORDS.length; i++) {
      if (lower.indexOf(LEGAL_KEYWORDS[i]) !== -1) { return 'legal_threat'; }
    }
    return false;
  }

  // T-02: Detect fraud/scam accusations
  function detectFraudAccusation(text) {
    var lower = text.toLowerCase();
    for (var i = 0; i < FRAUD_KEYWORDS.length; i++) {
      if (lower.indexOf(FRAUD_KEYWORDS[i]) !== -1) { return 'fraud_accusation'; }
    }
    return false;
  }

  // T-07: Detect frustration/negative sentiment
  function detectFrustration(text) {
    var lower = text.toLowerCase();
    var signals = 0;
    // Check keywords
    for (var i = 0; i < FRUSTRATION_KEYWORDS.length; i++) {
      if (lower.indexOf(FRUSTRATION_KEYWORDS[i]) !== -1) { signals++; }
    }
    // Check CAPS (more than 50% uppercase and length > 10)
    if (text.length > 10 && text.replace(/[^A-Z]/g, '').length > text.length * 0.5) { signals += 2; }
    // Check excessive punctuation (!!! or ???)
    if ((text.match(/[!?]{3,}/g) || []).length > 0) { signals++; }
    return signals >= 1;
  }

  // T-18: Detect client unhappy with answer
  function detectUnhappy(text) {
    var lower = text.toLowerCase();
    for (var i = 0; i < UNHAPPY_KEYWORDS.length; i++) {
      if (lower.indexOf(UNHAPPY_KEYWORDS[i]) !== -1) { return true; }
    }
    return false;
  }

  // T-17: Reset inactivity timer on every user action
  function resetInactivityTimer() {
    if (STATE.inactivityTimer) { clearTimeout(STATE.inactivityTimer); }
    if (STATE.phase !== 'CHAT' && STATE.phase !== 'LIVE_AGENT') return;
    STATE.inactivityReminded = false;
    STATE.inactivityTimer = setTimeout(function () {
      if (STATE.phase === 'CHAT' || STATE.phase === 'LIVE_AGENT') {
        if (!STATE.inactivityReminded) {
          STATE.inactivityReminded = true;
          addMessage('bot', lang === 'en' ? 'Are you still there? Let me know if you need anything else.' :
            lang === 'it' ? 'Sei ancora lì? Fammi sapere se hai bisogno di altro.' :
            lang === 'pt' ? 'Você ainda está aí? Me avise se precisar de algo mais.' :
            '¿Sigues ahí? Avísame si necesitas algo más.');
          // Set close timer
          STATE.inactivityTimer = setTimeout(function () {
            if (STATE.phase === 'CHAT') {
              addMessage('bot', lang === 'en' ? 'Chat closed due to inactivity. Click **New chat** to start again.' :
                lang === 'it' ? 'Chat chiusa per inattività. Clicca **Nuova conversazione** per ricominciare.' :
                lang === 'pt' ? 'Chat encerrado por inatividade. Clique em **Nova conversa** para recomeçar.' :
                'Chat cerrado por inactividad. Haz clic en **Nueva conversación** para volver a empezar.');
              STATE.phase = 'AGENT_CLOSED';
              setInputDisabled(true);
            }
          }, INACTIVITY_CLOSE_MS - INACTIVITY_REMINDER_MS);
        }
      }
    }, INACTIVITY_REMINDER_MS);
  }

  // T-19: Check session duration
  function checkSessionDuration() {
    if (!STATE.sessionStartTime) return false;
    return (Date.now() - STATE.sessionStartTime) > SESSION_MAX_MS;
  }

  // AI-based detection: check if AI response acknowledges a human request
  var HUMAN_RESPONSE_SIGNALS = [
    'prefer to speak','preferisca parlare','prefieres hablar','prefere falar',
    'human agent','agente humano','operatore','persona real','persona reale',
    'not available','non disponibile','no disponible','não disponível',
    'non posso metterti','no puedo conectarte','no puedo transferirte','cannot connect',
    'capisco che','entiendo que','entendo que','understand you',
    'parlare con una persona','hablar con una persona','falar com uma pessoa',
    'speak with someone','talk to someone','speak to a','talk to a',
    'frustración','frustrazione','frustration','frustraci'
  ];

  function aiDetectsHumanRequest(aiResponse) {
    var lower = aiResponse.toLowerCase();
    for (var i = 0; i < HUMAN_RESPONSE_SIGNALS.length; i++) {
      if (lower.indexOf(HUMAN_RESPONSE_SIGNALS[i]) !== -1) { return true; }
    }
    return false;
  }

  function handleWantsHuman(botMessage) {
    STATE.humanRequestCount++;
    // T-07: If frustrated, threshold drops to 1 (immediate escalation on first human request)
    var threshold = STATE.urgency === 'high' ? 1 : HUMAN_REQUEST_THRESHOLD;
    if (STATE.humanRequestCount >= threshold) {
      // T-06 (or T-07 fast-track): Escalate immediately
      addMessage('bot', t('human_escalate'));
      startEscalation(STATE.urgency === 'high' ? 'T-07_frustrated_human_request' : 'T-06_human_request_x2');
    } else {
      // T-05: First request → bot tries to help, acknowledges the request
      addMessage('bot', botMessage);
    }
  }

  // ============================================================
  // AUTO-DETECT PLAYER INFO from site (GR8/Modulor platform)
  // ============================================================
  function getPlayerInfo() {
    var info = { playerId: null, username: null, email: null };
    try {
      // Method 1: Check localStorage for user/auth data
      for (var i = 0; i < localStorage.length; i++) {
        var key = localStorage.key(i);
        if (!key) continue;
        var keyLow = key.toLowerCase();
        if (keyLow.indexOf('user') !== -1 || keyLow.indexOf('auth') !== -1 || keyLow.indexOf('session') !== -1 || keyLow.indexOf('account') !== -1) {
          try {
            var val = JSON.parse(localStorage.getItem(key));
            if (val && typeof val === 'object') {
              info.playerId = info.playerId || val.id || val.userId || val.user_id || val.playerId || val.player_id || val.accountId || null;
              info.username = info.username || val.username || val.login || val.name || val.displayName || null;
              info.email = info.email || val.email || val.mail || null;
            }
          } catch (e) { /* not JSON, skip */ }
        }
      }
      // Method 2: Check window objects
      if (window.__USER__) {
        info.playerId = info.playerId || window.__USER__.id || window.__USER__.playerId;
        info.username = info.username || window.__USER__.username;
        info.email = info.email || window.__USER__.email;
      }
      // Method 3: Check DOM for player ID / username in account area
      var accountEl = document.querySelector('[data-testid*="user"], [class*="user-name"], [class*="username"], [class*="player-id"], [class*="account-id"], [class*="userBox"]');
      if (accountEl && accountEl.textContent) {
        var text = accountEl.textContent.trim();
        if (text && text.length < 50) {
          info.username = info.username || text;
        }
      }
      // Method 4: Check cookies for user ID
      var cookies = document.cookie.split(';');
      for (var j = 0; j < cookies.length; j++) {
        var parts = cookies[j].trim().split('=');
        var cname = (parts[0] || '').toLowerCase();
        if (cname.indexOf('userid') !== -1 || cname.indexOf('player') !== -1 || cname === 'uid') {
          info.playerId = info.playerId || decodeURIComponent(parts[1] || '');
        }
      }
    } catch (e) { console.warn('[BetonWin Support] getPlayerInfo:', e); }
    // Convert any numeric ID to string
    if (info.playerId) { info.playerId = String(info.playerId); }
    return info;
  }

  // ============================================================
  // 5. INJECT CSS
  // ============================================================
  function injectCSS() {
    if (document.getElementById('__beton_css__')) return;
    // Load font asynchronously (non-render-blocking)
    var fontLink = document.createElement('link');
    fontLink.rel = 'preload';
    fontLink.as = 'style';
    fontLink.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap';
    fontLink.onload = function () { this.rel = 'stylesheet'; };
    document.head.appendChild(fontLink);

    var s = document.createElement('style');
    s.id = '__beton_css__';
    s.textContent = [

      /* Root */
      '#__beton_widget__{position:fixed;bottom:24px;right:24px;z-index:2147483647;font-family:"Inter",-apple-system,BlinkMacSystemFont,sans-serif;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}',
      '#__beton_widget__ *{box-sizing:border-box;margin:0;padding:0}',

      /* FAB — BetonWin branded with glow */
      '#bw-trigger{width:58px;height:58px;background:linear-gradient(135deg,'+C.green+' 0%,#1ac45e 100%);border:none;border-radius:16px;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:'+C.triggerShadow+';transition:all .45s cubic-bezier(.22,1,.36,1);position:relative;outline:none}',
      '#bw-trigger::after{content:"";position:absolute;inset:-6px;border-radius:20px;border:1.5px solid rgba(45,236,118,0.15);animation:bw-ring 3s ease-in-out infinite;pointer-events:none}',
      '#bw-trigger:hover{transform:scale(1.06) translateY(-2px);box-shadow:0 0 0 8px rgba(45,236,118,0.08),0 12px 40px rgba(0,0,0,0.5),0 0 30px rgba(45,236,118,0.12)}',
      '#bw-trigger:active{transform:scale(.94)}',
      '#bw-trigger.bw-open{transform:scale(0) rotate(90deg);opacity:0;pointer-events:none}',
      '#bw-trigger svg{width:24px;height:24px;fill:#fff;filter:drop-shadow(0 1px 2px rgba(0,0,0,0.2))}',
      '#bw-notif{position:absolute;top:-4px;right:-4px;width:16px;height:16px;background:'+C.danger+';border-radius:50%;border:2.5px solid '+C.bg+';display:none;box-shadow:0 2px 8px rgba(248,113,113,0.5)}',

      /* Window — deep teal glass */
      '#bw-window{position:absolute;bottom:74px;right:0;width:400px;height:620px;background:rgba(3,36,45,0.92);backdrop-filter:blur(28px) saturate(1.4);-webkit-backdrop-filter:blur(28px) saturate(1.4);border-radius:20px;border:1px solid rgba(45,236,118,0.08);box-shadow:'+C.shadow+';display:flex;flex-direction:column;overflow:hidden;transform-origin:calc(100% - 28px) calc(100% + 28px);transition:transform .45s cubic-bezier(.22,1,.36,1),opacity .25s ease;transform:scale(0);opacity:0;pointer-events:none}',
      '#bw-window.bw-open{transform:scale(1);opacity:1;pointer-events:all}',

      /* Header — branded gradient strip */
      '#bw-header{background:linear-gradient(135deg,rgba(3,36,45,0.95) 0%,rgba(4,46,56,0.95) 100%);border-bottom:1px solid rgba(45,236,118,0.1);padding:14px 18px;display:flex;align-items:center;gap:12px;flex-shrink:0;position:relative}',
      '#bw-header::after{content:"";position:absolute;bottom:0;left:18px;right:18px;height:1px;background:linear-gradient(90deg,transparent,rgba(45,236,118,0.2),transparent)}',
      '#bw-avatar{width:40px;height:40px;background:'+C.bg+';border-radius:12px;display:flex;align-items:center;justify-content:center;flex-shrink:0;box-shadow:0 0 0 1px rgba(45,236,118,0.15),0 0 16px rgba(45,236,118,0.08);position:relative;overflow:hidden;padding:6px}',
      '#bw-avatar img{width:100%;height:auto;display:block}',
      '#bw-hinfo{flex:1;min-width:0}',
      '#bw-botname{color:'+C.text+';font-weight:700;font-size:14px;line-height:1.2;letter-spacing:-0.3px}',
      '#bw-status{color:'+C.green+';font-size:11px;display:flex;align-items:center;gap:5px;margin-top:3px;font-weight:500;opacity:.8}',
      '#bw-statusdot{width:6px;height:6px;background:'+C.green+';border-radius:50%;animation:bw-pulse 2.5s ease-in-out infinite;flex-shrink:0;box-shadow:0 0 8px rgba(45,236,118,0.5)}',
      '#bw-hbtns{display:flex;gap:2px}',
      '.bw-hbtn{width:32px;height:32px;background:transparent;border:none;border-radius:10px;cursor:pointer;display:flex;align-items:center;justify-content:center;color:'+C.textMuted+';transition:all .2s;outline:none}',
      '.bw-hbtn:hover{background:rgba(45,236,118,.06);color:'+C.green+'}',
      '.bw-hbtn svg{width:14px;height:14px;fill:currentColor}',

      /* Messages area */
      '#bw-msgs{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:10px;scroll-behavior:smooth;overscroll-behavior:contain}',
      '#bw-msgs::-webkit-scrollbar{width:3px}',
      '#bw-msgs::-webkit-scrollbar-track{background:transparent}',
      '#bw-msgs::-webkit-scrollbar-thumb{background:rgba(45,236,118,0.12);border-radius:3px}',

      /* Message rows */
      '.bw-msg{display:flex;gap:8px;max-width:85%;animation:bw-up .35s cubic-bezier(.22,1,.36,1)}',
      '.bw-msg.user{margin-left:auto;flex-direction:row-reverse}',
      '.bw-mavatar{width:26px;height:26px;background:'+C.bg+';border:1px solid rgba(45,236,118,0.15);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:12px;flex-shrink:0;align-self:flex-end;overflow:hidden;padding:3px}',
      '.bw-mavatar svg{width:100%;height:auto}',

      /* Bubbles */
      '.bw-bubble{padding:10px 14px;border-radius:16px;font-size:13.5px;line-height:1.65;word-break:break-word;white-space:pre-line;letter-spacing:-0.01em}',
      '.bw-msg.bot .bw-bubble{background:rgba(45,236,118,0.03);border:1px solid rgba(45,236,118,0.08);color:rgba(232,240,242,0.85);border-bottom-left-radius:4px}',
      '.bw-msg.user .bw-bubble{background:linear-gradient(135deg,'+C.green+' 0%,#1ac45e 100%);color:#fff;border-bottom-right-radius:4px;box-shadow:0 4px 16px rgba(45,236,118,0.2)}',
      '.bw-bubble b,.bw-bubble strong{font-weight:600;color:#fff}',
      '.bw-msg.bot .bw-bubble strong{color:'+C.green+'}',
      '.bw-bubble em,.bw-bubble i{font-style:italic}',
      '.bw-bubble hr{border:none;border-top:1px solid rgba(45,236,118,.08);margin:8px 0}',

      /* Agent messages — distinct style from bot */
      '.bw-msg.agent .bw-bubble{background:rgba(251,191,36,0.06);border:1px solid rgba(251,191,36,0.15);color:rgba(232,240,242,0.9);border-bottom-left-radius:4px}',
      '.bw-msg.agent .bw-bubble strong{color:'+C.warning+'}',
      '.bw-msg.agent .bw-mavatar{border-color:rgba(251,191,36,0.3);background:rgba(251,191,36,0.08)}',
      '.bw-agent-name{font-size:10px;color:'+C.warning+';font-weight:600;margin-bottom:2px;letter-spacing:0.3px}',

      /* Typing indicator — AI pulse wave */
      '#bw-typing{display:none;align-items:center;gap:10px;animation:bw-up .28s ease;padding:2px 0}',
      '#bw-typing.show{display:flex}',
      '#bw-tdots{background:rgba(45,236,118,0.04);border:1px solid rgba(45,236,118,0.1);border-radius:4px 14px 14px 14px;padding:9px 16px;display:flex;gap:3px;align-items:center}',
      '.bw-dot{width:3px;height:12px;background:'+C.green+';border-radius:2px;animation:bw-wave 1.2s ease-in-out infinite;opacity:.4}',
      '.bw-dot:nth-child(2){animation-delay:.1s;height:18px}',
      '.bw-dot:nth-child(3){animation-delay:.2s;height:10px}',
      '#bw-tlabel{color:rgba(45,236,118,0.55);font-size:11px;font-weight:500;letter-spacing:.3px}',
      '#bw-tlabel::after{content:"";display:inline-block;animation:bw-ellipsis 1.5s steps(4,end) infinite;width:0;overflow:hidden;vertical-align:bottom}',

      /* Quick actions */
      '#bw-qactions{padding:4px 16px 12px;display:flex;flex-wrap:wrap;gap:8px;flex-shrink:0}',
      '.bw-qbtn{background:rgba(45,236,118,0.05);border:1px solid rgba(45,236,118,0.12);color:'+C.green+';border-radius:100px;padding:8px 16px;font-size:12.5px;font-weight:500;cursor:pointer;transition:all .25s cubic-bezier(.22,1,.36,1);font-family:inherit;outline:none;white-space:nowrap}',
      '.bw-qbtn:hover{background:rgba(45,236,118,0.1);border-color:rgba(45,236,118,0.25);transform:translateY(-1px);box-shadow:0 4px 16px rgba(45,236,118,0.1)}',
      '.bw-qbtn:active{transform:translateY(0) scale(.97)}',

      /* ID form */
      '#bw-idform{padding:4px 16px 12px;display:none;gap:8px;flex-shrink:0;align-items:center}',
      '#bw-idform.show{display:flex}',
      '#bw-idinput{flex:1;background:'+C.input+';border:1px solid '+C.inputBorder+';color:'+C.text+';border-radius:12px;padding:10px 13px;font-size:13px;outline:none;transition:all .2s;font-family:inherit}',
      '#bw-idinput:focus{border-color:rgba(45,236,118,0.3);box-shadow:0 0 0 3px rgba(45,236,118,0.06)}',
      '#bw-idinput::placeholder{color:'+C.textMuted+'}',
      '#bw-idconfirm{background:linear-gradient(135deg,'+C.green+',#1ac45e);border:none;color:#fff;border-radius:12px;padding:10px 18px;font-size:13px;font-weight:600;cursor:pointer;transition:all .2s;white-space:nowrap;font-family:inherit;outline:none}',
      '#bw-idconfirm:hover{opacity:.9;transform:translateY(-1px);box-shadow:0 4px 12px rgba(45,236,118,0.2)}',

      /* Upload area */
      '#bw-upload{margin:4px 16px 12px;border:1.5px dashed rgba(45,236,118,0.12);border-radius:14px;padding:22px 16px;text-align:center;cursor:pointer;transition:all .25s;display:none;flex-shrink:0}',
      '#bw-upload.show{display:block}',
      '#bw-upload.drag{border-color:'+C.green+';background:rgba(45,236,118,0.04)}',
      '#bw-upload.busy{opacity:.55;pointer-events:none}',
      '#bw-uico{font-size:28px;margin-bottom:6px}',
      '#bw-utxt{color:rgba(232,240,242,0.5);font-size:13px;font-weight:500}',
      '#bw-uhint{color:'+C.textMuted+';font-size:11px;margin-top:3px}',
      '#bw-ufile{display:none}',
      '#bw-uprog{margin-top:10px;background:rgba(45,236,118,0.06);border-radius:4px;height:3px;overflow:hidden;display:none}',
      '#bw-uprog.show{display:block}',
      '#bw-uprogbar{height:100%;background:linear-gradient(90deg,'+C.green+',#1ac45e);border-radius:3px;width:0%;transition:width .3s}',

      /* Chat input */
      '#bw-inputarea{padding:12px 16px 16px;border-top:1px solid rgba(45,236,118,0.06);display:flex;gap:8px;align-items:flex-end;background:transparent;flex-shrink:0}',
      '#bw-input{flex:1;background:rgba(45,236,118,0.03);border:1px solid rgba(45,236,118,0.08);color:'+C.text+';border-radius:14px;padding:10px 14px;font-size:13.5px;resize:none;outline:none;min-height:42px;max-height:120px;line-height:1.5;font-family:inherit;transition:all .25s cubic-bezier(.22,1,.36,1)}',
      '#bw-input:focus{border-color:rgba(45,236,118,0.25);box-shadow:0 0 0 3px rgba(45,236,118,0.06),0 0 24px -8px rgba(45,236,118,0.1)}',
      '#bw-input::placeholder{color:rgba(232,240,242,0.2)}',
      '#bw-send{width:40px;height:40px;background:linear-gradient(135deg,'+C.green+',#1ac45e);border:none;border-radius:12px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .2s cubic-bezier(.22,1,.36,1);flex-shrink:0;outline:none;box-shadow:0 2px 12px rgba(45,236,118,0.25)}',
      '#bw-send:hover{transform:translateY(-1px);box-shadow:0 4px 20px rgba(45,236,118,0.35)}',
      '#bw-send:active{transform:scale(.93)}',
      '#bw-send:disabled{opacity:.15;cursor:default;transform:none;box-shadow:none}',
      '#bw-send svg{width:16px;height:16px;fill:#fff}',

      /* Emoji picker */
      '#bw-emoji-btn{width:40px;height:40px;background:transparent;border:1px solid rgba(45,236,118,0.08);border-radius:12px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .2s;flex-shrink:0;outline:none;font-size:18px;color:'+C.textMuted+'}',
      '#bw-emoji-btn:hover{background:rgba(45,236,118,0.06);border-color:rgba(45,236,118,0.2)}',
      '#bw-emoji-panel{display:none;position:absolute;bottom:70px;left:16px;right:16px;background:'+C.bg+';border:1px solid rgba(45,236,118,0.12);border-radius:14px;padding:10px;max-height:180px;overflow-y:auto;z-index:10;box-shadow:0 -8px 32px rgba(0,0,0,0.5)}',
      '#bw-emoji-panel.show{display:grid;grid-template-columns:repeat(8,1fr);gap:4px}',
      '.bw-emo{width:100%;aspect-ratio:1;border:none;background:transparent;border-radius:8px;cursor:pointer;font-size:20px;display:flex;align-items:center;justify-content:center;transition:all .15s}',
      '.bw-emo:hover{background:rgba(45,236,118,0.08);transform:scale(1.15)}',

      /* Fullscreen mode */
      '#bw-window.bw-fullscreen{position:fixed;inset:0;width:100%;height:100%;max-height:100%;border-radius:0;bottom:0;right:0;z-index:2147483647}',

      /* Footer */
      '#bw-footer{text-align:center;padding:8px;color:rgba(45,236,118,0.12);font-size:10px;border-top:1px solid rgba(45,236,118,0.04);flex-shrink:0;letter-spacing:.3px;font-weight:500}',

      /* Animations */
      '@keyframes bw-up{from{opacity:0;transform:translateY(8px) scale(.98)}to{opacity:1;transform:translateY(0) scale(1)}}',
      '@keyframes bw-pulse{0%,100%{opacity:1}50%{opacity:.3}}',
      '@keyframes bw-wave{0%,100%{transform:scaleY(.4);opacity:.3}50%{transform:scaleY(1);opacity:1}}',
      '@keyframes bw-ellipsis{0%{content:"";width:0}25%{content:".";width:5px}50%{content:"..";width:10px}75%{content:"...";width:15px}}',
      '@keyframes bw-ring{0%,100%{transform:scale(1);opacity:.4}50%{transform:scale(1.15);opacity:0}}',

      /* Mobile */
      '@media(max-width:440px){#__beton_widget__{bottom:16px;right:12px;left:12px}#bw-window{width:100%;right:0;left:0;bottom:74px;height:calc(100dvh - 94px);max-height:620px;border-radius:18px;transform-origin:bottom center}#bw-trigger{width:52px;height:52px;border-radius:14px}#bw-trigger svg{width:22px;height:22px}#bw-emoji-panel.show{grid-template-columns:repeat(7,1fr)}}'
    ].join('');
    document.head.appendChild(s);
  }

  // ============================================================
  // 6. BUILD HTML
  // ============================================================
  function buildHTML() {
    var container = document.getElementById('__beton_widget__');
    if (!container) {
      container = document.createElement('div');
      container.id = '__beton_widget__';
      document.body.appendChild(container);
    }
    container.innerHTML =
      '<button id="bw-trigger" aria-label="Support Chat">' +
        '<span id="bw-notif"></span>' +
        '<svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H5.17L4 17.17V4h16v12z"/></svg>' +
      '</button>' +
      '<div id="bw-window" role="dialog" aria-label="BetonWin Support">' +
        '<div id="bw-header">' +
          '<div id="bw-avatar"><svg viewBox="0 0 140 20" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto"><path d="M8.25 5.24H6.5L5.9 8.72H7.62C9.11 8.72 9.86 8.06 9.86 6.76C9.86 6.31 9.72 5.94 9.45 5.66C9.18 5.38 8.78 5.24 8.25 5.24ZM7.62 11.54H5.41L4.85 14.75H7.15C7.87 14.75 8.44 14.58 8.86 14.25C9.28 13.92 9.49 13.51 9.49 13.03C9.49 12.03 8.86 11.54 7.62 11.54ZM9.72 1.61C11.49 1.61 12.75 2 13.49 2.77C14.05 3.36 14.33 4.11 14.33 5.01C14.33 5.32 14.3 5.65 14.24 5.99L14.03 7.11C13.86 7.99 13.53 8.68 13.04 9.18C12.55 9.68 12.12 9.93 11.75 9.93L11.72 10.11C12.16 10.11 12.6 10.36 13.05 10.84C13.5 11.32 13.73 11.89 13.73 12.54C13.73 12.8 13.7 13.08 13.63 13.38L13.49 14.1C13.24 15.44 12.65 16.48 11.71 17.25C10.77 18.01 9.46 18.39 7.78 18.39H0L2.96 1.61H9.72Z" fill="#2DEC76"/><path d="M27.01 18.39H15.31L18.27 1.61H28.54C29.29 1.61 29.85 2.28 29.72 3.01L29.32 5.24H21.81L21.28 8.39H27.48L26.82 12.02H20.63L20.16 14.75H27.66L27.01 18.39Z" fill="#2DEC76"/><path d="M46.31 5.24H40.57L38.27 18.39H34.05L36.36 5.24H30.6L31.25 1.61H45.53C46.28 1.61 46.84 2.28 46.71 3.01L46.31 5.24Z" fill="#2DEC76"/><path d="M73.66 9.98C72.99 13.81 69.33 16.93 65.5 16.93C61.67 16.93 59.11 13.81 59.78 9.98C60.45 6.15 64.11 3.04 67.94 3.04C71.78 3.04 74.34 6.15 73.66 9.98ZM68.2 1.6H56.12C51.51 1.61 47.1 5.37 46.28 9.98C45.47 14.6 48.56 18.36 53.16 18.37H65.24C69.86 18.37 74.29 14.61 75.11 9.98C75.92 5.36 72.82 1.6 68.2 1.6Z" fill="white"/><path d="M91.37 3.01L88.68 18.39H84.46L81.52 9.2L79.94 18.39H75.72L78.68 1.61H82.15C82.67 1.61 83.12 1.93 83.29 2.42L85.9 10.18L87.42 1.61H90.19C90.93 1.61 91.49 2.28 91.37 3.01Z" fill="white"/><path d="M108.7 2.84L108.35 14.31H108.88L112.94 1.61H115.83C116.65 1.61 117.23 2.41 116.96 3.19L111.75 18.39H104.76L105.39 7.64L102.26 18.39H95.27L95.43 1.61H98.77C99.44 1.61 99.98 2.17 99.96 2.84L99.58 14.31H100.12L104.2 1.61H107.51C108.18 1.61 108.72 2.17 108.7 2.84Z" fill="#2DEC76"/><path d="M123.74 3.01L121.05 18.39H116.83L119.79 1.61H122.56C123.3 1.61 123.87 2.28 123.74 3.01Z" fill="#2DEC76"/><path d="M139.98 3.01L137.29 18.39H133.07L130.14 9.2L128.55 18.39H124.33L127.29 1.61H130.77C131.28 1.61 131.74 1.93 131.9 2.42L134.52 10.18L136.03 1.61H138.81C139.55 1.61 140.11 2.28 139.98 3.01Z" fill="#2DEC76"/><circle cx="92.12" cy="16.4" r="1.97" fill="white"/></svg></div>' +
          '<div id="bw-hinfo">' +
            '<div id="bw-botname">' + CONFIG.BOT_NAME + '</div>' +
            '<div id="bw-status"><span id="bw-statusdot"></span><span>' + t('online') + '</span></div>' +
          '</div>' +
          '<div id="bw-hbtns">' +
            '<button class="bw-hbtn" id="bw-fullscreen" title="Fullscreen">' +
              '<svg viewBox="0 0 24 24"><path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/></svg>' +
            '</button>' +
            '<button class="bw-hbtn" id="bw-newchat" title="' + t('new_chat') + '">' +
              '<svg viewBox="0 0 24 24"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg>' +
            '</button>' +
            '<button class="bw-hbtn" id="bw-close" title="' + t('close') + '">' +
              '<svg viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>' +
            '</button>' +
          '</div>' +
        '</div>' +
        '<div id="bw-msgs" aria-live="polite" aria-relevant="additions">' +
          '<div id="bw-typing">' +
            '<div id="bw-tdots"><div class="bw-dot"></div><div class="bw-dot"></div><div class="bw-dot"></div></div>' +
            '<span id="bw-tlabel">' + t('typing') + '</span>' +
          '</div>' +
        '</div>' +
        '<div id="bw-qactions" style="display:none"></div>' +
        '<div id="bw-idform">' +
          '<input type="text" id="bw-idinput" placeholder="' + t('player_id_ph') + '" autocomplete="off" maxlength="50">' +
          '<button id="bw-idconfirm">' + t('confirm') + '</button>' +
        '</div>' +
        '<div id="bw-upload">' +
          '<input type="file" id="bw-ufile" accept=".jpg,.jpeg,.png,.webp,.pdf">' +
          '<div id="bw-uico"><svg viewBox="0 0 24 24" width="28" height="28" fill="'+C.textMuted+'"><path d="M9 16h6v-6h4l-7-7-7 7h4v6zm-4 2h14v2H5v-2z"/></svg></div>' +
          '<div id="bw-utxt">' + t('upload_drag') + '</div>' +
          '<div id="bw-uhint">' + t('upload_hint') + '</div>' +
          '<div id="bw-uprog"><div id="bw-uprogbar"></div></div>' +
        '</div>' +
        '<div id="bw-emoji-panel"></div>' +
        '<div id="bw-inputarea">' +
          '<button id="bw-emoji-btn" title="Emoji">😊</button>' +
          '<textarea id="bw-input" placeholder="' + t('placeholder') + '" rows="1"></textarea>' +
          '<button id="bw-send">' +
            '<svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>' +
          '</button>' +
        '</div>' +
        '<div id="bw-footer">Powered by BetonWin Support AI</div>' +
      '</div>';
  }

  // ============================================================
  // 7. UI HELPERS
  // ============================================================
  function escapeHTML(str) {
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function parseMarkdown(txt) {
    // Extract links BEFORE escaping so URLs keep their & chars intact
    var links = [];
    txt = txt.replace(/\[(.*?)\]\((https?:\/\/[^\s)]+)\)/g, function (_, text, url) {
      var idx = links.length;
      links.push({ text: text, url: url });
      return '%%LINK' + idx + '%%';
    });
    var out = escapeHTML(txt)
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      // Bullet lists: lines starting with * or - followed by space → bullet
      .replace(/^[*\-]\s+(.+)$/gm, '• $1')
      // Numbered lists: lines starting with 1. 2. etc → keep number with dot
      .replace(/^(\d+)\.\s+(.+)$/gm, '$1. $2')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/^---$/gm, '<hr>');
    // Restore links with safe escaped text and sanitized URL
    links.forEach(function (link, i) {
      var safeUrl = link.url.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
      out = out.replace('%%LINK' + i + '%%',
        '<a href="' + safeUrl + '" target="_blank" rel="noopener" style="color:' + C.green + ';text-decoration:underline">' + escapeHTML(link.text) + '</a>');
    });
    return out;
  }

  var BOT_AVATAR_SVG = '<svg viewBox="0 0 140 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M8.25 5.24H6.5L5.9 8.72H7.62C9.11 8.72 9.86 8.06 9.86 6.76C9.86 6.31 9.72 5.94 9.45 5.66C9.18 5.38 8.78 5.24 8.25 5.24ZM7.62 11.54H5.41L4.85 14.75H7.15C7.87 14.75 8.44 14.58 8.86 14.25C9.28 13.92 9.49 13.51 9.49 13.03C9.49 12.03 8.86 11.54 7.62 11.54ZM9.72 1.61C11.49 1.61 12.75 2 13.49 2.77C14.05 3.36 14.33 4.11 14.33 5.01C14.33 5.32 14.3 5.65 14.24 5.99L14.03 7.11C13.86 7.99 13.53 8.68 13.04 9.18C12.55 9.68 12.12 9.93 11.75 9.93L11.72 10.11C12.16 10.11 12.6 10.36 13.05 10.84C13.5 11.32 13.73 11.89 13.73 12.54C13.73 12.8 13.7 13.08 13.63 13.38L13.49 14.1C13.24 15.44 12.65 16.48 11.71 17.25C10.77 18.01 9.46 18.39 7.78 18.39H0L2.96 1.61H9.72Z" fill="#2DEC76"/><path d="M27.01 18.39H15.31L18.27 1.61H28.54C29.29 1.61 29.85 2.28 29.72 3.01L29.32 5.24H21.81L21.28 8.39H27.48L26.82 12.02H20.63L20.16 14.75H27.66L27.01 18.39Z" fill="#2DEC76"/><path d="M46.31 5.24H40.57L38.27 18.39H34.05L36.36 5.24H30.6L31.25 1.61H45.53C46.28 1.61 46.84 2.28 46.71 3.01L46.31 5.24Z" fill="#2DEC76"/><path d="M73.66 9.98C72.99 13.81 69.33 16.93 65.5 16.93C61.67 16.93 59.11 13.81 59.78 9.98C60.45 6.15 64.11 3.04 67.94 3.04C71.78 3.04 74.34 6.15 73.66 9.98ZM68.2 1.6H56.12C51.51 1.61 47.1 5.37 46.28 9.98C45.47 14.6 48.56 18.36 53.16 18.37H65.24C69.86 18.37 74.29 14.61 75.11 9.98C75.92 5.36 72.82 1.6 68.2 1.6Z" fill="white"/><circle cx="92.12" cy="16.4" r="1.97" fill="white"/></svg>';
  var AGENT_AVATAR_SVG = '<svg viewBox="0 0 24 24" fill="' + C.warning + '"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>';

  function addMessage(role, content) {
    var msgs   = document.getElementById('bw-msgs');
    var typing = document.getElementById('bw-typing');
    var div    = document.createElement('div');
    div.className = 'bw-msg ' + role;
    var html = parseMarkdown(content);
    if (role === 'bot') {
      div.innerHTML = '<div class="bw-mavatar">' + BOT_AVATAR_SVG + '</div><div class="bw-bubble">' + html + '</div>';
    } else if (role === 'agent') {
      div.innerHTML = '<div class="bw-mavatar">' + AGENT_AVATAR_SVG + '</div><div class="bw-bubble">' + html + '</div>';
    } else {
      div.innerHTML = '<div class="bw-bubble">' + html + '</div>';
    }
    msgs.insertBefore(div, typing);
    msgs.scrollTop = msgs.scrollHeight;
    STATE.messages.push({ role: role, content: content, ts: Date.now() });
    if (STATE.messages.length > MAX_MESSAGES) {
      STATE.messages = STATE.messages.slice(-MAX_MESSAGES);
    }
    saveChat();
    if (role === 'bot') { notifyNewMessage(); }
    return div;
  }

  // Agent message with name badge and distinct style
  function addAgentMessage(agentName, content) {
    var msgs   = document.getElementById('bw-msgs');
    var typing = document.getElementById('bw-typing');
    var div    = document.createElement('div');
    div.className = 'bw-msg agent';
    var html = parseMarkdown(content);
    div.innerHTML =
      '<div class="bw-mavatar">' + AGENT_AVATAR_SVG + '</div>' +
      '<div>' +
        '<div class="bw-agent-name">' + escapeHTML(agentName) + '</div>' +
        '<div class="bw-bubble">' + html + '</div>' +
      '</div>';
    msgs.insertBefore(div, typing);
    msgs.scrollTop = msgs.scrollHeight;
    STATE.messages.push({ role: 'agent', content: agentName + ': ' + content, ts: Date.now() });
    if (STATE.messages.length > MAX_MESSAGES) {
      STATE.messages = STATE.messages.slice(-MAX_MESSAGES);
    }
    saveChat();
    notifyNewMessage();
    return div;
  }

  function showTyping(show, writerName) {
    var el = document.getElementById('bw-typing');
    var label = document.getElementById('bw-tlabel');
    el.classList.toggle('show', show);
    if (show) {
      // Show who is writing: "BetonWin AI is writing" or "María is writing"
      var name = writerName || 'BetonWin AI';
      label.textContent = name + ' ' + t('typing').toLowerCase();
      var m = document.getElementById('bw-msgs'); m.scrollTop = m.scrollHeight;
    }
  }

  function showPlayerIdForm(show) {
    var f = document.getElementById('bw-idform');
    f.classList.toggle('show', show);
    if (show) { document.getElementById('bw-idinput').focus(); }
  }

  function showUpload(show) {
    document.getElementById('bw-upload').classList.toggle('show', show);
  }

  function showQuickActions(show) {
    document.getElementById('bw-qactions').style.display = show ? 'flex' : 'none';
  }

  function setInputDisabled(disabled) {
    document.getElementById('bw-input').disabled = disabled;
    document.getElementById('bw-send').disabled  = disabled;
  }

  function setProgress(pct) {
    var bar  = document.getElementById('bw-uprogbar');
    var prog = document.getElementById('bw-uprog');
    prog.classList.toggle('show', pct > 0);
    bar.style.width = pct + '%';
  }

  // ============================================================
  // 8. KNOWLEDGE BASE — Direct Google Drive search (no n8n)
  // ============================================================

  // Keyword translation map: EN/IT/PT → Spanish equivalents for KB search
  // KB content is primarily in Spanish, so we translate queries to match
  var KB_TRANSLATE = {
    // EN → ES
    'privacy policy': 'seguridad proteccion datos informacion personal privacidad',
    'privacy': 'seguridad proteccion datos informacion personal privacidad',
    'personal data': 'datos personales seguridad proteccion informacion',
    'my information': 'seguridad proteccion datos informacion personal',
    'my data': 'datos personales seguridad proteccion informacion',
    'register': 'registrarse registro cuenta',
    'registration': 'registro registrarse cuenta',
    'sign up': 'registrarse registro',
    'create account': 'crear cuenta registro',
    'refund': 'reembolso devolucion retiro rechazado dinero',
    'refund timeframes': 'reembolso devolucion retiro tiempo plazo dinero',
    'withdraw': 'retiro retirar',
    'withdrawal': 'retiro retirar',
    'deposit': 'deposito depositar',
    'bonus': 'bono bonos promocion',
    'terms and conditions': 'terminos condiciones',
    'terms': 'terminos condiciones',
    'change language': 'cambiar idioma',
    'language': 'idioma',
    'scam': 'estafa casino regulacion licencia juego justo seguridad',
    'manipulated': 'manipulados casino regulacion licencia juego justo RNG',
    'fair play': 'juego justo RNG casino regulacion licencia',
    'rigged': 'manipulados estafa casino regulacion RNG juego justo',
    'rng': 'RNG generador numeros aleatorios juego justo casino regulacion',
    'collaborate': 'colaboracion partnership afiliado programa',
    'collaboration': 'colaboracion partnership afiliado programa',
    'streamer': 'streamer colaboracion partnership afiliado programa',
    'partnership': 'partnership colaboracion afiliado programa',
    'sponsor': 'patrocinio colaboracion partnership afiliado programa',
    'password': 'contraseña clave',
    'forgot password': 'olvide contraseña recuperar clave',
    'reset password': 'restablecer contraseña recuperar clave',
    'login': 'iniciar sesion acceder cuenta',
    'log in': 'iniciar sesion acceder cuenta',
    'verification': 'verificacion KYC identidad',
    'kyc': 'verificacion KYC identidad documento',
    'identity': 'identidad verificacion KYC',
    'payment': 'pago metodo deposito',
    'payment method': 'metodo de pago depositar',
    'crypto': 'criptomonedas crypto bitcoin',
    'bitcoin': 'bitcoin criptomonedas crypto',
    'bet': 'apuesta apostar',
    'sports betting': 'apuestas deportivas',
    'casino': 'casino juegos',
    'slots': 'tragamonedas slots casino',
    'live dealer': 'crupier en vivo casino',
    'responsible gambling': 'juego responsable limites',
    'self-exclusion': 'autoexclusion juego responsable',
    'limit': 'limite limites juego responsable',
    'close account': 'cerrar cuenta cierre',
    'delete account': 'eliminar cuenta cierre datos',
    // IT → ES
    'politica sulla privacy': 'seguridad proteccion datos informacion personal privacidad',
    'dati personali': 'datos personales seguridad proteccion informacion',
    'le mie informazioni': 'seguridad proteccion datos informacion personal',
    'registrazione': 'registro registrarse cuenta',
    'come registrarsi': 'registrarse registro cuenta',
    'rimborso': 'reembolso devolucion retiro rechazado dinero',
    'prelievo': 'retiro retirar',
    'deposito': 'deposito depositar',
    'bonus': 'bono bonos promocion',
    'termini e condizioni': 'terminos condiciones',
    'cambiare lingua': 'cambiar idioma',
    'truffa': 'estafa casino regulacion licencia juego justo seguridad',
    'giochi manipolati': 'manipulados casino regulacion licencia juego justo RNG',
    'collaborazione': 'colaboracion partnership afiliado programa',
    'password dimenticata': 'olvide contraseña recuperar clave',
    'verifica': 'verificacion KYC identidad',
    'metodo di pagamento': 'metodo de pago depositar',
    'scommesse sportive': 'apuestas deportivas',
    'gioco responsabile': 'juego responsable limites',
    'chiudere account': 'cerrar cuenta cierre',
    // PT → ES
    'politica de privacidade': 'seguridad proteccion datos informacion personal privacidad',
    'dados pessoais': 'datos personales seguridad proteccion informacion',
    'minhas informacoes': 'seguridad proteccion datos informacion personal',
    'cadastro': 'registro registrarse cuenta',
    'como me cadastrar': 'registrarse registro cuenta',
    'reembolso': 'reembolso devolucion',
    'saque': 'retiro retirar',
    'deposito': 'deposito depositar',
    'termos e condicoes': 'terminos condiciones',
    'mudar idioma': 'cambiar idioma',
    'golpe': 'estafa casino regulacion licencia juego justo seguridad',
    'jogos manipulados': 'manipulados casino regulacion licencia juego justo RNG',
    'colaboracao': 'colaboracion partnership afiliado programa',
    'esqueci a senha': 'olvide contraseña recuperar clave',
    'verificacao': 'verificacion KYC identidad',
    'metodo de pagamento': 'metodo de pago depositar',
    'apostas esportivas': 'apuestas deportivas',
    'jogo responsavel': 'juego responsable limites',
    'fechar conta': 'cerrar cuenta cierre'
  };

  // Translate a user query into Spanish keywords for KB search
  function translateQueryForKB(query) {
    var lower = query.toLowerCase();
    var translations = [];
    // Check longest phrases first (sort by length descending)
    var keys = Object.keys(KB_TRANSLATE).sort(function (a, b) { return b.length - a.length; });
    keys.forEach(function (key) {
      if (lower.indexOf(key) !== -1) {
        translations.push(KB_TRANSLATE[key]);
      }
    });
    if (translations.length > 0) {
      return translations.join(' ');
    }
    return null; // no translation found, use original
  }

  // GET request to Apps Script / mock KB (CORS-friendly — no preflight triggered)
  function searchKBRaw(query) {
    var url = CONFIG.KB_URL + '?q=' + encodeURIComponent(query) + '&lang=' + lang + '&max=3';
    return fetch(url, { redirect: 'follow' }).then(function (r) {
      if (!r.ok) { throw new Error('KB ' + r.status); }
      return r.json();
    });
  }

  // Smart KB search: original query + translated Spanish query + FAQ fallback, merged & deduplicated
  function searchKB(query) {
    var translated = translateQueryForKB(query);
    var searches = [];

    // Always search with original query
    searches.push(searchKBRaw(query).catch(function () { return { results: [] }; }));

    // If we have a translation, search with translated keywords too
    if (translated) {
      searches.push(searchKBRaw(translated).catch(function () { return { results: [] }; }));
    }

    // Always include a FAQ fallback search to ensure the main FAQ doc is found
    searches.push(searchKBRaw('FAQ preguntas frecuentes atencion cliente').catch(function () { return { results: [] }; }));

    return Promise.all(searches).then(function (results) {
      var seen = {};
      var merged = [];
      // Priority: translated results first, then original, then FAQ fallback
      var allResults = [];
      // translated results (index 1 if exists)
      if (translated && results[1]) { allResults = allResults.concat((results[1].results) || []); }
      // original results (index 0)
      allResults = allResults.concat((results[0].results) || []);
      // FAQ fallback (last index)
      var faqResults = (results[results.length - 1].results) || [];
      allResults = allResults.concat(faqResults);

      allResults.forEach(function (r) {
        if (!seen[r.name]) {
          seen[r.name] = true;
          merged.push(r);
        }
      });
      return { results: merged.slice(0, 5), query: query, count: merged.length };
    });
  }

  // Language words for auto-detecting language from typed text
  // IMPORTANT: avoid shared words between languages to prevent false positives
  var LANG_WORDS = {
    en: ['hello','please','thank you','thanks','how do i','how can i','what is','where is',
         'i want','i need','help me','my account','my deposit','my withdrawal','my bonus',
         'password','register','sign up','refund','privacy','scam','manipulated','rigged',
         'collaborate','streamer','language','withdraw','payment','verify','verification',
         'fair play','terms and conditions','responsible gambling','close account','delete',
         'what happens','how to','can i','is this','are the','i can\'t','doesn\'t work'],
    it: ['ciao','grazie','buongiorno','buonasera','prelievo','prelevare','perché','perche','voglio',
         'questo','questa','subito','ancora','sono','mia','aiuto',
         'depositi','soldi','conto','non ho ricevuto','non è arrivato',
         'dove','come posso','non riesco','accedere','vedere','trovare','voglio sapere',
         'non capisco','qual è','mi serve','il mio','la mia','ho bisogno','vorrei',
         'quale','quanti','quante','ricevere','rispondi','scrivo','registrarmi','registrare',
         'minima','minimo','posso ricevere','come faccio','come si fa','non riesco a',
         'il bonus','il deposito','la password','il conto','cosa devo'],
    es: ['hola','gracias','buenos','retiro','retirar','también','quiero','cuánto','cuándo',
         'dinero','ayuda','cuenta','no he recibido','no ha llegado','por favor',
         'cómo','estoy','tengo','puedo','dónde','puedo ver','no puedo','necesito','quisiera',
         'como funciona','cuanto tarda','cuanto cuesta','como hago','que es','quiero saber',
         'cambiar','nombre','perfil','plata','descontaron','deposité','deposite',
         'retiro','bono','juego','pagina','celular','contraseña','saldo','cumpleaños',
         'porque','cuando','donde','como','mi cuenta','no me deja','que paso',
         'mañana','congelo','funciona','aparece','pendiente','cancelado','rechazado',
         'verificar','verificacion','documento','cerrar','abrir','soy vip','el sitio'],
    pt: ['olá','ola','obrigado','obrigada','saque','sacar','também','quero','quanto',
         'dinheiro','não recebi','não chegou',
         'como posso','estou','tenho','onde posso','não consigo','preciso de',
         'meu','minha','gostaria','verificar','retirada','depositar']
  };

  // Auto-detect language from user message text (overrides browser lang when confident)
  function detectLangFromText(text) {
    var lower = text.toLowerCase();
    var scores = { en: 0, it: 0, es: 0, pt: 0 };
    Object.keys(scores).forEach(function (l) {
      LANG_WORDS[l].forEach(function (w) {
        if (lower.indexOf(w) !== -1) { scores[l]++; }
      });
    });
    var best = null, bestScore = 0, tied = false;
    Object.keys(scores).forEach(function (l) {
      if (scores[l] > bestScore) { best = l; bestScore = scores[l]; tied = false; }
      else if (scores[l] === bestScore && scores[l] > 0) { tied = true; }
    });
    if (tied) { return null; }
    // If already in a non-Spanish language, 1 match is enough to stay
    // If switching TO a new language, require 2 matches
    var minScore = (lang !== 'es' && best === lang) ? 1 : 2;
    if (bestScore < minScore) { return null; }
    return best;
  }

  // Keywords that signal a deposit PROBLEM (triggers verification flow)
  var DEPOSIT_KEYWORDS = [
    'not received','not arrived','deposit missing','missing deposit',
    'deposit failed','deposit problem','check my deposit','verify deposit',
    'deposit not','my deposit',
    'no recibido','no llegó','deposito faltante','verificar deposito',
    'deposito no','mi deposito','problema deposito',
    'non ricevuto','non arrivato','deposito mancante','verifica deposito',
    'deposito non','mio deposito',
    'não recebi','não chegou','depósito não','meu depósito','verificar depósito'
  ];

  function detectIntent(msg) {
    var lower = msg.toLowerCase();
    for (var i = 0; i < DEPOSIT_KEYWORDS.length; i++) {
      if (lower.indexOf(DEPOSIT_KEYWORDS[i]) !== -1) { return 'DEPOSIT'; }
    }
    return 'GENERAL';
  }


  // ============================================================
  // 9. n8n API — webhook calls
  // ============================================================
  function n8nCall(endpoint, body, method) {
    method = method || 'POST';
    var url  = CONFIG.N8N_BASE + endpoint;
    var opts = { method: method, headers: { 'Content-Type': 'application/json' } };
    if (method !== 'GET') {
      var payload = body || {};
      if (STATE.sessionId) { payload.session_id = STATE.sessionId; }
      opts.body = JSON.stringify(payload);
    }
    return fetch(url, opts).then(function (r) {
      if (!r.ok) { throw new Error('n8n HTTP ' + r.status); }
      return r.json();
    });
  }

function apiVerify(playerId) {
    return n8nCall(CONFIG.ENDPOINTS.VERIFY, { player_id: playerId, language: lang });
  }
  function apiStatus(jobId) {
    // Sanitize jobId to prevent path traversal
    var safeId = (jobId || '').replace(/[^a-zA-Z0-9_\-]/g, '');
    return n8nCall(CONFIG.ENDPOINTS.STATUS + '/' + safeId, null, 'GET');
  }
  function apiPresignedUrl(playerId, fileName, fileType) {
    return n8nCall(CONFIG.ENDPOINTS.PRESIGNED, { player_id: playerId, file_name: fileName, file_type: fileType });
  }
  function apiAnalyze(playerId, s3Url, jobId) {
    return n8nCall(CONFIG.ENDPOINTS.ANALYZE, { player_id: playerId, s3_url: s3Url, job_id: jobId });
  }

  // ============================================================
  // 10. POLLING
  // ============================================================
  function startPolling(jobId, onDone) {
    STATE.jobId     = jobId;
    STATE.pollCount = 0;
    clearInterval(STATE.pollTimer);
    STATE.pollTimer = setInterval(function () {
      STATE.pollCount++;
      if (STATE.pollCount > CONFIG.POLL_MAX) {
        clearInterval(STATE.pollTimer);
        onDone({ status: 'TIMEOUT' });
        return;
      }
      apiStatus(jobId).then(function (res) {
        if (res.status && res.status !== 'PENDING') {
          clearInterval(STATE.pollTimer);
          onDone(res);
        }
      }).catch(function (e) { console.warn('[BetonWin Support] poll:', e); });
    }, CONFIG.POLL_INTERVAL_MS);
  }

  function stopPolling() {
    clearInterval(STATE.pollTimer);
    STATE.pollTimer = null;
  }

  // ============================================================
  // 11. FILE UPLOAD — presigned URL → direct S3
  // ============================================================
  function handleFile(file) {
    if (STATE.phase !== 'UPLOAD_REQUIRED') return; // only accept during upload phase
    if (!STATE.playerId) return; // need player ID
    if (!file || file.size === 0) { addMessage('bot', t('err_file_type')); return; }
    if (file.size > CONFIG.MAX_FILE_MB * 1024 * 1024) { addMessage('bot', t('err_file_size')); return; }
    if (CONFIG.ACCEPTED_TYPES.indexOf(file.type) === -1) { addMessage('bot', t('err_file_type')); return; }

    STATE.phase = 'UPLOADING';
    showUpload(false);
    addMessage('bot', t('uploading'));
    setProgress(0);

    apiPresignedUrl(STATE.playerId, file.name, file.type)
      .then(function (data) {
        return uploadToS3(data.presigned_url, file, setProgress).then(function () { return data.s3_url; });
      })
      .then(function (s3Url) {
        addMessage('bot', t('analyzing'));
        STATE.phase = 'ANALYZING';
        return apiAnalyze(STATE.playerId, s3Url, STATE.jobId);
      })
      .then(function (res) {
        if (res.job_id) { startPolling(res.job_id, handleFinalResult); }
        else { handleFinalResult(res); }
      })
      .catch(function (e) {
        console.error('[BetonWin Support] upload:', e);
        addMessage('bot', t('err_generic'));
        STATE.phase = 'CHAT';
        setInputDisabled(false);
      });
  }

  function uploadToS3(url, file, onProgress) {
    return new Promise(function (resolve, reject) {
      var xhr = new XMLHttpRequest();
      xhr.timeout = 60000; // 60s timeout
      xhr.upload.addEventListener('progress', function (e) {
        if (e.lengthComputable) { onProgress(Math.round(e.loaded / e.total * 100)); }
      });
      xhr.addEventListener('load', function () {
        if (xhr.status >= 200 && xhr.status < 300) { resolve(); }
        else { reject(new Error('S3 ' + xhr.status)); }
      });
      xhr.addEventListener('error', reject);
      xhr.addEventListener('timeout', function () { reject(new Error('Upload timeout')); });
      xhr.open('PUT', url);
      xhr.setRequestHeader('Content-Type', file.type);
      xhr.send(file);
    });
  }

  // ============================================================
  // 12. FLOW LOGIC
  // ============================================================
  function handleFinalResult(result) {
    stopPolling();
    setInputDisabled(false);
    setProgress(0);
    switch (result.status) {
      case 'APPROVED':       addMessage('bot', t('result_approved')); break;
      case 'REJECTED':       addMessage('bot', t('result_rejected')); break;
      case 'PENDING_REVIEW': addMessage('bot', t('result_pending'));  break;
      case 'TIMEOUT':        addMessage('bot', t('err_generic'));     break;
      default:               addMessage('bot', t('err_generic'));
    }
    STATE.phase = 'RESULT';
    showQuickActions(true);
  }

  // ============================================================
  // 12b. ESCALATION — Live Agent via Zendesk
  // ============================================================

  // Start escalation: create Zendesk ticket with conversation history
  function startEscalation(reason) {
    STATE.phase = 'ESCALATING';
    showQuickActions(false);
    addMessage('bot', t('escalating'));
    showTyping(true, 'BetonWin AI');
    trackEvent('escalation', { reason: reason });
    setInputDisabled(true);

    var history = STATE.messages.map(function (m) {
      return { role: m.role, content: m.content, ts: m.ts };
    });

    // Auto-detect player info from site
    var playerInfo = getPlayerInfo();
    var playerId = STATE.playerId || playerInfo.playerId || 'unknown';
    var playerName = playerInfo.username || null;
    var playerEmail = playerInfo.email || null;

    // Calculate session duration
    var sessionDuration = STATE.sessionStartTime ? Math.floor((Date.now() - STATE.sessionStartTime) / 1000) : 0;

    n8nCall(CONFIG.ENDPOINTS.ESCALATE, {
      reason: reason,
      priority: reason.startsWith('T-01') || reason.startsWith('T-02') || reason.startsWith('T-03') ? 'CRITICAL' :
               reason.startsWith('T-07') || reason.startsWith('T-06') ? 'HIGH' : 'MEDIUM',
      language: lang,
      conversation_history: history,
      player_id: playerId,
      player_name: playerName,
      player_email: playerEmail,
      urgency: STATE.urgency,
      session_duration_seconds: sessionDuration
    })
    .then(function (res) {
      showTyping(false);
      if (res.ticket_id) {
        STATE.ticketId = res.ticket_id;
        STATE.phase = 'LIVE_AGENT';
        var ticketMsg = t('escalate_ticket').replace('{{id}}', res.ticket_id);
        addMessage('bot', ticketMsg);
        addMessage('bot', t('escalated'));
        setInputDisabled(false);
        // Update header to show "Live Agent" mode
        document.getElementById('bw-botname').textContent = t('live_agent');
        document.getElementById('bw-statusdot').style.background = '#fbbf24';
        // Start polling for agent replies
        startAgentPolling(res.ticket_id);
      } else {
        addMessage('bot', t('err_generic'));
        STATE.phase = 'CHAT';
        setInputDisabled(false);
      }
    })
    .catch(function () {
      showTyping(false);
      addMessage('bot', t('err_generic') + '\n\nEmail: **ayuda@beton.win**');
      STATE.phase = 'CHAT';
      STATE.humanRequestCount = 0;
      setInputDisabled(false);
    });
  }

  // In LIVE_AGENT mode: send user messages to Zendesk as ticket comments
  function sendToAgent(text) {
    if (!STATE.ticketId) return;
    if (!text || text === 'undefined') return;
    addMessage('user', text);
    document.getElementById('bw-input').value = '';
    document.getElementById('bw-input').style.height = 'auto';
    showTyping(true, STATE._agentName || t('live_agent'));
    setInputDisabled(true);

    n8nCall(CONFIG.ENDPOINTS.AGENT_REPLY, {
      ticket_id: STATE.ticketId,
      message: text,
      language: lang
    })
    .then(function () {
      showTyping(false);
      setInputDisabled(false);
    })
    .catch(function () {
      showTyping(false);
      addMessage('bot', t('err_generic'));
      setInputDisabled(false);
    });
  }

  // Poll Zendesk for new agent replies
  function startAgentPolling(ticketId) {
    var pollCount = 0;
    var shownBodies = [];
    clearInterval(STATE.agentPollTimer);

    STATE.agentPollTimer = setInterval(function () {
      pollCount++;
      if (pollCount > AGENT_POLL_MAX) {
        stopAgentPolling();
        addMessage('bot', t('agent_closed'));
        STATE.phase = 'AGENT_CLOSED';
        setInputDisabled(true);
        return;
      }
      n8nCall(CONFIG.ENDPOINTS.AGENT_POLL, { ticket_id: ticketId, since: 0 })
        .then(function (res) {
          if (res.comments && res.comments.length > 0) {
            showTyping(false);
            res.comments.forEach(function (c) {
              var key = c.body + '|' + c.ts;
              if (shownBodies.indexOf(key) !== -1) return;
              shownBodies.push(key);
              var agentName = c.author || t('live_agent');
              addAgentMessage(agentName, c.body);
              document.getElementById('bw-botname').textContent = agentName;
              STATE._agentName = agentName;
            });
          }
          // Only close on truly closed — NOT on pending/solved/open
          if (res.status === 'closed') {
            stopAgentPolling();
            addAgentMessage(t('live_agent'), t('agent_closed'));
            STATE.phase = 'AGENT_CLOSED';
            setInputDisabled(true);
            // Restore bot header
            document.getElementById('bw-botname').textContent = CONFIG.BOT_NAME;
            document.getElementById('bw-statusdot').style.background = C.green;
            // Show CSAT rating
            setTimeout(function () { showCSAT(); }, 1000);
          }
        })
        .catch(function (err) { console.warn('[BetonWin] poll error:', err.message); });
    }, AGENT_POLL_INTERVAL);
  }

  function stopAgentPolling() {
    clearInterval(STATE.agentPollTimer);
    STATE.agentPollTimer = null;
  }

  // Main chat handler — KB first, n8n fallback
  function handleChatMessage(text) {
    text = (text || '').trim();
    if (!text) return;

    // Rate limit + prevent double-send
    var now = Date.now();
    if (STATE.busy || (now - STATE.lastSendTs) < SEND_COOLDOWN) return;
    STATE.busy = true;
    STATE.lastSendTs = now;

    // Cap message length to prevent huge payloads
    if (text.length > MAX_MSG_LENGTH) { text = text.slice(0, MAX_MSG_LENGTH); }

    // Auto-detect language from what the user typed (update global lang + UI)
    var detected = detectLangFromText(text);
    if (detected && LANG[detected] && detected !== lang) {
      lang = detected;
      // Update UI elements to match new language
      document.getElementById('bw-input').placeholder = t('placeholder');
      document.getElementById('bw-idinput').placeholder = t('player_id_ph');
      document.getElementById('bw-idconfirm').textContent = t('confirm');
    }

    // If in LIVE_AGENT mode, send directly to Zendesk (not to AI)
    if (STATE.phase === 'LIVE_AGENT') {
      STATE.busy = false;
      sendToAgent(text);
      return;
    }
    // If agent closed, only allow new chat
    if (STATE.phase === 'AGENT_CLOSED') {
      STATE.busy = false;
      return;
    }

    addMessage('user', text);
    trackEvent('message_sent', { length: text.length });
    document.getElementById('bw-input').value = '';
    document.getElementById('bw-input').style.height = 'auto';
    showTyping(true, 'BetonWin AI');
    setInputDisabled(true);

    // T-17: Reset inactivity timer on user message
    resetInactivityTimer();

    // T-19: Track session start
    if (!STATE.sessionStartTime) { STATE.sessionStartTime = Date.now(); }

    // T-07: Check frustration → increase urgency
    if (detectFrustration(text)) {
      STATE.urgency = 'high';
    }

    // T-18: Check if client is unhappy with previous answer
    if (detectUnhappy(text)) {
      STATE.unhappyCount++;
      if (STATE.unhappyCount >= 2) {
        // Second time unhappy → propose agent
        showTyping(false);
        var proposeMsg = lang === 'en' ? 'I see my answer didn\'t help. Would you like me to connect you with a support agent?' :
          lang === 'it' ? 'Vedo che la mia risposta non è stata utile. Vuoi che ti colleghi con un agente?' :
          lang === 'pt' ? 'Vejo que minha resposta não ajudou. Quer que eu conecte você com um agente?' :
          'Veo que mi respuesta no te ayudó. ¿Quieres que te conecte con un agente de soporte?';
        addMessage('bot', proposeMsg);
        STATE.busy = false;
        return;
      }
    }

    // Safety: auto-recover if stuck for 30s (network hang, unhandled error)
    var safetyTimer = setTimeout(function () {
      if (STATE.busy) {
        showTyping(false);
        setInputDisabled(false);
        STATE.busy = false;
      }
    }, 30000);

    // Helper: reset busy state + clear safety timer
    function unlockInput() {
      clearTimeout(safetyTimer);
      setInputDisabled(false);
      STATE.busy = false;
    }

    // T-01/T-03: Legal threats + regulator → CRITICAL immediate escalation
    if (detectLegalThreat(text)) {
      showTyping(false);
      addMessage('bot', t('human_escalate'));
      clearTimeout(safetyTimer);
      STATE.busy = false;
      startEscalation('T-01_legal_threat');
      return;
    }

    // T-02: Fraud/scam accusations → CRITICAL immediate escalation
    if (detectFraudAccusation(text)) {
      showTyping(false);
      addMessage('bot', t('human_escalate'));
      clearTimeout(safetyTimer);
      STATE.busy = false;
      startEscalation('T-02_fraud_accusation');
      return;
    }

    // T-07: If high urgency from frustration → reduce human request threshold to 1
    if (STATE.urgency === 'high' && STATE.humanRequestCount === 0) {
      // Don't escalate yet, but any human request signal will trigger immediately
    }

    // 1. Detect deposit problem → start verification flow
    if (detectIntent(text) === 'DEPOSIT') {
      showTyping(false);
      addMessage('bot', t('deposit_intent'));
      unlockInput();
      startDepositFlow();
      return;
    }

    // 2. Search KB (max 1.5s) → send content + history to n8n AI
    var kbCall = Promise.race([
      searchKB(text),
      new Promise(function (resolve) { setTimeout(function () { resolve({ results: [] }); }, 1500); })
    ]);
    kbCall
      .catch(function () { return { results: [] }; })
      .then(function (data) {
        // Guard against malformed KB response (e.g. empty query returns {status, message})
        if (!data.results || !Array.isArray(data.results)) { data = { results: [] }; }
        var kbContent = '';
        if (data.results && data.results.length > 0) {
          // Filter out PDFs (no useful text content) and take top 2
          var useful = data.results.filter(function (r) {
            return r.type !== 'application/pdf' && (r.content || '').length > 50;
          });
          kbContent = useful.slice(0, 2).map(function (r, i) {
            var c = (r.content || '').slice(0, 1200);
            return '[' + (i + 1) + '] ' + (r.name || '') + ':\n' + c;
          }).join('\n\n---\n\n');
        }
        var history = STATE.messages.slice(-6).map(function (m) {
          return { role: (m.role === 'bot' || m.role === 'agent') ? 'assistant' : 'user', content: m.content };
        });
        var aiTimeout = new Promise(function (_, reject) {
          setTimeout(function () { reject(new Error('timeout')); }, 12000);
        });
        // Add language instruction to kb_content so AI knows to respond in the right language
        var LANG_NAMES = { en: 'English', es: 'Spanish', it: 'Italian', pt: 'Portuguese' };
        var langInstruction = '';
        if (lang !== 'es') {
          langInstruction = 'IMPORTANT: The user is writing in ' + (LANG_NAMES[lang] || 'Spanish') +
            '. You MUST respond in ' + (LANG_NAMES[lang] || 'Spanish') + '. Do NOT refuse or redirect to another language.\n\n';
        }
        var payload = { message: text, kb_content: langInstruction + kbContent, lang: lang, history: history };
        return Promise.race([
          n8nCall(CONFIG.ENDPOINTS.CHAT, payload),
          aiTimeout
        ]);
      })
      .then(function (res) {
        showTyping(false);
        var raw = res.response || res.message || t('err_generic');
        // Strip <!--lang:XX--> tag and update language
        var langMatch = raw.match(/<!--lang:([a-z]{2})-->/);
        if (langMatch && LANG[langMatch[1]]) { lang = langMatch[1]; }
        raw = raw.replace(/<!--lang:[a-z]{2}-->\s*/g, '').trim();
        // Detect language rejection from n8n and retry in Spanish as fallback
        var rejectPatterns = ['non offriamo supporto', 'no ofrecemos soporte', 'no ofrezco soporte',
          'do not offer support', 'não oferecemos suporte', 'riformulare', 'reformule',
          'not offer assistance', 'currently not available in', 'parlo solo',
          'can only answer in', 'solo puedo responder en', 'posso rispondere solo in',
          'only answer in spanish', 'only respond in spanish'];
        var isRejected = rejectPatterns.some(function (p) { return raw.toLowerCase().indexOf(p) !== -1; });
        if (isRejected) {
          // Retry with Spanish-wrapped message so n8n AI accepts it
          var wrappedMsg = 'Pregunta del cliente (responde en español): ' + text;
          var retryPayload = { message: wrappedMsg, kb_content: langInstruction + kbContent, lang: 'es', history: history };
          n8nCall(CONFIG.ENDPOINTS.CHAT, retryPayload)
            .then(function (r2) {
              var retryRaw = r2.response || r2.message || t('err_generic');
              retryRaw = retryRaw.replace(/<!--lang:[a-z]{2}-->\s*/g, '').trim();
              // Check if retry was also rejected
              var retryRejected = rejectPatterns.some(function (p) { return retryRaw.toLowerCase().indexOf(p) !== -1; });
              addMessage('bot', retryRejected ? t('no_results') : retryRaw);
              unlockInput();
            })
            .catch(function () {
              addMessage('bot', t('no_results'));
              unlockInput();
            });
          return;
        }
        // AI-based human request detection:
        // If AI response acknowledges the user wants a human → count it
        if (aiDetectsHumanRequest(raw)) {
          handleWantsHuman(raw);
          unlockInput();
          return;
        }
        addMessage('bot', raw);

        // T-19: Check if session exceeded 10 minutes
        if (checkSessionDuration()) {
          var sessionMsg = lang === 'en' ? 'I see this is taking a while. Would you like me to connect you with a support agent for faster help?' :
            lang === 'it' ? 'Vedo che ci sta mettendo un po\'. Vuoi che ti colleghi con un agente per un aiuto più rapido?' :
            lang === 'pt' ? 'Vejo que está demorando. Quer que eu conecte você com um agente para ajuda mais rápida?' :
            'Veo que esto está tomando un poco más de tiempo. ¿Quieres que te conecte con un agente para ayuda más rápida?';
          addMessage('bot', sessionMsg);
          STATE.sessionStartTime = null; // reset so we don't repeat
        }

        unlockInput();
      })
      .catch(function () {
        showTyping(false);
        addMessage('bot', t('err_generic'));
        unlockInput();
      });
  }

  function startDepositFlow() {
    STATE.phase = 'DEPOSIT_ASK_ID';
    showQuickActions(false);
    setTimeout(function () {
      addMessage('bot', t('deposit_ask_id'));
      showPlayerIdForm(true);
    }, 350);
  }

  function handlePlayerIdSubmit(id) {
    id = (id || '').trim();
    if (!id) return;
    if (STATE.phase !== 'DEPOSIT_ASK_ID') return; // only accept during deposit flow
    // Sanitize: alphanumeric + dash/underscore only, max 50 chars
    id = id.replace(/[^a-zA-Z0-9_\-]/g, '').slice(0, 50);
    if (!id) return;
    STATE.playerId = id;
    showPlayerIdForm(false);
    addMessage('user', id);
    setInputDisabled(true);
    addMessage('bot', t('deposit_checking'));
    showTyping(true, 'BetonWin AI');
    STATE.phase = 'DEPOSIT_CHECKING';

    apiVerify(id)
      .then(function (res) {
        showTyping(false);
        if (res.status === 'PROCESSING') {
          addMessage('bot', t('deposit_proc'));
          STATE.phase = 'CHAT';
          setInputDisabled(false);
          showQuickActions(true);
        } else if (res.status === 'NEED_UPLOAD') {
          if (res.job_id) { STATE.jobId = res.job_id; }
          addMessage('bot', t('upload_required'));
          showUpload(true);
          STATE.phase = 'UPLOAD_REQUIRED';
        } else if (res.status === 'PENDING' && res.job_id) {
          startPolling(res.job_id, handleFinalResult);
        } else {
          handleFinalResult(res);
        }
      })
      .catch(function () {
        showTyping(false);
        addMessage('bot', t('err_generic'));
        STATE.phase = 'CHAT';
        setInputDisabled(false);
      });
  }

  // ============================================================
  // 13. EVENT BINDING
  // ============================================================
  function bindEvents() {
    document.getElementById('bw-trigger').addEventListener('click', function () { unlockAudio(); toggleOpen(true); });
    document.getElementById('bw-close').addEventListener('click', function ()   { toggleOpen(false); });
    document.getElementById('bw-newchat').addEventListener('click', resetChat);

    document.getElementById('bw-send').addEventListener('click', function () {
      var val = document.getElementById('bw-input').value;
      if (val && val !== 'undefined') handleChatMessage(val);
    });
    document.getElementById('bw-input').addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); if (this.value && this.value !== 'undefined') handleChatMessage(this.value); }
    });
    document.getElementById('bw-input').addEventListener('input', function () {
      this.style.height = 'auto';
      this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });

    // Fullscreen toggle
    var isFullscreen = false;
    document.getElementById('bw-fullscreen').addEventListener('click', function () {
      isFullscreen = !isFullscreen;
      document.getElementById('bw-window').classList.toggle('bw-fullscreen', isFullscreen);
      this.innerHTML = isFullscreen
        ? '<svg viewBox="0 0 24 24"><path d="M5 16h3v3h2v-5H5v2zm3-8H5v2h5V5H8v3zm6 11h2v-3h3v-2h-5v5zm2-11V5h-2v5h5V8h-3z"/></svg>'
        : '<svg viewBox="0 0 24 24"><path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/></svg>';
    });

    // Emoji picker
    var emojiPanel = document.getElementById('bw-emoji-panel');
    var EMOJIS = ['👍','👎','😊','😂','😢','😡','🙏','❤️','🔥','⭐','✅','❌','💰','🎰','🎲','💳','🏦','📧','📞','⏳','🤔','👋','🎁','🍀'];
    emojiPanel.innerHTML = EMOJIS.map(function (e) {
      return '<button class="bw-emo" data-e="' + e + '">' + e + '</button>';
    }).join('');
    document.getElementById('bw-emoji-btn').addEventListener('click', function () {
      emojiPanel.classList.toggle('show');
    });
    emojiPanel.addEventListener('click', function (e) {
      var btn = e.target.closest('.bw-emo');
      if (!btn) return;
      var input = document.getElementById('bw-input');
      input.value += btn.getAttribute('data-e');
      input.focus();
      emojiPanel.classList.remove('show');
    });
    document.addEventListener('click', function (e) {
      if (!e.target.closest('#bw-emoji-panel') && !e.target.closest('#bw-emoji-btn')) {
        emojiPanel.classList.remove('show');
      }
    });

    // Quick deposit button
    document.getElementById('bw-qactions').innerHTML =
      '<button class="bw-qbtn" id="bw-qdep">' + t('quick_deposit') + '</button>';
    document.getElementById('bw-qdep').addEventListener('click', function () {
      showQuickActions(false);
      startDepositFlow();
    });

    document.getElementById('bw-idconfirm').addEventListener('click', function () {
      handlePlayerIdSubmit(document.getElementById('bw-idinput').value);
    });
    document.getElementById('bw-idinput').addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { handlePlayerIdSubmit(this.value); }
    });

    var uploadArea = document.getElementById('bw-upload');
    var fileInput  = document.getElementById('bw-ufile');
    uploadArea.addEventListener('click', function () { if (STATE.phase === 'UPLOAD_REQUIRED') fileInput.click(); });
    fileInput.addEventListener('change', function (e) {
      if (e.target.files[0]) { handleFile(e.target.files[0]); }
    });
    uploadArea.addEventListener('dragover',  function (e) { e.preventDefault(); this.classList.add('drag'); });
    uploadArea.addEventListener('dragleave', function ()  { this.classList.remove('drag'); });
    uploadArea.addEventListener('drop', function (e) {
      e.preventDefault();
      this.classList.remove('drag');
      if (e.dataTransfer.files[0]) { handleFile(e.dataTransfer.files[0]); }
    });
  }

  // ============================================================
  // 14. WIDGET CONTROL
  // ============================================================
  function toggleOpen(open) {
    STATE.isOpen = open;
    document.getElementById('bw-trigger').classList.toggle('bw-open', open);
    document.getElementById('bw-window').classList.toggle('bw-open', open);
    if (open) {
      document.getElementById('bw-input').focus();
      unreadCount = 0;
      updateBadge();
    }
    // If user closes widget during live agent session → notify agent on Zendesk
    if (!open && STATE.phase === 'LIVE_AGENT' && STATE.ticketId) {
      n8nCall(CONFIG.ENDPOINTS.AGENT_REPLY, {
        ticket_id: STATE.ticketId,
        message: '⚠️ The customer has closed the chat widget.'
      }).catch(function () {});
    }
  }

  function resetChat() {
    stopPolling();
    stopAgentPolling();
    STATE.messages = []; STATE.jobId = null; STATE.playerId = null; STATE.phase = 'CHAT';
    STATE.busy = false; STATE.lastSendTs = 0;
    STATE.humanRequestCount = 0; STATE.ticketId = null;
    STATE.urgency = 'low'; STATE.unhappyCount = 0;
    STATE.sessionStartTime = Date.now();
    STATE.inactivityReminded = false;
    if (STATE.inactivityTimer) { clearTimeout(STATE.inactivityTimer); STATE.inactivityTimer = null; }
    clearSavedChat();
    // Restore bot header
    document.getElementById('bw-botname').textContent = CONFIG.BOT_NAME;
    document.getElementById('bw-statusdot').style.background = C.green;
    document.getElementById('bw-msgs').innerHTML =
      '<div id="bw-typing">' +
        '<div id="bw-tdots"><div class="bw-dot"></div><div class="bw-dot"></div><div class="bw-dot"></div></div>' +
        '<span id="bw-tlabel">' + t('typing') + '</span>' +
      '</div>';
    showPlayerIdForm(false); showUpload(false); setProgress(0);
    document.getElementById('bw-ufile').value = '';
    // Re-create quick deposit button and show
    document.getElementById('bw-qactions').innerHTML =
      '<button class="bw-qbtn" id="bw-qdep">' + t('quick_deposit') + '</button>';
    document.getElementById('bw-qdep').addEventListener('click', function () {
      showQuickActions(false);
      startDepositFlow();
    });
    showQuickActions(true);
    setInputDisabled(false); setProgress(0);
    document.getElementById('bw-idinput').value = '';
    document.getElementById('bw-input').value   = '';
    document.getElementById('bw-input').style.height = 'auto';
    setTimeout(function () { addMessage('bot', t('welcome')); }, 300);
  }

  // ============================================================
  // 15. INIT
  // ============================================================
  // ============================================================
  // CSAT RATING
  // ============================================================
  function showCSAT() {
    var msgs = document.getElementById('bw-msgs');
    var typing = document.getElementById('bw-typing');
    var div = document.createElement('div');
    div.className = 'bw-msg bot';
    div.innerHTML =
      '<div class="bw-mavatar">' + BOT_AVATAR_SVG + '</div>' +
      '<div class="bw-bubble">' +
        '<div>' + t('csat_ask') + '</div>' +
        '<div id="bw-csat" style="display:flex;gap:4px;margin-top:8px;cursor:pointer">' +
          '<span class="bw-star" data-r="1" style="font-size:22px;opacity:0.4">★</span>' +
          '<span class="bw-star" data-r="2" style="font-size:22px;opacity:0.4">★</span>' +
          '<span class="bw-star" data-r="3" style="font-size:22px;opacity:0.4">★</span>' +
          '<span class="bw-star" data-r="4" style="font-size:22px;opacity:0.4">★</span>' +
          '<span class="bw-star" data-r="5" style="font-size:22px;opacity:0.4">★</span>' +
        '</div>' +
      '</div>';
    msgs.insertBefore(div, typing);
    msgs.scrollTop = msgs.scrollHeight;

    var csatEl = document.getElementById('bw-csat');
    if (csatEl) {
      csatEl.addEventListener('click', function (e) {
        var star = e.target.closest('.bw-star');
        if (!star) return;
        var rating = parseInt(star.getAttribute('data-r'));
        // Highlight stars
        var stars = csatEl.querySelectorAll('.bw-star');
        stars.forEach(function (s) {
          s.style.opacity = parseInt(s.getAttribute('data-r')) <= rating ? '1' : '0.4';
          s.style.color = parseInt(s.getAttribute('data-r')) <= rating ? C.warning : C.textMuted;
        });
        // Send rating
        csatEl.style.pointerEvents = 'none';
        addMessage('bot', t('csat_thanks') + ' (' + rating + '/5)');
        // Track analytics
        trackEvent('csat_rating', { rating: rating, ticketId: STATE.ticketId });
        // Send to n8n if there's a ticket
        if (STATE.ticketId) {
          n8nCall(CONFIG.ENDPOINTS.AGENT_REPLY, {
            ticket_id: STATE.ticketId,
            message: '⭐ Customer rated experience: ' + rating + '/5'
          }).catch(function () {});
        }
      });
    }
  }

  // ============================================================
  // FILE SHARE IN LIVE AGENT MODE
  // ============================================================
  function sendFileToAgent(file) {
    if (STATE.phase !== 'LIVE_AGENT' || !STATE.ticketId) return;
    if (!file || file.size === 0) return;
    if (file.size > CONFIG.MAX_FILE_MB * 1024 * 1024) { addMessage('bot', t('err_file_size')); return; }
    if (CONFIG.ACCEPTED_TYPES.indexOf(file.type) === -1) { addMessage('bot', t('err_file_type')); return; }

    addMessage('user', '📎 ' + file.name);
    showTyping(true, STATE._agentName || t('live_agent'));

    // Upload via presigned URL then notify agent
    n8nCall(CONFIG.ENDPOINTS.PRESIGNED, {
      player_id: STATE.playerId || 'live_agent',
      file_name: file.name,
      file_type: file.type
    })
    .then(function (data) {
      return uploadToS3(data.presigned_url, file, function () {}).then(function () { return data.s3_url; });
    })
    .then(function (s3Url) {
      // Send file URL as comment on Zendesk ticket
      return n8nCall(CONFIG.ENDPOINTS.AGENT_REPLY, {
        ticket_id: STATE.ticketId,
        message: '📎 Customer shared a file: ' + file.name + '\nURL: ' + s3Url
      });
    })
    .then(function () {
      showTyping(false);
      addMessage('bot', t('file_sent'));
    })
    .catch(function () {
      showTyping(false);
      addMessage('bot', t('err_generic'));
    });
  }

  // ============================================================
  // INIT
  // ============================================================
  function init() {
    STATE.sessionId = generateUUID();
    STATE.sessionStartTime = Date.now(); // T-19: track session start
    injectCSS();
    buildHTML();
    bindEvents();

    setTimeout(function () { addMessage('bot', t('welcome')); }, 500);

    // Proactive message after 30s if user hasn't interacted
    setTimeout(function () {
      if (STATE.messages.length <= 1 && !STATE.isOpen) {
        notifyNewMessage();
      }
    }, PROACTIVE_DELAY);

    // Stop polling on page unload
    window.addEventListener('beforeunload', function () {
      stopPolling();
      stopAgentPolling();
    });

    // Add file input for live agent mode
    var fileBtn = document.createElement('input');
    fileBtn.type = 'file';
    fileBtn.id = 'bw-agent-file';
    fileBtn.style.display = 'none';
    fileBtn.accept = '.jpg,.jpeg,.png,.webp,.pdf';
    fileBtn.addEventListener('change', function (e) {
      if (e.target.files[0]) { sendFileToAgent(e.target.files[0]); }
      e.target.value = '';
    });
    document.getElementById('__beton_widget__').appendChild(fileBtn);

    console.log('[BetonWin Support] v3.0.0 ready — lang:', lang);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
