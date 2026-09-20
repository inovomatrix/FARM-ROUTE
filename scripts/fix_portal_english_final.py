import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/portal.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix line 9472 in getLoginRoleConfig
old_role_config = "const isHi = !window.kisanI18n || window.kisanI18n.lang === 'hi';"
new_role_config = "const isHi = window.kisanI18n ? window.kisanI18n.currentLang === 'hi' : false;"
if old_role_config in content:
    content = content.replace(old_role_config, new_role_config)
    print("Fixed getLoginRoleConfig isHi definition.")
else:
    print("Warning: old_role_config not found directly")

# 2. Fix line 4030 and 5819 isHi check
content = content.replace(
    "const isHi = window.kisanI18n && window.kisanI18n.lang === 'hi';",
    "const isHi = window.kisanI18n ? window.kisanI18n.currentLang === 'hi' : false;"
)

# 3. Fix line 3476 corpText
old_corp_text = "corpText.innerText = isHi ? 'English' : 'हिंदी';"
new_corp_text = "corpText.innerText = isHi ? '🌐 English' : '🌐 Hindi';"
content = content.replace(old_corp_text, new_corp_text)

# 4. Fix createSoilRequest default crop
content = content.replace("crop: 'Wheat (गेहूँ)',", "crop: 'Wheat (WH-1105)',")

# 5. Fix soil test report fallbacks
content = content.replace(
    "soilType: report.soilType || 'Alluvial Clay Loam (दोमट मिट्टी)',",
    "soilType: report.soilType || (window.tDual ? window.tDual('दोमट मिट्टी (Alluvial Clay Loam)', 'Alluvial Clay Loam') : 'Alluvial Clay Loam'),"
)
content = content.replace(
    "nitrogenStatus: n < 200 ? 'Low (कमी)' : 'Medium',",
    "nitrogenStatus: n < 200 ? (window.tDual ? window.tDual('निम्न (कमी)', 'Low (Deficient)') : 'Low (Deficient)') : 'Medium',"
)
content = content.replace(
    "potassiumStatus: 'High (पर्याप्त)',",
    "potassiumStatus: (window.tDual ? window.tDual('उच्च (पर्याप्त)', 'High (Optimal)') : 'High (Optimal)'),"
)
content = content.replace(
    "zincStatus: zinc < 0.6 ? 'Deficient (जिंक की कमी)' : 'Adequate',",
    "zincStatus: zinc < 0.6 ? (window.tDual ? window.tDual('कमी (जिंक की कमी)', 'Deficient') : 'Deficient') : 'Adequate',"
)

# 6. Fix fertilizers in submitAdvisory
old_ferts = """        fertilizers: [
          { name: 'यूरिया (Urea 46% N)', dose: advisory.ureaBags || '2.0 बैग / एकड़', timing: 'बुवाई के 21 व 45 दिन बाद (विभाजित मात्रा)' },
          { name: 'डीएपी (DAP 18:46:0)', dose: advisory.dapBags || '1.0 बैग / एकड़', timing: 'बुवाई के समय बेसल डोज (हल के पीछे)' },
          { name: (window.tDual ? window.tDual('म्यूरेट ऑफ पोटाश', 'MOP (Potash)') : 'MOP'), dose: advisory.mopBags || (window.tDual ? window.tDual('0.5 बैग / एकड़', '0.5 Bag / Acre') : '0.5 Bag/Acre'), timing: (window.tDual ? window.tDual('बुवाई के समय डीएपी के साथ', 'At sowing with DAP') : 'At sowing with DAP') },
          { name: 'जिंक सल्फेट 21%', dose: advisory.zincDose || '10 kg / एकड़', timing: 'पहली सिंचाई के समय यूरिया के साथ' }
        ],"""

