import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/portal.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

content = "".join(lines)

# 1. LAN sync modal
content = content.replace(
    "window.app.openModal('📲 मल्टी-डिवाइस लाइव सिंक (Multi-Device Sync)', `",
    "window.app.openModal(tDual('📲 मल्टी-डिवाइस लाइव सिंक (Multi-Device Sync)', '📲 Multi-Device Live Sync'), `"
)
content = content.replace(
    "अपने <strong>मोबाइल फोन, टैबलेट या दूसरे लैपटॉप</strong> पर यह पोर्टल खोलने के लिए नीचे दिए गए QR कोड को मोबाइल कैमरा से स्कैन करें:",
    "${tDual('अपने <strong>मोबाइल फोन, टैबलेट या दूसरे लैपटॉप</strong> पर यह पोर्टल खोलने के लिए नीचे दिए गए QR कोड को मोबाइल कैमरा से स्कैन करें:', 'Scan the QR code below with your mobile camera to open this portal on your <strong>mobile phone, tablet, or secondary laptop</strong>:')}"
)
content = content.replace(
    '<div style="font-size:0.75rem; color:#64748b; font-weight:700; text-transform:uppercase;">सीधा नेटवर्क लिंक (Direct Wi-Fi / Hotspot URL):</div>',
    '<div style="font-size:0.75rem; color:#64748b; font-weight:700; text-transform:uppercase;">${tDual(\'सीधा नेटवर्क लिंक (Direct Wi-Fi / Hotspot URL):\', \'Direct Wi-Fi / Hotspot Network Link:\')}</div>'
)
content = content.replace(
    "window.app.showToast('लिंक कॉपी किया गया! मोबाइल में पेस्ट करें।', 'success');\">📋 कॉपी</button>",
    "window.app.showToast(tDual('लिंक कॉपी किया गया! मोबाइल में पेस्ट करें।', 'Link copied! Paste into mobile browser.'), 'success');\">${tDual('📋 कॉपी', '📋 Copy')}</button>"
)
content = content.replace(
    "<strong>💡 3 आसान चरणों में उपयोग करें:</strong>",
    "<strong>💡 ${tDual('3 आसान चरणों में उपयोग करें:', 'How to use in 3 easy steps:')}</strong>"
)
content = content.replace(
    "<li>सुनिश्चित करें कि आपका फोन उसी <strong>Wi-Fi</strong> या लैपटॉप के <strong>Mobile Hotspot</strong> से जुड़ा है।</li>",
    "<li>${tDual('सुनिश्चित करें कि आपका फोन उसी <strong>Wi-Fi</strong> या लैपटॉप के <strong>Mobile Hotspot</strong> से जुड़ा है।', 'Ensure your phone is connected to the same <strong>Wi-Fi</strong> or laptop <strong>Mobile Hotspot</strong>.')}</li>"
)
content = content.replace(
    "<li>मोबाइल कैमरा से QR कोड स्कैन करें या ब्राउज़र में <code>${mobileUrl}</code> खोलें।</li>",
    "<li>${tDual(`मोबाइल कैमरा से QR कोड स्कैन करें या ब्राउज़र में <code>${mobileUrl}</code> खोलें।`, `Scan QR code with phone camera or navigate to <code>${mobileUrl}</code> in your mobile browser.`)}</li>"
)
content = content.replace(
    "<li><strong>लाइव सिंक:</strong> सभी डिवाइसों पर बिना री-लॉगिन किए डेटा तुरंत अपडेट दिखाई देगा!</li>",
    "<li><strong>${tDual('लाइव सिंक:', 'Live Sync:')}</strong> ${tDual('सभी डिवाइसों पर बिना री-लॉगिन किए डेटा तुरंत अपडेट दिखाई देगा!', 'Data updates instantaneously across all devices without requiring re-login!')}</li>"
)
content = content.replace(
    "window.kisanSync.pullServerState(true); window.app.showToast('डेटा पुनः सिंक किया गया', 'info');",
    "window.kisanSync.pullServerState(true); window.app.showToast(tDual('डेटा पुनः सिंक किया गया', 'Data refreshed successfully'), 'info');"
)

