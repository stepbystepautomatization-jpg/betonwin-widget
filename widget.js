(function () {
  'use strict';

  // ============================================================
  // 1. CONFIGURATION
  // ============================================================
  var IS_LOCAL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');

  var CONFIG = {
    N8N_BASE: IS_LOCAL ? 'http://localhost:8080' : 'https://n8nbeton.online',
    KB_URL:   IS_LOCAL ? 'http://localhost:8080/kb' : 'https://script.google.com/macros/s/AKfycbw4QH_cxD2HmW18ReyCUzo4BDPwrHeUaMwYKxXnjwSNc0yhPxCAFqZRkI6dDBD5y0ZI/exec',
    ENDPOINTS: {
      CHAT:        '/webhook/chat',
      VERIFY:      '/webhook/verify-deposit',
      STATUS:      '/webhook/status',
      PRESIGNED:   '/webhook/presigned-url',
      ANALYZE:     '/webhook/analyze'
    },
    POLL_INTERVAL_MS: 3000,
    POLL_MAX:         40,
    BOT_NAME:         'BetonBot',
    MAX_FILE_MB:      10,
    ACCEPTED_TYPES:   ['image/jpeg', 'image/png', 'image/webp', 'application/pdf']
  };

  // ============================================================
  // 2. COLORS
  // ============================================================
  var C = {
    bg:            '#0c1018',
    widget:        '#131923',
    header:        '#1a2535',
    green:         '#39d353',
    greenDark:     '#2aa644',
    greenGlow:     'rgba(57,211,83,0.12)',
    greenGlowB:    'rgba(57,211,83,0.25)',
    text:          '#e2e8f0',
    textMuted:     '#8892a4',
    border:        'rgba(255,255,255,0.07)',
    headerBorder:  'rgba(57,211,83,0.2)',
    userBubble:    '#1a472a',
    botBubble:     '#1e2535',
    input:         '#1a2030',
    inputBorder:   'rgba(255,255,255,0.1)',
    scrollbar:     '#2a3548',
    danger:        '#f87171',
    warning:       '#fbbf24',
    shadow:        '0 24px 64px rgba(0,0,0,0.6), 0 4px 16px rgba(0,0,0,0.4)',
    triggerShadow: '0 4px 24px rgba(57,211,83,0.4)'
  };

  // ============================================================
  // 3. TRANSLATIONS (i18n) — EN / ES / IT / PT
  // ============================================================
  var LANG = {
    en: {
      welcome:          "Hi! I'm **BetonBot**, your 24/7 support assistant. How can I help you today?",
      placeholder:      'Type your message...',
      send:             'Send',
      typing:           'BetonBot is typing...',
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
      close:            'Close'
    },
    es: {
      welcome:          '¡Hola! Soy **BetonBot**, tu asistente de soporte 24/7. ¿En qué puedo ayudarte hoy?',
      placeholder:      'Escribe tu mensaje...',
      send:             'Enviar',
      typing:           'BetonBot está escribiendo...',
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
      close:            'Cerrar'
    },
    it: {
      welcome:          'Ciao! Sono **BetonBot**, il tuo assistente di supporto 24/7. Come posso aiutarti oggi?',
      placeholder:      'Scrivi il tuo messaggio...',
      send:             'Invia',
      typing:           'BetonBot sta scrivendo...',
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
      close:            'Chiudi'
    },
    pt: {
      welcome:          'Olá! Sou o **BetonBot**, seu assistente de suporte 24/7. Como posso ajudá-lo hoje?',
      placeholder:      'Digite sua mensagem...',
      send:             'Enviar',
      typing:           'BetonBot está digitando...',
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
      close:            'Fechar'
    }
  };

  var lang = 'en';
  function t(k) { return (LANG[lang] || LANG.en)[k] || k; }

  // ============================================================
  // 4. STATE
  // ============================================================
  var STATE = {
    isOpen:     false,
    phase:      'CHAT',
    playerId:   null,
    jobId:      null,
    pollTimer:  null,
    pollCount:  0,
    messages:   []
  };

  // ============================================================
  // 5. INJECT CSS
  // ============================================================
  function injectCSS() {
    if (document.getElementById('__beton_css__')) return;
    var s = document.createElement('style');
    s.id = '__beton_css__';
    s.textContent = [
      '#__beton_widget__{position:fixed;bottom:24px;right:24px;z-index:2147483647;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}',
      '#__beton_widget__ *{box-sizing:border-box;margin:0;padding:0}',

      '#bw-trigger{width:60px;height:60px;background:linear-gradient(135deg,'+C.green+','+C.greenDark+');border:none;border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:'+C.triggerShadow+';transition:all .3s cubic-bezier(.175,.885,.32,1.275);position:relative;outline:none}',
      '#bw-trigger:hover{transform:scale(1.1)}',
      '#bw-trigger.bw-open{transform:scale(0.85);opacity:0;pointer-events:none}',
      '#bw-trigger svg{width:28px;height:28px;fill:#fff}',
      '#bw-notif{position:absolute;top:-2px;right:-2px;width:14px;height:14px;background:'+C.danger+';border-radius:50%;border:2px solid '+C.bg+';display:none}',

      '#bw-window{position:absolute;bottom:76px;right:0;width:390px;height:600px;background:'+C.widget+';border-radius:20px;border:1px solid '+C.border+';box-shadow:'+C.shadow+';display:flex;flex-direction:column;overflow:hidden;transform-origin:bottom right;transition:all .35s cubic-bezier(.175,.885,.32,1.275);transform:scale(.85) translateY(16px);opacity:0;pointer-events:none}',
      '#bw-window.bw-open{transform:scale(1) translateY(0);opacity:1;pointer-events:all}',

      '#bw-header{background:linear-gradient(135deg,'+C.header+','+C.widget+');border-bottom:1px solid '+C.headerBorder+';padding:14px 18px;display:flex;align-items:center;gap:12px;flex-shrink:0}',
      '#bw-avatar{width:42px;height:42px;background:linear-gradient(135deg,'+C.green+','+C.greenDark+');border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0;box-shadow:0 0 16px '+C.greenGlowB+'}',
      '#bw-hinfo{flex:1;min-width:0}',
      '#bw-botname{color:'+C.text+';font-weight:700;font-size:15px;line-height:1.2}',
      '#bw-status{color:'+C.green+';font-size:12px;display:flex;align-items:center;gap:5px;margin-top:2px}',
      '#bw-statusdot{width:6px;height:6px;background:'+C.green+';border-radius:50%;animation:bw-pulse 2s infinite;flex-shrink:0}',
      '#bw-hbtns{display:flex;gap:4px}',
      '.bw-hbtn{width:32px;height:32px;background:transparent;border:none;border-radius:8px;cursor:pointer;display:flex;align-items:center;justify-content:center;color:'+C.textMuted+';transition:all .2s;outline:none}',
      '.bw-hbtn:hover{background:rgba(255,255,255,.06);color:'+C.text+'}',
      '.bw-hbtn svg{width:16px;height:16px;fill:currentColor}',

      '#bw-msgs{flex:1;overflow-y:auto;padding:18px 14px;display:flex;flex-direction:column;gap:10px;scroll-behavior:smooth}',
      '#bw-msgs::-webkit-scrollbar{width:4px}',
      '#bw-msgs::-webkit-scrollbar-track{background:transparent}',
      '#bw-msgs::-webkit-scrollbar-thumb{background:'+C.scrollbar+';border-radius:4px}',

      '.bw-msg{display:flex;gap:8px;max-width:86%;animation:bw-up .28s ease}',
      '.bw-msg.user{margin-left:auto;flex-direction:row-reverse}',
      '.bw-mavatar{width:28px;height:28px;background:linear-gradient(135deg,'+C.green+','+C.greenDark+');border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0;align-self:flex-end}',
      '.bw-bubble{padding:10px 14px;border-radius:18px;font-size:14px;line-height:1.55;word-break:break-word;white-space:pre-line}',
      '.bw-msg.bot .bw-bubble{background:'+C.botBubble+';border:1px solid rgba(255,255,255,.05);color:'+C.text+';border-bottom-left-radius:4px}',
      '.bw-msg.user .bw-bubble{background:linear-gradient(135deg,'+C.green+','+C.greenDark+');color:#fff;border-bottom-right-radius:4px}',
      '.bw-bubble b,.bw-bubble strong{font-weight:700}',
      '.bw-bubble em,.bw-bubble i{font-style:italic}',
      '.bw-bubble hr{border:none;border-top:1px solid rgba(255,255,255,.1);margin:8px 0}',

      '#bw-typing{display:none;align-items:center;gap:8px;animation:bw-up .28s ease;padding:2px 0}',
      '#bw-typing.show{display:flex}',
      '#bw-tdots{display:flex;gap:4px}',
      '.bw-dot{width:6px;height:6px;background:'+C.green+';border-radius:50%;animation:bw-bounce 1.2s infinite}',
      '.bw-dot:nth-child(2){animation-delay:.2s}',
      '.bw-dot:nth-child(3){animation-delay:.4s}',
      '#bw-tlabel{color:'+C.textMuted+';font-size:12px}',

      '#bw-qactions{padding:0 14px 10px;display:flex;flex-wrap:wrap;gap:8px;flex-shrink:0}',
      '.bw-qbtn{background:transparent;border:1px solid '+C.green+';color:'+C.green+';border-radius:20px;padding:7px 15px;font-size:13px;cursor:pointer;transition:all .2s;font-family:inherit;outline:none;white-space:nowrap}',
      '.bw-qbtn:hover{background:'+C.greenGlow+';transform:translateY(-1px)}',

      '#bw-idform{padding:0 14px 10px;display:none;gap:8px;flex-shrink:0;align-items:center}',
      '#bw-idform.show{display:flex}',
      '#bw-idinput{flex:1;background:'+C.input+';border:1px solid '+C.inputBorder+';color:'+C.text+';border-radius:10px;padding:10px 13px;font-size:14px;outline:none;transition:border-color .2s;font-family:inherit}',
      '#bw-idinput:focus{border-color:'+C.green+'}',
      '#bw-idinput::placeholder{color:'+C.textMuted+'}',
      '#bw-idconfirm{background:linear-gradient(135deg,'+C.green+','+C.greenDark+');border:none;color:#fff;border-radius:10px;padding:10px 16px;font-size:14px;font-weight:600;cursor:pointer;transition:all .2s;white-space:nowrap;font-family:inherit;outline:none}',
      '#bw-idconfirm:hover{opacity:.9;transform:translateY(-1px)}',

      '#bw-upload{margin:0 14px 10px;border:2px dashed '+C.inputBorder+';border-radius:14px;padding:22px 16px;text-align:center;cursor:pointer;transition:all .3s;display:none;flex-shrink:0}',
      '#bw-upload.show{display:block}',
      '#bw-upload.drag{border-color:'+C.green+';background:'+C.greenGlow+'}',
      '#bw-upload.busy{opacity:.55;pointer-events:none}',
      '#bw-uico{font-size:34px;margin-bottom:8px}',
      '#bw-utxt{color:'+C.text+';font-size:14px;font-weight:500}',
      '#bw-uhint{color:'+C.textMuted+';font-size:12px;margin-top:4px}',
      '#bw-ufile{display:none}',
      '#bw-uprog{margin-top:12px;background:'+C.border+';border-radius:4px;height:4px;overflow:hidden;display:none}',
      '#bw-uprog.show{display:block}',
      '#bw-uprogbar{height:100%;background:linear-gradient(90deg,'+C.green+','+C.greenDark+');border-radius:4px;width:0%;transition:width .3s}',

      '#bw-inputarea{padding:12px 14px;border-top:1px solid '+C.border+';display:flex;gap:8px;align-items:flex-end;background:'+C.widget+';flex-shrink:0}',
      '#bw-input{flex:1;background:'+C.input+';border:1px solid '+C.inputBorder+';color:'+C.text+';border-radius:12px;padding:10px 13px;font-size:14px;resize:none;outline:none;min-height:42px;max-height:120px;line-height:1.45;font-family:inherit;transition:border-color .2s}',
      '#bw-input:focus{border-color:'+C.green+'}',
      '#bw-input::placeholder{color:'+C.textMuted+'}',
      '#bw-send{width:42px;height:42px;background:linear-gradient(135deg,'+C.green+','+C.greenDark+');border:none;border-radius:12px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .2s;flex-shrink:0;outline:none}',
      '#bw-send:hover{transform:translateY(-1px);box-shadow:0 4px 14px '+C.greenGlowB+'}',
      '#bw-send:disabled{opacity:.4;cursor:not-allowed;transform:none;box-shadow:none}',
      '#bw-send svg{width:18px;height:18px;fill:#fff}',

      '#bw-footer{text-align:center;padding:6px;color:'+C.textMuted+';font-size:10px;border-top:1px solid '+C.border+';flex-shrink:0;letter-spacing:.3px}',

      '@keyframes bw-up{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}',
      '@keyframes bw-pulse{0%,100%{opacity:1}50%{opacity:.35}}',
      '@keyframes bw-bounce{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-5px)}}',

      '@media(max-width:440px){#__beton_widget__{bottom:16px;right:16px;left:16px}#bw-window{width:100%;right:0;left:0;bottom:76px;height:calc(100vh - 100px);max-height:600px}}'
    ].join('');
    document.head.appendChild(s);
  }

  // ============================================================
  // 6. BUILD HTML
  // ============================================================
  function buildHTML() {
    document.getElementById('__beton_widget__').innerHTML =
      '<button id="bw-trigger" aria-label="Support Chat">' +
        '<span id="bw-notif"></span>' +
        '<svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H5.17L4 17.17V4h16v12z"/></svg>' +
      '</button>' +
      '<div id="bw-window" role="dialog" aria-label="BetonBot">' +
        '<div id="bw-header">' +
          '<div id="bw-avatar">🎯</div>' +
          '<div id="bw-hinfo">' +
            '<div id="bw-botname">' + CONFIG.BOT_NAME + '</div>' +
            '<div id="bw-status"><span id="bw-statusdot"></span><span>' + t('online') + '</span></div>' +
          '</div>' +
          '<div id="bw-hbtns">' +
            '<button class="bw-hbtn" id="bw-newchat" title="' + t('new_chat') + '">' +
              '<svg viewBox="0 0 24 24"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg>' +
            '</button>' +
            '<button class="bw-hbtn" id="bw-close" title="' + t('close') + '">' +
              '<svg viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>' +
            '</button>' +
          '</div>' +
        '</div>' +
        '<div id="bw-msgs">' +
          '<div id="bw-typing">' +
            '<div id="bw-tdots"><div class="bw-dot"></div><div class="bw-dot"></div><div class="bw-dot"></div></div>' +
            '<span id="bw-tlabel">' + t('typing') + '</span>' +
          '</div>' +
        '</div>' +
        '<div id="bw-qactions">' +
          '<button class="bw-qbtn" id="bw-qa-deposit">💳 ' + t('quick_deposit') + '</button>' +
        '</div>' +
        '<div id="bw-idform">' +
          '<input type="text" id="bw-idinput" placeholder="' + t('player_id_ph') + '" autocomplete="off" maxlength="50">' +
          '<button id="bw-idconfirm">' + t('confirm') + '</button>' +
        '</div>' +
        '<div id="bw-upload">' +
          '<input type="file" id="bw-ufile" accept=".jpg,.jpeg,.png,.webp,.pdf">' +
          '<div id="bw-uico">📎</div>' +
          '<div id="bw-utxt">' + t('upload_drag') + '</div>' +
          '<div id="bw-uhint">' + t('upload_hint') + '</div>' +
          '<div id="bw-uprog"><div id="bw-uprogbar"></div></div>' +
        '</div>' +
        '<div id="bw-inputarea">' +
          '<textarea id="bw-input" placeholder="' + t('placeholder') + '" rows="1"></textarea>' +
          '<button id="bw-send">' +
            '<svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>' +
          '</button>' +
        '</div>' +
        '<div id="bw-footer">Powered by BetonBot AI</div>' +
      '</div>';
  }

  // ============================================================
  // 7. UI HELPERS
  // ============================================================
  function parseMarkdown(txt) {
    return txt
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/^---$/gm, '<hr>')
      .replace(/\n\n/g, '<br><br>')
      .replace(/\n/g, '<br>');
  }

  function addMessage(role, content) {
    var msgs   = document.getElementById('bw-msgs');
    var typing = document.getElementById('bw-typing');
    var div    = document.createElement('div');
    div.className = 'bw-msg ' + role;
    var html = parseMarkdown(content);
    if (role === 'bot') {
      div.innerHTML = '<div class="bw-mavatar">🎯</div><div class="bw-bubble">' + html + '</div>';
    } else {
      div.innerHTML = '<div class="bw-bubble">' + html + '</div>';
    }
    msgs.insertBefore(div, typing);
    msgs.scrollTop = msgs.scrollHeight;
    STATE.messages.push({ role: role, content: content, ts: Date.now() });
    return div;
  }

  function showTyping(show) {
    var el = document.getElementById('bw-typing');
    el.classList.toggle('show', show);
    if (show) { var m = document.getElementById('bw-msgs'); m.scrollTop = m.scrollHeight; }
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

  // GET request to Apps Script / mock KB (CORS-friendly — no preflight triggered)
  function searchKB(query) {
    var url = CONFIG.KB_URL + '?q=' + encodeURIComponent(query) + '&lang=' + lang + '&max=3';
    return fetch(url, { redirect: 'follow' }).then(function (r) {
      if (!r.ok) { throw new Error('KB ' + r.status); }
      return r.json();
    });
  }

  // Language words for auto-detecting language from typed text
  var LANG_WORDS = {
    it: ['ciao','grazie','buongiorno','buonasera','prelievo','prelevare','perché','voglio',
         'questo','questa','subito','ancora','sono','mio','mia','quanto','quando','aiuto',
         'problema','depositi','soldi','conto','non ho ricevuto','non è arrivato'],
    es: ['hola','gracias','buenos','retiro','retirar','también','quiero','cuánto','cuándo',
         'dinero','ayuda','problema','cuenta','no he recibido','no ha llegado','por favor',
         'cómo','estoy','tengo','puedo'],
    pt: ['olá','ola','obrigado','obrigada','saque','sacar','também','quero','quanto','quando',
         'dinheiro','ajuda','problema','conta','não recebi','não chegou','por favor',
         'como','estou','tenho','posso']
  };

  // Auto-detect language from user message text (overrides browser lang when confident)
  function detectLangFromText(text) {
    var lower = text.toLowerCase();
    var scores = { it: 0, es: 0, pt: 0 };
    Object.keys(scores).forEach(function (l) {
      LANG_WORDS[l].forEach(function (w) {
        if (lower.indexOf(w) !== -1) { scores[l]++; }
      });
    });
    var best = null, bestScore = 0; // require at least 1 match
    Object.keys(scores).forEach(function (l) {
      if (scores[l] > bestScore) { best = l; bestScore = scores[l]; }
    });
    return best; // null if no confident match → keep current lang
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

  // Smart extraction: finds the most relevant paragraph for the user's query (zero AI)
  function smartExtract(content, query) {
    var clean = content.trim().replace(/\r\n/g, '\n').replace(/\n{3,}/g, '\n\n');
    var blocks = clean.split(/\n\n+/).map(function (b) { return b.trim(); })
                      .filter(function (b) { return b.length > 10; });

    // Short content — return as-is
    if (blocks.length <= 2) { return clean; }

    // Score each block by how many query words appear in it
    var words = query.toLowerCase().split(/[\s,.?!;:]+/)
                     .filter(function (w) { return w.length > 2; });
    var scored = blocks.map(function (block) {
      var lower = block.toLowerCase();
      var score = words.reduce(function (acc, w) {
        return acc + (lower.indexOf(w) !== -1 ? 1 : 0);
      }, 0);
      return { block: block, score: score };
    });
    scored.sort(function (a, b) { return b.score - a.score; });

    // No matches at all → return full content
    if (scored[0].score === 0) { return clean; }

    // Best block found — add a second block only if best is short AND second is substantial
    var result = scored[0].block;
    if (result.length < 220 && scored.length > 1 && scored[1].score > 0 && scored[1].block.length >= 60) {
      result += '\n\n' + scored[1].block;
    }
    return result;
  }

  // Security: strip lines containing credentials or internal-only info before showing to users
  function sanitizeForUser(text) {
    var CRED_PATTERNS = [
      /contrase[ñn]a/i, /password/i,
      /usuario\s*(→|:)/i, /user\s*(→|:)/i,
      /pass\s*(→|:)/i,
      /merchants\./i, /atlassian\.net/i, /backoffice/i,
      /\d{4,}Welcome/i
    ];
    var lines = text.split('\n').filter(function (line) {
      return !CRED_PATTERNS.some(function (re) { return re.test(line); });
    });
    return lines.join('\n').trim();
  }

  // Build a natural response: intro (in user's language) + relevant content + closing
  function buildResponse(articleName, content, query) {
    var extracted = sanitizeForUser(smartExtract(content, query));
    var name = (articleName || '').replace(/\.[^.]+$/, '');
    var intros = {
      en: 'Here\'s what I found' + (name ? ' about **' + name + '**' : '') + ':\n\n',
      it: 'Ecco le informazioni' + (name ? ' su **' + name + '**' : '') + ':\n\n',
      es: 'Aquí está la información' + (name ? ' sobre **' + name + '**' : '') + ':\n\n',
      pt: 'Aqui estão as informações' + (name ? ' sobre **' + name + '**' : '') + ':\n\n'
    };
    var outros = {
      en: '\n\nIs there anything else I can help you with?',
      it: '\n\nPosso aiutarti con qualcos\'altro?',
      es: '\n\n¿Puedo ayudarte con algo más?',
      pt: '\n\nPosso ajudá-lo com mais alguma coisa?'
    };
    return (intros[lang] || intros.en) + extracted + (outros[lang] || outros.en);
  }

  // ============================================================
  // 9. n8n API — webhook calls (used as fallback / deposit flow)
  // ============================================================
  function n8nCall(endpoint, body, method) {
    method = method || 'POST';
    var url  = CONFIG.N8N_BASE + endpoint;
    var opts = { method: method, headers: { 'Content-Type': 'application/json' } };
    if (method !== 'GET') { opts.body = JSON.stringify(body); }
    return fetch(url, opts).then(function (r) {
      if (!r.ok) { throw new Error('n8n HTTP ' + r.status); }
      return r.json();
    });
  }

  function apiChat(message) {
    return n8nCall(CONFIG.ENDPOINTS.CHAT, { message: message, language: lang, history: STATE.messages.slice(-8) });
  }
  function apiVerify(playerId) {
    return n8nCall(CONFIG.ENDPOINTS.VERIFY, { player_id: playerId, language: lang });
  }
  function apiStatus(jobId) {
    return n8nCall(CONFIG.ENDPOINTS.STATUS + '/' + jobId, null, 'GET');
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
      }).catch(function (e) { console.warn('[BetonBot] poll:', e); });
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
        console.error('[BetonBot] upload:', e);
        addMessage('bot', t('err_generic'));
        STATE.phase = 'CHAT';
        setInputDisabled(false);
      });
  }

  function uploadToS3(url, file, onProgress) {
    return new Promise(function (resolve, reject) {
      var xhr = new XMLHttpRequest();
      xhr.upload.addEventListener('progress', function (e) {
        if (e.lengthComputable) { onProgress(Math.round(e.loaded / e.total * 100)); }
      });
      xhr.addEventListener('load', function () {
        if (xhr.status >= 200 && xhr.status < 300) { resolve(); }
        else { reject(new Error('S3 ' + xhr.status)); }
      });
      xhr.addEventListener('error', reject);
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
    switch (result.status) {
      case 'APPROVED':       addMessage('bot', t('result_approved')); break;
      case 'REJECTED':       addMessage('bot', t('result_rejected')); break;
      case 'PENDING_REVIEW': addMessage('bot', t('result_pending'));  break;
      default:               addMessage('bot', t('err_generic'));
    }
    STATE.phase = 'RESULT';
    showQuickActions(true);
  }

  // Main chat handler — KB first, n8n fallback
  function handleChatMessage(text) {
    text = (text || '').trim();
    if (!text) return;

    // Auto-detect language from what the user typed (update global lang)
    var detected = detectLangFromText(text);
    if (detected && LANG[detected]) { lang = detected; }

    addMessage('user', text);
    document.getElementById('bw-input').value = '';
    document.getElementById('bw-input').style.height = 'auto';
    showTyping(true);
    setInputDisabled(true);

    // 1. Detect deposit problem → start verification flow
    if (detectIntent(text) === 'DEPOSIT') {
      showTyping(false);
      addMessage('bot', t('deposit_intent'));
      setInputDisabled(false);
      startDepositFlow();
      return;
    }

    // 2. Search knowledge base directly, extract the most relevant section
    searchKB(text)
      .then(function (data) {
        showTyping(false);
        if (data.results && data.results.length > 0) {
          var r    = data.results[0];
          var name = (r.name || '').replace(/\.[^.]+$/, '');
          addMessage('bot', buildResponse(name, r.content || '', text));
        } else {
          addMessage('bot', t('no_results'));
        }
        setInputDisabled(false);
      })
      .catch(function (kbErr) {
        // 3. KB unavailable → fallback to n8n /webhook/chat
        console.warn('[BetonBot] KB error, fallback to n8n:', kbErr.message);
        apiChat(text)
          .then(function (res) {
            showTyping(false);
            addMessage('bot', res.message || t('err_generic'));
            if (res.action === 'START_DEPOSIT_FLOW') { startDepositFlow(); }
            else { setInputDisabled(false); }
          })
          .catch(function () {
            showTyping(false);
            addMessage('bot', t('no_results'));
            setInputDisabled(false);
          });
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
    STATE.playerId = id;
    showPlayerIdForm(false);
    addMessage('user', id);
    showTyping(true);
    setInputDisabled(true);
    addMessage('bot', t('deposit_checking'));
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
    document.getElementById('bw-trigger').addEventListener('click', function () { toggleOpen(true); });
    document.getElementById('bw-close').addEventListener('click', function ()   { toggleOpen(false); });
    document.getElementById('bw-newchat').addEventListener('click', resetChat);

    document.getElementById('bw-send').addEventListener('click', function () {
      handleChatMessage(document.getElementById('bw-input').value);
    });
    document.getElementById('bw-input').addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleChatMessage(this.value); }
    });
    document.getElementById('bw-input').addEventListener('input', function () {
      this.style.height = 'auto';
      this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });

    document.getElementById('bw-qa-deposit').addEventListener('click', function () {
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
    uploadArea.addEventListener('click', function () { fileInput.click(); });
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
    if (open) { document.getElementById('bw-input').focus(); }
  }

  function resetChat() {
    stopPolling();
    STATE.messages = []; STATE.jobId = null; STATE.playerId = null; STATE.phase = 'CHAT';
    document.getElementById('bw-msgs').innerHTML =
      '<div id="bw-typing">' +
        '<div id="bw-tdots"><div class="bw-dot"></div><div class="bw-dot"></div><div class="bw-dot"></div></div>' +
        '<span id="bw-tlabel">' + t('typing') + '</span>' +
      '</div>';
    showPlayerIdForm(false); showUpload(false); showQuickActions(true);
    setInputDisabled(false); setProgress(0);
    document.getElementById('bw-idinput').value = '';
    document.getElementById('bw-input').value   = '';
    document.getElementById('bw-input').style.height = 'auto';
    setTimeout(function () { addMessage('bot', t('welcome')); }, 300);
  }

  // ============================================================
  // 15. INIT
  // ============================================================
  function init() {
    injectCSS();
    buildHTML();
    bindEvents();
    setTimeout(function () { addMessage('bot', t('welcome')); }, 500);
    console.log('[BetonBot] v1.1.0 ready — lang:', lang);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
