/**
 * Farm Route — Kisan Vani AI Voice Assistant & Chatbot
 * Non-blocking floating popup widget with Speech-to-Text (STT) & Text-to-Speech (TTS).
 * Answers questions about Crop Prices (MSP), Procurement Starting Dates/Schedules,
 * Mandi Centers, Slot Booking, Live Queues, and Farmer Grievance Redressal.
 */

(function () {
  'use strict';

  // Prevent multiple initializations
  if (window.KisanVoiceAssistant) return;

  // Determine base path for relative URLs
  function getBasePath() {
    const p = window.location.pathname;
    if (p.includes('/farmer/') || p.includes('/admin/') || p.includes('/operator/') || p.includes('/pages/')) {
      return '../';
    }
    return './';
  }

  const BASE = getBasePath();

  // Assistant State
  const State = {
    isOpen: false,
    isMinimized: false,
    isListening: false,
    isSpeaking: false,
    ttsEnabled: true,
    hasSpokenWelcome: false,
    welcomeAudioText: '',
    currentLanguage: 'en-IN',
    activeUtterance: null,
    recognition: null,
    messages: []
  };

  window.addEventListener('kisan_language_changed', (e) => {
    State.currentLanguage = 'en-IN';
    if (State.recognition) {
      State.recognition.lang = State.currentLanguage;
    }
  });

  // Offline/Fallback Knowledge for 100% Reliability
  const LOCAL_KNOWLEDGE = {
    wheat: {
      crop: "Wheat (Grade A)",
      msp: "₹2,275 / Quintal",
      demo: "₹2,425 / Quintal",
      start: "1 April 2026",
      end: "15 May 2026",
      season: "Rabi 2026",
      moisture: "12% Max",
      desc: "Government procurement of wheat runs from 1 April to 15 May 2026. The minimum support price (MSP) is ₹2,275 per quintal."
    },
    mustard: {
      crop: "Mustard",
      msp: "₹5,650 / Quintal",
      demo: "₹5,650 / Quintal",
      start: "15 March 2026",
      end: "30 April 2026",
      season: "Rabi 2026",
      moisture: "9% Max",
      desc: "Mustard procurement started on 15 March 2026 and continues until 30 April. The MSP is ₹5,650 per quintal."
    },
    gram: {
      crop: "Gram / Chickpea",
      msp: "₹5,440 / Quintal",
      demo: "₹5,440 / Quintal",
      start: "1 April 2026",
      end: "15 May 2026",
      season: "Rabi 2026",
      moisture: "10% Max",
      desc: "Gram procurement is scheduled from 1 April to 15 May 2026. The MSP rate is ₹5,440 per quintal."
    },
    barley: {
      crop: "Barley",
      msp: "₹1,850 / Quintal",
      demo: "₹1,980 / Quintal",
      start: "1 April 2026",
      end: "15 May 2026",
      season: "Rabi 2026",
      moisture: "12% Max",
      desc: "Barley procurement runs from 1 April to 15 May 2026. The MSP rate is ₹1,850 per quintal."
    },
    paddy: {
      crop: "Paddy (Common)",
      msp: "₹2,183 / Quintal",
      demo: "₹2,320 / Quintal",
      start: "1 October 2026",
      end: "15 November 2026",
      season: "Kharif 2026",
      moisture: "17% Max",
      desc: "Government paddy procurement is scheduled from 1 October to 15 November 2026. The MSP is ₹2,183 per quintal."
    },
    bajra: {
      crop: "Bajra (Pearl Millet)",
      msp: "₹2,500 / Quintal",
      demo: "₹2,625 / Quintal",
      start: "1 October 2026",
      end: "15 November 2026",
      season: "Kharif 2026",
      moisture: "12% Max",
      desc: "Bajra procurement runs from 1 October to 15 November 2026. The MSP rate is ₹2,500 per quintal."
    },
    cotton: {
      crop: "Cotton",
      msp: "₹6,620 / Quintal",
      demo: "₹7,122 / Quintal",
      start: "15 October 2026",
      end: "31 December 2026",
      season: "Kharif 2026",
      moisture: "8.5% Max",
      desc: "Cotton procurement runs from 15 October to 31 December 2026. The MSP rate is ₹6,620 per quintal."
    }
  };

  // UI Elements container
  let UI = {};

  // -------------------------------------------------------------
  // 1. INJECT STYLESHEET IF MISSING
  // -------------------------------------------------------------
  function ensureStylesheet() {
    const existing = document.getElementById('kisan-voice-assistant-css');
    if (!existing) {
      const link = document.createElement('link');
      link.id = 'kisan-voice-assistant-css';
      link.rel = 'stylesheet';
      link.href = BASE + 'css/voice-assistant.css';
      document.head.appendChild(link);
    }
  }

  // -------------------------------------------------------------
  // 2. INJECT WIDGET DOM
  // -------------------------------------------------------------
  function createWidgetDOM() {
    ensureStylesheet();

    // Launcher container
    const launcherContainer = document.createElement('div');
    launcherContainer.className = 'kv-launcher-container';
    launcherContainer.id = 'kv-launcher-root';
    launcherContainer.innerHTML = `
      <button type="button" class="kv-launcher-btn" id="kv-launcher-btn" aria-label="Kisan Vani AI Voice Assistant">
        <div class="kv-launcher-pulse"></div>
        <div class="kv-launcher-avatar">
          <span>🌾</span>
        </div>
        <div class="kv-launcher-text-box">
          <div class="kv-launcher-title">
            <span>Kisan Vani</span>
            <span class="kv-launcher-mic-badge">AI Voice</span>
          </div>
          <span class="kv-launcher-sub">Rates, Dates & Market Support</span>
        </div>
      </button>
    `;

    // Popup window
    const popupWindow = document.createElement('div');
    popupWindow.className = 'kv-popup-window';
    popupWindow.id = 'kv-popup-window';
    popupWindow.setAttribute('role', 'dialog');
    popupWindow.setAttribute('aria-label', 'Kisan Vani Chatbot');
    popupWindow.innerHTML = `
      <!-- Header -->
      <div class="kv-header" id="kv-header">
        <div class="kv-header-profile">
          <div class="kv-header-avatar">
            <span>🌾</span>
            <div class="kv-header-online-dot"></div>
          </div>
          <div class="kv-header-title-box">
            <div class="kv-header-title">
              <span>Kisan Vani</span>
              <span class="kv-header-badge">AI Assistant</span>
              <div class="kv-equalizer" id="kv-header-equalizer" style="display: none;">
                <div class="kv-eq-bar"></div>
                <div class="kv-eq-bar"></div>
                <div class="kv-eq-bar"></div>
                <div class="kv-eq-bar"></div>
              </div>
            </div>
            <span class="kv-header-sub">Rates • Procurement Schedules • Slot Help</span>
          </div>
        </div>
        <div class="kv-header-actions">
          <button type="button" class="kv-icon-btn" id="kv-tts-toggle-btn" title="Toggle Audio (Speech)">
            🔊
          </button>
          <button type="button" class="kv-icon-btn" id="kv-reset-btn" title="Clear Conversation">
            🔄
          </button>
          <button type="button" class="kv-icon-btn" id="kv-minimize-btn" title="Minimize">
            ➖
          </button>
          <button type="button" class="kv-icon-btn" id="kv-close-btn" title="Close">
            ✕
          </button>
        </div>
      </div>

      <!-- Status banner (Listening / Speaking) -->
      <div class="kv-status-banner" id="kv-status-banner" style="display: none;">
        <span id="kv-status-text">🎤 Listening... please speak</span>
        <button type="button" id="kv-status-cancel-btn" style="background:none;border:none;cursor:pointer;font-weight:700;color:inherit;">✕</button>
      </div>

      <!-- Chat Body -->
      <div class="kv-chat-body" id="kv-chat-body">
        <!-- Messages will be injected here -->
      </div>

      <!-- Footer / Input -->
      <div class="kv-chat-footer">
        <div class="kv-input-row">
          <button type="button" class="kv-mic-btn" id="kv-mic-btn" title="Click to Speak">
            🎙️
          </button>
          <input type="text" class="kv-text-input" id="kv-text-input" placeholder="Ask a question or click mic to speak..." autocomplete="off" />
          <button type="button" class="kv-send-btn" id="kv-send-btn" title="Send">
            ➤
          </button>
        </div>
        <div class="kv-footer-sub">
          <span class="kv-lang-indicator">
            <span>🌐</span> <span id="kv-lang-label">English (EN)</span>
          </span>
          <span>Use alongside website 🌐</span>
        </div>
      </div>
    `;

    document.body.appendChild(launcherContainer);
    document.body.appendChild(popupWindow);

    // Bind UI references
    UI = {
      launcher: document.getElementById('kv-launcher-btn'),
      popup: document.getElementById('kv-popup-window'),
      chatBody: document.getElementById('kv-chat-body'),
      textInput: document.getElementById('kv-text-input'),
      sendBtn: document.getElementById('kv-send-btn'),
      micBtn: document.getElementById('kv-mic-btn'),
      closeBtn: document.getElementById('kv-close-btn'),
      minimizeBtn: document.getElementById('kv-minimize-btn'),
      resetBtn: document.getElementById('kv-reset-btn'),
      ttsToggleBtn: document.getElementById('kv-tts-toggle-btn'),
      statusBanner: document.getElementById('kv-status-banner'),
      statusText: document.getElementById('kv-status-text'),
      statusCancelBtn: document.getElementById('kv-status-cancel-btn'),
      headerEqualizer: document.getElementById('kv-header-equalizer')
    };

    bindEvents();
    initSpeechRecognition();
    showWelcomeMessage();
  }

  // -------------------------------------------------------------
  // 3. SPEECH RECOGNITION (STT) SETUP
  // -------------------------------------------------------------
  function initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      console.warn("KisanVoiceAssistant: Web Speech Recognition API not supported in this browser.");
      if (UI.micBtn) {
        UI.micBtn.title = "Voice input is not supported in this browser. Type instead.";
      }
      return;
    }

    const rec = new SpeechRecognition();
    rec.continuous = false;
    rec.interimResults = true;
    rec.lang = State.currentLanguage;

    rec.onstart = () => {
      State.isListening = true;
      UI.micBtn.classList.add('kv-listening');
      UI.statusBanner.className = 'kv-status-banner kv-listening';
      UI.statusBanner.style.display = 'flex';
      UI.statusText.textContent = '🎤 Listening... please speak';
      stopSpeaking();
    };

    rec.onresult = (event) => {
      let interim = '';
      let final = '';
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          final += event.results[i][0].transcript;
        } else {
          interim += event.results[i][0].transcript;
        }
      }

      if (interim) {
        UI.textInput.value = interim;
      }
      if (final) {
        UI.textInput.value = final;
        stopListening();
        submitQuery(final);
      }
    };

    rec.onerror = (event) => {
      console.warn("Speech recognition error:", event.error);
      stopListening();
      if (event.error === 'not-allowed') {
        alert("Microphone permission was denied. Please allow microphone access in your browser settings.");
      }
    };

    rec.onend = () => {
      stopListening();
    };

    State.recognition = rec;
  }

  function startListening() {
    if (!State.recognition) {
      alert("Voice recognition is not supported in your browser. Please type your query.");
      return;
    }
    try {
      State.recognition.lang = State.currentLanguage;
      State.recognition.start();
    } catch (err) {
      console.warn("Failed to start speech recognition:", err);
      stopListening();
    }
  }

  function stopListening() {
    State.isListening = false;
    if (UI.micBtn) UI.micBtn.classList.remove('kv-listening');
    if (UI.statusBanner && !State.isSpeaking) UI.statusBanner.style.display = 'none';
    if (State.recognition) {
      try {
        State.recognition.abort();
      } catch (e) {
        try { State.recognition.stop(); } catch (err) {}
      }
    }
  }

  // -------------------------------------------------------------
  // 4. TEXT TO SPEECH (TTS) SETUP
  // -------------------------------------------------------------
  function speakText(text) {
    if (!State.isOpen) return;
    if (!State.ttsEnabled || !window.speechSynthesis) return;

    stopSpeaking();

    // Clean markdown characters for speech
    const cleanSpeech = text
      .replace(/[*_#`~[\]()•]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();

    if (!cleanSpeech) return;

    const utterance = new SpeechSynthesisUtterance(cleanSpeech);
    utterance.lang = State.currentLanguage;
    utterance.rate = 0.95;
    utterance.pitch = 1.0;

    const voices = window.speechSynthesis.getVoices();
    const englishVoice = voices.find(v => v.lang && (v.lang.startsWith('en-IN') || v.lang.startsWith('en-US') || v.lang.startsWith('en-GB') || v.lang.startsWith('en')));
    if (englishVoice) {
      utterance.voice = englishVoice;
    }

    utterance.onstart = () => {
      if (!State.isOpen) {
        stopSpeaking();
        return;
      }
      State.isSpeaking = true;
      if (UI.headerEqualizer) UI.headerEqualizer.style.display = 'inline-flex';
      if (UI.statusBanner) {
        UI.statusBanner.className = 'kv-status-banner kv-speaking';
        UI.statusBanner.style.display = 'flex';
        UI.statusText.innerHTML = '🔊 Kisan Vani is speaking...';
      }
    };

    utterance.onend = () => {
      State.isSpeaking = false;
      if (UI.headerEqualizer) UI.headerEqualizer.style.display = 'none';
      if (UI.statusBanner && !State.isListening) UI.statusBanner.style.display = 'none';
      document.querySelectorAll('.kv-read-btn.kv-playing').forEach(btn => {
        btn.classList.remove('kv-playing');
        btn.innerHTML = '🔊 Listen';
      });
    };

    utterance.onerror = () => {
      State.isSpeaking = false;
      if (UI.headerEqualizer) UI.headerEqualizer.style.display = 'none';
      if (UI.statusBanner && !State.isListening) UI.statusBanner.style.display = 'none';
      document.querySelectorAll('.kv-read-btn.kv-playing').forEach(btn => {
        btn.classList.remove('kv-playing');
        btn.innerHTML = '🔊 Listen';
      });
    };

    State.activeUtterance = utterance;
    window.speechSynthesis.speak(utterance);
  }

  function stopSpeaking() {
    State.isSpeaking = false;

    if (State.activeUtterance) {
      State.activeUtterance.onstart = null;
      State.activeUtterance.onend = null;
      State.activeUtterance.onerror = null;
      State.activeUtterance = null;
    }

    if (window.speechSynthesis) {
      try {
        window.speechSynthesis.cancel();
        if (window.speechSynthesis.speaking || window.speechSynthesis.pending) {
          window.speechSynthesis.pause();
          window.speechSynthesis.cancel();
          window.speechSynthesis.resume();
          window.speechSynthesis.cancel();
        }
      } catch (e) {
        console.warn("speechSynthesis cancel error:", e);
      }
    }

    if (UI.headerEqualizer) UI.headerEqualizer.style.display = 'none';
    if (UI.statusBanner && !State.isListening) UI.statusBanner.style.display = 'none';
    document.querySelectorAll('.kv-read-btn.kv-playing').forEach(btn => {
      btn.classList.remove('kv-playing');
      btn.innerHTML = '🔊 Listen';
    });
  }

  // -------------------------------------------------------------
  // 5. MESSAGE RENDERING & CHAT UI
  // -------------------------------------------------------------
  function getTimeString() {
    const d = new Date();
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  function formatMarkdown(text) {
    let html = text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n• /g, '<br>• ')
      .replace(/\n/g, '<br>');
    return `<p>${html}</p>`;
  }

  function appendUserMessage(text) {
    const msgEl = document.createElement('div');
    msgEl.className = 'kv-msg kv-msg-user';
    msgEl.innerHTML = `
      <div class="kv-bubble">${text}</div>
      <span class="kv-msg-time">${getTimeString()}</span>
    `;
    UI.chatBody.appendChild(msgEl);
    scrollToBottom();
  }

  function appendBotMessage(data, autoSpeak = true) {
    const msgEl = document.createElement('div');
    msgEl.className = 'kv-msg kv-msg-bot';

    const bodyHtml = formatMarkdown(data.response);

    let actionChipsHtml = '';
    if (data.quick_actions && data.quick_actions.length > 0) {
      actionChipsHtml = `
        <div class="kv-action-chips">
          ${data.quick_actions.map(act => {
            let targetUrl = act.url;
            if (!targetUrl.startsWith('http') && !targetUrl.startsWith('#')) {
              targetUrl = BASE + targetUrl;
            }
            return `<a href="${targetUrl}" class="kv-action-link">${act.label} &rarr;</a>`;
          }).join('')}
        </div>
      `;
    }

    const audioTextEscaped = (data.audio_text || data.response).replace(/"/g, '&quot;');

    msgEl.innerHTML = `
      <div class="kv-bubble">
        ${bodyHtml}
        ${actionChipsHtml}
        <button type="button" class="kv-read-btn" data-audio="${audioTextEscaped}">
          🔊 Listen
        </button>
      </div>
      <span class="kv-msg-time">Kisan Vani • ${getTimeString()}</span>
    `;

    UI.chatBody.appendChild(msgEl);

    const readBtn = msgEl.querySelector('.kv-read-btn');
    readBtn.addEventListener('click', () => {
      if (readBtn.classList.contains('kv-playing')) {
        stopSpeaking();
      } else {
        document.querySelectorAll('.kv-read-btn.kv-playing').forEach(b => {
          b.classList.remove('kv-playing');
          b.innerHTML = '🔊 Listen';
        });
        readBtn.classList.add('kv-playing');
        readBtn.innerHTML = '⏹️ Stop';
        speakText(data.audio_text || data.response);
      }
    });

    if (data.suggestions && data.suggestions.length > 0) {
      appendSuggestionChips(data.suggestions);
    }

    scrollToBottom();

    if (autoSpeak && State.isOpen && State.ttsEnabled && data.audio_text) {
      speakText(data.audio_text);
    }
  }

  function appendSuggestionChips(suggestions) {
    const existing = UI.chatBody.querySelector('.kv-quick-prompts-dynamic');
    if (existing) existing.remove();

    const container = document.createElement('div');
    container.className = 'kv-quick-prompts kv-quick-prompts-dynamic';
    container.innerHTML = `
      <div class="kv-prompts-title">Suggested Queries:</div>
      <div class="kv-prompts-grid">
        ${suggestions.map(s => `<button type="button" class="kv-prompt-chip">${s}</button>`).join('')}
      </div>
    `;

    container.querySelectorAll('.kv-prompt-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        submitQuery(chip.textContent.trim());
      });
    });

    UI.chatBody.appendChild(container);
    scrollToBottom();
  }

  function showWelcomeMessage() {
    let farmerName = "Farmer";
    if (window.KisanAuth && window.KisanAuth.getCurrentUser()) {
      farmerName = window.KisanAuth.getCurrentUser().name || farmerName;
    }

    const welcomeData = {
      response: `**Welcome ${farmerName}! 🙏 I am Kisan Vani, your digital agricultural assistant.**\n\n` +
        `I can assist you with:\n` +
        `• 🌾 **MSP Floor Prices & Market Rates**\n` +
        `• 📅 **Official Procurement Schedules & Dates**\n` +
        `• 📍 **Nearby Procurement Centers & Queue Congestion**\n` +
        `• ⚡ **Digital Tokens & Weighbridge Slot Booking**\n` +
        `• 💳 **Direct Benefit Transfer (DBT) & Grievance Redressal**\n\n` +
        `*Click the microphone to speak, type your question, or choose an option below.*`,
      audio_text: `Welcome ${farmerName}! I am Kisan Vani. You can ask me about crop MSP rates, procurement schedules, nearby markets, and slot bookings.`,
      quick_actions: [
        { label: "🌾 MSP Floor Rates", url: "farmer/centers.html" },
        { label: "📍 Nearby Centers", url: "farmer/centers.html" },
        { label: "⚡ Book a Slot", url: "farmer/booking.html" }
      ],
      suggestions: [
        "What is the MSP rate for wheat?",
        "When does mustard procurement start?",
        "How congested is Karnal market?",
        "How do I book a token?",
        "When will DBT payment be credited?"
      ]
    };

    State.welcomeAudioText = welcomeData.audio_text;
    appendBotMessage(welcomeData, false);
  }

  function scrollToBottom() {
    setTimeout(() => {
      UI.chatBody.scrollTop = UI.chatBody.scrollHeight;
    }, 50);
  }

  // -------------------------------------------------------------
  // 6. QUERY EXECUTION (API + LOCAL ENGINE FALLBACK)
  // -------------------------------------------------------------
  async function submitQuery(queryText) {
    if (!queryText || !queryText.trim()) return;

    const cleanQuery = queryText.trim();
    appendUserMessage(cleanQuery);
    UI.textInput.value = '';

    const loadingEl = document.createElement('div');
    loadingEl.className = 'kv-msg kv-msg-bot kv-loading-indicator';
    loadingEl.innerHTML = `
      <div class="kv-bubble" style="color: #64748b; font-style: italic;">
        <span>🌾 Preparing response...</span>
      </div>
    `;
    UI.chatBody.appendChild(loadingEl);
    scrollToBottom();

    try {
      const res = await fetch('/api/v1/assistant/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: cleanQuery,
          language: 'en',
          user_id: window.KisanAuth?.getCurrentUser()?.id || null,
          current_page: window.location.pathname
        })
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      loadingEl.remove();
      appendBotMessage(data, State.isOpen);

    } catch (err) {
      console.warn("KisanVoiceAssistant: Backend query fallback triggered:", err.message);
      loadingEl.remove();
      const localResp = processLocalQuery(cleanQuery);
      appendBotMessage(localResp, State.isOpen);
    }
  }

  function processLocalQuery(q) {
    const qLower = q.toLowerCase();

    let matchedCropKey = null;
    if (qLower.includes('wheat') || qLower.includes('gehu')) matchedCropKey = 'wheat';
    else if (qLower.includes('mustard') || qLower.includes('sarson')) matchedCropKey = 'mustard';
    else if (qLower.includes('gram') || qLower.includes('chana') || qLower.includes('chickpea')) matchedCropKey = 'gram';
    else if (qLower.includes('barley')) matchedCropKey = 'barley';
    else if (qLower.includes('paddy') || qLower.includes('rice') || qLower.includes('dhan')) matchedCropKey = 'paddy';
    else if (qLower.includes('bajra') || qLower.includes('millet')) matchedCropKey = 'bajra';
    else if (qLower.includes('cotton') || qLower.includes('kapas')) matchedCropKey = 'cotton';

    // 1. Dates query
    if (qLower.includes('date') || qLower.includes('when') || qLower.includes('start') || qLower.includes('schedule') || qLower.includes('procurement')) {
      if (matchedCropKey && LOCAL_KNOWLEDGE[matchedCropKey]) {
        const k = LOCAL_KNOWLEDGE[matchedCropKey];
        return {
          response: `📅 **${k.crop} Procurement Schedule (${k.season})**:\n\n` +
            `• **Start Date:** **${k.start}**\n` +
            `• **End Date:** **${k.end}**\n` +
            `• **Minimum Support Price (MSP):** **${k.msp}**\n` +
            `• **Moisture Ceiling:** ${k.moisture}\n\n` +
            `💡 *Ensure you reserve a time slot on Farm Route before departing for the market.*`,
          audio_text: `Government procurement of ${k.crop} runs from ${k.start} to ${k.end}. The support price is ${k.msp}.`,
          quick_actions: [
            { label: "⚡ Book a Slot", url: `farmer/booking.html?crop=${matchedCropKey}` },
            { label: "📍 View Centers", url: "farmer/centers.html" }
          ],
          suggestions: ["What is the MSP for wheat?", "When does mustard procurement start?", "How do I get a token?"]
        };
      } else {
        return {
          response: `📅 **Government Procurement Schedule 2026**:\n\n` +
            `🌾 **Rabi Season:**\n` +
            `• Mustard: 15 March 2026 to 30 April 2026 (MSP: ₹5,650)\n` +
            `• Wheat: 1 April 2026 to 15 May 2026 (MSP: ₹2,275)\n` +
            `• Gram: 1 April 2026 to 15 May 2026 (MSP: ₹5,440)\n\n` +
            `🌾 **Kharif Season:**\n` +
            `• Paddy: 1 October 2026 to 15 November 2026 (MSP: ₹2,183)\n` +
            `• Bajra: 1 October 2026 to 15 November 2026 (MSP: ₹2,500)\n\n` +
            `🕒 Market Operational Hours: 09:00 AM to 05:00 PM (Monday - Saturday)`,
          audio_text: "Mustard procurement starts on 15 March, and wheat and gram begin on 1 April 2026. Paddy procurement starts on 1 October.",
          quick_actions: [
            { label: "⚡ Book a Token", url: "farmer/booking.html" },
            { label: "📍 View Centers", url: "farmer/centers.html" }
          ],
          suggestions: ["What is the price of wheat?", "How do I book a token?"]
        };
      }
    }

    // 2. Price query
    if (qLower.includes('price') || qLower.includes('msp') || qLower.includes('rate') || matchedCropKey) {
      if (matchedCropKey && LOCAL_KNOWLEDGE[matchedCropKey]) {
        const k = LOCAL_KNOWLEDGE[matchedCropKey];
        return {
          response: `🌾 **${k.crop} Official MSP & Rate Structure**:\n\n` +
            `• **Government MSP:** **${k.msp}**\n` +
            `• **Demo Market Rate:** ${k.demo}\n` +
            `• **Acceptable Moisture:** ${k.moisture}\n` +
            `• **Payment:** Direct bank transfer (DBT) within 48-72 hours.`,
          audio_text: `The government MSP rate for ${k.crop} is ${k.msp}.`,
          quick_actions: [
            { label: "⚡ Book a Slot", url: `farmer/booking.html?crop=${matchedCropKey}` }
          ],
          suggestions: ["When does procurement start?", "How many days for DBT payout?"]
        };
      }
    }

    // 3. Booking query
    if (qLower.includes('booking') || qLower.includes('book') || qLower.includes('token') || qLower.includes('slot')) {
      return {
        response: `⚡ **Easy Steps to Book a Market Token**:\n\n` +
          `1. Go to 'Find Procurement Center' and select your market.\n` +
          `2. Choose your crop and enter estimated quantity in quintals.\n` +
          `3. Pick a convenient date and time slot (e.g. 09:00 AM).\n` +
          `4. Enter your vehicle number and confirm to receive your digital pass!`,
        audio_text: "To book a token, select your procurement center, choose crop and arrival slot, and receive an instant digital token pass.",
        quick_actions: [
          { label: "⚡ Book Slot Now", url: "farmer/booking.html" },
          { label: "🎫 My Digital Pass", url: "farmer/token.html" }
        ],
        suggestions: ["What is the price of wheat?", "How do I track live queue?"]
      };
    }

    // 4. Fertilizer / Nutrition advisory
    if (qLower.includes('urea') || qLower.includes('fertilizer') || qLower.includes('dap') || qLower.includes('nutrient') || qLower.includes('zinc')) {
      return {
        response: `🌿 **Scientific Fertilizer & Nutrition Management**:\n\n` +
          `• **DAP:** Apply 50 to 55 kg per acre as a basal dose at sowing time.\n` +
          `• **Urea in Three Splits:** Total 45 kg/acre (50% basal, 25% at first irrigation at 21 days, 25% at tillering).\n` +
          `• **Zinc Sulphate:** 10 kg per acre (21% Zinc). Never mix directly with DAP.\n` +
          `• **Soil Test Benefits:** Applying fertilizers per soil card recommendations qualifies you for **Grade A Procurement Bonus**.`,
        audio_text: "For wheat and rabi crops, apply 50 kg DAP at sowing and 45 kg Urea split across first and second irrigation.",
        quick_actions: [
          { label: "🧪 Soil Health Card", url: "farmer/soil-testing.html" }
        ],
        suggestions: ["When should Urea be applied?", "What are the rules for soil testing?"]
      };
    }

    // 5. Soil testing & 48-hour SLA
    if (qLower.includes('soil') || qLower.includes('test') || qLower.includes('sla') || qLower.includes('health card')) {
      return {
        response: `🧪 **Soil Health Testing & 48-Hour Service Guarantee (SLA)**:\n\n` +
          `• **48-Hour SLA Guarantee:** Within 48 working hours of application, the laboratory field team collects samples and issues your digital card.\n` +
          `• **Tested Parameters:** Nitrogen (N), Phosphorus (P), Potassium (K), pH, Organic Carbon (OC%), and Electrical Conductivity (EC).\n` +
          `• **Compliance Certification:** Farmers adhering to soil advice receive a 'Certified Compliance Badge' and MSP bonus.`,
        audio_text: "Under the 48-hour SLA guarantee, the laboratory team collects soil samples and issues your digital health card within 48 working hours.",
        quick_actions: [
          { label: "🧪 Apply for Soil Test", url: "farmer/soil-testing.html" }
        ],
        suggestions: ["How much DAP should I use?", "How do I book a token?"]
      };
    }

    // 6. Weather query
    if (qLower.includes('weather') || qLower.includes('rain') || qLower.includes('temp') || qLower.includes('forecast')) {
      const w = window.KisanAgriService?.weatherCache;
      if (w) {
        return {
          response: `🌤️ **Live Agro-Weather (${w.location}, ${w.region})**:\n\n` +
            `• **Temperature:** ${w.tempC}°C (Feels like: ${w.feelsLikeC}°C)\n` +
            `• **Humidity:** ${w.humidity}% • **Wind:** ${w.windKph} km/h (${w.windDir})\n` +
            `• **Condition:** ${w.conditionText}\n` +
            `• **Agro Advisory:** ${w.agroAdvice?.desc || 'Weather is favorable for agricultural operations.'}`,
          audio_text: `Current temperature is ${w.tempC} degrees with ${w.conditionText}. ${w.agroAdvice?.desc || ''}`,
          quick_actions: [
            { label: "🌾 View Dashboard", url: "farmer/dashboard.html" }
          ],
          suggestions: ["Will it rain today?", "What are current crop prices?"]
        };
      }
    }

    // Default Fallback
    return {
      response: `🌾 **Kisan Vani Market Assistance**:\n\n` +
        `• **Crop MSP Rates:** Wheat ₹2,275/Q, Mustard ₹5,650/Q, Gram ₹5,440/Q, Paddy ₹2,183/Q.\n` +
        `• **Procurement Schedules:** Mustard from 15 March, Wheat from 1 April 2026.\n` +
        `• **Slot Booking:** Book a digital pass to avoid waiting in long queues at the market.`,
      audio_text: "You can ask about crop MSP prices, procurement schedules, and slot bookings.",
      quick_actions: [
        { label: "🌾 Crop MSP Prices", url: "farmer/centers.html" },
        { label: "⚡ Book a Token", url: "farmer/booking.html" }
      ],
      suggestions: ["What is the price of wheat?", "When does mustard procurement start?", "How do I book a token?"]
    };
  }

  // -------------------------------------------------------------
  // 7. EVENT BINDINGS & CONTROLS
  // -------------------------------------------------------------
  function openPopup() {
    if (State.isOpen) return;
    State.isOpen = true;
    State.isMinimized = false;
    UI.popup.classList.add('kv-open');
    UI.popup.classList.remove('kv-minimized');
    if (UI.minimizeBtn) {
      UI.minimizeBtn.textContent = '➖';
      UI.minimizeBtn.title = 'Minimize';
    }
    setTimeout(() => {
      if (UI.textInput) UI.textInput.focus();
    }, 250);
  }

  function closePopup() {
    if (!State.isOpen) return;
    State.isOpen = false;
    State.isMinimized = false;
    UI.popup.classList.remove('kv-open');
    UI.popup.classList.remove('kv-minimized');
    stopSpeaking();
    stopListening();
  }

  function togglePopup() {
    if (State.isOpen) {
      closePopup();
    } else {
      openPopup();
    }
  }

  function toggleMinimize() {
    State.isMinimized = !State.isMinimized;
    if (State.isMinimized) {
      UI.popup.classList.add('kv-minimized');
      UI.minimizeBtn.textContent = '🗖';
      UI.minimizeBtn.title = 'Expand';
    } else {
      UI.popup.classList.remove('kv-minimized');
      UI.minimizeBtn.textContent = '➖';
      UI.minimizeBtn.title = 'Minimize';
      scrollToBottom();
    }
  }

  function bindEvents() {
    UI.launcher.addEventListener('click', togglePopup);
    UI.closeBtn.addEventListener('click', closePopup);
    UI.minimizeBtn.addEventListener('click', toggleMinimize);

    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && State.isOpen) {
        closePopup();
      }
    });

    document.addEventListener('pointerdown', (e) => {
      if (!State.isOpen) return;
      const isInsidePopup = UI.popup && UI.popup.contains(e.target);
      const isInsideLauncher = UI.launcher && UI.launcher.contains(e.target);
      const isHeaderOpenBtn = e.target.closest && e.target.closest('button[onclick*="KisanVoiceAssistant"]');
      if (!isInsidePopup && !isInsideLauncher && !isHeaderOpenBtn) {
        closePopup();
      }
    });

    UI.ttsToggleBtn.addEventListener('click', () => {
      State.ttsEnabled = !State.ttsEnabled;
      if (State.ttsEnabled) {
        UI.ttsToggleBtn.textContent = '🔊';
        UI.ttsToggleBtn.classList.remove('kv-active');
        UI.ttsToggleBtn.title = 'Voice Audio ON';
      } else {
        stopSpeaking();
        UI.ttsToggleBtn.textContent = '🔇';
        UI.ttsToggleBtn.classList.add('kv-active');
        UI.ttsToggleBtn.title = 'Voice Audio Muted';
      }
    });

    UI.resetBtn.addEventListener('click', () => {
      stopListening();
      stopSpeaking();
      UI.chatBody.innerHTML = '';
      State.hasSpokenWelcome = false;
      showWelcomeMessage();
    });

    UI.micBtn.addEventListener('click', () => {
      if (State.isListening) {
        stopListening();
      } else {
        startListening();
      }
    });

    UI.statusCancelBtn.addEventListener('click', () => {
      stopListening();
      stopSpeaking();
    });

    UI.sendBtn.addEventListener('click', () => {
      submitQuery(UI.textInput.value);
    });

    UI.textInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        submitQuery(UI.textInput.value);
      }
    });

    UI.popup.querySelector('#kv-header').addEventListener('click', (e) => {
      if (State.isMinimized && !e.target.closest('.kv-icon-btn')) {
        toggleMinimize();
      }
    });
  }

  // -------------------------------------------------------------
  // 8. AUDIO CHIME & GATE PA ANNOUNCER
  // -------------------------------------------------------------
  function playAudioChime() {
    try {
      const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(587.33, audioCtx.currentTime); // D5
      osc.frequency.setValueAtTime(880, audioCtx.currentTime + 0.15); // A5
      gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.85);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + 0.85);
    } catch (e) {
      console.warn("Chime audio error:", e);
    }
  }

  function announceTokenPA(tokenNumber, gateNumber = 2, farmerName = '') {
    playAudioChime();
    setTimeout(() => {
      const enText = `Attention please. Token number ${tokenNumber}. Please proceed to Gate number ${gateNumber}.`;
      speakText(enText);
    }, 450);

    if (window.KisanEventBus && typeof window.KisanEventBus.publish === 'function') {
      window.KisanEventBus.publish('GATE_CALLOUT', {
        tokenNumber,
        gateNumber,
        farmerName,
        timestamp: new Date().toISOString()
      });
    }
  }

  // -------------------------------------------------------------
  // 9. PUBLIC API & DOMCONTENTLOADED INITIALIZATION
  // -------------------------------------------------------------
  const KisanVoiceAssistant = {
    open: () => openPopup(),
    close: () => closePopup(),
    toggle: () => togglePopup(),
    ask: (question) => {
      openPopup();
      submitQuery(question);
    },
    speak: (text) => speakText(text),
    stop: () => {
      stopListening();
      stopSpeaking();
    },
    playChime: () => playAudioChime(),
    announceToken: (tokenNumber, gateNumber, farmerName) => announceTokenPA(tokenNumber, gateNumber, farmerName),
    callNextToken: (tokenNumber, gateNumber, farmerName) => announceTokenPA(tokenNumber, gateNumber, farmerName)
  };

  window.KisanVoiceAssistant = KisanVoiceAssistant;

  // Auto-mount on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createWidgetDOM);
  } else {
    createWidgetDOM();
  }

})();
