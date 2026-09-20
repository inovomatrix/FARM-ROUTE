import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/portal.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Clean HTML comment at top
content = content.replace("HARVEST HUB (हार्वेस्ट हब) - SIH 2026 Problem Statement 26032", "HARVEST HUB - SIH 2026 Problem Statement 26032")

# 2. Fix FALLBACK_MANDI_RECORDS
old_mandi_block = """const FALLBACK_MANDI_RECORDS = [
  { state: "Haryana", district: "Rohtak", market: "नई अनाज मंडी, दिल्ली रोड रोहतक", commodity: (window.tDual ? window.tDual('गेहूँ', 'Wheat') : 'Wheat'), variety: "WH-1105 (CCSHAU)", grade: "Grade A", arrival_date: "14/09/2026", min_price: 2275, max_price: 2450, modal_price: 2380 },
  { state: "Haryana", district: "Rohtak", market: "नई अनाज मंडी, दिल्ली रोड रोहतक", commodity: "Paddy (धान / बासमती)", variety: "PB-1121", grade: "Grade A", arrival_date: "14/09/2026", min_price: 3600, max_price: 4200, modal_price: 3950 },
  { state: "Haryana", district: "Rohtak", market: "अनाज मंडी, महम (Meham)", commodity: (window.tDual ? window.tDual('सरसों / राई', 'Mustard') : 'Mustard'), variety: "RH-725", grade: "Grade A", arrival_date: "14/09/2026", min_price: 5400, max_price: 5900, modal_price: 5650 },
  { state: "Haryana", district: "Rohtak", market: "अनाज मंडी, सांपला (Sampla)", commodity: (window.tDual ? window.tDual('गेहूँ', 'Wheat') : 'Wheat'), variety: "HD-2967", grade: "FAQ", arrival_date: "14/09/2026", min_price: 2275, max_price: 2425, modal_price: 2350 },
  { state: "Haryana", district: "Rohtak", market: "अनाज मंडी, कलानौर (Kalanaur)", commodity: (window.tDual ? window.tDual('चना', 'Gram') : 'Gram'), variety: "HC-5 (Haryana)", grade: "Grade A", arrival_date: "14/09/2026", min_price: 5200, max_price: 5600, modal_price: 5420 },
  { state: "Haryana", district: "Rohtak", market: "अनाज मंडी, महम (Meham)", commodity: (window.tDual ? window.tDual('बाजरा', 'Pearl Millet') : 'Pearl Millet'), variety: "HHB-67", grade: "FAQ", arrival_date: "14/09/2026", min_price: 2150, max_price: 2350, modal_price: 2250 },
  { state: "Haryana", district: "Karnal", market: "Karnal Mandi", commodity: "Paddy (धान)", variety: "PR-126", grade: "Grade A", arrival_date: "14/09/2026", min_price: 2320, max_price: 2450, modal_price: 2400 },
  { state: "Haryana", district: "Hisar", market: "Hisar APMC", commodity: "Cotton (कपास)", variety: "RCH-659", grade: "Grade A", arrival_date: "14/09/2026", min_price: 6800, max_price: 7400, modal_price: 7150 }
];"""

