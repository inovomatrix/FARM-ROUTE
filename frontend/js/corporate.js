/* ==========================================================================
   HARVEST HUB (हार्वेस्ट हब) - CORPORATE JAVASCRIPT CONTROLLER & I18N ENGINE
   Smart India Hackathon 2026 • Problem Statement #26032
   Bilingual Localization, MSP Calculator, Queue Simulator, and Micro-interactions
   ========================================================================== */

(function () {
  'use strict';

  // 1. Bilingual Translation Dictionary (Hindi & English)
  const I18N_TRANSLATIONS = {
    hi: {
      // Top Bar & Branding
      gov_title: 'हरियाणा सरकार | कृषि एवं किसान कल्याण विभाग (जिला रोहतक)',
      sih_badge: 'SIH 2026 • PS #26032 • रोहतक कृषि नवाचार',
      reset_demo: '🔄 डेटा सिंक करें',
      lang_switch: '🌐 English',
      live_ticker: 'लाइव मंडी भाव',
      logout: '🚪 लॉगआउट',

      // Brand & Logo
      corp_brand_title: 'Harvest <span>Hub</span>',
      corp_brand_badge: 'SIH 2026 • PS #26032 • APMC रोहतक',
      footer_brand: 'Harvest Hub',
      footer_copyright: '© 2026 <strong>Harvest Hub</strong> • Smart India Hackathon 2026. सर्वाधिकार सुरक्षित।',

      // Corporate Navigation
      nav_overview: 'अवलोकन',
      nav_ecosystem: '5 पोर्टल',
      nav_workflow: 'कार्यप्रणाली',
      nav_calculator: 'एमएसपी कैलकुलेटर',
      nav_queue: 'स्मार्ट कतार',
      nav_impact: 'प्रभाव',
      nav_team: 'टीम',
      nav_faq: 'प्रश्नोत्तरी',
      nav_launch_app: '🚀 पोर्टल खोलें',

      // Corporate Hero
      corp_hero_badge: 'Smart India Hackathon 2026 • Problem Statement #26032',
      corp_hero_title_1: 'वैज्ञानिक मृदा परामर्श, पारदर्शी फसल खरीद एवं',
      corp_hero_title_highlight: 'स्मार्ट मंडी कतार प्रणाली',
      corp_hero_sub: 'बुवाई पूर्व <strong>48 घंटे में गारंटीकृत वैज्ञानिक खाद परामर्श</strong>, बिना किसी प्रयोगशाला विलंब के सीधे <strong>Base MSP + मृदा अनुपालन बोनस</strong>, लाइव <strong>डिजिटल मंडी गेट टोकन</strong>, एवं <strong>शत-प्रतिशत प्रत्यक्ष DBT बैंक भुगतान</strong>।',
      corp_hero_cta_portals: '🌾 लाइव 5 पोर्टल में प्रवेश करें',
      corp_hero_cta_calc: '🧮 सरकारी दर व बोनस कैलकुलेटर',
      corp_partners_label: 'संबद्ध संस्थान व पायलट:',

      // Corporate Stats
      stat_sla_title: 'गारंटीकृत SLA एडवाइजरी',
      stat_sla_desc: 'मृदा परीक्षण उपरांत 48 कार्य घंटों में सटीक खाद व बीज पर्चा',
      stat_wait_title: 'मंडी गेट वेटिंग टाइम',
      stat_wait_desc: '24 से 48 घंटे की कतारों से मुक्ति, डिजिटल स्लॉट व वॉइस PA कॉल',
      stat_bonus_title: 'मृदा अनुपालन बोनस प्रति क्विंटल',
      stat_bonus_desc: 'वैज्ञानिक सलाह मानने वाले किसानों को न्यूनतम समर्थन मूल्य पर सीधा प्रीमियम',
      stat_dbt_title: 'पारदर्शी DBT बैंक भुगतान',
      stat_dbt_desc: 'धर्मकांटा पर्ची से सीधे बैंक खाते में UTR आधारित ऑडिटेड अंतरण',

      // Corporate Team Header
      team_section_tag: 'नवाचार टीम • SIH 2026',
      team_section_title: 'हार्वेस्ट हब के निर्माणकर्ता एवं विशेषज्ञ',
      team_section_sub: 'Smart India Hackathon 2026 के अंतर्गत भारतीय किसानों के सशक्तिकरण हेतु समर्पित बहुविषयक टीम।',

      // Team Members
      team_member_1_name: 'चिराग',
      team_member_1_role: 'टीम लीडर व क्लाउड सिस्टम्स इंजीनियर',
      team_member_1_bio: 'टीम नेतृत्व, उच्च-समवर्ती एपीआई एंडपॉइंट्स, फायरबेस/क्लाउड डेटाबेस स्केलिंग, डेटा ऑथेंटिकेशन और ऑटोमेटेड परीक्षण पाइपलाइन।',
      team_member_1_skill1: 'टीम लीडरशिप',
      team_member_1_skill2: 'क्लाउड बैकएंड',
      team_member_1_skill3: 'REST APIs व सुरक्षा',

      team_member_2_name: 'शिवम गोयल',
      team_member_2_role: 'फुल-स्टैक सिस्टम्स आर्किटेक्ट',
      team_member_2_bio: 'कोर 5-पोर्टल वास्तुकला, रियल-टाइम स्टेट सिंक्रनाइज़ेशन, e-NAM एपीआई एकीकरण व स्केलेबल वेब इन्फ्रास्ट्रक्चर डिज़ाइन।',
      team_member_2_skill1: 'सिस्टम आर्किटेक्चर',
      team_member_2_skill2: 'फुल-स्टैक वेब',
      team_member_2_skill3: 'e-NAM एकीकरण',

      team_member_3_name: 'अमीना',
      team_member_3_role: 'मृदा विज्ञान व AI एल्गोरिदम लीड',
      team_member_3_bio: 'NPK व सूक्ष्म पोषक तत्व अनुकूलन मॉडल, 48-घंटे की वैज्ञानिक परामर्श प्रणाली एवं मृदा स्वास्थ्य कार्ड अनुपालन सत्यापन।',
      team_member_3_skill1: 'मृदा स्वास्थ्य कार्ड',
      team_member_3_skill2: '48h परामर्श इंजन',
      team_member_3_skill3: 'NPK विश्लेषण',

      team_member_4_name: 'मनोती',
      team_member_4_role: 'UI/UX व प्रोडक्ट डिज़ाइन स्पेशलिस्ट',
      team_member_4_bio: 'बहुभाषी किसान-अनुकूल इंटरफ़ेस, आधुनिक डैशबोर्ड सौंदर्यशास्त्र, सुगमता अनुपालन एवं सहज मोबाइल लेआउट।',
      team_member_4_skill1: 'UI/UX डिज़ाइन',
      team_member_4_skill2: 'किसान सुगमता',
      team_member_4_skill3: 'डिज़ाइन सिस्टम',

      team_member_5_name: 'सुमित',
      team_member_5_role: 'स्मार्ट मंडी लॉजिस्टिक्स व टोकन समन्वयक',
      team_member_5_bio: 'डिजिटल गेट पास एल्गोरिदम, इलेक्ट्रॉनिक धर्मकांटा तुलाई स्वचालन, रोहतक APMC यार्ड वाहन नियंत्रण।',
      team_member_5_skill1: 'मंडी कतार प्रणाली',
      team_member_5_skill2: 'धर्मकांटा तुलाई',
      team_member_5_skill3: 'यार्ड लॉजिस्टिक्स',

      team_member_6_name: 'साहिल',
      team_member_6_role: 'फिनटेक डीबीटी एवं गुणवत्ता आश्वासन लीड',
      team_member_6_bio: 'मूल समर्थन मूल्य + मृदा अनुपालन बोनस गणना इंजन, UTR-आधारित प्रत्यक्ष बैंक अंतरण (DBT) सत्यापन एवं परीक्षण।',
      team_member_6_skill1: 'फिनटेक DBT स्वचालन',
      team_member_6_skill2: 'MSP बोनस कैलकुलेटर',
      team_member_6_skill3: 'गुणवत्ता आश्वासन (QA)'
    },

    en: {
      // Top Bar & Branding
      gov_title: 'Govt. of Haryana | Department of Agriculture & Farmers Welfare (Rohtak District)',
      sih_badge: 'SIH 2026 • PS #26032 • Rohtak Agri Innovation',
      reset_demo: '🔄 Sync Data',
      lang_switch: '🌐 Hindi',
      live_ticker: 'LIVE MANDI TICKER',
      logout: '🚪 Logout',

      // Brand & Logo
      corp_brand_title: 'Harvest <span>Hub</span>',
      corp_brand_badge: 'SIH 2026 • PS #26032 • APMC Rohtak',
      footer_brand: 'Harvest Hub',
      footer_copyright: '© 2026 <strong>Harvest Hub</strong> • Smart India Hackathon 2026. All rights reserved.',

      // Corporate Navigation
      nav_overview: 'Overview',
      nav_ecosystem: '5 Portals',
      nav_workflow: 'Process',
      nav_calculator: 'MSP Calculator',
      nav_queue: 'Smart Queue',
      nav_impact: 'Impact',
      nav_team: 'Team',
      nav_faq: 'FAQ',
      nav_launch_app: '🚀 Launch Portals',

      // Corporate Hero
      corp_hero_badge: 'Smart India Hackathon 2026 • Problem Statement #26032',
      corp_hero_title_1: 'Pre-Sowing Soil Intelligence, Direct Crop Procurement &',
      corp_hero_title_highlight: 'Smart Mandi Queue Ecosystem',
      corp_hero_sub: 'Pre-sowing <strong>48-Hour SLA scientific fertilizer advisories</strong>, direct <strong>Base MSP + Soil Compliance Bonus</strong> with zero laboratory friction, live <strong>e-Mandi gate tokens</strong>, and <strong>100% direct DBT bank settlements</strong>.',
      corp_hero_cta_portals: '🌾 Launch 5-Portal Platform',
      corp_hero_cta_calc: '🧮 Procurement & Bonus Calculator',
      corp_partners_label: 'Affiliated Bodies & Pilot Mandis:',

      // Corporate Stats
      stat_sla_title: 'Guaranteed Advisory SLA',
      stat_sla_desc: 'Precise fertilizer & seed prescription delivered within 48 working hours',
      stat_wait_title: 'Mandi Gate Waiting Time',
      stat_wait_desc: 'Drop from 24-48 hrs to <90 mins via digital tokens & voice calling',
      stat_bonus_title: 'Soil Compliance Bonus per Quintal',
      stat_bonus_desc: 'Direct cash premium added over Base MSP for adhering to soil advisories',
      stat_dbt_title: 'Direct DBT Bank Settlement',
      stat_dbt_desc: 'Automated electronic weighment slip to UTR verified bank transfer',

      // Corporate Team Header
      team_section_tag: 'Innovation Team • SIH 2026',
      team_section_title: 'Builders & Specialists Behind Harvest Hub',
      team_section_sub: 'A multidisciplinary team dedicated to transforming Indian agricultural procurement for Smart India Hackathon 2026.',

      // Team Members
      team_member_1_name: 'Chirag',
      team_member_1_role: 'Team Leader & Cloud Systems Engineer',
      team_member_1_bio: 'Team leadership, high-concurrency API endpoints, cloud database scaling, cryptographic data validation, and automated test pipelines.',
      team_member_1_skill1: 'Team Leadership',
      team_member_1_skill2: 'Cloud Backend',
      team_member_1_skill3: 'REST APIs & Security',

      team_member_2_name: 'Shivam Goyal',
      team_member_2_role: 'Full-Stack Systems Architect',
      team_member_2_bio: 'Core 5-portal architecture, real-time reactive state management, e-NAM API integration, and scalable web infrastructure.',
      team_member_2_skill1: 'System Architecture',
      team_member_2_skill2: 'Full-Stack Web',
      team_member_2_skill3: 'e-NAM Integration',

      team_member_3_name: 'Ameena',
      team_member_3_role: 'Agronomy & Soil Intelligence Lead',
      team_member_3_bio: 'NPK and micronutrient optimization algorithms, 48-hour scientific SLA advisory engine, and Soil Health Card compliance analytics.',
      team_member_3_skill1: 'Soil Health Card',
      team_member_3_skill2: '48h SLA Engine',
      team_member_3_skill3: 'NPK Analytics',

      team_member_4_name: 'Manoti',
      team_member_4_role: 'Lead UI/UX & Product Design Specialist',
      team_member_4_bio: 'Multilingual farmer-first interfaces, glassmorphic GovTech dashboard aesthetics, accessibility compliance, and ergonomic flows.',
      team_member_4_skill1: 'UI/UX Design Systems',
      team_member_4_skill2: 'Farmer Accessibility',
      team_member_4_skill3: 'Glassmorphism Tokens',

      team_member_5_name: 'Sumit',
      team_member_5_role: 'Smart Mandi Logistics Coordinator',
      team_member_5_bio: 'Digital gate token algorithms, E-Weighbridge gross-to-tare automation, and Rohtak APMC yard vehicle congestion optimization.',
      team_member_5_skill1: 'Mandi Queue Algorithms',
      team_member_5_skill2: 'E-Weighbridge Flow',
      team_member_5_skill3: 'Yard Logistics',

      team_member_6_name: 'Sahil',
      team_member_6_role: 'FinTech DBT & Quality Assurance Lead',
      team_member_6_bio: 'Base MSP + soil compliance bonus calculation engine, UTR-based Direct Benefit Transfer (DBT) verification, and system QA.',
      team_member_6_skill1: 'FinTech DBT Automation',
      team_member_6_skill2: 'MSP Bonus Calculator',
      team_member_6_skill3: 'Quality Assurance (QA)'
    }
  };

  // 2. Localization Class
  class I18nManager {
    constructor() {
      const saved = localStorage.getItem('HARVEST_HUB_LANG_v2');
      this.currentLang = (saved === 'hi') ? 'hi' : 'en';
      localStorage.setItem('HARVEST_HUB_LANG_v2', this.currentLang);
      localStorage.setItem('HARVEST_HUB_LANG', this.currentLang);
    }

    get lang() {
      return this.currentLang;
    }

    setLanguage(lang) {
      if (lang === 'hi' || lang === 'en') {
        this.currentLang = lang;
        localStorage.setItem('HARVEST_HUB_LANG_v2', lang);
        localStorage.setItem('HARVEST_HUB_LANG', lang);
        localStorage.setItem('KISAN_SETU_LANG', lang);
        document.documentElement.lang = lang;
        this.translatePage();
      }
    }

    toggleLanguage() {
      const nextLang = this.currentLang === 'hi' ? 'en' : 'hi';
      this.setLanguage(nextLang);
      return nextLang;
    }

    translatePage() {
      const isHi = this.currentLang === 'hi';
      const t = I18N_TRANSLATIONS[this.currentLang] || I18N_TRANSLATIONS.hi;

      // Update all elements with data-i18n attribute
      document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (t[key]) {
          if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
            el.placeholder = t[key];
          } else {
            el.innerHTML = t[key];
          }
        }
      });

      // Update language toggle button label: strictly show '🌐 Hindi' in English mode, and '🌐 English' in Hindi mode
      const langBtnText = document.getElementById('corpLangText');
      if (langBtnText) {
        langBtnText.textContent = isHi ? '🌐 English' : '🌐 Hindi';
      }

      // Update document title dynamically
      document.title = isHi
        ? 'हार्वेस्ट हब - डिजिटल फसल खरीद एवं स्मार्ट मंडी तंत्र | SIH 2026'
        : 'Harvest Hub - Next-Gen Digital Crop Procurement & Smart Mandi Ecosystem | SIH 2026';

      // Dispatch custom event for dynamic components
      window.dispatchEvent(new CustomEvent('kisan-lang-changed', { detail: { lang: this.currentLang } }));
    }
  }

  window.kisanI18n = new I18nManager();

  // Crop MSP and Soil Compliance Bonus Configuration
  const CROP_RATES = {
    wheat: { nameEn: 'Wheat (WH-1105)', nameHi: 'गेहूँ (Wheat WH-1105)', baseMsp: 2275, bonus: 115 },
    mustard: { nameEn: 'Mustard / Rapeseed (RH-725)', nameHi: 'सरसों / राई (Mustard RH-725)', baseMsp: 5650, bonus: 100 },
    paddy: { nameEn: 'Paddy / Basmati (PB-1121)', nameHi: 'धान / बासमती (Paddy PB-1121)', baseMsp: 2300, bonus: 90 },
    gram: { nameEn: 'Gram / Chickpea (HC-5)', nameHi: 'चना / छोले (Gram HC-5)', baseMsp: 5440, bonus: 80 },
    millet: { nameEn: 'Pearl Millet / Bajra (HHB-67)', nameHi: 'बाजरा (Pearl Millet HHB-67)', baseMsp: 2625, bonus: 75 }
  };

  // 3. Calculator Logic
  function updateCalculator() {
    const cropSelect = document.getElementById('calcCrop');
    const qtyInput = document.getElementById('calcQty');
    const compCheckbox = document.getElementById('calcCompliance');

    if (!cropSelect || !qtyInput || !compCheckbox) return;

    const cropKey = cropSelect.value || 'wheat';
    const qty = parseFloat(qtyInput.value) || 0;
    const isCompliant = compCheckbox.checked;

    const cropData = CROP_RATES[cropKey] || CROP_RATES.wheat;
    const baseMsp = cropData.baseMsp;
    const bonusPerQ = isCompliant ? cropData.bonus : 0;
    const effectiveRate = baseMsp + bonusPerQ;

    const totalBasePayout = qty * baseMsp;
    const totalBonusPayout = qty * bonusPerQ;
    const grandTotalPayout = totalBasePayout + totalBonusPayout;

    const totalEl = document.getElementById('calcGrandTotal');
    const baseRateEl = document.getElementById('calcBaseMsp');
    const bonusRateEl = document.getElementById('calcBonusRate');
    const effRateEl = document.getElementById('calcEffectiveRate');
    const totalQtyEl = document.getElementById('calcDisplayQty');

    const isEn = window.kisanI18n && window.kisanI18n.lang === 'en';
    if (totalEl) totalEl.textContent = '₹' + grandTotalPayout.toLocaleString('en-IN');
    if (baseRateEl) baseRateEl.textContent = '₹' + baseMsp.toLocaleString('en-IN') + '/Q';
    if (bonusRateEl) {
      const notAppText = isEn ? '₹0 (Not Applicable)' : '₹0 (लागू नहीं)';
      bonusRateEl.textContent = isCompliant ? '+₹' + bonusPerQ + (isEn ? '/Q (Bonus Applied)' : '/Q (लागू)') : notAppText;
      bonusRateEl.style.color = isCompliant ? '#15803d' : '#94a3b8';
    }
    if (effRateEl) effRateEl.textContent = '₹' + effectiveRate.toLocaleString('en-IN') + '/Q';
    if (totalQtyEl) totalQtyEl.textContent = qty + (isEn ? ' Quintals' : ' क्विंटल');
  }

  // 4. Live Queue Simulator
  function getInitialSimulatedTokens(isHi) {
    return [
      { num: 8294, vehicle: 'HR-12-BZ-9481 (Tractor)', crop: isHi ? 'गेहूँ' : 'Wheat (WH-1105)', status: 'weighbridge_in', statusLabel: isHi ? 'धर्मकांटा तौल (Gross Wt)' : 'Weighbridge IN (Gross Wt)', calling: true },
      { num: 8293, vehicle: 'HR-12-AK-1029 (Tata 407)', crop: isHi ? 'सरसों' : 'Mustard (RH-725)', status: 'unloading', statusLabel: isHi ? 'गोदाम अनलोडिंग (Silo 2)' : 'Warehouse Unloading (Silo 2)', calling: false },
      { num: 8292, vehicle: 'HR-12-CX-4491 (Tractor)', crop: isHi ? 'धान' : 'Paddy (PB-1121)', status: 'gate_entry', statusLabel: isHi ? 'गेट प्रवेश (Gate Entry)' : 'Gate Entry (Verification)', calling: false },
      { num: 8291, vehicle: 'HR-12-DF-7812 (Canter)', crop: isHi ? 'गेहूँ' : 'Wheat (WH-1105)', status: 'waiting', statusLabel: isHi ? 'कतार में (Waiting)' : 'In Queue (Waiting)', calling: false }
    ];
  }
  let simulatedTokens = getInitialSimulatedTokens(false);

  function renderQueueSimulator() {
    const container = document.getElementById('queueSlotsContainer');
    if (!container) return;
    const isEn = window.kisanI18n && window.kisanI18n.lang === 'en';

    container.innerHTML = simulatedTokens.map(t => `
      <div class="corp-queue-tile ${t.calling ? 'calling' : ''}">
        <div class="corp-queue-tile-head">
          <span>${t.calling ? (isEn ? '📢 Active (Calling)' : '📢 सक्रिय (Calling)') : (isEn ? 'In Queue' : 'कतार में (Queue)')}</span>
          <span style="font-weight:700; color:${t.calling ? '#10b981' : '#64748b'};">${t.statusLabel}</span>
        </div>
        <div class="corp-queue-token-num">#${t.num}</div>
        <div class="corp-queue-vehicle">🚛 ${t.vehicle}</div>
        <div style="font-size:0.75rem; color:#64748b; margin-top:4px;">${isEn ? 'Crop:' : 'फसल:'} <strong>${t.crop}</strong></div>
      </div>
    `).join('');
  }

  function advanceQueueSimulator() {
    const nextNum = Math.floor(8295 + Math.random() * 50);
    const vehicles = ['HR-12-ER-3391 (Tractor)', 'HR-12-MN-4421 (Tata Ace)', 'HR-12-PQ-8812 (Tractor)', 'HR-12-ST-1945 (Pickup)'];
    const isEn = !window.kisanI18n || window.kisanI18n.lang === 'en';
    const crops = isEn ? ['Wheat (WH-1105)', 'Mustard (RH-725)', 'Paddy (PB-1121)'] : ['गेहूँ (Wheat)', 'सरसों (Mustard)', 'धान (Paddy)'];

    const newCallingToken = {
      num: nextNum,
      vehicle: vehicles[Math.floor(Math.random() * vehicles.length)],
      crop: crops[Math.floor(Math.random() * crops.length)],
      status: 'gate_entry',
      statusLabel: isEn ? 'Gate Entry (Now Calling)' : 'गेट प्रवेश (Now Calling)',
      calling: true
    };

    simulatedTokens = [newCallingToken, ...simulatedTokens.slice(0, 3)];
    renderQueueSimulator();

    // Trigger voice announcement if available
    if (window.KisanVoiceAssistant && typeof window.KisanVoiceAssistant.announceToken === 'function') {
      window.KisanVoiceAssistant.announceToken(nextNum, 1, isEn ? 'Rohtak Mandi Gate 1' : 'रोहतक मंडी गेट 1');
    }

    showCorpToast(isEn ? `📢 Token #${nextNum} called to Rohtak Mandi Gate 1!` : `📢 टोकन #${nextNum} को रोहतक मंडी गेट 1 पर आमंत्रित किया गया!`, 'success');
  }

  // 5. FAQ Accordion Toggle
  function setupFaqAccordions() {
    const items = document.querySelectorAll('.corp-faq-item');
    items.forEach(item => {
      const q = item.querySelector('.corp-faq-q');
      if (q) {
        q.addEventListener('click', () => {
          const isActive = item.classList.contains('active');
          items.forEach(i => i.classList.remove('active'));
          if (!isActive) item.classList.add('active');
        });
      }
    });
  }

  // 6. Toast Notification
  function showCorpToast(message, type) {
    let toast = document.getElementById('corpToast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'corpToast';
      toast.style.cssText = `
        position: fixed;
        bottom: 24px;
        left: 50%;
        transform: translateX(-50%);
        background: #0f172a;
        color: #ffffff;
        padding: 12px 24px;
        border-radius: 9999px;
        font-size: 0.9rem;
        font-weight: 700;
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        z-index: 9999;
        display: flex;
        align-items: center;
        gap: 10px;
        transition: opacity 0.3s ease;
      `;
      document.body.appendChild(toast);
    }
    toast.innerHTML = type === 'success' ? `✅ ${message}` : `ℹ️ ${message}`;
    toast.style.display = 'flex';
    toast.style.opacity = '1';

    setTimeout(() => {
      toast.style.opacity = '0';
      setTimeout(() => { toast.style.display = 'none'; }, 300);
    }, 3500);
  }

  // 7. Sticky Header Scroll Effect
  function setupHeaderScroll() {
    const header = document.querySelector('.corp-header');
    if (!header) return;
    window.addEventListener('scroll', () => {
      if (window.scrollY > 30) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    });
  }

  // 8. Mobile Drawer Toggle
  function setupMobileMenu() {
    const toggle = document.querySelector('.corp-menu-toggle');
    const navLinks = document.querySelector('.corp-nav-links');
    if (!toggle || !navLinks) return;

    toggle.addEventListener('click', () => {
      const isVisible = navLinks.style.display === 'flex';
      navLinks.style.display = isVisible ? 'none' : 'flex';
      if (!isVisible) {
        navLinks.style.flexDirection = 'column';
        navLinks.style.position = 'absolute';
        navLinks.style.top = '72px';
        navLinks.style.left = '0';
        navLinks.style.width = '100%';
        navLinks.style.background = '#ffffff';
        navLinks.style.padding = '20px';
        navLinks.style.boxShadow = '0 10px 25px rgba(0,0,0,0.1)';
        navLinks.style.borderBottom = '1px solid #e2e8f0';
      }
    });

    // Close menu when clicking nav link
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        if (window.innerWidth <= 768) {
          navLinks.style.display = 'none';
        }
      });
    });
  }

  // 9. Floating Voice Assistant Button handler
  function handleVoiceClick(e) {
    if (window.KisanVoiceAssistant && typeof window.KisanVoiceAssistant.open === 'function') {
      e.preventDefault();
      window.KisanVoiceAssistant.open();
    }
  }

  // Expose global methods
  window.corpWebsite = {
    updateCalculator,
    advanceQueueSimulator,
    showCorpToast,
    handleVoiceClick
  };

  // Initialize on DOMContentLoaded
  document.addEventListener('DOMContentLoaded', () => {
    // Initial translation check
    if (window.kisanI18n) {
      window.kisanI18n.translatePage();
    }

    updateCalculator();
    renderQueueSimulator();
    setupFaqAccordions();
    setupHeaderScroll();
    setupMobileMenu();

    // Re-render dynamic text on language change
    window.addEventListener('kisan-lang-changed', () => {
      updateCalculator();
      renderQueueSimulator();
    });

    // Attach calculator events
    const cropSelect = document.getElementById('calcCrop');
    const qtyInput = document.getElementById('calcQty');
    const compCheckbox = document.getElementById('calcCompliance');
    if (cropSelect) cropSelect.addEventListener('change', updateCalculator);
    if (qtyInput) qtyInput.addEventListener('input', updateCalculator);
    if (compCheckbox) compCheckbox.addEventListener('change', updateCalculator);

    // Voice assistant button
    const voiceBtn = document.querySelector('.corp-voice-float-btn');
    if (voiceBtn) {
      voiceBtn.addEventListener('click', handleVoiceClick);
    }
  });

})();
