/**
 * KisanSetu — UI Localization Engine (English Platform Standard)
 * Clean key-value dictionary routing supporting English.
 */

(function (window) {
  'use strict';

  const STORAGE_KEY = "kisan_setu_language";
  const COMPAT_KEY = "kisansetu_language";
  const EXPLICIT_FLAG = "kisan_lang_explicit_choice";

  const DICTIONARY = {
    // Brand & App
    "app.title": { en: "KisanSetu", hi: "KisanSetu" },
    "app.subtitle": { en: "Smart Agricultural Logistics & Procurement Platform", hi: "Smart Agricultural Logistics & Procurement Platform" },
    "app.tagline": { en: "Digital Mandi Platform", hi: "Digital Mandi Platform" },

    // Navigation Links
    "nav.home": { en: "Home", hi: "Home" },
    "nav.crops": { en: "Crops", hi: "Crops" },
    "nav.centers": { en: "Procurement Centers", hi: "Procurement Centers" },
    "nav.farmerPortal": { en: "Farmer Portal", hi: "Farmer Portal" },
    "nav.farmerPortalSub": { en: "Farmer Procurement & Queue Portal", hi: "Farmer Procurement & Queue Portal" },
    "nav.login": { en: "Login", hi: "Login" },
    "nav.register": { en: "Register", hi: "Register" },
    "nav.logout": { en: "Logout", hi: "Logout" },
    "nav.dashboard": { en: "Dashboard", hi: "Dashboard" },
    "nav.more": { en: "More", hi: "More" },
    "nav.journey": { en: "7-Step Process", hi: "7-Step Process" },
    "nav.compare": { en: "Comparison", hi: "Comparison" },
    "nav.faq": { en: "FAQ", hi: "FAQ" },
    "nav.about": { en: "Platform Details", hi: "Platform Details" },
    "nav.voiceAssistant": { en: "Kisan Vani AI", hi: "Kisan Vani AI" },
    "nav.soilTesting": { en: "Soil Health", hi: "Soil Health" },
    "nav.salesHistory": { en: "Sales History", hi: "Sales History" },
    "nav.myBookings": { en: "My Bookings", hi: "My Bookings" },
    "nav.booking": { en: "Slot Booking", hi: "Slot Booking" },
    "nav.token": { en: "Digital Pass", hi: "Digital Pass" },
    "nav.queue": { en: "Live Queue", hi: "Live Queue" },
    "nav.complaints": { en: "Complaints", hi: "Complaints" },
    "nav.activeSession": { en: "Active Session", hi: "Active Session" },
    "nav.commandCenter": { en: "Command Center", hi: "Command Center" },
    "nav.yardScreen": { en: "Live Yard Billboard", hi: "Live Yard Billboard" },
    "nav.adminOverview": { en: "Admin Overview", hi: "Admin Overview" },
    "nav.operatorQueue": { en: "Operator Queue", hi: "Operator Queue" },
    "nav.gateVerification": { en: "Gate Verification", hi: "Gate Verification" },
    "nav.procurementOps": { en: "Procurement Operations", hi: "Procurement Operations" },
    "nav.queueMgmt": { en: "Queue Management", hi: "Queue Management" },
    "nav.districtConsole": { en: "District Oversight Console", hi: "District Oversight Console" },

    // Common UI Text
    "common.loading": { en: "Loading...", hi: "Loading..." },
    "common.active": { en: "Active", hi: "Active" },
    "common.liveMandiRates": { en: "Live Mandi Rates", hi: "Live Mandi Rates" },
    "common.agroWeather": { en: "Local Agro-Weather", hi: "Local Agro-Weather" },
    "common.search": { en: "Search", hi: "Search" },
    "common.filter": { en: "Filter", hi: "Filter" },
    "common.reset": { en: "Reset", hi: "Reset" },
    "common.submit": { en: "Submit", hi: "Submit" },
    "common.cancel": { en: "Cancel", hi: "Cancel" },
    "common.view": { en: "View", hi: "View" },
    "common.back": { en: "Back", hi: "Back" },
    "common.status": { en: "Status", hi: "Status" },
    "common.date": { en: "Date", hi: "Date" },
    "common.time": { en: "Time", hi: "Time" },
    "common.action": { en: "Action", hi: "Action" },
    "common.download": { en: "Download", hi: "Download" },
    "common.print": { en: "Print", hi: "Print" },
    "common.verified": { en: "Verified", hi: "Verified" },
    "common.pending": { en: "Pending", hi: "Pending" },
    "common.refresh": { en: "Refresh", hi: "Refresh" },
    "common.language": { en: "Language", hi: "Language" },
    "common.switchLang": { en: "Language: English", hi: "Language: English" },

    // Farmer Portal Features
    "farmer.greeting": { en: "Welcome, Farmer!", hi: "Welcome, Farmer!" },
    "farmer.welcomeSub": { en: "Track mandi arrivals, book weighbridge slots, and monitor live queue status.", hi: "Track mandi arrivals, book weighbridge slots, and monitor live queue status." },
    "farmer.quickActions": { en: "Quick Actions", hi: "Quick Actions" },
    "farmer.bookNewSlot": { en: "Book Delivery Slot", hi: "Book Delivery Slot" },
    "farmer.viewToken": { en: "View Digital Pass", hi: "View Digital Pass" },
    "farmer.activeBooking": { en: "Active Booking & Pass", hi: "Active Booking & Pass" },
    "farmer.noActiveBooking": { en: "No Active Booking", hi: "No Active Booking" },
    "farmer.noActiveBookingSub": { en: "You have no upcoming procurement slots or active tokens. Find a center to book a slot.", hi: "You have no upcoming procurement slots or active tokens. Find a center to book a slot." },
    "farmer.findCenters": { en: "Find Procurement Center", hi: "Find Procurement Center" },
    "farmer.salesSummary": { en: "Sales & Procurement Summary", hi: "Sales & Procurement Summary" },
    "farmer.totalCropSold": { en: "Total Crop Sold", hi: "Total Crop Sold" },
    "farmer.completedSales": { en: "Completed Transactions", hi: "Completed Transactions" },
    "farmer.totalPayment": { en: "Total Payment Released", hi: "Total Payment Released" },
    "farmer.helpline": { en: "Kisan Helpline & Support", hi: "Kisan Helpline & Support" },
    "farmer.tollFree": { en: "Toll-Free Helpline", hi: "Toll-Free Helpline" },
    "farmer.hours": { en: "7:00 AM – 7:00 PM (Monday to Saturday)", hi: "7:00 AM – 7:00 PM (Monday to Saturday)" },
    "farmer.profileDetails": { en: "Farmer Profile", hi: "Farmer Profile" },

    // Throughput & Slots
    "throughput.title": { en: "Dynamic Mandi Throughput Engine", hi: "Dynamic Mandi Throughput Engine" },
    "throughput.formula": { en: "Capacity Formula", hi: "Capacity Formula" },
    "throughput.weighbridges": { en: "Active Weighbridges", hi: "Active Weighbridges" },
    "throughput.rate": { en: "Hourly Weighing Rate", hi: "Hourly Weighing Rate" },
    "throughput.selectSlot": { en: "Select Time Slot", hi: "Select Time Slot" },
    "throughput.greenTier": { en: "Low Load (Fast-Track)", hi: "Low Load (Fast-Track)" },
    "throughput.amberTier": { en: "Moderate Load (Normal)", hi: "Moderate Load (Normal)" },
    "throughput.redTier": { en: "Heavy Congestion (Locked)", hi: "Heavy Congestion (Locked)" },
    "throughput.alternativeTitle": { en: "Nearby Low-Load Alternative Centers", hi: "Nearby Low-Load Alternative Centers" },
    "throughput.divertBtn": { en: "Book at This Mandi", hi: "Book at This Mandi" },

    // Gate Verification & Security
    "gate.title": { en: "Gate Verification Station", hi: "Gate Verification Station" },
    "gate.scanQR": { en: "Scan QR Token", hi: "Scan QR Token" },
    "gate.tokenNumber": { en: "Token Number", hi: "Token Number" },
    "gate.verify": { en: "Verify Entry", hi: "Verify Entry" },
    "gate.bufferValid": { en: "On-Time Arrival (Valid)", hi: "On-Time Arrival (Valid)" },
    "gate.bufferOverdue": { en: "Buffer Overdue (Standby Lane)", hi: "Buffer Overdue (Standby Lane)" },
    "gate.tamperAlert": { en: "SECURITY ALERT: Forged/Hoarded Pass!", hi: "SECURITY ALERT: Forged/Hoarded Pass!" },
    "gate.callTokenPA": { en: "Call Token (PA)", hi: "Call Token (PA)" },
    "gate.audioChime": { en: "Audio Chime", hi: "Audio Chime" },
    "gate.speakToken": { en: "Calling token over public address system...", hi: "Calling token over public address system..." },

    // State Machine Stages
    "stage.booked": { en: "Slot Booked", hi: "Slot Booked" },
    "stage.gateScanned": { en: "Gate Verified", hi: "Gate Verified" },
    "stage.assayTesting": { en: "Moisture & Assay Testing", hi: "Moisture & Assay Testing" },
    "stage.weighbridgeIn": { en: "Weighbridge Gross In", hi: "Weighbridge Gross In" },
    "stage.weighbridgeOut": { en: "Weighbridge Net Tare", hi: "Weighbridge Net Tare" },
    "stage.dbtDispatched": { en: "DBT Payment Dispatched", hi: "DBT Payment Dispatched" },

    // Superintendent & Command Center
    "supt.title": { en: "Mandi Superintendent Command Center", hi: "Mandi Superintendent Command Center" },
    "supt.controlRoom": { en: "CONTROL ROOM", hi: "CONTROL ROOM" },
    "supt.tonnageGauge": { en: "Real-Time Mandi Yard Tonnage Gauge", hi: "Real-Time Mandi Yard Tonnage Gauge" },
    "supt.realtimeIntake": { en: "Inbound Tonnage Saturation vs Mandi Threshold", hi: "Inbound Tonnage Saturation vs Mandi Threshold" },
    "supt.targetCap": { en: "Target Daily Intake Capacity", hi: "Target Daily Intake Capacity" },
    "supt.weighed": { en: "Weighed Inbound (Gate-In)", hi: "Weighed Inbound (Gate-In)" },
    "supt.enroute": { en: "En-Route / Scheduled Bookings", hi: "En-Route / Scheduled Bookings" },
    "supt.cumProgress": { en: "Cumulative Inbound Progress", hi: "Cumulative Inbound Progress" },
    "supt.emergencyBreaker": { en: "Emergency Circuit Breaker", hi: "Emergency Circuit Breaker" },
    "supt.breakerDesc": { 
      en: "Instantly halt incoming traffic and upcoming slots in case of sudden weather changes, machinery breakdown, or godown saturation.", 
      hi: "Instantly halt incoming traffic and upcoming slots in case of sudden weather changes, machinery breakdown, or godown saturation." 
    },
    "supt.reasonHalt": { en: "Reason for Halt", hi: "Reason for Halt" },
    "supt.deferDuration": { en: "Deferral Duration", hi: "Deferral Duration" },
    "supt.haltBtn": { en: "Halt Upcoming Slots & Send Mass SMS", hi: "Halt Upcoming Slots & Send Mass SMS" },
    "supt.resumeBtn": { en: "Resume Normal Yard Intake", hi: "Resume Normal Yard Intake" },
    "supt.stageLatency": { en: "End-to-End Turnaround Analytics", hi: "End-to-End Turnaround Analytics" },
    "supt.stageLatencyTitle": { en: "Stage Latency & Bottleneck Detector", hi: "Stage Latency & Bottleneck Detector" },
    "supt.liveIntake": { en: "Live Intake Stream", hi: "Live Intake Stream" },
    "supt.yardTelemetry": { en: "Mandi Yard Telemetry & Vehicle Pipeline", hi: "Mandi Yard Telemetry & Vehicle Pipeline" },
    "supt.refreshBtn": { en: "Refresh Telemetry", hi: "Refresh Telemetry" },

    // Table Headers
    "th.tokenBooking": { en: "Token & Booking", hi: "Token & Booking" },
    "th.farmerDetails": { en: "Farmer Details", hi: "Farmer Details" },
    "th.vehicleCrop": { en: "Vehicle & Crop", hi: "Vehicle & Crop" },
    "th.scheduledSlot": { en: "Scheduled Slot", hi: "Scheduled Slot" },
    "th.currentStage": { en: "Current Pipeline Stage", hi: "Current Pipeline Stage" },
    "th.allocatedBay": { en: "Allocated Bay / WB", hi: "Allocated Bay / WB" },
    "th.waitTime": { en: "Wait Time", hi: "Wait Time" },
    "th.action": { en: "Superintendent Action", hi: "Superintendent Action" }
  };

  // Language Resolution: Always "en" (English)
  function resolveInitialLanguage() {
    localStorage.setItem(STORAGE_KEY, "en");
    localStorage.setItem(COMPAT_KEY, "en");
    return "en";
  }

  let currentLang = "en";

  const KisanI18n = {
    getLanguage() {
      return "en";
    },

    setLanguage(lang) {
      currentLang = "en";
      localStorage.setItem(STORAGE_KEY, "en");
      localStorage.setItem(COMPAT_KEY, "en");
      document.documentElement.lang = "en";
      this.applyTranslations();
      this.updateSwitcherUI();

      // Broadcast event for dynamic components (telemetry, charts, Voice Assistant)
      window.dispatchEvent(new CustomEvent('kisan_language_changed', { detail: { lang: "en" } }));
    },

    toggleLanguage() {
      this.setLanguage("en");
    },

    t(key) {
      const entry = DICTIONARY[key];
      if (!entry) return key;
      return entry["en"] || key;
    },

    applyTranslations() {
      // 1. Elements with data-i18n dictionary keys
      document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.getAttribute("data-i18n");
        const translation = this.t(key);
        if (translation) {
          if (el.tagName === "INPUT" || el.tagName === "TEXTAREA") {
            el.placeholder = translation;
          } else {
            el.textContent = translation;
          }
        }
      });

      // 2. Direct bilingual inline attributes: data-i18n-en always wins
      document.querySelectorAll("[data-i18n-en]").forEach(el => {
        const text = el.getAttribute("data-i18n-en");
        if (text) {
          if (el.tagName === "INPUT" || el.tagName === "TEXTAREA") {
            el.placeholder = text;
          } else {
            el.textContent = text;
          }
        }
      });

      // 3. Document Title if meta tag provided
      const docTitleKey = document.querySelector("meta[name='i18n-title-key']");
      if (docTitleKey) {
        const t = this.t(docTitleKey.getAttribute("content"));
        if (t) document.title = `${t} | KisanSetu`;
      }
    },

    updateSwitcherUI() {
      // A. Update all segmented option switchers (.kisan-lang-switcher)
      document.querySelectorAll(".kisan-lang-switcher").forEach(container => {
        const enBtn = container.querySelector('[data-lang="en"]');
        const hiBtn = container.querySelector('[data-lang="hi"]');
        const isDark = container.closest('.bg-slate-900, .bg-slate-950, [data-theme="dark"]');

        if (enBtn) {
          enBtn.className = isDark
            ? "px-2.5 py-1 rounded-md text-xs font-bold bg-teal-600 text-white shadow-xs transition-all cursor-default"
            : "px-2.5 py-1 rounded-md text-xs font-bold bg-emerald-600 text-white shadow-xs transition-all cursor-default";
          enBtn.textContent = "EN";
        }
        if (hiBtn) {
          hiBtn.style.display = "none";
        }
      });

      // B. Update all single toggle buttons (.kisan-lang-btn)
      document.querySelectorAll(".kisan-lang-btn").forEach(btn => {
        const label = "English (EN)";
        const title = "Language: English";
        
        const labelSpan = btn.querySelector(".lang-text");
        if (labelSpan) {
          labelSpan.textContent = label;
        } else {
          btn.textContent = `🌐 ${label}`;
        }
        btn.setAttribute("title", title);
        btn.setAttribute("aria-label", `Current language: English.`);
      });

      // C. Update select dropdowns (.kisan-lang-select)
      document.querySelectorAll(".kisan-lang-select").forEach(sel => {
        sel.value = "en";
      });
    },

    renderLanguageSwitchButton() {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "kisan-lang-btn px-2.5 py-1.5 rounded-lg text-xs font-bold border border-slate-700 bg-slate-800 text-teal-300 transition-all shadow-xs flex items-center gap-1.5";
      btn.innerHTML = `<span>🌐</span><span class="lang-text">English (EN)</span>`;
      btn.title = "Language: English";
      btn.onclick = () => this.setLanguage("en");
      return btn;
    }
  };

  // Auto apply on DOM ready
  document.addEventListener("DOMContentLoaded", () => {
    document.documentElement.lang = "en";
    KisanI18n.applyTranslations();
    KisanI18n.updateSwitcherUI();
  });

  window.KisanI18n = KisanI18n;
})(window);
