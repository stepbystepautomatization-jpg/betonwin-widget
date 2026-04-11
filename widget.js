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
    POLL_MAX:         80,
    BOT_NAME:         'BetonWin AI',
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
    gold:          '#ffb64f',
    goldDark:      '#e5a040',
    green:         '#45cd98',
    greenDark:     '#33b98d',
    text:          '#e8f0f2',
    textMuted:     '#7a9aa8',
    border:        'rgba(69,205,152,0.06)',
    headerBorder:  'rgba(69,205,152,0.08)',
    userBubble:    '#0a3d2a',
    botBubble:     '#042e38',
    input:         '#042a33',
    inputBorder:   'rgba(69,205,152,0.1)',
    scrollbar:     'rgba(69,205,152,0.08)',
    danger:        '#f54943',
    warning:       '#ffc572',
    shadow:        '0 0 0 1px rgba(69,205,152,0.06),0 24px 80px rgba(0,0,0,0.7),0 0 60px rgba(69,205,152,0.04)',
    triggerShadow: '0 0 0 0 rgba(69,205,152,0.35),0 8px 32px rgba(0,0,0,0.5)'
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
      file_sent:        'File sent to agent.',
      exit_new_chat:    'New chat',
      exit_feedback:    'Rate us',
      exit_close:       'Exit',
      exit_title:       'See you soon 👋',
      exit_thanks:      'Thank you! 💚',
      splash_line1:     'BetonWin AI Support',
      splash_line2:     '24/7 Always available'
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
      file_sent:        'Archivo enviado al agente.',
      exit_new_chat:    'Nueva chat',
      exit_feedback:    'Calificar',
      exit_close:       'Salir',
      exit_title:       '¡Hasta pronto! 👋',
      exit_thanks:      '¡Gracias! 💚',
      splash_line1:     'BetonWin AI Support',
      splash_line2:     '24/7 Siempre disponible'
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
      file_sent:        "File inviato all'agente.",
      exit_new_chat:    'Nuova chat',
      exit_feedback:    'Valutaci',
      exit_close:       'Esci',
      exit_title:       'A presto! 👋',
      exit_thanks:      'Grazie! 💚',
      splash_line1:     'BetonWin AI Support',
      splash_line2:     '24/7 Sempre disponibile'
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
      file_sent:        'Arquivo enviado ao agente.',
      exit_new_chat:    'Nova chat',
      exit_feedback:    'Avaliar',
      exit_close:       'Sair',
      exit_title:       'Até logo! 👋',
      exit_thanks:      'Obrigado! 💚',
      splash_line1:     'BetonWin AI Support',
      splash_line2:     '24/7 Sempre disponível'
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

  // Stubs (persistence/analytics disabled)
  function saveChat() {}
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
  function notifyNewMessage() {
    if (!STATE.isOpen) {
      playNotifSound();
    }
  }

  // ============================================================
  // ESCALATION — Legal = immediate, Human = AI-detected after 3x
  // ============================================================
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

  // Sensitive: gambling addiction, fraud accusations → immediate escalation
  var SENSITIVE_KEYWORDS = [
    // Gambling addiction (all languages)
    'problema con el juego','adicción','adiccion','ludopatía','ludopatia','autoexclusión','autoexclusion',
    'gambling problem','gambling addiction','self-exclusion','addicted',
    'problema col gioco','dipendenza','autoesclusione','ludopatia',
    'problema com jogo','vício','vicio','autoexclusão',
    // Fraud/scam accusations
    'estafa','fraude','manipulado','amañado','scam','rigged','fraud',
    'truffa','truccato','manipolato','fraudolento',
    'golpe','fraude','manipulado','fraudulento'
  ];

  function detectLegalThreat(text) {
    var lower = text.toLowerCase();
    for (var i = 0; i < LEGAL_KEYWORDS.length; i++) {
      if (lower.indexOf(LEGAL_KEYWORDS[i]) !== -1) { return true; }
    }
    return false;
  }

  function detectSensitive(text) {
    var lower = text.toLowerCase();
    for (var i = 0; i < SENSITIVE_KEYWORDS.length; i++) {
      if (lower.indexOf(SENSITIVE_KEYWORDS[i]) !== -1) { return true; }
    }
    return false;
  }

  // T-02: Fraud/scam accusations → CRITICAL (immediate escalation)
  var FRAUD_KEYWORDS = [
    'fraude','estafa','me estafaron','esto es un fraude','están estafando','empresa fraudulenta','sitio falso','es falso',
    'fraud','scam','scammed','i\'ve been scammed','this is fraud','you\'re scamming','fraudulent company','fake site',
    'frode','truffa','mi hanno truffato','questa è una frode','state truffando','azienda fraudolenta','sito falso',
    'golpe','fui enganado','isso é fraude','estão enganando','empresa fraudulenta','site falso'
  ];

  function detectFraudAccusation(text) {
    var lower = text.toLowerCase();
    for (var i = 0; i < FRAUD_KEYWORDS.length; i++) {
      if (lower.indexOf(FRAUD_KEYWORDS[i]) !== -1) { return 'fraud_accusation'; }
    }
    return false;
  }

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

  function detectFrustration(text) {
    var lower = text.toLowerCase();
    var signals = 0;
    for (var i = 0; i < FRUSTRATION_KEYWORDS.length; i++) {
      if (lower.indexOf(FRUSTRATION_KEYWORDS[i]) !== -1) { signals++; }
    }
    // Check CAPS (more than 50% uppercase and length > 10)
    if (text.length > 10 && text.replace(/[^A-Z]/g, '').length > text.length * 0.5) { signals += 2; }
    // Check excessive punctuation (!!! or ???)
    if ((text.match(/[!?]{3,}/g) || []).length > 0) { signals++; }
    return signals >= 1;
  }

  // T-18: Client unhappy with bot answer
  var UNHAPPY_KEYWORDS = [
    'esto no es correcto','no es correcto','estás equivocado','respuesta incorrecta','eso no es verdad','no me sirve',
    'this is wrong','you\'re wrong','you are wrong','that\'s incorrect','that is incorrect','not correct','doesn\'t help','does not help','useless answer',
    'non è corretto','è sbagliato','risposta sbagliata','non è vero','non mi serve',
    'isso não está certo','está errado','resposta errada','não está correto','não me ajuda'
  ];

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

  // === HUMAN REQUEST DETECTION (dual: user message + AI response) ===

  // Direct user keywords — all languages, explicit requests for human
  var HUMAN_USER_KEYWORDS = [
    // English
    'human','agent','operator','real person','speak to someone','talk to someone',
    'live chat','live agent','real agent','customer service','support agent',
    'i want a person','need a person','connect me','transfer me',
    // Spanish
    'agente','operador','persona real','hablar con alguien','quiero un humano',
    'quiero una persona','agente real','soporte humano','atencion humana',
    'conectame','transferime','quiero hablar con','pasame con',
    // Italian
    'operatore','persona reale','parlare con qualcuno','voglio un umano',
    'agente reale','supporto umano','assistenza umana','voglio parlare con',
    'passami a','collegami con',
    // Portuguese
    'atendente','pessoa real','falar com alguém','quero um humano',
    'agente real','suporte humano','quero falar com','me transfira'
  ];

  // AI response signals (bot acknowledges human request)
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

  // Check USER message for human request keywords
  function userWantsHuman(userMessage) {
    var lower = userMessage.toLowerCase();
    for (var i = 0; i < HUMAN_USER_KEYWORDS.length; i++) {
      if (lower.indexOf(HUMAN_USER_KEYWORDS[i]) !== -1) { return true; }
    }
    return false;
  }

  // Check AI response for acknowledgment signals
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
    } catch (e) { /* silent */ }
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
      '#__beton_widget__{position:fixed;bottom:24px;right:24px;z-index:2147483647;font-family:"Inter",-apple-system,BlinkMacSystemFont,sans-serif;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;line-height:normal;text-align:left;color:#e8f0f2;font-size:14px;font-weight:400;-webkit-tap-highlight-color:transparent}',
      '#__beton_widget__ *{box-sizing:border-box;margin:0;padding:0;border:none;text-decoration:none;list-style:none;-webkit-user-select:none;user-select:none}',
      '#__beton_widget__ textarea,#__beton_widget__ input{-webkit-user-select:text;user-select:text}',

      /* FAB — logo + label */
      '#bw-trigger{height:44px;background:'+C.bg+';border:1px solid rgba(69,205,152,0.15);border-radius:22px;cursor:pointer;display:flex;align-items:center;gap:8px;padding:0 16px 0 4px;box-shadow:0 4px 24px rgba(0,0,0,0.4),0 0 0 1px rgba(69,205,152,0.08);transition:all .35s cubic-bezier(.22,1,.36,1);position:relative;outline:none;animation:bw-float 3s ease-in-out infinite}',
      '#bw-trigger::after{content:"";position:absolute;inset:-5px;border-radius:26px;border:1px solid rgba(69,205,152,0.1);animation:bw-ring 3s ease-in-out infinite;pointer-events:none}',
      '#bw-trigger:hover{transform:translateY(-2px);box-shadow:0 8px 32px rgba(0,0,0,0.5),0 0 20px rgba(69,205,152,0.1);border-color:rgba(69,205,152,0.25);animation:none}',
      '#bw-trigger:active{transform:scale(.96);animation:none}',
      '#bw-trigger.bw-open{transform:scale(0) rotate(90deg);opacity:0;pointer-events:none;animation:none}',
      /* FAB logo */
      '#bw-fab-logo{width:36px;height:36px;border-radius:50%;overflow:hidden;flex-shrink:0}',
      '#bw-fab-logo img{width:100%;height:100%;object-fit:cover;border-radius:50%}',
      /* FAB label */
      '#bw-fab-label{color:rgba(232,240,242,0.85);font-size:12px;font-weight:600;letter-spacing:.3px;font-family:"Inter",-apple-system,sans-serif;white-space:nowrap}',
      /* FAB busy state */
      '#bw-trigger.bw-busy{animation:bw-busy-pulse 1.5s ease-in-out infinite}',

      /* Window — deep teal glass with green glow */
      '#bw-window{position:absolute;bottom:74px;right:0;width:400px;height:620px;overscroll-behavior:contain;touch-action:pan-y;background:rgba(3,36,45,0.95);backdrop-filter:blur(28px) saturate(1.4);-webkit-backdrop-filter:blur(28px) saturate(1.4);border-radius:22px;border:1px solid rgba(69,205,152,0.08);border-top:1px solid rgba(69,205,152,0.15);box-shadow:0 0 0 1px rgba(69,205,152,0.05),0 24px 80px rgba(0,0,0,0.7),0 0 120px -20px rgba(69,205,152,0.06);display:flex;flex-direction:column;overflow:hidden;transform-origin:calc(100% - 28px) calc(100% + 28px);transition:transform .45s cubic-bezier(.34,1.56,.64,1),opacity .3s ease;transform:scale(0);opacity:0;pointer-events:none}',
      '#bw-window.bw-open{transform:scale(1);opacity:1;pointer-events:all}',

      /* Logo watermark background — premium, fades on conversation */
      '#bw-logo-bg{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;pointer-events:none;z-index:0;opacity:0.04;transition:opacity 1.2s ease}',
      '#bw-logo-bg img{width:140px;height:140px;object-fit:contain;filter:grayscale(0.5) brightness(1.2)}',
      '#bw-logo-bg.hidden{opacity:0}',

      /* Header — modern glass with subtle gradient */
      '#bw-header{background:linear-gradient(180deg,rgba(4,50,62,0.95) 0%,rgba(3,36,45,0.98) 100%);border-bottom:none;padding:14px 16px;display:flex;align-items:center;gap:12px;flex-shrink:0;position:relative;z-index:1;box-shadow:0 1px 0 0 rgba(69,205,152,0.08),0 4px 20px -4px rgba(0,0,0,0.4)}',
      '#bw-header::after{content:"";position:absolute;bottom:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(69,205,152,0.2),transparent)}',

      /* Avatar — circular logo 160px, pulse glow */
      '#bw-avatar{width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;position:relative;overflow:hidden;cursor:pointer;transition:all .3s ease;box-shadow:0 0 0 2px rgba(69,205,152,0.15),0 0 12px rgba(69,205,152,0.1)}',
      '#bw-avatar:hover{box-shadow:0 0 0 2px rgba(69,205,152,0.3),0 0 20px rgba(69,205,152,0.2);animation:bw-avatar-buzz .2s ease-in-out}',
      '#bw-avatar img{width:100%;height:100%;object-fit:cover;display:block;border-radius:50%}',
      /* Green ring animation around avatar */
      '#bw-avatar::after{content:"";position:absolute;inset:-3px;border-radius:50%;border:1.5px solid rgba(69,205,152,0.2);animation:bw-avatar-ring 3s ease-in-out infinite;pointer-events:none}',
      '#bw-hinfo{flex:1;min-width:0}',
      '#bw-botname{color:'+C.text+';font-weight:700;font-size:13.5px;line-height:1.2;letter-spacing:-0.2px}',
      '#bw-status{display:flex;align-items:center;gap:5px;margin-top:3px}',
      '#bw-statusdot{width:6px;height:6px;background:'+C.green+';border-radius:50%;animation:bw-pulse 2.5s ease-in-out infinite;flex-shrink:0;box-shadow:0 0 6px rgba(69,205,152,0.5)}',
      '#bw-status span:last-child{color:rgba(69,205,152,0.6);font-size:10.5px;font-weight:500;letter-spacing:.5px}',
      '#bw-hbtns{display:flex;gap:2px}',
      '.bw-hbtn{width:30px;height:30px;background:transparent;border:none;border-radius:8px;cursor:pointer;display:flex;align-items:center;justify-content:center;color:'+C.textMuted+';transition:all .2s;outline:none}',
      '.bw-hbtn:hover{background:rgba(69,205,152,0.06);color:'+C.green+'}',
      '.bw-hbtn svg{width:13px;height:13px;fill:currentColor}',

      /* Messages area — spacious, breathable */
      '#bw-msgs{flex:1;overflow-y:auto;padding:18px 18px;display:flex;flex-direction:column;gap:4px;scroll-behavior:smooth;overscroll-behavior:contain;-webkit-overflow-scrolling:touch;position:relative;z-index:1}',
      '#bw-msgs::-webkit-scrollbar{width:3px}',
      '#bw-msgs::-webkit-scrollbar-track{background:transparent}',
      '#bw-msgs::-webkit-scrollbar-thumb{background:rgba(69,205,152,0.1);border-radius:3px}',

      /* Message rows — no bubble for bot, minimal pill for user */
      '.bw-msg{display:flex;gap:10px;animation:bw-msg-in .55s cubic-bezier(.16,1,.3,1) both;min-width:0;opacity:0}',
      '.bw-msg.user{margin-left:auto;flex-direction:row-reverse;max-width:82%}',
      '.bw-msg.bot{max-width:100%}',
      /* Stagger: user messages slide from right */
      '.bw-msg.user{animation-name:bw-msg-user}',
      '.bw-mavatar{width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;align-self:flex-start;overflow:hidden;margin-top:2px}',
      '.bw-mavatar img{width:100%;height:100%;object-fit:cover;border-radius:50%}',
      '.bw-mavatar svg{width:100%;height:auto}',

      /* Text — clear, modern, generous spacing */
      '.bw-bubble{font-size:14px;line-height:1.75;word-break:break-word;overflow-wrap:anywhere;white-space:pre-wrap;letter-spacing:0.01em;font-weight:400;min-width:0;max-width:100%;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;background:transparent!important;border:none!important;box-shadow:none!important}',
      /* Bot — pure text, zero decoration */
      '.bw-msg.bot .bw-bubble{color:rgba(232,240,242,0.93);padding:2px 0;border-radius:0!important}',
      /* User — green solid pill, stands out */
      '.bw-msg.user .bw-bubble{background:'+C.green+'!important;border:none!important;color:#042a33;font-weight:500;padding:10px 18px;border-radius:20px!important;border-bottom-right-radius:6px!important;box-shadow:0 2px 12px rgba(69,205,152,0.25)!important}',
      '.bw-bubble a{word-break:break-all;color:'+C.green+';text-decoration:none;border-bottom:1px solid rgba(69,205,152,0.25);transition:all .2s}',
      '.bw-bubble a:hover{border-bottom-color:'+C.green+';color:#fff}',
      '.bw-msg.user .bw-bubble a{color:#042a33;border-bottom-color:rgba(4,42,51,0.3)}',
      '.bw-bubble b,.bw-bubble strong{font-weight:600;color:#fff}',
      '.bw-msg.bot .bw-bubble strong{color:'+C.green+';font-weight:600}',
      '.bw-msg.user .bw-bubble b,.bw-msg.user .bw-bubble strong{color:#021a20;font-weight:700}',
      '.bw-bubble em,.bw-bubble i{font-style:italic;opacity:.8}',
      '.bw-bubble hr{border:none;height:1px;background:linear-gradient(90deg,rgba(69,205,152,0.15),transparent 80%);margin:12px 0}',
      /* Separator line between bot messages for visual rhythm */
      '.bw-msg.bot+.bw-msg.bot{padding-top:2px}',
      '.bw-msg.bot+.bw-msg.user,.bw-msg.user+.bw-msg.bot{margin-top:8px}',

      /* Media — images & videos inline */
      '.bw-media{margin:6px 0;border-radius:12px;overflow:hidden;max-width:100%}',
      '.bw-media img{display:block;max-width:100%;height:auto;border-radius:12px;cursor:pointer;transition:opacity .2s}',
      '.bw-media img:hover{opacity:.9}',
      '.bw-media video{display:block;max-width:100%;height:auto;border-radius:12px;outline:none;background:#000}',
      '.bw-msg.user .bw-media img,.bw-msg.user .bw-media video{max-width:200px}',

      /* Agent messages — warm gold accent, glass surface */
      '.bw-msg.agent{max-width:100%}',
      '.bw-msg.agent .bw-mavatar{display:flex}',
      '.bw-msg.agent .bw-bubble{background:none;border:none;border-left:2px solid '+C.warning+';color:rgba(232,240,242,0.92);padding:4px 2px 4px 14px;border-radius:0}',
      '.bw-msg.agent .bw-bubble strong{color:'+C.warning+'}',
      '.bw-msg.agent .bw-mavatar{background:rgba(69,205,152,0.06)}',
      '.bw-agent-name{font-size:10px;color:'+C.warning+';font-weight:600;margin-bottom:4px;letter-spacing:0.4px;text-transform:uppercase}',

      /* Typing indicator — clean, matches borderless style */
      '#bw-typing{display:none;align-items:center;gap:12px;animation:bw-up .35s ease;padding:4px 0}',
      '#bw-typing.show{display:flex}',
      '#bw-tdots{background:none;border:none;padding:4px 0;display:flex;gap:4px;align-items:center}',
      '.bw-dot{width:6px;height:6px;background:'+C.green+';border-radius:50%;animation:bw-dot-fade 1.4s ease-in-out infinite;opacity:.25}',
      '.bw-dot:nth-child(2){animation-delay:.2s}',
      '.bw-dot:nth-child(3){animation-delay:.4s}',
      '#bw-tlabel{color:rgba(69,205,152,0.5);font-size:11px;font-weight:500;letter-spacing:.3px}',
      '#bw-tlabel::after{content:"";display:inline-block;animation:bw-ellipsis 1.5s steps(4,end) infinite;width:0;overflow:hidden;vertical-align:bottom}',

      /* Quick actions */
      '#bw-qactions{padding:4px 16px 12px;display:flex;flex-wrap:wrap;gap:8px;flex-shrink:0;position:relative;z-index:1}',
      '.bw-qbtn{background:rgba(69,205,152,0.05);border:1px solid rgba(69,205,152,0.12);color:'+C.green+';border-radius:100px;padding:8px 16px;font-size:12.5px;font-weight:500;cursor:pointer;transition:all .25s cubic-bezier(.22,1,.36,1);font-family:inherit;outline:none;white-space:nowrap}',
      '.bw-qbtn:hover{background:rgba(69,205,152,0.1);border-color:rgba(69,205,152,0.25);transform:translateY(-1px);box-shadow:0 4px 16px rgba(69,205,152,0.1)}',
      '.bw-qbtn:active{transform:translateY(0) scale(.97)}',

      /* ID form */
      '#bw-idform{padding:4px 16px 12px;display:none;gap:8px;flex-shrink:0;align-items:center;position:relative;z-index:1}',
      '#bw-idform.show{display:flex}',
      '#bw-idinput{flex:1;background:'+C.input+';border:1px solid '+C.inputBorder+';color:'+C.text+';border-radius:12px;padding:10px 13px;font-size:13px;outline:none;transition:all .2s;font-family:inherit}',
      '#bw-idinput:focus{border-color:rgba(69,205,152,0.3);box-shadow:0 0 0 3px rgba(69,205,152,0.06)}',
      '#bw-idinput::placeholder{color:'+C.textMuted+'}',
      '#bw-idconfirm{background:linear-gradient(135deg,'+C.green+','+C.greenDark+');border:none;color:#fff;font-weight:700;border-radius:12px;padding:10px 18px;font-size:13px;cursor:pointer;transition:all .2s;white-space:nowrap;font-family:inherit;outline:none}',
      '#bw-idconfirm:hover{opacity:.9;transform:translateY(-1px);box-shadow:0 4px 12px rgba(69,205,152,0.25)}',

      /* Upload area */
      '#bw-upload{margin:4px 16px 12px;border:1.5px dashed rgba(69,205,152,0.12);border-radius:14px;padding:22px 16px;text-align:center;cursor:pointer;transition:all .25s;display:none;flex-shrink:0;position:relative;z-index:1}',
      '#bw-upload.show{display:block}',
      '#bw-upload.drag{border-color:'+C.green+';background:rgba(69,205,152,0.08);border-width:2px;box-shadow:inset 0 0 20px rgba(69,205,152,0.06)}',
      '#bw-upload.busy{opacity:.55;pointer-events:none}',
      '#bw-uico{font-size:28px;margin-bottom:6px}',
      '#bw-utxt{color:rgba(232,240,242,0.5);font-size:13px;font-weight:500}',
      '#bw-uhint{color:'+C.textMuted+';font-size:11px;margin-top:3px}',
      '#bw-ufile{display:none}',
      '#bw-uprog{margin-top:10px;background:rgba(69,205,152,0.06);border-radius:4px;height:3px;overflow:hidden;display:none}',
      '#bw-uprog.show{display:block}',
      '#bw-uprogbar{height:100%;background:linear-gradient(90deg,'+C.green+','+C.greenDark+');border-radius:3px;width:0%;transition:width .3s}',

      /* Chat input — modern unified bar */
      '#bw-inputarea{padding:10px 14px calc(14px + env(safe-area-inset-bottom,0px));border-top:1px solid rgba(255,255,255,0.03);display:flex;align-items:flex-end;flex-shrink:0;position:relative;z-index:1}',
      /* Input wrapper — everything inside one bar */
      '#bw-input-wrap{flex:1;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.06);border-radius:22px;display:flex;flex-direction:column;transition:border-color .2s}',
      '#bw-input-wrap:focus-within{border-color:rgba(69,205,152,0.2)}',
      '#bw-input{flex:1;background:transparent;border:none;color:'+C.text+';padding:10px 14px 2px;font-size:13px;resize:none;outline:none;min-height:34px;max-height:100px;line-height:1.5;font-family:inherit}',
      '#bw-input::placeholder{color:rgba(232,240,242,0.18)}',
      /* Bottom row — toolbar left + send right */
      '#bw-input-toolbar{display:flex;align-items:center;padding:2px 4px 5px 8px}',
      '.bw-toolbar-btn{width:28px;height:28px;background:transparent;border:none;border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .15s;outline:none;color:'+C.textMuted+';font-size:15px}',
      '.bw-toolbar-btn:hover{color:'+C.green+';background:rgba(69,205,152,0.06)}',
      '.bw-toolbar-btn svg{width:15px;height:15px;fill:currentColor}',
      /* Send button — inside the bar, right side */
      '#bw-send{width:34px;height:34px;background:'+C.green+';border:none;border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .15s cubic-bezier(.22,1,.36,1);flex-shrink:0;outline:none;margin-left:auto}',
      '#bw-send:hover{background:'+C.greenDark+';transform:scale(1.08)}',
      '#bw-send:active{transform:scale(.88)}',
      '#bw-send:disabled{opacity:.1;cursor:default;transform:none}',
      '#bw-send svg{width:16px;height:16px;fill:#fff}',
      /* Language popup */
      '#bw-lang-popup{display:none;position:absolute;bottom:70px;right:14px;background:'+C.bg+';border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:6px;z-index:10;box-shadow:0 -4px 20px rgba(0,0,0,0.4)}',
      '#bw-lang-popup.show{display:flex;flex-direction:column;gap:2px}',
      '.bw-lang-opt{display:flex;align-items:center;gap:8px;padding:8px 14px;border:none;background:transparent;border-radius:8px;cursor:pointer;color:'+C.text+';font-size:12px;font-weight:500;font-family:inherit;outline:none;transition:all .15s;white-space:nowrap}',
      '.bw-lang-opt:hover{background:rgba(69,205,152,0.06)}',
      '.bw-lang-opt.active{color:'+C.green+'}',
      '.bw-lang-opt span:first-child{font-size:16px}',
      '#bw-emoji-panel{display:none;position:absolute;bottom:70px;left:16px;right:16px;background:'+C.bg+';border:1px solid rgba(69,205,152,0.12);border-radius:14px;padding:10px;max-height:180px;overflow-y:auto;z-index:10;box-shadow:0 -8px 32px rgba(0,0,0,0.5)}',
      '#bw-emoji-panel.show{display:grid;grid-template-columns:repeat(8,1fr);gap:4px}',
      '.bw-emo{width:100%;aspect-ratio:1;border:none;background:transparent;border-radius:8px;cursor:pointer;font-size:20px;display:flex;align-items:center;justify-content:center;transition:all .15s}',
      '.bw-emo:hover{background:rgba(69,205,152,0.08);transform:scale(1.15)}',

      /* Fullscreen mode */
      '#bw-window.bw-fullscreen{position:fixed;inset:0;width:100%;height:100%;max-height:100%;border-radius:0;bottom:0;right:0;z-index:2147483647}',

      /* Footer */
      '#bw-footer{text-align:center;padding:8px;color:rgba(69,205,152,0.1);font-size:10px;border-top:1px solid rgba(69,205,152,0.04);flex-shrink:0;letter-spacing:.3px;font-weight:500;position:relative;z-index:1}',

      /* Exit overlay */
      '#bw-exit-overlay{display:none;position:absolute;inset:0;background:rgba(3,36,45,0.97);backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);z-index:20;align-items:center;justify-content:center;border-radius:22px}',
      '#bw-exit-overlay.show{display:flex;animation:bw-exit-in .3s ease-out}',
      '@keyframes bw-exit-in{from{opacity:0;transform:scale(.98)}to{opacity:1;transform:scale(1)}}',
      '#bw-exit-panel{padding:32px 24px;text-align:center;width:100%}',
      '#bw-exit-title{font-size:20px;font-weight:600;color:rgba(232,240,242,0.9);margin-bottom:28px;letter-spacing:-0.3px}',
      /* 3 actions in a row — icon circles */
      '#bw-exit-options{display:flex;justify-content:center;gap:28px}',
      /* Each action — icon on top, label below */
      '.bw-exit-card{display:flex;flex-direction:column;align-items:center;gap:10px;cursor:pointer;outline:none;font-family:inherit;background:none;border:none;transition:all .2s ease}',
      '.bw-exit-card:hover{transform:translateY(-3px)}',
      '.bw-exit-card:active{transform:scale(.94)}',
      /* Icon circle */
      '.bw-exit-circle{width:56px;height:56px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:22px;transition:all .25s;position:relative;overflow:hidden}',
      '.bw-exit-label{font-size:11px;font-weight:500;letter-spacing:.3px;white-space:nowrap;transition:color .2s}',
      /* New chat — green */
      '#bw-exit-newchat .bw-exit-circle{background:rgba(69,205,152,0.1);border:1.5px solid rgba(69,205,152,0.2);box-shadow:0 0 16px rgba(69,205,152,0.08)}',
      '#bw-exit-newchat .bw-exit-circle::after{content:"";position:absolute;inset:0;border-radius:50%;border:1.5px solid transparent;border-top-color:'+C.green+';animation:bw-orbit 2.5s linear infinite}',
      '#bw-exit-newchat .bw-exit-label{color:'+C.green+'}',
      '#bw-exit-newchat:hover .bw-exit-circle{background:rgba(69,205,152,0.15);box-shadow:0 0 24px rgba(69,205,152,0.15)}',
      '@keyframes bw-orbit{from{transform:rotate(0)}to{transform:rotate(360deg)}}',
      /* Rate — gold */
      '#bw-exit-feedback .bw-exit-circle{background:rgba(255,197,114,0.08);border:1.5px solid rgba(255,197,114,0.15);box-shadow:0 0 16px rgba(255,197,114,0.06)}',
      '#bw-exit-feedback .bw-exit-label{color:rgba(255,197,114,0.7)}',
      '#bw-exit-feedback:hover .bw-exit-circle{background:rgba(255,197,114,0.13);box-shadow:0 0 24px rgba(255,197,114,0.12)}',
      '#bw-exit-feedback:hover .bw-exit-label{color:rgba(255,197,114,0.9)}',
      /* Exit — muted */
      '#bw-exit-close{display:flex;flex-direction:column;align-items:center;gap:10px;cursor:pointer;outline:none;font-family:inherit;background:none;border:none;transition:all .2s}',
      '#bw-exit-close:hover{transform:translateY(-3px)}',
      '#bw-exit-close:active{transform:scale(.94)}',
      '#bw-exit-close .bw-exit-circle{width:56px;height:56px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:22px;background:rgba(255,255,255,0.03);border:1.5px solid rgba(255,255,255,0.06);transition:all .25s}',
      '#bw-exit-close:hover .bw-exit-circle{background:rgba(255,255,255,0.06)}',
      '#bw-exit-close .bw-exit-label{font-size:11px;font-weight:500;color:rgba(232,240,242,0.3);letter-spacing:.3px;transition:color .2s}',
      '#bw-exit-close:hover .bw-exit-label{color:rgba(232,240,242,0.5)}',
      /* CSAT stars */
      '#bw-exit-csat{display:none;animation:bw-up .3s cubic-bezier(.34,1.56,.64,1);padding:12px 0 0}',
      '#bw-exit-csat-label{color:rgba(232,240,242,0.5);font-size:11px;font-weight:500;margin-bottom:14px;letter-spacing:.5px;text-transform:uppercase}',
      '#bw-exit-stars{display:flex;justify-content:center;gap:6px}',
      '.bw-exit-star{font-size:34px;color:rgba(255,182,79,0.15);cursor:pointer;transition:all .2s cubic-bezier(.34,1.56,.64,1);padding:2px;border:none;background:none;outline:none}',
      '.bw-exit-star:hover{transform:scale(1.25)}',
      '.bw-exit-star.active{color:'+C.gold+';filter:drop-shadow(0 0 8px rgba(255,182,79,0.4))}',

      /* Splash — clean logo focus */
      '#bw-splash{position:absolute;inset:0;z-index:15;display:flex;flex-direction:column;align-items:center;justify-content:center;background:#03242D;border-radius:22px;pointer-events:none;overflow:hidden}',
      /* Logo — clean, no dark border visible */
      '#bw-splash-logo{width:140px;height:140px;position:relative;z-index:3;border-radius:50%;animation:bw-logo-in .7s cubic-bezier(.22,1,.36,1) .1s both}',
      '#bw-splash-logo img{width:100%;height:100%;object-fit:cover;display:block;border-radius:50%}',
      /* Green glow pulse behind logo */
      '#bw-splash-logo::before{content:"";position:absolute;inset:-8px;border-radius:50%;background:radial-gradient(circle,rgba(69,205,152,0.15) 40%,transparent 70%);z-index:-1;opacity:0;animation:bw-glow-pulse 1.5s ease-in-out .6s infinite}',
      /* Typewriter text */
      '#bw-splash-text{margin-top:28px;text-align:center;min-height:40px;z-index:3;position:relative}',
      '#bw-splash-line1{color:rgba(232,240,242,0.85);font-size:14px;font-weight:600;letter-spacing:1px;font-family:"Inter",-apple-system,sans-serif;min-height:20px}',
      '#bw-splash-line2{color:rgba(69,205,152,0.5);font-size:10.5px;font-weight:500;letter-spacing:3px;text-transform:uppercase;font-family:"Inter",-apple-system,sans-serif;margin-top:6px;min-height:14px}',
      '#bw-splash-cursor{display:inline-block;width:1.5px;height:12px;background:'+C.green+';margin-left:2px;animation:bw-cursor-blink .5s step-end infinite;vertical-align:text-bottom}',
      /* Exit */
      '#bw-splash.bw-splash-out{animation:bw-splash-exit .5s ease-out forwards;pointer-events:none}',
      /* Keyframes */
      '@keyframes bw-logo-in{0%{opacity:0;transform:scale(0) rotate(-20deg)}50%{opacity:1;transform:scale(1.1) rotate(5deg)}70%{transform:scale(.95) rotate(-2deg)}85%{transform:scale(1.02) rotate(.5deg)}100%{transform:scale(1) rotate(0)}}',
      '@keyframes bw-glow-pulse{0%,100%{opacity:.4;transform:scale(1)}50%{opacity:1;transform:scale(1.15)}}',
      '@keyframes bw-cursor-blink{0%,100%{opacity:1}50%{opacity:0}}',
      '@keyframes bw-splash-exit{to{opacity:0;transform:scale(1.05)}}',

      /* Animations */
      '@keyframes bw-up{from{opacity:0;transform:translateY(8px) scale(.98)}to{opacity:1;transform:translateY(0) scale(1)}}',
      '@keyframes bw-msg-in{0%{opacity:0;transform:translateY(20px)}60%{opacity:1;transform:translateY(-2px)}100%{opacity:1;transform:translateY(0)}}',
      '@keyframes bw-msg-user{0%{opacity:0;transform:translateX(20px)}60%{opacity:1;transform:translateX(-2px)}100%{opacity:1;transform:translateX(0)}}',
      '@keyframes bw-pulse{0%,100%{opacity:1}50%{opacity:.3}}',
      '@keyframes bw-wave{0%,100%{transform:scaleY(.4);opacity:.3}50%{transform:scaleY(1);opacity:1}}',
      '@keyframes bw-dot-fade{0%,100%{opacity:.2;transform:scale(.8)}50%{opacity:1;transform:scale(1.1)}}',
      '@keyframes bw-scan{0%{opacity:.15;transform:scaleX(.3)}50%{opacity:.8;transform:scaleX(1)}100%{opacity:.15;transform:scaleX(.3)}}',
      '@keyframes bw-ellipsis{0%{content:"";width:0}25%{content:".";width:5px}50%{content:"..";width:10px}75%{content:"...";width:15px}}',
      '@keyframes bw-ring{0%,100%{transform:scale(1);opacity:.4}50%{transform:scale(1.15);opacity:0}}',
      '@keyframes bw-float{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}',
      '@keyframes bw-busy-pulse{0%,100%{box-shadow:0 0 0 0 rgba(69,205,152,0.4),0 8px 32px rgba(0,0,0,0.5)}50%{box-shadow:0 0 0 14px rgba(69,205,152,0),0 8px 32px rgba(0,0,0,0.5)}}',
      '@keyframes bw-fab-wave{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}',
      '@keyframes bw-badge-in{from{transform:scale(0)}to{transform:scale(1)}}',
      '@keyframes bw-avatar-buzz{0%{transform:translateX(0)}15%{transform:translateX(-1.5px) rotate(-.5deg)}30%{transform:translateX(1.5px) rotate(.5deg)}45%{transform:translateX(-1px) rotate(-.3deg)}60%{transform:translateX(1px) rotate(.3deg)}75%{transform:translateX(-.5px)}100%{transform:translateX(0)}}',
      '@keyframes bw-avatar-ring{0%,100%{opacity:.4;transform:scale(1)}50%{opacity:.8;transform:scale(1.08)}}',

      /* ═══ MOBILE — WhatsApp-style: fixed fullscreen, keyboard-aware ═══ */
      '@media(max-width:440px){'+

        /* FAB — logo only, above site nav bar (~60px) */
        '#__beton_widget__{bottom:80px;right:14px;left:auto}'+
        '#bw-trigger{width:48px;height:48px;padding:0;border-radius:50%;justify-content:center}'+
        '#bw-fab-logo{width:42px;height:42px}'+
        '#bw-fab-label{display:none}'+

        /* ── Window: bottom-anchored, 75% height, rounded top ── */
        '#bw-window{position:fixed;left:0;right:0;bottom:0;top:auto;width:auto;height:75vh;max-height:75vh;border-radius:18px 18px 0 0;border:none;border-top:1px solid rgba(69,205,152,0.1);transform-origin:bottom center;transition:transform .35s cubic-bezier(.32,1,.22,1),opacity .2s ease}'+

        /* ── Header ── */
        '#bw-header{padding:12px 14px 10px;gap:10px}'+
        '#bw-avatar{width:32px;height:32px}'+
        '#bw-avatar::after{inset:-2px}'+  /* smaller ring */
        '#bw-botname{font-size:13px}'+
        '#bw-status span:last-child{font-size:9.5px}'+
        '.bw-hbtn{width:36px;height:36px;min-width:36px}'+
        '.bw-hbtn svg{width:14px;height:14px}'+

        /* ── Messages: flex:1 fills available space between header and input ── */
        '#bw-msgs{padding:10px 14px;gap:4px}'+
        '.bw-msg.bot{max-width:100%}'+
        '.bw-msg.user{max-width:85%}'+
        '.bw-bubble{font-size:14px;line-height:1.7}'+
        '.bw-msg.user .bw-bubble{padding:9px 16px;border-radius:18px!important;border-bottom-right-radius:6px!important}'+

        /* ── Input: anchored at bottom, keyboard pushes it up naturally ── */
        '#bw-inputarea{padding:6px 10px calc(6px + env(safe-area-inset-bottom,0px));border-top:1px solid rgba(255,255,255,0.05)}'+
        '#bw-input-wrap{border-radius:20px}'+
        '#bw-input{font-size:16px;padding:8px 14px 2px;min-height:34px}'+
        '#bw-input::placeholder{font-size:14px}'+
        '#bw-input-toolbar{padding:2px 6px 4px}'+
        '.bw-toolbar-btn{width:30px;height:30px;font-size:15px}'+
        '.bw-toolbar-btn svg{width:14px;height:14px}'+
        '#bw-send{width:32px;height:32px}'+
        '#bw-send svg{width:14px;height:14px}'+

        /* ── Footer: minimal, safe-area ── */
        '#bw-footer{padding:4px 8px calc(4px + env(safe-area-inset-bottom,0px));font-size:9px}'+

        /* ── Upload ── */
        '#bw-upload{margin:4px 14px 8px;padding:16px 14px}'+

        /* ── Emoji: bigger targets ── */
        '#bw-emoji-panel{left:6px;right:6px;bottom:58px;padding:10px}'+
        '#bw-emoji-panel.show{grid-template-columns:repeat(7,1fr)}'+
        '.bw-emo{font-size:22px}'+

        /* ── Language popup ── */
        '#bw-lang-popup{right:6px;left:6px;bottom:58px}'+
        '.bw-lang-opt{padding:12px 16px;font-size:13px}'+

        /* ── Exit overlay ── */
        '#bw-exit-overlay{border-radius:18px 18px 0 0}'+
        '#bw-exit-panel{padding:28px 20px}'+
        '#bw-exit-title{font-size:20px;margin-bottom:24px}'+
        '#bw-exit-options{gap:22px}'+
        '.bw-exit-circle{width:50px;height:50px;font-size:21px}'+
        '.bw-exit-label{font-size:11.5px}'+
        '.bw-exit-star{font-size:34px;padding:4px}'+

        /* ── Splash ── */
        '#bw-splash{border-radius:18px 18px 0 0}'+
        '#bw-splash-logo{width:100px;height:100px}'+
        '#bw-splash-text{margin-top:20px}'+
        '#bw-splash-line1{font-size:13px}'+
        '#bw-splash-line2{font-size:10px}'+

        /* ── Quick actions ── */
        '#bw-qactions{padding:4px 14px 8px}'+
        '.bw-qbtn{padding:10px 18px;font-size:13px}'+

        /* ── ID form ── */
        '#bw-idform{padding:4px 14px 8px}'+
        '#bw-idinput{padding:11px 14px;font-size:14px;border-radius:14px}'+
        '#bw-idconfirm{padding:11px 18px;font-size:14px;border-radius:14px}'+

        /* ── Fullscreen toggle ── */
        '#bw-window.bw-fullscreen{top:0;height:100vh;max-height:100vh;border-radius:0}'+

        /* ── Logo watermark ── */
        '#bw-logo-bg img{width:80px;height:80px}'+
      '}'
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
        '<div id="bw-fab-logo"><img src="' + LOGO_FULL_B64 + '" alt="BW"></div>' +
        '<span id="bw-fab-label">Here to help</span>' +
      '</button>' +
      '<div id="bw-window" role="dialog" aria-label="BetonWin Support">' +
        /* Splash */
        '<div id="bw-splash">' +
          '<div id="bw-splash-logo"><img src="' + LOGO_FULL_B64 + '" alt="BetonWin"></div>' +
          '<div id="bw-splash-text">' +
            '<div id="bw-splash-line1"></div>' +
            '<div id="bw-splash-line2"></div>' +
          '</div>' +
        '</div>' +
        '<div id="bw-logo-bg"><img src="' + LOGO_FULL_B64 + '"></div>' +
        '<div id="bw-header">' +
          '<div id="bw-avatar"><img src="' + LOGO_FULL_B64 + '" alt="BetonWin"></div>' +
          '<div id="bw-hinfo">' +
            '<div id="bw-botname">' + CONFIG.BOT_NAME + '</div>' +
            '<div id="bw-status"><span id="bw-statusdot"></span><span>' + t('online') + '</span></div>' +
          '</div>' +
          '<div id="bw-hbtns">' +
            '<button class="bw-hbtn" id="bw-fullscreen" title="Fullscreen">' +
              '<svg viewBox="0 0 24 24"><path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/></svg>' +
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
        '<div id="bw-lang-popup"></div>' +
        '<div id="bw-inputarea">' +
          '<div id="bw-input-wrap">' +
            '<textarea id="bw-input" placeholder="' + t('placeholder') + '" rows="1"></textarea>' +
            '<div id="bw-input-toolbar">' +
              '<button class="bw-toolbar-btn" id="bw-emoji-btn" title="Emoji" aria-label="Emoji">😊</button>' +
              '<button class="bw-toolbar-btn" id="bw-attach-btn" title="Attach file" aria-label="Attach file">' +
                '<svg viewBox="0 0 24 24"><path d="M16.5 6v11.5c0 2.21-1.79 4-4 4s-4-1.79-4-4V5a2.5 2.5 0 015 0v10.5c0 .55-.45 1-1 1s-1-.45-1-1V6h-1.5v9.5a2.5 2.5 0 005 0V5c0-2.21-1.79-4-4-4S7 2.79 7 5v12.5c0 3.04 2.46 5.5 5.5 5.5s5.5-2.46 5.5-5.5V6H16.5z"/></svg>' +
              '</button>' +
              '<button class="bw-toolbar-btn" id="bw-lang-btn" title="Language" aria-label="Change language">' +
                '<svg viewBox="0 0 24 24"><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zm6.93 6h-2.95a15.65 15.65 0 00-1.38-3.56A8.03 8.03 0 0118.92 8zM12 4.04c.83 1.2 1.48 2.53 1.91 3.96h-3.82c.43-1.43 1.08-2.76 1.91-3.96zM4.26 14C4.1 13.36 4 12.69 4 12s.1-1.36.26-2h3.38c-.08.66-.14 1.32-.14 2s.06 1.34.14 2H4.26zm.82 2h2.95c.32 1.25.78 2.45 1.38 3.56A7.987 7.987 0 015.08 16zm2.95-8H5.08a7.987 7.987 0 014.33-3.56A15.65 15.65 0 008.03 8zM12 19.96c-.83-1.2-1.48-2.53-1.91-3.96h3.82c-.43 1.43-1.08 2.76-1.91 3.96zM14.34 14H9.66c-.09-.66-.16-1.32-.16-2s.07-1.35.16-2h4.68c.09.65.16 1.32.16 2s-.07 1.34-.16 2zm.25 5.56c.6-1.11 1.06-2.31 1.38-3.56h2.95a8.03 8.03 0 01-4.33 3.56zM16.36 14c.08-.66.14-1.32.14-2s-.06-1.34-.14-2h3.38c.16.64.26 1.31.26 2s-.1 1.36-.26 2h-3.38z"/></svg>' +
              '</button>' +
              '<button id="bw-send" aria-label="Send message">' +
                '<svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>' +
              '</button>' +
            '</div>' +
          '</div>' +
        '</div>' +
        '<div id="bw-footer">Powered by BetonWin AI</div>' +
        /* Exit overlay panel */
        '<div id="bw-exit-overlay">' +
          '<div id="bw-exit-panel">' +
            '<div id="bw-exit-title">' + t('exit_title') + '</div>' +
            '<div id="bw-exit-options">' +
              '<button id="bw-exit-newchat" class="bw-exit-card">' +
                '<div class="bw-exit-circle">💬</div>' +
                '<span class="bw-exit-label">' + t('exit_new_chat') + '</span>' +
              '</button>' +
              '<button id="bw-exit-feedback" class="bw-exit-card">' +
                '<div class="bw-exit-circle">⭐</div>' +
                '<span class="bw-exit-label">' + t('exit_feedback') + '</span>' +
              '</button>' +
              '<button id="bw-exit-close">' +
                '<div class="bw-exit-circle">👋</div>' +
                '<span class="bw-exit-label">' + t('exit_close') + '</span>' +
              '</button>' +
            '</div>' +
            '<div id="bw-exit-csat">' +
              '<div id="bw-exit-csat-label">' + t('csat_ask') + '</div>' +
              '<div id="bw-exit-stars">' +
                '<span class="bw-exit-star" data-r="1">★</span>' +
                '<span class="bw-exit-star" data-r="2">★</span>' +
                '<span class="bw-exit-star" data-r="3">★</span>' +
                '<span class="bw-exit-star" data-r="4">★</span>' +
                '<span class="bw-exit-star" data-r="5">★</span>' +
              '</div>' +
            '</div>' +
          '</div>' +
        '</div>' +
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

  var IMG_EXT = /\.(jpg|jpeg|png|gif|webp|svg|bmp)(\?[^\s]*)?$/i;
  var VID_EXT = /\.(mp4|webm|mov|ogg)(\?[^\s]*)?$/i;

  function parseMarkdown(txt) {
    // 1. Extract media URLs BEFORE escaping — images and videos rendered inline
    var media = [];
    // Markdown images: ![alt](url)
    txt = txt.replace(/!\[(.*?)\]\((https?:\/\/[^\s)]+)\)/g, function (_, alt, url) {
      var idx = media.length;
      media.push({ type: 'img', url: url, alt: alt });
      return '%%MEDIA' + idx + '%%';
    });
    // Raw image URLs on their own line
    txt = txt.replace(/^(https?:\/\/[^\s]+(?:\.(?:jpg|jpeg|png|gif|webp|svg|bmp))(?:\?[^\s]*)?)$/gim, function (_, url) {
      var idx = media.length;
      media.push({ type: 'img', url: url, alt: '' });
      return '%%MEDIA' + idx + '%%';
    });
    // Raw video URLs on their own line
    txt = txt.replace(/^(https?:\/\/[^\s]+(?:\.(?:mp4|webm|mov|ogg))(?:\?[^\s]*)?)$/gim, function (_, url) {
      var idx = media.length;
      media.push({ type: 'vid', url: url });
      return '%%MEDIA' + idx + '%%';
    });

    // 2. Extract markdown links BEFORE escaping
    var links = [];
    txt = txt.replace(/\[(.*?)\]\((https?:\/\/[^\s)]+)\)/g, function (_, text, url) {
      var idx = links.length;
      // If link points to image/video, render as media instead
      if (IMG_EXT.test(url)) {
        var mIdx = media.length;
        media.push({ type: 'img', url: url, alt: text });
        return '%%MEDIA' + mIdx + '%%';
      }
      if (VID_EXT.test(url)) {
        var mIdx = media.length;
        media.push({ type: 'vid', url: url });
        return '%%MEDIA' + mIdx + '%%';
      }
      links.push({ text: text, url: url });
      return '%%LINK' + idx + '%%';
    });

    // 3. Escape HTML + apply markdown formatting
    var out = escapeHTML(txt)
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/^[•*\-]\s+(.+)$/gm, '<span style="display:flex;align-items:flex-start;gap:10px;padding:4px 0"><span style="color:rgba(69,205,152,0.5);font-size:16px;line-height:1;flex-shrink:0;margin-top:2px">&#8226;</span><span style="flex:1">$1</span></span>')
      .replace(/^(\d+)\.\s+(.+)$/gm, '<span style="display:flex;align-items:flex-start;gap:10px;padding:4px 0"><span style="color:rgba(69,205,152,0.55);font-weight:600;font-size:13px;min-width:16px;flex-shrink:0;font-variant-numeric:tabular-nums">$1.</span><span style="flex:1">$2</span></span>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/^---$/gm, '<hr>');

    // 4. Restore links
    links.forEach(function (link, i) {
      var safeUrl = link.url.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
      out = out.replace('%%LINK' + i + '%%',
        '<a href="' + safeUrl + '" target="_blank" rel="noopener">' + escapeHTML(link.text) + '</a>');
    });

    // 5. Restore media (images + videos)
    media.forEach(function (m, i) {
      var safeUrl = m.url.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
      var html;
      if (m.type === 'img') {
        html = '<div class="bw-media"><img src="' + safeUrl + '" alt="' + escapeHTML(m.alt || '') + '" loading="lazy" onclick="window.open(this.src,\'_blank\')"></div>';
      } else {
        html = '<div class="bw-media"><video src="' + safeUrl + '" controls playsinline preload="metadata"></video></div>';
      }
      out = out.replace('%%MEDIA' + i + '%%', html);
    });

    return out;
  }

  var LOGO_FULL_B64 = 'data:image/png;base64,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';
  var BOT_AVATAR_IMG = '<img src="' + LOGO_FULL_B64 + '" alt="BW">';
  var AGENT_AVATAR_SVG = '<svg viewBox="0 0 24 24" fill="' + C.warning + '"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>';

  function addMessage(role, content) {
    var msgs   = document.getElementById('bw-msgs');
    var typing = document.getElementById('bw-typing');
    var div    = document.createElement('div');
    div.className = 'bw-msg ' + role;
    var html = parseMarkdown(content);
    if (role === 'bot') {
      div.innerHTML = '<div class="bw-mavatar">' + BOT_AVATAR_IMG + '</div><div class="bw-bubble">' + html + '</div>';
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
      '<div style="min-width:0">' +
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
    var trigger = document.getElementById('bw-trigger');
    el.classList.toggle('show', show);
    trigger.classList.toggle('bw-busy', show);
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
      var allResults = [];
      // translated results (index 1 if exists) — priority
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
         'withdraw','withdrawal','my balance','can you','could you','i have','support','available'],
    it: ['ciao','grazie','buongiorno','buonasera','prelievo','prelevare','perché','perche','voglio',
         'questo','questa','subito','ancora','sono','mia','aiuto','stai','bene','cosa',
         'come stai','che dici','dimmi','salve','scusa','prego','buona','giorno','sera',
         'depositi','soldi','conto','non ho ricevuto','non è arrivato',
         'dove','come posso','non riesco','accedere','vedere','trovare','voglio sapere',
         'non capisco','qual è','mi serve','il mio','la mia','ho bisogno','vorrei',
         'quale','quanti','quante','ricevere','rispondi','scrivo','registrarmi','registrare',
         'minima','minimo','posso ricevere','come faccio','come si fa','non riesco a',
         'il bonus','il deposito','la password','il conto','cosa devo'],
    es: ['hola','gracias','buenos','retiro','retirar','también','quiero','cuánto','cuándo',
         'dinero','ayuda','cuenta','no he recibido','no ha llegado','por favor',
         'cómo','estoy','tengo','puedo','dónde','puedo ver','no puedo','necesito','quisiera',
         'como funciona','cuanto tarda','cuanto cuesta','como hago','que es','quiero saber'],
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
    // Short messages (greetings): 1 match is enough
    // Longer messages: require 2 matches to avoid false positives
    // If already in that language: 1 match always enough
    var isShort = text.length < 30;
    var minScore = (lang === best || isShort) ? 1 : 2;
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
      // Feedback intermedio
      if (STATE.pollCount === 10) addMessage('bot', '⏳ Still analyzing...');
      if (STATE.pollCount === 30) addMessage('bot', '⏳ Almost done...');
      // Timeout → escalate instead of error
      if (STATE.pollCount > CONFIG.POLL_MAX) {
        clearInterval(STATE.pollTimer);
        addMessage('bot', '⏳ Analysis is taking longer than expected. Connecting you with an agent...');
        startEscalation('deposit_analysis_timeout');
        return;
      }
      apiStatus(jobId).then(function (res) {
        if (res.status && res.status !== 'PENDING') {
          clearInterval(STATE.pollTimer);
          onDone(res);
        }
      }).catch(function () { /* poll error — silent */ });
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
    // Allow during UPLOAD_REQUIRED (deposit) OR LIVE_AGENT (file sharing)
    if (STATE.phase === 'LIVE_AGENT' && STATE.ticketId) {
      sendFileToAgent(file);
      return;
    }
    if (STATE.phase !== 'UPLOAD_REQUIRED') return;
    if (!STATE.playerId) return;
    if (!file || file.size === 0) { addMessage('bot', t('err_file_type')); return; }
    if (file.size > CONFIG.MAX_FILE_MB * 1024 * 1024) { addMessage('bot', t('err_file_size')); return; }
    if (CONFIG.ACCEPTED_TYPES.indexOf(file.type) === -1) { addMessage('bot', t('err_file_type')); return; }

    STATE.phase = 'UPLOADING';
    STATE._uploadFile = file;
    STATE._uploadRetries = 0;
    showUpload(false);
    addMessage('bot', t('uploading'));
    setProgress(0);
    performUpload(file);
  }

  function performUpload(file) {
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
      .catch(function () {
        STATE._uploadRetries = (STATE._uploadRetries || 0) + 1;
        if (STATE._uploadRetries < 3 && STATE._uploadFile) {
          setProgress(0);
          addMessage('bot', 'Upload failed, retrying... (' + STATE._uploadRetries + '/3)');
          setTimeout(function () { performUpload(STATE._uploadFile); }, 2000 * STATE._uploadRetries);
        } else {
          addMessage('bot', t('err_generic'));
          STATE.phase = 'UPLOAD_REQUIRED';
          showUpload(true);
          setInputDisabled(false);
        }
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

    n8nCall(CONFIG.ENDPOINTS.ESCALATE, {
      reason: reason,
      language: lang,
      conversation_history: history,
      player_id: playerId,
      player_name: playerName,
      player_email: playerEmail
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

  // Poll Zendesk for new agent replies — with since tracking + backoff
  function startAgentPolling(ticketId) {
    var pollCount = 0;
    var shownKeys = {};
    var lastTs = 0;
    var idleCount = 0;
    var currentInterval = AGENT_POLL_INTERVAL;
    clearTimeout(STATE.agentPollTimer);

    function poll() {
      pollCount++;
      if (pollCount > AGENT_POLL_MAX) {
        stopAgentPolling();
        addMessage('bot', t('agent_closed'));
        STATE.phase = 'AGENT_CLOSED';
        setInputDisabled(true);
        return;
      }
      n8nCall(CONFIG.ENDPOINTS.AGENT_POLL, { ticket_id: ticketId, since: lastTs })
        .then(function (res) {
          var hasNew = false;
          if (res.comments && res.comments.length > 0) {
            showTyping(false);
            res.comments.forEach(function (c) {
              var key = (c.body || '') + '|' + (c.ts || '');
              if (shownKeys[key]) return;
              shownKeys[key] = true;
              hasNew = true;
              if (c.ts) lastTs = c.ts;
              var agentName = c.author || t('live_agent');
              addAgentMessage(agentName, c.body);
              document.getElementById('bw-botname').textContent = agentName;
              STATE._agentName = agentName;
            });
          }
          // Backoff: if no new comments, slow down polling
          if (hasNew) {
            idleCount = 0;
            currentInterval = AGENT_POLL_INTERVAL; // Reset to 5s
          } else {
            idleCount++;
            if (idleCount > 6) currentInterval = Math.min(currentInterval * 1.3, 20000); // Max 20s
          }
          // Close on 'closed' OR 'solved'
          if (res.status === 'closed' || res.status === 'solved') {
            stopAgentPolling();
            addAgentMessage(t('live_agent'), t('agent_closed'));
            STATE.phase = 'AGENT_CLOSED';
            setInputDisabled(true);
            document.getElementById('bw-botname').textContent = CONFIG.BOT_NAME;
            document.getElementById('bw-statusdot').style.background = C.green;
            setTimeout(function () { showCSAT(); }, 1000);
          } else {
            STATE.agentPollTimer = setTimeout(poll, currentInterval);
          }
        })
        .catch(function () {
          STATE.agentPollTimer = setTimeout(poll, currentInterval);
        });
    }
    STATE.agentPollTimer = setTimeout(poll, AGENT_POLL_INTERVAL);
  }

  function stopAgentPolling() {
    clearTimeout(STATE.agentPollTimer);
    STATE.agentPollTimer = null;
  }

  // Main chat handler — KB first, n8n fallback
  function updateUILanguage() {
    document.getElementById('bw-input').placeholder = t('placeholder');
    document.getElementById('bw-idinput').placeholder = t('player_id_ph');
    document.getElementById('bw-idconfirm').textContent = t('confirm');
    // Exit overlay labels
    var nc = document.querySelector('#bw-exit-newchat .bw-exit-label');
    var fb = document.querySelector('#bw-exit-feedback .bw-exit-label');
    var cl = document.querySelector('#bw-exit-close .bw-exit-label');
    if (nc) nc.textContent = t('exit_new_chat');
    if (fb) fb.textContent = t('exit_feedback');
    if (cl) cl.textContent = t('exit_close');
  }

  function handleChatMessage(text) {
    text = (text || '').trim();
    if (!text) return;

    // Fade out logo watermark on first message
    var logoBg = document.getElementById('bw-logo-bg');
    if (logoBg && !logoBg.classList.contains('hidden')) {
      logoBg.classList.add('hidden');
    }

    // Rate limit + prevent double-send
    var now = Date.now();
    if (STATE.busy || (now - STATE.lastSendTs) < SEND_COOLDOWN) return;
    STATE.busy = true;
    STATE.lastSendTs = now;

    // Cap message length to prevent huge payloads
    if (text.length > MAX_MSG_LENGTH) { text = text.slice(0, MAX_MSG_LENGTH); }

    // Auto-detect language from what the user typed (update global lang + UI)
    var detected = detectLangFromText(text);
    var userSetLang = false;
    if (detected && LANG[detected] && detected !== lang) {
      lang = detected;
      userSetLang = true;
      updateUILanguage();
    } else if (detected && detected === lang) {
      userSetLang = true;
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
    if (window.innerWidth < 440) document.getElementById('bw-input').blur();
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

    // 0b. Sensitive content (gambling addiction) → immediate escalation
    if (detectSensitive(text)) {
      showTyping(false);
      addMessage('bot', t('human_escalate'));
      clearTimeout(safetyTimer);
      STATE.busy = false;
      startEscalation('sensitive_content');
      return;
    }

    // T-07: If high urgency from frustration → reduce human request threshold to 1
    if (STATE.urgency === 'high' && STATE.humanRequestCount === 0) {
      // Don't escalate yet, but any human request signal will trigger immediately
    }

    // 0c. User explicitly asks for human → increment counter, maybe escalate
    if (userWantsHuman(text)) {
      STATE.humanRequestCount++;
      // T-07: If frustrated, threshold drops to 1 (immediate escalation on first human request)
      var threshold = STATE.urgency === 'high' ? 1 : HUMAN_REQUEST_THRESHOLD;
      if (STATE.humanRequestCount >= threshold) {
        showTyping(false);
        addMessage('bot', t('human_escalate'));
        clearTimeout(safetyTimer);
        STATE.busy = false;
        startEscalation(STATE.urgency === 'high' ? 'T-07_frustrated_human_request' : 'human_request');
        return;
      }
      // Not at threshold yet — let AI respond, but counter is already incremented
      // The AI response check (aiDetectsHumanRequest) will NOT double-count
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
      new Promise(function (resolve) { setTimeout(function () { resolve({ results: [] }); }, 3500); })
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
        var history = STATE.messages.slice(-12).map(function (m) {
          return { role: (m.role === 'bot' || m.role === 'agent') ? 'assistant' : 'user', content: m.content };
        });
        var aiTimeout = new Promise(function (_, reject) {
          setTimeout(function () { reject(new Error('timeout')); }, 18000);
        });
        // Add language instruction to kb_content so AI knows to respond in the right language
        var LANG_NAMES = { en: 'English', es: 'Spanish', it: 'Italian', pt: 'Portuguese' };
        var langInstruction = 'IMPORTANT: The user is writing in ' + (LANG_NAMES[lang] || 'Spanish') +
          '. You MUST respond in ' + (LANG_NAMES[lang] || 'Spanish') + '.\n\n';
        // Inject language hint directly into the message so AI cannot ignore it
        var msgWithLang = lang !== 'es'
          ? '[Reply ONLY in ' + (LANG_NAMES[lang] || 'Spanish') + '] ' + text
          : text;
        var payload = { message: msgWithLang, kb_content: langInstruction + kbContent, lang: lang, history: history };
        return Promise.race([
          n8nCall(CONFIG.ENDPOINTS.CHAT, payload),
          aiTimeout
        ]);
      })
      .then(function (res) {
        showTyping(false);
        var raw = res.response || res.message || t('err_generic');
        // Strip <!--lang:XX--> tag — only update language if user didn't just set it
        var langMatch = raw.match(/<!--lang:([a-z]{2})-->/);
        if (langMatch && LANG[langMatch[1]] && !userSetLang) { lang = langMatch[1]; }
        raw = raw.replace(/<!--lang:[a-z]{2}-->\s*/g, '').trim();
        // Detect language rejection from n8n and retry in Spanish as fallback
        var rejectPatterns = ['non offriamo supporto', 'no ofrecemos soporte', 'no ofrezco soporte',
          'do not offer support', 'não oferecemos suporte', 'riformulare', 'reformule',
          'not offer assistance', 'currently not available in', 'parlo solo'];
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
        // AI-based human request detection (second layer):
        // Only count if user's message didn't already trigger userWantsHuman
        if (!userWantsHuman(text) && aiDetectsHumanRequest(raw)) {
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
    document.getElementById('bw-close').addEventListener('click', function () { showExitOverlay(true); });

    // Exit overlay buttons
    document.getElementById('bw-exit-newchat').addEventListener('click', function () {
      showExitOverlay(false);
      resetChat();
    });
    document.getElementById('bw-exit-feedback').addEventListener('click', function () {
      // Hide cards, show stars
      document.getElementById('bw-exit-options').style.display = 'none';
      document.getElementById('bw-exit-csat').style.display = 'block';
      document.getElementById('bw-exit-title').textContent = t('csat_ask');
    });
    document.getElementById('bw-exit-close').addEventListener('click', function () {
      showExitOverlay(false);
      toggleOpen(false);
    });
    // Star hover + click
    var exitStars = document.getElementById('bw-exit-stars');
    exitStars.addEventListener('mouseover', function (e) {
      var star = e.target.closest('.bw-exit-star');
      if (!star) return;
      var r = parseInt(star.getAttribute('data-r'));
      exitStars.querySelectorAll('.bw-exit-star').forEach(function (s) {
        s.classList.toggle('active', parseInt(s.getAttribute('data-r')) <= r);
      });
    });
    exitStars.addEventListener('mouseleave', function () {
      // Reset unless already submitted
      if (exitStars.dataset.submitted) return;
      exitStars.querySelectorAll('.bw-exit-star').forEach(function (s) {
        s.classList.remove('active');
      });
    });
    exitStars.addEventListener('click', function (e) {
      var star = e.target.closest('.bw-exit-star');
      if (!star) return;
      var rating = parseInt(star.getAttribute('data-r'));
      exitStars.dataset.submitted = '1';
      // Lock stars visual
      exitStars.querySelectorAll('.bw-exit-star').forEach(function (s) {
        s.classList.toggle('active', parseInt(s.getAttribute('data-r')) <= rating);
      });
      exitStars.style.pointerEvents = 'none';
      // Track + send to Zendesk
      trackEvent('csat_rating', { rating: rating, ticketId: STATE.ticketId });
      if (STATE.ticketId) {
        n8nCall(CONFIG.ENDPOINTS.AGENT_REPLY, {
          ticket_id: STATE.ticketId,
          message: '⭐ Customer rated experience: ' + rating + '/5'
        }).catch(function () {});
      }
      // Show thanks, then close
      document.getElementById('bw-exit-csat-label').textContent = t('exit_thanks');
      setTimeout(function () {
        showExitOverlay(false);
        toggleOpen(false);
      }, 1200);
    });

    // Click outside exit panel → back to chat
    document.getElementById('bw-exit-overlay').addEventListener('click', function (e) {
      if (e.target === this) showExitOverlay(false);
    });

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

    // Attach button — opens file picker
    document.getElementById('bw-attach-btn').addEventListener('click', function () {
      document.getElementById('bw-ufile').click();
    });

    // Language popup
    var langPopup = document.getElementById('bw-lang-popup');
    var LANG_OPTIONS = [
      { code: 'es', flag: '🇪🇸', label: 'Español' },
      { code: 'en', flag: '🇬🇧', label: 'English' },
      { code: 'it', flag: '🇮🇹', label: 'Italiano' },
      { code: 'pt', flag: '🇧🇷', label: 'Português' }
    ];
    langPopup.innerHTML = LANG_OPTIONS.map(function (l) {
      return '<button class="bw-lang-opt' + (l.code === lang ? ' active' : '') + '" data-lang="' + l.code + '"><span>' + l.flag + '</span><span>' + l.label + '</span></button>';
    }).join('');
    document.getElementById('bw-lang-btn').addEventListener('click', function () {
      langPopup.classList.toggle('show');
      // Update active state
      langPopup.querySelectorAll('.bw-lang-opt').forEach(function (b) {
        b.classList.toggle('active', b.getAttribute('data-lang') === lang);
      });
    });
    langPopup.addEventListener('click', function (e) {
      var opt = e.target.closest('.bw-lang-opt');
      if (!opt) return;
      lang = opt.getAttribute('data-lang');
      updateUILanguage();
      langPopup.querySelectorAll('.bw-lang-opt').forEach(function (b) {
        b.classList.toggle('active', b.getAttribute('data-lang') === lang);
      });
      langPopup.classList.remove('show');
    });
    document.addEventListener('click', function (e) {
      if (!e.target.closest('#bw-lang-popup') && !e.target.closest('#bw-lang-btn')) {
        langPopup.classList.remove('show');
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
  function showExitOverlay(show) {
    var overlay = document.getElementById('bw-exit-overlay');
    if (show) {
      // Reset panel to initial state each time
      document.getElementById('bw-exit-title').textContent = t('exit_title');
      document.getElementById('bw-exit-options').style.display = '';
      document.getElementById('bw-exit-csat').style.display = 'none';
      var exitStars = document.getElementById('bw-exit-stars');
      exitStars.style.pointerEvents = '';
      delete exitStars.dataset.submitted;
      exitStars.querySelectorAll('.bw-exit-star').forEach(function (s) { s.classList.remove('active'); });
    }
    overlay.classList.toggle('show', show);
  }

  var splashShown = false;
  function toggleOpen(open) {
    STATE.isOpen = open;
    document.getElementById('bw-trigger').classList.toggle('bw-open', open);
    document.getElementById('bw-window').classList.toggle('bw-open', open);
    // Mobile: hide page scroll when widget is open
    if (window.innerWidth <= 440) {
      document.documentElement.style.overflow = open ? 'hidden' : '';
      document.body.style.overflow = open ? 'hidden' : '';
    }
    if (open) {
      // Splash screen on first open only
      if (!splashShown) {
        splashShown = true;
        var splash = document.getElementById('bw-splash');
        if (splash) {
          // Typewriter effect — starts after logo animation
          var tw1 = document.getElementById('bw-splash-line1');
          var tw2 = document.getElementById('bw-splash-line2');
          var text1 = t('splash_line1');
          var text2 = t('splash_line2');
          var cursor = '<span id="bw-splash-cursor"></span>';
          var i = 0, j = 0;
          // Start typing line 1 after logo appears
          setTimeout(function () {
            var typeInterval1 = setInterval(function () {
              if (i < text1.length) {
                tw1.innerHTML = text1.substring(0, ++i) + cursor;
              } else {
                clearInterval(typeInterval1);
                tw1.innerHTML = text1;
                setTimeout(function () {
                  var typeInterval2 = setInterval(function () {
                    if (j < text2.length) {
                      tw2.innerHTML = text2.substring(0, ++j) + cursor;
                    } else {
                      clearInterval(typeInterval2);
                      tw2.innerHTML = text2;
                    }
                  }, 25);
                }, 100);
              }
            }, 30);
          }, 600);
          // Exit splash
          setTimeout(function () {
            splash.classList.add('bw-splash-out');
            splash.addEventListener('animationend', function () {
              splash.remove();
              document.getElementById('bw-input').focus();
            }, { once: true });
          }, 2200);
        }
      } else {
        document.getElementById('bw-input').focus();
      }
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
    // Restore logo watermark
    var logoBg = document.getElementById('bw-logo-bg');
    if (logoBg) logoBg.classList.remove('hidden');
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
      '<div class="bw-mavatar">' + BOT_AVATAR_IMG + '</div>' +
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

    // Mobile: scroll messages when keyboard opens
    if (window.visualViewport && window.innerWidth <= 440) {
      window.visualViewport.addEventListener('resize', function() {
        if (!STATE.isOpen) return;
        var m = document.getElementById('bw-msgs');
        if (m) m.scrollTop = m.scrollHeight;
      });
    }

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

  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
