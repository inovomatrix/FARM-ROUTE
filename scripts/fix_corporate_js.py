import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/js/corporate.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update constructor of I18nManager in corporate.js
old_constructor = """  class I18nManager {
    constructor() {
      this.currentLang = localStorage.getItem('HARVEST_HUB_LANG') || localStorage.getItem('KISAN_SETU_LANG') || 'hi';
    }"""

new_constructor = """  class I18nManager {
    constructor() {
      const saved = localStorage.getItem('HARVEST_HUB_LANG_v2');
      this.currentLang = (saved === 'hi') ? 'hi' : 'en';
      localStorage.setItem('HARVEST_HUB_LANG_v2', this.currentLang);
      localStorage.setItem('HARVEST_HUB_LANG', this.currentLang);
    }"""

if old_constructor in content:
    content = content.replace(old_constructor, new_constructor)
    print("Updated I18nManager constructor in corporate.js")
else:
    print("Warning: old_constructor not found exactly, using regex")
    content = re.sub(
        r'class I18nManager\s*\{\s*constructor\(\)\s*\{\s*this\.currentLang\s*=\s*[^;]+;\s*\}',
        """class I18nManager {
    constructor() {
      const saved = localStorage.getItem('HARVEST_HUB_LANG_v2');
      this.currentLang = (saved === 'hi') ? 'hi' : 'en';
      localStorage.setItem('HARVEST_HUB_LANG_v2', this.currentLang);
      localStorage.setItem('HARVEST_HUB_LANG', this.currentLang);
    }""",
        content
    )

# 2. Update setLanguage in corporate.js
old_set_lang = """      if (lang === 'hi' || lang === 'en') {
        this.currentLang = lang;
        localStorage.setItem('HARVEST_HUB_LANG', lang);
        localStorage.setItem('KISAN_SETU_LANG', lang);
        document.documentElement.lang = lang;
        this.translatePage();
      }"""

new_set_lang = """      if (lang === 'hi' || lang === 'en') {
        this.currentLang = lang;
        localStorage.setItem('HARVEST_HUB_LANG_v2', lang);
        localStorage.setItem('HARVEST_HUB_LANG', lang);
        localStorage.setItem('KISAN_SETU_LANG', lang);
        document.documentElement.lang = lang;
        this.translatePage();
      }"""

content = content.replace(old_set_lang, new_set_lang)

# 3. Update langBtnText in corporate.js
old_lang_btn = """      // Update language toggle button label
      const langBtnText = document.getElementById('corpLangText');
      if (langBtnText) {
        langBtnText.textContent = isHi ? 'English' : 'हिंदी';
      }"""

new_lang_btn = """      // Update language toggle button label: strictly show '🌐 Hindi' in English mode, and '🌐 English' in Hindi mode
      const langBtnText = document.getElementById('corpLangText');
      if (langBtnText) {
        langBtnText.textContent = isHi ? '🌐 English' : '🌐 Hindi';
      }"""

content = content.replace(old_lang_btn, new_lang_btn)

# 4. Update CROP_RATES in corporate.js
old_crop_rates = """  // Crop MSP and Soil Compliance Bonus Configuration
  const CROP_RATES = {
    wheat: { name: 'गेहूँ (Wheat WH-1105)', baseMsp: 2275, bonus: 115 },
    mustard: { name: 'सरसों / राई (Mustard RH-725)', baseMsp: 5650, bonus: 100 },
    paddy: { name: 'धान / बासमती (Paddy PB-1121)', baseMsp: 2300, bonus: 90 },
    gram: { name: 'चना / छोले (Gram HC-5)', baseMsp: 5440, bonus: 80 },
    millet: { name: 'बाजरा (Pearl Millet HHB-67)', baseMsp: 2625, bonus: 75 }
  };"""

new_crop_rates = """  // Crop MSP and Soil Compliance Bonus Configuration
  const CROP_RATES = {
    wheat: { nameEn: 'Wheat (WH-1105)', nameHi: 'गेहूँ (Wheat WH-1105)', baseMsp: 2275, bonus: 115 },
    mustard: { nameEn: 'Mustard / Rapeseed (RH-725)', nameHi: 'सरसों / राई (Mustard RH-725)', baseMsp: 5650, bonus: 100 },
    paddy: { nameEn: 'Paddy / Basmati (PB-1121)', nameHi: 'धान / बासमती (Paddy PB-1121)', baseMsp: 2300, bonus: 90 },
    gram: { nameEn: 'Gram / Chickpea (HC-5)', nameHi: 'चना / छोले (Gram HC-5)', baseMsp: 5440, bonus: 80 },
    millet: { nameEn: 'Pearl Millet / Bajra (HHB-67)', nameHi: 'बाजरा (Pearl Millet HHB-67)', baseMsp: 2625, bonus: 75 }
  };"""