new_mandi_block = """const FALLBACK_MANDI_RECORDS = [
  { state: "Haryana", district: "Rohtak", market: (window.tDual ? window.tDual("नई अनाज मंडी, दिल्ली रोड रोहतक", "New Grain Market, Delhi Road Rohtak") : "New Grain Market, Delhi Road Rohtak"), commodity: (window.tDual ? window.tDual('गेहूँ', 'Wheat') : 'Wheat'), variety: "WH-1105 (CCSHAU)", grade: "Grade A", arrival_date: "14/09/2026", min_price: 2275, max_price: 2450, modal_price: 2380 },
  { state: "Haryana", district: "Rohtak", market: (window.tDual ? window.tDual("नई अनाज मंडी, दिल्ली रोड रोहतक", "New Grain Market, Delhi Road Rohtak") : "New Grain Market, Delhi Road Rohtak"), commodity: (window.tDual ? window.tDual("धान / बासमती", "Paddy (Basmati)") : "Paddy (Basmati)"), variety: "PB-1121", grade: "Grade A", arrival_date: "14/09/2026", min_price: 3600, max_price: 4200, modal_price: 3950 },
  { state: "Haryana", district: "Rohtak", market: (window.tDual ? window.tDual("अनाज मंडी, महम", "Grain Market, Meham") : "Grain Market, Meham"), commodity: (window.tDual ? window.tDual('सरसों / राई', 'Mustard') : 'Mustard'), variety: "RH-725", grade: "Grade A", arrival_date: "14/09/2026", min_price: 5400, max_price: 5900, modal_price: 5650 },
  { state: "Haryana", district: "Rohtak", market: (window.tDual ? window.tDual("अनाज मंडी, सांपला", "Grain Market, Sampla") : "Grain Market, Sampla"), commodity: (window.tDual ? window.tDual('गेहूँ', 'Wheat') : 'Wheat'), variety: "HD-2967", grade: "FAQ", arrival_date: "14/09/2026", min_price: 2275, max_price: 2425, modal_price: 2350 },
  { state: "Haryana", district: "Rohtak", market: (window.tDual ? window.tDual("अनाज मंडी, कलानौर", "Grain Market, Kalanaur") : "Grain Market, Kalanaur"), commodity: (window.tDual ? window.tDual('चना', 'Gram') : 'Gram'), variety: "HC-5 (Haryana)", grade: "Grade A", arrival_date: "14/09/2026", min_price: 5200, max_price: 5600, modal_price: 5420 },
  { state: "Haryana", district: "Rohtak", market: (window.tDual ? window.tDual("अनाज मंडी, महम", "Grain Market, Meham") : "Grain Market, Meham"), commodity: (window.tDual ? window.tDual('बाजरा', 'Pearl Millet') : 'Pearl Millet'), variety: "HHB-67", grade: "FAQ", arrival_date: "14/09/2026", min_price: 2150, max_price: 2350, modal_price: 2250 },
  { state: "Haryana", district: "Karnal", market: "Karnal Mandi", commodity: (window.tDual ? window.tDual("धान", "Paddy") : "Paddy"), variety: "PR-126", grade: "Grade A", arrival_date: "14/09/2026", min_price: 2320, max_price: 2450, modal_price: 2400 },
  { state: "Haryana", district: "Hisar", market: "Hisar APMC", commodity: (window.tDual ? window.tDual("कपास", "Cotton") : "Cotton"), variety: "RCH-659", grade: "Grade A", arrival_date: "14/09/2026", min_price: 6800, max_price: 7400, modal_price: 7150 }
];"""

content = content.replace(old_mandi_block, new_mandi_block)

# 3. Fix agroAdvice fallback
content = re.sub(
    r"agroAdvice:\s*'रोहतक जिले में बुवाई पूर्व जुताई व मिट्टी नमूना एकत्रीकरण हेतु मौसम अनुकूल है। अगले 24 घंटों में बारिश का कोई अलर्ट नहीं।'",
    "agroAdvice: (window.tDual ? window.tDual('रोहतक जिले में बुवाई पूर्व जुताई व मिट्टी नमूना एकत्रीकरण हेतु मौसम अनुकूल है। अगले 24 घंटों में बारिश का कोई अलर्ट नहीं।', 'Optimal weather for pre-sowing ploughing and soil sample collection across Rohtak. Zero rain alert for next 24 hours.') : 'Optimal weather for field operations.')",
    content
)

# 4. Fix Firebase modal paragraph (handling trailing spaces with regex)
content = re.sub(
    r'फायरबेस रियलटाइम डेटाबेस के माध्यम से आप किसी भी डिवाइस [^\n]+\n\s*<strong>एक डिवाइस पर किया गया बदलाव [^\n]+</strong>',
    "${tDual('फायरबेस रियलटाइम डेटाबेस के माध्यम से आप किसी भी डिवाइस पर दुनिया के किसी भी कोने से पोर्टल का उपयोग कर सकते हैं। एक डिवाइस पर किया गया बदलाव तुरंत सभी डिवाइसों पर दिखाई देगा।', 'Through Firebase Realtime Database, access the portal from any device anywhere in the world. Changes made on one device instantly propagate to all connected portals without re-login.')}",
    content
)

# 5. Fix Account Officer empty message (handling trailing spaces with regex)
content = re.sub(
    r"\$\{this\.activeTab === 'pending'\s*\n\s*\?\s*'मंडी संचालक द्वारा खाली गाड़ी की अंतिम तुलाई पूरी करने के बाद बिल संख्या के साथ यहाँ भुगतान आदेश स्वतः प्रदर्शित होगा\.'\s*\n\s*:\s*'लेखा अधिकारी द्वारा डीबीटी भुगतान जारी करने पर सभी रिकॉर्ड यहाँ सहेजे जाएंगे\.'\}",
    "${this.activeTab === 'pending' ? tDual('मंडी संचालक द्वारा खाली गाड़ी की अंतिम तुलाई पूरी करने के बाद बिल संख्या के साथ यहाँ भुगतान आदेश स्वतः प्रदर्शित होगा।', 'Payment orders will appear here automatically with bill numbers after the mandi operator completes final tare weighment.') : tDual('लेखा अधिकारी द्वारा डीबीटी भुगतान जारी करने पर सभी रिकॉर्ड यहाँ सहेजे जाएंगे।', 'All payment records will be archived here once the account officer authorizes the DBT transfer.')}",
    content
)

with open('frontend/portal.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied precision fixes.")