new_ferts = """        fertilizers: [
          { name: (window.tDual ? window.tDual('यूरिया (Urea 46% N)', 'Urea (46% N)') : 'Urea (46% N)'), dose: advisory.ureaBags || (window.tDual ? window.tDual('2.0 बैग / एकड़', '2.0 Bags / Acre') : '2.0 Bags / Acre'), timing: (window.tDual ? window.tDual('बुवाई के 21 व 45 दिन बाद (विभाजित मात्रा)', '21 & 45 days after sowing (split dose)') : '21 & 45 days after sowing (split dose)') },
          { name: (window.tDual ? window.tDual('डीएपी (DAP 18:46:0)', 'DAP (18:46:0)') : 'DAP (18:46:0)'), dose: advisory.dapBags || (window.tDual ? window.tDual('1.0 बैग / एकड़', '1.0 Bag / Acre') : '1.0 Bag / Acre'), timing: (window.tDual ? window.tDual('बुवाई के समय बेसल डोज (हल के पीछे)', 'Basal dose at sowing') : 'Basal dose at sowing') },
          { name: (window.tDual ? window.tDual('म्यूरेट ऑफ पोटाश (MOP)', 'MOP (Potash)') : 'MOP (Potash)'), dose: advisory.mopBags || (window.tDual ? window.tDual('0.5 बैग / एकड़', '0.5 Bag / Acre') : '0.5 Bag / Acre'), timing: (window.tDual ? window.tDual('बुवाई के समय डीएपी के साथ', 'At sowing with DAP') : 'At sowing with DAP') },
          { name: (window.tDual ? window.tDual('जिंक सल्फेट 21%', 'Zinc Sulfate 21%') : 'Zinc Sulfate 21%'), dose: advisory.zincDose || (window.tDual ? window.tDual('10 kg / एकड़', '10 kg / Acre') : '10 kg / Acre'), timing: (window.tDual ? window.tDual('पहली सिंचाई के समय यूरिया के साथ', 'At first irrigation with Urea') : 'At first irrigation with Urea') }
        ],"""

content = content.replace(old_ferts, new_ferts)

# 7. Fix Firebase modal strings
content = content.replace(
    "${isConn ? '🟢 फायरबेस क्लाउड सिंक सक्रिय (Connected & Real-Time Active)' : '🟡 फायरबेस कनेक्ट हो रहा है... (Connecting)'}",
    "${isConn ? tDual('🟢 फायरबेस क्लाउड सिंक सक्रिय (Connected & Real-Time Active)', '🟢 Firebase Cloud Sync Active (Connected & Real-Time Live)') : tDual('🟡 फायरबेस कनेक्ट हो रहा है... (Connecting)', '🟡 Connecting to Firebase Cloud...')}"
)
content = content.replace(
    "प्रोजेक्ट आईडी: <strong>${projId}</strong> | क्लाउड नोड: <code>/kisan_setu_live_state</code>",
    "${tDual('प्रोजेक्ट आईडी:', 'Project ID:')} <strong>${projId}</strong> | ${tDual('क्लाउड नोड:', 'Cloud Node:')} <code>/kisan_setu_live_state</code>"
)
content = content.replace(
    "<strong>⚠️ सूचना / एरर विवरण:</strong> ${err}",
    "<strong>⚠️ ${tDual('सूचना / एरर विवरण:', 'Notice / Error Details:')}</strong> ${err}"
)
content = content.replace(
    "💡 <strong>समाधान:</strong> <a href=\"https://console.firebase.google.com/project/${projId}/database\" target=\"_blank\" style=\"color:#2563eb; font-weight:700;\">फ़ायरबेस कंसोल खोलें</a>",
    "💡 <strong>${tDual('समाधान:', 'Resolution:')}</strong> <a href=\"https://console.firebase.google.com/project/${projId}/database\" target=\"_blank\" style=\"color:#2563eb; font-weight:700;\">${tDual('फ़ायरबेस कंसोल खोलें', 'Open Firebase Console')}</a>"
)
content = content.replace(
    "फायरबेस रियलटाइम डेटाबेस के माध्यम से आप किसी भी डिवाइस (मोबाइल फोन, लैपटॉप, टैबलेट) पर दुनिया के किसी भी कोने से रीयल-टाइम डेटा सिंक कर सकते हैं।",
    "${tDual('फायरबेस रियलटाइम डेटाबेस के माध्यम से आप किसी भी डिवाइस (मोबाइल फोन, लैपटॉप, टैबलेट) पर दुनिया के किसी भी कोने से रीयल-टाइम डेटा सिंक कर सकते हैं।', 'Through Firebase Realtime Database, you can sync data in real time across any device (phone, laptop, tablet) anywhere in the world.')}"
)
content = content.replace(
    "<strong>एक डिवाइस पर किया गया बदलाव तुरंत सभी डिवाइसों पर दिखाई देगा। बिना री-लॉगिन किए सभी अधिकारियों को अपडेट्स मिलते रहेंगे।</strong>",
    "<strong>${tDual('एक डिवाइस पर किया गया बदलाव तुरंत सभी डिवाइसों पर दिखाई देगा। बिना री-लॉगिन किए सभी अधिकारियों को अपडेट्स मिलते रहेंगे।', 'Changes made on one device instantly propagate to all connected devices without requiring re-login.')}</strong>"
)
content = content.replace(
    "<button class=\"btn btn-primary btn-sm\" onclick=\"window.kisanFirebaseSync.updateRtdbUrl()\">बदलें</button>",
    "<button class=\"btn btn-primary btn-sm\" onclick=\"window.kisanFirebaseSync.updateRtdbUrl()\">${tDual('बदलें', 'Update URL')}</button>"
)
content = content.replace(
    "डिफ़ॉल्ट: <code>https://${projId}-default-rtdb.firebaseio.com</code>",
    "${tDual('डिफ़ॉल्ट:', 'Default:')} <code>https://${projId}-default-rtdb.firebaseio.com</code>"
)