# 2. Firebase sync modal
content = content.replace(
    "${isConn ? '🟢 फायरबेस क्लाउड सिंक सक्रिय (Connected & Real-Time Active)' : '🟡 फायरबेस कनेक्ट हो रहा है / नियम जांचें'}",
    "${isConn ? tDual('🟢 फायरबेस क्लाउड सिंक सक्रिय (Connected & Real-Time Active)', '🟢 Firebase Cloud Sync Active (Connected & Real-Time Live)') : tDual('🟡 फायरबेस कनेक्ट हो रहा है / नियम जांचें', '🟡 Connecting to Firebase / Verify Rules')}"
)
content = content.replace(
    "💡 <strong>समाधान:</strong> <a href=\"https://console.firebase.google.com/project/${projId}/database\" target=\"_blank\" style=\"color:#b91c1c; font-weight:700; text-decoration:underline;\">Firebase Console</a> में जाकर <strong>Realtime Database</strong> बनाएं और <strong>Rules</strong> में <code>{ \"rules\": { \".read\": true, \".write\": true } }</code> सेट करें।",
    "💡 <strong>${tDual('समाधान:', 'Resolution:')}</strong> ${tDual('Firebase Console में जाकर Realtime Database बनाएं और Rules में', 'Go to Firebase Console, create Realtime Database and set Rules to')} <code>{ \"rules\": { \".read\": true, \".write\": true } }</code>"
)
content = content.replace(
    "फायरबेस रियलटाइम डेटाबेस के माध्यम से आप किसी भी डिवाइस (मोबाइल फोन, लैपटॉप, टैबलेट) पर दुनिया के किसी भी कोने से पोर्टल का उपयोग कर सकते हैं।\n          <strong>एक डिवाइस पर किया गया बदलाव तुरंत सभी डिवाइसों पर दिखाई देगा। बिना री-लॉगिन किए सभी अधिकारियों को अपडेटेड डेटा मिलेगा।</strong>",
    "${tDual('फायरबेस रियलटाइम डेटाबेस के माध्यम से आप किसी भी डिवाइस पर दुनिया के किसी भी कोने से पोर्टल का उपयोग कर सकते हैं। एक डिवाइस पर किया गया बदलाव तुरंत सभी डिवाइसों पर दिखाई देगा।', 'Through Firebase Realtime Database, access the portal from any device anywhere in the world. Changes made on one device instantly propagate to all connected portals without re-login.')}"
)
content = content.replace(
    "window.kisanFirebaseSync.pushToFirebase(); window.app.showToast('क्लाउड पर डेटा भेजा गया', 'success');",
    "window.kisanFirebaseSync.pushToFirebase(); window.app.showToast(tDual('क्लाउड पर डेटा भेजा गया', 'Data synced to cloud successfully'), 'success');"
)

# 3. Voice assistant error message
content = content.replace(
    "this.addChatMessage('bot', 'माफ़ कीजिए, आवाज़ साफ़ नहीं आई। कृपया दोबारा बोलें या नीचे लिखकर पूछें। (Could not capture audio clearly. Please try again or type.)');",
    "const isHi = window.kisanI18n ? window.kisanI18n.currentLang === 'hi' : false;\n          this.addChatMessage('bot', isHi ? 'माफ़ कीजिए, आवाज़ साफ़ नहीं आई। कृपया दोबारा बोलें या नीचे लिखकर पूछें।' : 'Sorry, could not capture audio clearly. Please try again or type below.');"
)

# 4. Account officer empty table
old_acct_pattern = re.compile(
    r"\$\{this\.activeTab === 'pending'\s*\?\s*'मंडी संचालक द्वारा खाली गाड़ी की अंतिम तुलाई पूरी करने के बाद बिल संख्या के साथ यहाँ भुगतान आदेश स्वतः प्रदर्शित होगा\.'\s*:\s*'लेखा अधिकारी द्वारा डीबीटी भुगतान जारी करने पर सभी रिकॉर्ड यहाँ सहेजे जाएंगे\.'\}",
    re.MULTILINE
)
new_acct_replacement = "${this.activeTab === 'pending' ? tDual('मंडी संचालक द्वारा खाली गाड़ी की अंतिम तुलाई पूरी करने के बाद बिल संख्या के साथ यहाँ भुगतान आदेश स्वतः प्रदर्शित होगा।', 'Payment orders will appear here automatically with the bill number after the mandi operator completes final tare weighment.') : tDual('लेखा अधिकारी द्वारा डीबीटी भुगतान जारी करने पर सभी रिकॉर्ड यहाँ सहेजे जाएंगे।', 'All payment records will be archived here once the account officer authorizes the DBT transfer.')}"

content = old_acct_pattern.sub(new_acct_replacement, content)

# 5. Comment at 8218
content = content.replace(
    "<!-- WORKQUEUE 3: 20 KM DAILY ROUTE CLUSTERING (बहु-किसान दैनिक क्लस्टर) -->",
    "<!-- WORKQUEUE 3: 20 KM DAILY ROUTE CLUSTERING (Multi-Farmer Daily Cluster) -->"
)

with open('frontend/portal.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully applied remaining fixes to portal.html")