content = content.replace(old_crop_rates, new_crop_rates)

# 5. Update updateCalculator bonus rate and display qty
old_calc_bonus = """      const notAppText = isEn ? '₹0 (Not Applicable)' : '₹0 (लागू नहीं)';
      bonusRateEl.textContent = isCompliant ? '+₹' + bonusPerQ + '/Q (लागू)' : notAppText;"""

new_calc_bonus = """      const notAppText = isEn ? '₹0 (Not Applicable)' : '₹0 (लागू नहीं)';
      bonusRateEl.textContent = isCompliant ? '+₹' + bonusPerQ + (isEn ? '/Q (Bonus Applied)' : '/Q (लागू)') : notAppText;"""

content = content.replace(old_calc_bonus, new_calc_bonus)

# 6. Update simulatedTokens queue simulator in corporate.js
old_sim_tokens = """  // 4. Live Queue Simulator
  let simulatedTokens = [
    { num: 8294, vehicle: 'HR-12-BZ-9481 (Tractor)', crop: 'गेहूँ', status: 'weighbridge_in', statusLabel: 'धर्मकांटा तौल (Gross Wt)', calling: true },
    { num: 8293, vehicle: 'HR-12-AK-1029 (Tata 407)', crop: 'सरसों', status: 'unloading', statusLabel: 'गोदाम अनलोडिंग (Silo 2)', calling: false },
    { num: 8292, vehicle: 'HR-12-CX-4491 (Tractor)', crop: 'धान', status: 'gate_entry', statusLabel: 'गेट प्रवेश (Gate Entry)', calling: false },
    { num: 8291, vehicle: 'HR-12-DF-7812 (Canter)', crop: 'गेहूँ', status: 'waiting', statusLabel: 'कतार में (Waiting)', calling: false }
  ];"""

new_sim_tokens = """  // 4. Live Queue Simulator
  function getInitialSimulatedTokens(isHi) {
    return [
      { num: 8294, vehicle: 'HR-12-BZ-9481 (Tractor)', crop: isHi ? 'गेहूँ' : 'Wheat (WH-1105)', status: 'weighbridge_in', statusLabel: isHi ? 'धर्मकांटा तौल (Gross Wt)' : 'Weighbridge IN (Gross Wt)', calling: true },
      { num: 8293, vehicle: 'HR-12-AK-1029 (Tata 407)', crop: isHi ? 'सरसों' : 'Mustard (RH-725)', status: 'unloading', statusLabel: isHi ? 'गोदाम अनलोडिंग (Silo 2)' : 'Warehouse Unloading (Silo 2)', calling: false },
      { num: 8292, vehicle: 'HR-12-CX-4491 (Tractor)', crop: isHi ? 'धान' : 'Paddy (PB-1121)', status: 'gate_entry', statusLabel: isHi ? 'गेट प्रवेश (Gate Entry)' : 'Gate Entry (Verification)', calling: false },
      { num: 8291, vehicle: 'HR-12-DF-7812 (Canter)', crop: isHi ? 'गेहूँ' : 'Wheat (WH-1105)', status: 'waiting', statusLabel: isHi ? 'कतार में (Waiting)' : 'In Queue (Waiting)', calling: false }
    ];
  }
  let simulatedTokens = getInitialSimulatedTokens(false);"""

content = content.replace(old_sim_tokens, new_sim_tokens)

# 7. Update advanceQueueSimulator in corporate.js
old_advance = """    const crops = ['गेहूँ (Wheat)', 'सरसों (Mustard)', 'धान (Paddy)'];
    const isEn = window.kisanI18n && window.kisanI18n.lang === 'en';

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
      window.KisanVoiceAssistant.announceToken(nextNum, 1, 'रोहतक मंडी');
    }"""

new_advance = """    const isEn = !window.kisanI18n || window.kisanI18n.lang === 'en';
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
    }"""

content = content.replace(old_advance, new_advance)

# Save updated file
with open('frontend/js/corporate.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated corporate.js")