# 8. Fix Staff users in seedStaffUsersToFirebase
content = content.replace("name: 'Smt. Anjali Sharma (अंजलि शर्मा)',", "name: 'Smt. Anjali Sharma', nameHi: 'अंजलि शर्मा',")
content = content.replace("name: 'Dr. V. K. Verma (डॉ. वी. के. वर्मा)',", "name: 'Dr. V. K. Verma', nameHi: 'डॉ. वी. के. वर्मा',")
content = content.replace("name: 'Shri Ravindra Nath (रविन्द्र नाथ)',", "name: 'Shri Ravindra Nath', nameHi: 'रविन्द्र नाथ',")
content = content.replace("department: 'New Grain Market Rohtak (नई अनाज मंडी)',", "department: 'New Grain Market Rohtak', departmentHi: 'नई अनाज मंडी',")
content = content.replace("name: 'Shri R. K. Goyal (श्री आर. के. गोयल)',", "name: 'Shri R. K. Goyal', nameHi: 'श्री आर. के. गोयल',")

# 9. Fix Firebase toasts
content = content.replace(
    "window.app.showToast('फायरबेस एसडीके अभी लोड हो रहा है...', 'warning');",
    "window.app.showToast(window.tDual ? window.tDual('फायरबेस एसडीके अभी लोड हो रहा है...', 'Firebase SDK is currently loading...') : 'Firebase SDK is currently loading...', 'warning');"
)
content = content.replace(
    "window.app.showToast('फायरबेस कनेक्शन की जांच की जा रही है...', 'info');",
    "window.app.showToast(window.tDual ? window.tDual('फायरबेस कनेक्शन की जांच की जा रही है...', 'Checking Firebase connection...') : 'Checking Firebase connection...', 'info');"
)
content = content.replace(
    "window.app.showToast('🟢 फायरबेस क्लाउड डेटाबेस सफलतापूर्वक कनेक्टेड है (Read/Write OK)!', 'success');",
    "window.app.showToast(window.tDual ? window.tDual('🟢 फायरबेस क्लाउड डेटाबेस सफलतापूर्वक कनेक्टेड है (Read/Write OK)!', '🟢 Firebase Cloud Database successfully connected (Read/Write OK)!') : '🟢 Firebase Cloud Database successfully connected (Read/Write OK)!', 'success');"
)
content = content.replace(
    "window.app.showToast(`⚠️ फायरबेस स्थिति: ${err.message}`, 'danger');",
    "window.app.showToast(window.tDual ? window.tDual(`⚠️ फायरबेस स्थिति: ${err.message}`, `⚠️ Firebase Status: ${err.message}`) : `⚠️ Firebase Status: ${err.message}`, 'danger');"
)
content = content.replace(
    "window.app.showToast('डेटाबेस URL अपडेट किया गया! पोर्टल रीलोड हो रहा है...', 'info');",
    "window.app.showToast(window.tDual ? window.tDual('डेटाबेस URL अपडेट किया गया! पोर्टल रीलोड हो रहा है...', 'Database URL updated! Reloading portal...') : 'Database URL updated! Reloading portal...', 'info');"
)

