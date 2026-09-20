import re

with open('frontend/portal.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. HTML Title & Metadata
content = content.replace(
    '<title>Harvest Hub (हार्वेस्ट हब) - Unified Digital Crop Procurement & Smart Mandi Platform | Govt. of Haryana</title>',
    '<title>Harvest Hub - Unified Digital Crop Procurement & Smart Mandi Platform | Govt. of Haryana</title>'
)
content = content.replace(
    '<strong style="color:white; font-size:0.95rem;">Harvest Hub (हार्वेस्ट हब)</strong>',
    '<strong style="color:white; font-size:0.95rem;">Harvest Hub</strong>'
)
content = content.replace(
    '<h4 style="font-size:1.05rem; font-weight:800;">Kisan Vani AI (किसान वाणी सहायक)</h4>',
    '<h4 style="font-size:1.05rem; font-weight:800;">Kisan Vani AI Assistant</h4>'
)
content = content.replace(
    'title="Click to Speak / माइक दबाकर बोलें"',
    'title="Click to Speak"'
)
content = content.replace(
    'title="Switch Language / भाषा बदलें"',
    'title="Switch Language"'
)
content = content.replace(
    'title="Sync with Cloud Database / डेटा सिंक करें"',
    'title="Sync with Cloud Database"'
)

# 2. I18nManager default language strictly English
old_i18n_mgr = '''class I18nManager {
  constructor() {
    this.currentLang = localStorage.getItem('HARVEST_HUB_LANG') || localStorage.getItem('KISAN_SETU_LANG') || 'en';
  }'''

new_i18n_mgr = '''class I18nManager {
  constructor() {
    const saved = localStorage.getItem('HARVEST_HUB_LANG_v2');
    this.currentLang = (saved === 'hi') ? 'hi' : 'en';
    localStorage.setItem('HARVEST_HUB_LANG_v2', this.currentLang);
    localStorage.setItem('HARVEST_HUB_LANG', this.currentLang);
  }'''

if old_i18n_mgr in content:
    content = content.replace(old_i18n_mgr, new_i18n_mgr, 1)

# Ensure setLanguage updates v2 key
old_set_lang = '''  setLanguage(lang) {
    if (lang === 'hi' || lang === 'en') {
      this.currentLang = lang;
      localStorage.setItem('HARVEST_HUB_LANG', lang);
      localStorage.setItem('KISAN_SETU_LANG', lang);
      document.documentElement.lang = lang;
      this.translatePage();
    }
  }'''

new_set_lang = '''  setLanguage(lang) {
    if (lang === 'hi' || lang === 'en') {
      this.currentLang = lang;
      localStorage.setItem('HARVEST_HUB_LANG_v2', lang);
      localStorage.setItem('HARVEST_HUB_LANG', lang);
      localStorage.setItem('KISAN_SETU_LANG', lang);
      document.documentElement.lang = lang;
      this.translatePage();
    }
  }'''

if old_set_lang in content:
    content = content.replace(old_set_lang, new_set_lang, 1)

# 3. Clean DEFAULT_USERS names
old_users = '''const DEFAULT_USERS = [
  {
    id: 'FARM-ROH-101',
    name: 'Rameshwar Hooda (रामेश्वर हुड्डा)',
    role: 'farmer',
    mobile: '9876543210',
    email: 'farmer@demo.com',
    demoEmail: 'farmer@demo.com',
    password: '1234567890',
    aadhaar: 'XXXX-XXXX-7142',
    state: 'Haryana',
    district: 'Rohtak',
    tehsil: 'Rohtak',
    village: 'Bohar (बोहर)',
    totalOwnedLandAcres: 5.0,
    primaryKhasraNo: '142//5, 142//6',
    primaryBankAccount: null
  },
  {
    id: 'OFF-ROH-001',
    name: 'Smt. Anjali Sharma (श्रीमती अंजलि शर्मा)',
    role: 'officer',
    mobile: '9876500001',
    email: 'officer@demo.com',
    demoEmail: 'officer@demo.com',
    password: '1234567890',
    designation: 'Senior Procurement Officer (वरिष्ठ खरीद अधिकारी)',
    apmc: 'APMC New Grain Market, Delhi Road, Rohtak'
  },
  {
    id: 'TEST-ROH-004',
    name: 'Dr. V. K. Verma (डॉ. वी. के. वर्मा)',
    role: 'testing',
    mobile: '9876500002',
    email: 'testing@demo.com',
    demoEmail: 'testing@demo.com',
    password: '1234567890',
    designation: 'Chief Soil & Grain Chemist (मुख्य कृषि विश्लेषक)',
    lab: 'Regional Agri QA & Soil Testing Laboratory, Rohtak'
  },
  {
    id: 'WH-ROH-009',
    name: 'Sh. Ravindra Nath (श्री रविन्द्र नाथ)',
    role: 'warehouse',
    mobile: '9876500003',
    email: 'operator@demo.com',
    demoEmail: 'operator@demo.com',
    password: '1234567890',
    designation: 'Mandi Secretary & Warehouse In-Charge (मंडी सचिव)',
    mandi: 'Krishi Upaj Mandi Samiti, Delhi Road, Rohtak'
  },
  {
    id: 'ACC-ROH-001',
    name: 'Sh. R. K. Goyal (श्री आर. के. गोयल)',
    role: 'account',
    mobile: '9876500004',
    email: 'accounts@demo.com',
    demoEmail: 'accounts@demo.com',
    password: '1234567890',
    designation: 'Senior Accounts Officer (वरिष्ठ लेखा अधिकारी)',
    apmc: 'APMC New Grain Market, Delhi Road, Rohtak'
  }
];'''

new_users = '''const DEFAULT_USERS = [
  {
    id: 'FARM-ROH-101',
    name: 'Rameshwar Hooda',
    role: 'farmer',
    mobile: '9876543210',
    email: 'farmer@demo.com',
    demoEmail: 'farmer@demo.com',
    password: '1234567890',
    aadhaar: 'XXXX-XXXX-7142',
    state: 'Haryana',
    district: 'Rohtak',
    tehsil: 'Rohtak',
    village: 'Bohar',
    totalOwnedLandAcres: 5.0,
    primaryKhasraNo: '142//5, 142//6',
    primaryBankAccount: null
  },
  {
    id: 'OFF-ROH-001',
    name: 'Smt. Anjali Sharma',
    role: 'officer',
    mobile: '9876500001',
    email: 'officer@demo.com',
    demoEmail: 'officer@demo.com',
    password: '1234567890',
    designation: 'Senior Procurement Officer',
    apmc: 'APMC New Grain Market, Delhi Road, Rohtak'
  },
  {
    id: 'TEST-ROH-004',
    name: 'Dr. V. K. Verma',
    role: 'testing',
    mobile: '9876500002',
    email: 'testing@demo.com',
    demoEmail: 'testing@demo.com',
    password: '1234567890',
    designation: 'Chief Soil & Grain Chemist',
    lab: 'Regional Agri QA & Soil Testing Laboratory, Rohtak'
  },
  {
    id: 'WH-ROH-009',
    name: 'Sh. Ravindra Nath',
    role: 'warehouse',
    mobile: '9876500003',
    email: 'operator@demo.com',
    demoEmail: 'operator@demo.com',
    password: '1234567890',
    designation: 'Mandi Secretary & Warehouse In-Charge',
    mandi: 'Krishi Upaj Mandi Samiti, Delhi Road, Rohtak'
  },
  {
    id: 'ACC-ROH-001',
    name: 'Sh. R. K. Goyal',
    role: 'account',
    mobile: '9876500004',
    email: 'accounts@demo.com',
    demoEmail: 'accounts@demo.com',
    password: '1234567890',
    designation: 'Senior Accounts Officer',
    apmc: 'APMC New Grain Market, Delhi Road, Rohtak'
  }
];'''

if old_users in content:
    content = content.replace(old_users, new_users, 1)

# 4. Clean farmerProfile default
old_profile = '''  farmerProfile: {
    id: 'FARM-ROH-101',
    name: 'Rameshwar Hooda (रामेश्वर हुड्डा)',
    fatherName: '',
    mobile: '+91 98765 43210',
    aadhaar: 'XXXX-XXXX-7142',
    state: 'Haryana',
    district: 'Rohtak',
    tehsil: 'Rohtak',
    village: 'Bohar (बोहर)',
    totalOwnedLandAcres: 5.0,
    primaryKhasraNo: '142//5, 142//6',
    primaryBankAccount: null
  },'''

new_profile = '''  farmerProfile: {
    id: 'FARM-ROH-101',
    name: 'Rameshwar Hooda',
    fatherName: '',
    mobile: '+91 98765 43210',
    aadhaar: 'XXXX-XXXX-7142',
    state: 'Haryana',
    district: 'Rohtak',
    tehsil: 'Rohtak',
    village: 'Bohar',
    totalOwnedLandAcres: 5.0,
    primaryKhasraNo: '142//5, 142//6',
    primaryBankAccount: null
  },'''

if old_profile in content:
    content = content.replace(old_profile, new_profile, 1)

# 5. Clean ROHTAK_CROPS
old_crops = '''const ROHTAK_CROPS = [
  { name: 'गेहूँ', nameHi: 'गेहूँ', nameEn: 'Wheat', varieties: ['WH-1105', 'HD-2967', 'HD-3086', 'PBW-550', 'DBW-187', 'DBW-303', 'देशी शरबती'] },
  { name: 'सरसों / राई', nameHi: 'सरसों / राई', nameEn: 'Mustard', varieties: ['RH-725', 'RH-749', 'पूसा बोल्ड', 'गिरिराज', 'लक्ष्मी', 'काली सरसों'] },
  { name: 'धान / बासमती (Paddy / Basmati)', varieties: ['बासमती 1121 (PB-1121)', 'पूसा 1509 (Pusa 1509)', 'बासमती 1718', 'पूसा बासमती 1', 'पीआर-126 (PR-126)', 'शरबती धान'] },
  { name: 'चना / छोले (Gram / Chickpea)', varieties: ['एचसी-5 (HC-5)', 'पूसा 362', 'देशी चना', 'काबुली चना'] },
  { name: 'बाजरा', nameHi: 'बाजरा', nameEn: 'Pearl Millet', varieties: ['एचएचबी-67', 'एचएचबी-299', 'पायनियर संकर बाजरा'] },
  { name: 'कपास / नरमा', nameHi: 'कपास / नरमा', nameEn: 'Cotton', varieties: ['बीटी कॉटन', 'देसी कपास HD-123'] },
  { name: 'गन्ना', nameHi: 'गन्ना', nameEn: 'Sugarcane', varieties: ['को 0238', 'को 15023'] }
];'''

new_crops = '''const ROHTAK_CROPS = [
  { name: 'Wheat', nameHi: 'गेहूँ', nameEn: 'Wheat', varieties: ['WH-1105', 'HD-2967', 'HD-3086', 'PBW-550', 'DBW-187', 'DBW-303', 'Desi Sharbati'] },
  { name: 'Mustard', nameHi: 'सरसों / राई', nameEn: 'Mustard', varieties: ['RH-725', 'RH-749', 'Pusa Bold', 'Giriraj', 'Laxmi', 'Black Mustard'] },
  { name: 'Paddy / Basmati', nameHi: 'धान / बासमती', nameEn: 'Paddy / Basmati', varieties: ['Basmati 1121 (PB-1121)', 'Pusa 1509', 'Basmati 1718', 'Pusa Basmati 1', 'PR-126', 'Sharbati Paddy'] },
  { name: 'Gram / Chickpea', nameHi: 'चना / छोले', nameEn: 'Gram / Chickpea', varieties: ['HC-5', 'Pusa 362', 'Desi Gram', 'Kabuli Chana'] },
  { name: 'Pearl Millet', nameHi: 'बाजरा', nameEn: 'Pearl Millet', varieties: ['HHB-67', 'HHB-299', 'Pioneer Hybrid'] },
  { name: 'Cotton', nameHi: 'कपास / नरमा', nameEn: 'Cotton', varieties: ['Bt Cotton', 'Desi Cotton HD-123'] },
  { name: 'Sugarcane', nameHi: 'गन्ना', nameEn: 'Sugarcane', varieties: ['Co 0238', 'Co 15023'] }
];'''

if old_crops in content:
    content = content.replace(old_crops, new_crops, 1)

# 6. Clean onTehsilChange in app
old_on_tehsil = '''  onTehsilChange(tehsilId) {
    const villageSelect = document.getElementById('regVillage');
    if (!villageSelect) return;
    if (typeof ROHTAK_VILLAGES !== 'undefined') {
      const filtered = ROHTAK_VILLAGES.filter(v => !v.tehsil || v.tehsil === tehsilId);
      const options = filtered.map(v => `<option value="${v.nameHi}">${v.nameHi}</option>`);
      options.push('<option value="अन्य गाँव (रोहतक) / Other Rohtak Village">अन्य गाँव (रोहतक) / Other Village</option>');
      villageSelect.innerHTML = options.join('');
    }
  }'''

new_on_tehsil = '''  onTehsilChange(tehsilId) {
    const villageSelect = document.getElementById('regVillage');
    if (!villageSelect) return;
    const isHi = window.kisanI18n && window.kisanI18n.currentLang === 'hi';
    if (typeof ROHTAK_VILLAGES !== 'undefined') {
      const filtered = ROHTAK_VILLAGES.filter(v => !v.tehsil || v.tehsil === tehsilId);
      const options = filtered.map(v => `<option value="${isHi ? v.nameHi : v.nameEn}">${isHi ? v.nameHi : v.nameEn}</option>`);
      options.push(`<option value="Other Rohtak Village">${isHi ? "अन्य गाँव (रोहतक)" : "Other Rohtak Village"}</option>`);
      villageSelect.innerHTML = options.join('');
    }
  }'''

if old_on_tehsil in content:
    content = content.replace(old_on_tehsil, new_on_tehsil, 1)

# 7. Voicebot initial chat history in English
old_bot_history = '''    this.chatHistory = [
      {
        sender: 'bot',
        text: 'नमस्ते किसान भाई! मैं आपका डिजिटल कृषि सहायक "किसान वाणी" हूँ। आप मुझसे मिट्टी जांच, खाद (यूरिया/डीएपी), फसल बुवाई, मौसम, मंडी भाव या टोकन लाइन के बारे में पूछ सकते हैं।\\n\\n(Hello! I am Kisan Vani AI. Ask me about soil testing, fertilizer dosage, crop care, weather, mandi rates, or token queue!)'
      }
    ];'''

new_bot_history = '''    this.chatHistory = [
      {
        sender: 'bot',
        text: 'Hello farmer! I am your digital agricultural assistant "Kisan Vani AI". You can ask me about soil testing, fertilizer recommendations (Urea/DAP), crop sowing, weather forecasts, mandi prices, or live queue token status.'
      }
    ];'''

if old_bot_history in content:
    content = content.replace(old_bot_history, new_bot_history, 1)

# 8. Voicebot response English by default
old_voice_resp = '''  generateAgriResponse(input) {
    const q = input.toLowerCase();'''

new_voice_resp = '''  generateAgriResponse(input) {
    const q = input.toLowerCase();
    const isHi = window.kisanI18n && window.kisanI18n.lang === 'hi';

    if (!isHi) {
      if (q.includes('token') || q.includes('queue') || q.includes('line') || q.includes('wait')) {
        const tokens = window.kisanState.state.mandiTokens || [];
        const myToken = tokens.find(t => t.farmerId === window.kisanState.state.farmerProfile.id && t.status !== 'completed');
        const curServing = window.kisanState.state.warehouseState.currentServingTokenNumber || 0;
        if (myToken) {
          return `Dear farmer, your active token is #${myToken.tokenNumber}. Currently, Token #${curServing} is being processed at the weighbridge. There are ${myToken.queuePosition} vehicles ahead of you with an estimated wait time of approximately ${myToken.estimatedWaitMinutes} minutes. Please report to Gate 2 upon arrival.`;
        } else {
          return `You do not have an active mandi delivery token currently. You can book a time slot in the 'Mandi Token' section to get a digital gate pass.`;
        }
      }
      if (q.includes('urea') || q.includes('fertilizer') || q.includes('dap') || q.includes('dose')) {
        return `Official scientific fertilizer advisory for Rohtak: Apply 45 kg Urea per acre in three split doses (50% basal, 25% at first irrigation at 21 days, 25% at tillering). Apply 50-55 kg DAP only as basal dose at sowing. Important: Never mix DAP with Zinc Sulfate directly.`;
      }
      if (q.includes('soil') || q.includes('test') || q.includes('sla') || q.includes('advisory')) {
        return `Pre-sowing soil testing is available under Harvest Hub. Once the laboratory logs the NPK parameters, the procurement officer must issue a certified fertilizer and seed prescription within 48 working hours. Adhering to this earns you a cash compliance bonus over Base MSP!`;
      }
      if (q.includes('rate') || q.includes('price') || q.includes('msp') || q.includes('mandi')) {
        return `Today's live mandi prices (Agmarknet Rohtak): Wheat Base MSP is ₹2,275/Q (+ up to ₹115/Q soil compliance bonus). Basmati Paddy is ₹3,950/Q, and Mustard is ₹5,650/Q. Following your soil test advisory unlocks direct premium bonuses on government procurement.`;
      }
      if (q.includes('weather') || q.includes('rain') || q.includes('temp')) {
        const w = window.kisanApi.weatherCache;
        if (w) {
          return `Current Rohtak weather: Temperature is ${w.tempC}°C, humidity is ${w.humidity}%, wind is ${w.windKph} km/h. Conditions: ${w.conditionText}. ${w.agroAdvice}`;
        }
        return `Today's weather in Rohtak is optimal and clear (31.8°C). Ideal for soil sampling, land preparation, and crop transport. No heavy rain warnings.`;
      }
      if (q.includes('seed') || q.includes('wheat') || q.includes('variety') || q.includes('sow')) {
        return `Recommended certified wheat varieties for Rohtak district are 'WH-1105 (CCSHAU)' and 'HD-2967 (Pusa Shresth)' at 40 kg seed per acre. Always treat seeds with Thiram or Carbendazim before sowing.`;
      }
      return `Hello farmer! You can use Harvest Hub to: 1. Submit a pre-sowing soil test request. 2. View your 48h scientific fertilizer advisory. 3. Register your harvest lot for Base MSP + Soil Bonus. 4. Track your live mandi gate pass without waiting in highway queues.`;
    }'''

if old_voice_resp in content:
    content = content.replace(old_voice_resp, new_voice_resp, 1)

# Write updated file
with open('frontend/portal.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated portal.html base sections successfully.')