# 10. Fix Voice Assistant audio error message
content = content.replace(
    "this.addChatMessage('bot', 'माफ़ कीजिए, आवाज़ साफ़ नहीं आई। कृपया दोबारा बोलें या नीचे लिखकर पूछें। (Could not capture audio clearly. Please repeat or type below).');",
    "this.addChatMessage('bot', (window.kisanI18n && window.kisanI18n.currentLang === 'hi') ? 'माफ़ कीजिए, आवाज़ साफ़ नहीं आई। कृपया दोबारा बोलें या नीचे लिखकर पूछें।' : 'Sorry, could not capture audio clearly. Please repeat or type below.');"
)
content = content.replace(
    "if (statusText) statusText.innerText = 'सुन रहा हूँ... बोलिए (Listening...)';",
    "if (statusText) statusText.innerText = (window.kisanI18n && window.kisanI18n.currentLang === 'hi') ? 'सुन रहा हूँ... बोलिए' : 'Listening... Please speak';"
)
content = content.replace(
    "statusText.innerText = this.isSpeaking ? 'बोल रहा हूँ... (Speaking...)' : 'माइक दबाकर बोलें या नीचे सवाल चुनें';",
    "statusText.innerText = this.isSpeaking ? ((window.kisanI18n && window.kisanI18n.currentLang === 'hi') ? 'बोल रहा हूँ...' : 'Speaking...') : ((window.kisanI18n && window.kisanI18n.currentLang === 'hi') ? 'माइक दबाकर बोलें या नीचे सवाल चुनें' : 'Tap microphone to speak or choose a question below');"
)

# 11. Fix option values and static dummy table
content = content.replace('<option value="एचसी-5 (HC-5)">', '<option value="HC-5 (Gram)">')
content = content.replace('<option value="पूसा 362">', '<option value="Pusa 362 (Gram)">')
content = content.replace('<option value="देशी चना">', '<option value="Desi Chana (Gram)">')
content = content.replace('<td style="padding:6px;">श्री दरियाव सिंह हुड्डा</td>', '<td style="padding:6px;">Shri Daryao Singh Hooda</td>')
content = content.replace('<td style="padding:6px;">बोहर (रोहतक)</td>', '<td style="padding:6px;">Bohar (Rohtak)</td>')
content = content.replace('<td style="padding:6px;">रोहतक, हरियाणा</td>', '<td style="padding:6px;">Rohtak, Haryana</td>')
content = content.replace('<option value="Tractor Trolley (ट्रैक्टर ट्रॉली)">Tractor Trolley (ट्रैक्टर ट्रॉली)</option>', '<option value="Tractor Trolley">Tractor Trolley</option>')
content = content.replace('<option value="Bullock Cart (बैलगाड़ी)">Bullock Cart (बैलगाड़ी)</option>', '<option value="Bullock Cart">Bullock Cart</option>')

# 12. Fix khasra display
content = content.replace(
    "`• ${d.crop.split(' ')[0]}: ${d.acres}A (खसरा: ${d.khasraNo})`",
    "`• ${d.crop.split(' ')[0]}: ${d.acres}A (${window.tDual ? window.tDual('खसरा: ' + d.khasraNo, 'Khasra: ' + d.khasraNo) : 'Khasra: ' + d.khasraNo})`"
)

# 13. Fix Account Officer empty message
old_acct_empty = """                      ${this.activeTab === 'pending'
                        ? 'मंडी संचालक द्वारा खाली गाड़ी की अंतिम तुलाई पूरी करने के बाद बिल संख्या के साथ यहाँ भुगतान आदेश स्वतः प्रदर्शित होगा।'
                        : 'लेखा अधिकारी द्वारा डीबीटी भुगतान जारी करने पर सभी रिकॉर्ड यहाँ सहेजे जाएंगे।'}"""

new_acct_empty = """                      ${this.activeTab === 'pending'
                        ? tDual('मंडी संचालक द्वारा खाली गाड़ी की अंतिम तुलाई पूरी करने के बाद बिल संख्या के साथ यहाँ भुगतान आदेश स्वतः प्रदर्शित होगा।', 'Payment orders will appear here automatically with the bill number after the mandi operator completes final tare weighment.')
                        : tDual('लेखा अधिकारी द्वारा डीबीटी भुगतान जारी करने पर सभी रिकॉर्ड यहाँ सहेजे जाएंगे।', 'All payment records will be archived here once the account officer authorizes the DBT transfer.')}"""

content = content.replace(old_acct_empty, new_acct_empty)

# 14. Fix console.log
content = content.replace(
    "console.log('Initializing Harvest Hub (हार्वेस्ट हब) - Rohtak District Edition...');",
    "console.log('Initializing Harvest Hub - Rohtak District Edition...');"
)

with open('frontend/portal.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully applied updates to portal.html")
