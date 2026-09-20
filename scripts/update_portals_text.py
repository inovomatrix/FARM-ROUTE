import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/portal.html', 'r', encoding='utf-8') as f:
    text = f.read()

replacements = [
    # Officer Portal Hero & KPIs
    (
        '<p>अधिकारी: <strong>श्रीमती अंजलि शर्मा (वरिष्ठ खरीद अधिकारी, APMC रोहतक)</strong> | प्रभाग: केंद्रीय एवं राज्य कृषि खरीद प्रकोष्ठ | 48-घंटे वैज्ञानिक परामर्श एवं मूल्य नियंत्रण</p>',
        "<p>${tDual('अधिकारी: <strong>श्रीमती अंजलि शर्मा (वरिष्ठ खरीद अधिकारी, APMC रोहतक)</strong> | प्रभाग: केंद्रीय एवं राज्य कृषि खरीद प्रकोष्ठ | 48-घंटे वैज्ञानिक परामर्श एवं मूल्य नियंत्रण', 'Officer: <strong>Smt. Anjali Sharma (Senior Procurement Officer, APMC Rohtak)</strong> | Division: Central & State Agri Procurement Cell | 48h Advisory & MSP Control')}</p>"
    ),
    (
        '<div style="font-size:0.75rem; color:#b45309; text-transform:uppercase; font-weight:700;">आगामी 48 कार्य घंटे समय सीमा (48h Working SLA)</div>',
        "<div style=" + '"font-size:0.75rem; color:#b45309; text-transform:uppercase; font-weight:700;">${tDual(\'आगामी 48 कार्य घंटे समय सीमा (48h Working SLA)\', \'Upcoming 48-Hour Advisory SLA\')}</div>'
    ),
    (
        '<span style="font-size:0.85rem; font-weight:400; color:#64748b;">परामर्श लंबित</span>',
        "<span style=" + '"font-size:0.85rem; font-weight:400; color:#64748b;">${tDual(\'परामर्श लंबित\', \'Pending Advisories\')}</span>'
    ),
    (
        '<small style="color:#059669;">⏳ प्रयोगशाला रिपोर्ट आते ही 48 घंटे में पर्चा देना अनिवार्य</small>',
        "<small style=" + '"color:#059669;">⏳ ${tDual(\'प्रयोगशाला रिपोर्ट आते ही 48 घंटे में पर्चा देना अनिवार्य\', \'Mandatory prescription issuance within 48h of test report\')}</small>'
    ),
    (
        '<span style="font-size:0.85rem; font-weight:400; color:#64748b;">लॉट जांच में</span>',
        "<span style=" + '"font-size:0.85rem; font-weight:400; color:#64748b;">${tDual(\'लॉट जांच में\', \'Lots Pending Review\')}</span>'
    ),
    (
        '<small style="color:#64748b;">नमी व दाने के लस्टर आधार पर MSP दर तय करें</small>',
        "<small style=" + '"color:#64748b;">${tDual(\'नमी व दाने के लस्टर आधार पर MSP दर तय करें\', \'Set MSP rate based on moisture & grain luster\')}</small>'
    ),
    (
        '<small style="color:#15803d;">किसानों द्वारा सुझाई गई यूरिया व डीएपी का पालन</small>',
        "<small style=" + '"color:#15803d;">${tDual(\'किसानों द्वारा सुझाई गई यूरिया व डीएपी का पालन\', \'Farmer adherence to prescribed Urea & DAP dosages\')}</small>'
    ),
    # Registered Farmers Table
    (
        '<h3><span>🌾</span> पंजीकृत किसान डेटाबेस (Registered Farmers - Live Synced)</h3>',
        "<h3><span>🌾</span> ${tDual('पंजीकृत किसान डेटाबेस (Registered Farmers - Live Synced)', 'Registered Farmers Database - Live Synced')}</h3>"
    ),
    (
        '<small style="color:#64748b;">रोहतक जिले के सभी पंजीकृत किसान और उनके खेत का विवरण सीधे फायरबेस / सर्वर से लाइव सिंक है।</small>',
        "<small style=" + '"color:#64748b;">${tDual(\'रोहतक जिले के सभी पंजीकृत किसान और उनके खेत का विवरण सीधे फायरबेस / सर्वर से लाइव सिंक है।\', \'All registered farmers across Rohtak district and their plot records synced live with cloud.\')}</small>'
    ),
    (
        '<th>किसान का नाम व पिता</th>',
        "<th>${tDual('किसान का नाम व पिता', 'Farmer & Father Name')}</th>"
    ),
    (
        '<th>मोबाइल नंबर</th>',
        "<th>${tDual('मोबाइल नंबर', 'Mobile Number')}</th>"
    ),
    (
        '<th>मुख्य खसरा सं.</th>',
        "<th>${tDual('मुख्य खसरा सं.', 'Primary Khasra No')}</th>"
    ),
    (
        '<th>क्लाउड स्थिति</th>',
        "<th>${tDual('क्लाउड स्थिति', 'Cloud Status')}</th>"
    ),
    (
        '<small style="color:#64748b;">पिता: ${f.fatherName}</small>',
        "<small style=" + '"color:#64748b;">${tDual(\'पिता:\', \'Father:\')} ${f.fatherName}</small>'
    ),
    (
        '<td><strong>${f.totalOwnedLandAcres || 0} एकड़</strong></td>',
        "<td><strong>${f.totalOwnedLandAcres || 0} ${tDual('एकड़', 'Acres')}</strong></td>"
    ),
    # Officer Section 1
    (
        '<h3><span>🧪</span> मृदा परीक्षण अनुरोध एवं 48-घंटे वैज्ञानिक परामर्श प्रबंधन (Soil Testing & Advisory)</h3>',
        "<h3><span>🧪</span> ${tDual('मृदा परीक्षण अनुरोध एवं 48-घंटे वैज्ञानिक परामर्श प्रबंधन (Soil Testing & Advisory)', 'Soil Testing Requests & 48h Advisory Management')}</h3>"
    ),
    (
        '<th>किसान व खेत विवरण</th>',
        "<th>${tDual('किसान व खेत विवरण', 'Farmer & Plot Details')}</th>"
    ),
    (
        '<th>प्रस्तावित फसल</th>',
        "<th>${tDual('प्रस्तावित फसल', 'Proposed Crop')}</th>"
    ),
    (
        '<th>परीक्षण दल स्थिति</th>',
        "<th>${tDual('परीक्षण दल स्थिति', 'Lab Team Status')}</th>"
    ),
    (
        '<th>48h SLA शेष समय</th>',
        "<th>${tDual('48h SLA शेष समय', '48h SLA Time Left')}</th>"
    ),
    (
        '<small style="color:#1b5e20; font-weight:600;">कुल: ${req.totalOwnedLandAcres || 0} एकड़ | बुवाई: ${req.seedingLandAcres || 0} एकड़</small>',
        "<small style=" + '"color:#1b5e20; font-weight:600;">${tDual(\'कुल:\', \'Total:\')} ${req.totalOwnedLandAcres || 0} ${tDual(\'एकड़\', \'Acres\')} | ${tDual(\'बुवाई:\', \'Seeding:\')} ${req.seedingLandAcres || 0} ${tDual(\'एकड़\', \'Acres\')}</small>'
    ),
    (
        '📄 रजिस्ट्री PDF देखें',
        "📄 ${tDual('रजिस्ट्री PDF देखें', 'View Registry PDF')}"
    ),
    (
        "<small style=\"color:#15803d;\">${req.testReport ? '✅ परीक्षण रिपोर्ट उपलब्ध' : '⏳ सैंपल एकत्रित किया जा रहा है'}</small>",
        "<small style=\"color:#15803d;\">${req.testReport ? tDual('✅ परीक्षण रिपोर्ट उपलब्ध', '✅ Test Report Ready') : tDual('⏳ सैंपल एकत्रित किया जा रहा है', '⏳ Sample Collection in Progress')}</small>"
    ),
    (
        '<span style="font-size:0.75rem; color:#94a3b8;">रिपोर्ट का इंतज़ार</span>',
        "<span style=" + '"font-size:0.75rem; color:#94a3b8;">${tDual(\'रिपोर्ट का इंतज़ार\', \'Waiting for Report\')}</span>'
    ),
    (
        '<small style="color:#64748b;">पूर्व फसल: ${req.previousCrop || \'N/A\'}</small>',
        "<small style=\"color:#64748b;\">${tDual('पूर्व फसल:', 'Previous Crop:')} ${req.previousCrop || 'N/A'}</small>"
    ),
    # Officer Section 2 (Harvest QA & MSP)
    (
        '<h3><span>🌾</span> फसल कटाई बाद गुणवत्ता निरीक्षण एवं सरकारी खरीद मूल्य निर्धारण (Harvest QA & Rate Quotation)</h3>',
        "<h3><span>🌾</span> ${tDual('फसल कटाई बाद गुणवत्ता निरीक्षण एवं सरकारी खरीद मूल्य निर्धारण (Harvest QA & Rate Quotation)', 'Harvest Crop QA Inspection & Procurement Rate Quotation')}</h3>"
    ),
    (
        '<th>किसान एवं फसल</th>',
        "<th>${tDual('किसान एवं फसल', 'Farmer & Crop')}</th>"
    ),
    (
        '<th>मात्रा</th>',
        "<th>${tDual('मात्रा', 'Quantity')}</th>"
    ),
    (
        '<th>गुणवत्ता निरीक्षण रिपोर्ट</th>',
        "<th>${tDual('गुणवत्ता निरीक्षण रिपोर्ट', 'QA Inspection Report')}</th>"
    ),
    (
        '<small style="color:#64748b;">किसान: ${cr.farmerName}</small>',
        "<small style=" + '"color:#64748b;">${tDual(\'किसान:\', \'Farmer:\')} ${cr.farmerName}</small>'
    ),
    (
        '<td><strong>${cr.quantityQuintals} क्विंटल</strong></td>',
        "<td><strong>${cr.quantityQuintals} ${tDual('क्विंटल', 'Quintals')}</strong></td>"
    ),
    (
        '<small style="color:#334155;">नमी: ${cr.qualityReport.moisturePercent}% | विदेशी तत्व: ${cr.qualityReport.foreignMatterPercent}%</small>',
        "<small style=" + '"color:#334155;">${tDual(\'नमी:\', \'Moisture:\')} ${cr.qualityReport.moisturePercent}% | ${tDual(\'विदेशी तत्व:\', \'Foreign Matter:\')} ${cr.qualityReport.foreignMatterPercent}%</small>'
    ),
    (
        '<span style="color:#0284c7; font-size:0.8rem;">निरीक्षण दल फील्ड पर है (${cr.assignedInspector})</span>',
        "<span style=" + '"color:#0284c7; font-size:0.8rem;">${tDual(\'निरीक्षण दल फील्ड पर है\', \'Inspection team in field\')} (${cr.assignedInspector})</span>'
    ),
    (
        'गुणवत्ता परीक्षक भेजें',
        "${tDual('गुणवत्ता परीक्षक भेजें', 'Dispatch Inspector')}"
    ),
    (
        '<small style="color:#64748b;">कुल: ₹${(cr.rateQuotation.totalEstimatedValue || 0).toLocaleString(\'en-IN\')}</small>',
        "<small style=\"color:#64748b;\">${tDual('कुल:', 'Total:')} ₹${(cr.rateQuotation.totalEstimatedValue || 0).toLocaleString('en-IN')}</small>"
    ),
    (
        '<span style="color:#94a3b8; font-size:0.8rem;">दर निर्धारण शेष</span>',
        "<span style=" + '"color:#94a3b8; font-size:0.8rem;">${tDual(\'दर निर्धारण शेष\', \'Pending Quotation\')}</span>'
    ),
    (
        "${cr.rateQuotation.farmerAccepted ? '✅ किसान द्वारा स्वीकृत' : 'किसान निर्णय की प्रतीक्षा'}",
        "${cr.rateQuotation.farmerAccepted ? tDual('✅ किसान द्वारा स्वीकृत', '✅ Accepted by Farmer') : tDual('किसान निर्णय की प्रतीक्षा', 'Awaiting Farmer Decision')}"
    ),
    (
        '<span style="color:#94a3b8; font-size:0.75rem;">निरीक्षण रिपोर्ट प्रतीक्षारत</span>',
        "<span style=" + '"color:#94a3b8; font-size:0.75rem;">${tDual(\'निरीक्षण रिपोर्ट प्रतीक्षारत\', \'Awaiting Inspection Report\')}</span>'
    ),
    # Officer Section 3 (Transport Pooling)
    (
        '<h3><span>🚜</span> लघु किसान संयुक्त परिवहन डेस्क (Small Farmer Transport Pooling &lt; 4 MT / 20 km)</h3>',
        "<h3><span>🚜</span> ${tDual('लघु किसान संयुक्त परिवहन डेस्क (Small Farmer Transport Pooling < 4 MT / 20 km)', 'Small Farmer Transport Pooling Desk (< 4 MT / 20 km)')}</h3>"
    ),
    (
        '<small style="color:#64748b;">40 क्विंटल से कम पैदावार वाले 20 किमी परिधि के छोटे किसानों को साझा ट्रैक्टर-ट्रॉली से जोड़ें।</small>',
        "<small style=" + '"color:#64748b;">${tDual(\'40 क्विंटल से कम पैदावार वाले 20 किमी परिधि के छोटे किसानों को साझा ट्रैक्टर-ट्रॉली से जोड़ें।\', \'Pool small & marginal farmers (< 40 Quintals) within a 20 km radius to share tractor-trolleys and reduce freight costs.\')}</small>'
    ),
    (
        '<span class="badge" style="background:#fef3c7; color:#b45309;">लॉजिस्टिक्स बचत</span>',
        "<span class=" + '"badge" style="background:#fef3c7; color:#b45309;">${tDual(\'लॉजिस्टिक्स बचत\', \'Logistics Savings\')}</span>'
    ),
    (
        '<span class="badge status-optimal">ऑडिट सुरक्षित</span>',
        "<span class=" + '"badge status-optimal">${tDual(\'ऑडिट सुरक्षित\', \'Audit Verified\')}</span>'
    ),
    (
        '<th>फसल का नाम</th>',
        "<th>${tDual('फसल का नाम', 'Crop Name')}</th>"
    ),
    (
        '<th>किसान एवं मंडी</th>',
        "<th>${tDual('किसान एवं मंडी', 'Farmer & Mandi')}</th>"
    ),
    (
        '<th>कुल भुगतान राशि</th>',
        "<th>${tDual('कुल भुगतान राशि', 'Total Payout')}</th>"
    ),
    (
        '<th>पूर्ण तिथि</th>',
        "<th>${tDual('पूर्ण तिथि', 'Completion Date')}</th>"
    ),
    (
        '<th>स्थिति</th>',
        "<th>${tDual('स्थिति', 'Status')}</th>"
    ),
    # Officer Modals
    (
        "window.app.openModal(tDual('मृदा परीक्षण अधिकारी नियुक्ति', 'Assign Testing Officer'), `\n      <form onsubmit=\"window.officerPortal.submitAssignTestingOfficer('${requestId}', event)\">\n        <p style=\"font-size:0.88rem; color:#475569; margin-bottom:14px;\">\n          अनुरोध सं. <strong>${requestId}</strong> के लिए सरकारी मृदा परीक्षण प्रयोगशाला से विशेषज्ञ अधिकारी का चयन करें:\n        </p>\n        <div class=\"form-group\">\n          <label class=\"form-label\">मृदा वैज्ञानिक / परीक्षण अधिकारी चुनें:</label>",
        "window.app.openModal(tDual('मृदा परीक्षण अधिकारी नियुक्ति', 'Assign Testing Officer'), `\\n      <form onsubmit=\"window.officerPortal.submitAssignTestingOfficer('${requestId}', event)\">\\n        <p style=\"font-size:0.88rem; color:#475569; margin-bottom:14px;\">\\n          ${tDual('अनुरोध सं.', 'Request ID')} <strong>${requestId}</strong>: ${tDual('सरकारी प्रयोगशाला से विशेषज्ञ अधिकारी का चयन करें:', 'select an agronomist from Regional Agri Soil Testing Lab:')}\\n        </p>\\n        <div class=\"form-group\">\\n          <label class=\"form-label\">${tDual('मृदा वैज्ञानिक / परीक्षण अधिकारी चुनें:', 'Select Soil Testing Officer / Agronomist:')}</label>"
    ),
    (
        '<textarea class="form-control" rows="2" placeholder="GPS टैग्ड सैंपल लें, 15 सेमी गहराई से 8 स्थानों का मिश्रण बनाएं..."></textarea>',
        "<textarea class=" + '"form-control" rows="2" placeholder="${tDual(\'GPS टैग्ड सैंपल लें, 15 सेमी गहराई से 8 स्थानों का मिश्रण बनाएं...\', \'Collect GPS-tagged composite soil samples at 15cm depth from 8 spots...\')}"></textarea>'
    ),
    (
        'window.app.showToast(`मृदा परीक्षण अधिकारी ${officer.split(\' \')[0]} को फील्ड भेजा गया!`, \'success\');',
        "window.app.showToast(tDual(`मृदा परीक्षण अधिकारी ${officer.split(' ')[0]} को फील्ड भेजा गया!`, `Soil testing officer ${officer.split(' ')[0]} dispatched to the field!`), 'success');"
    ),
    (
        "window.app.openModal('48-घंटे अनिवार्य वैज्ञानिक परामर्श तैयार करें (48h Scientific Advisory)', `",
        "window.app.openModal(tDual('48-घंटे अनिवार्य वैज्ञानिक परामर्श तैयार करें (48h Scientific Advisory)', 'Formulate 48-Hour Scientific Fertilizer & Seed Advisory'), `"
    ),
    (
        '<strong>किसान:</strong> ${req.farmerName} | <strong>खेत:</strong> ${req.plotName} (${req.seedingLandAcres || 3.0} एकड़)<br>',
        "<strong>${tDual('किसान:', 'Farmer:')}</strong> ${req.farmerName} | <strong>${tDual('खेत:', 'Plot:')}</strong> ${req.plotName} (${req.seedingLandAcres || 3.0} ${tDual('एकड़', 'Acres')})<br>"
    ),
    (
        '<strong>मिट्टी रिपोर्ट:</strong> N: ${req.testReport ? req.testReport.nitrogenKgPerHa : 165} kg/ha (कम), P: ${req.testReport ? req.testReport.phosphorusKgPerHa : 18.2} kg/ha, K: ${req.testReport ? req.testReport.potassiumKgPerHa : 280} kg/ha, pH: ${req.testReport ? req.testReport.soilPh : 7.8}',
        "<strong>${tDual('मिट्टी रिपोर्ट:', 'Soil Report:')}</strong> N: ${req.testReport ? req.testReport.nitrogenKgPerHa : 165} kg/ha (${tDual('कम', 'Low')}), P: ${req.testReport ? req.testReport.phosphorusKgPerHa : 18.2} kg/ha, K: ${req.testReport ? req.testReport.potassiumKgPerHa : 280} kg/ha, pH: ${req.testReport ? req.testReport.soilPh : 7.8}"
    ),
    (
        '<label class="form-label">बीज दर (Seed Rate kg/Acre):</label>',
        "<label class=" + '"form-label">${tDual(\'बीज दर (Seed Rate kg/Acre):\', \'Seed Rate (kg/Acre):\')}</label>'
    ),
    (
        '<h5 style="color:#1b5e20; margin:12px 0 6px 0; font-size:0.92rem;">🧪 ${tDual(\'वैज्ञानिक खाद व उर्वरक मात्रा (प्रति एकड़):\', \'Fertilizer Dosage per Acre:\')}</h5>',
        "<h5 style=" + '"color:#1b5e20; margin:12px 0 6px 0; font-size:0.92rem;">🧪 ${tDual(\'वैज्ञानिक खाद व उर्वरक मात्रा (प्रति एकड़):\', \'Prescribed Fertilizer Dosage per Acre:\')}</h5>'
    ),
    (
        '<input type="text" id="advUrea" class="form-control" value="2.0 बोरी (विभाजित खुराक)" required>',
        "<input type=" + '"text" id="advUrea" class="form-control" value="${tDual(\'2.0 बोरी (विभाजित खुराक)\', \'2.0 Bags (Split application)\')}" required>'
    ),
    (
        '<label class="form-label">डीएपी की मात्रा (DAP 18:46:0 Dose):</label>',
        "<label class=" + '"form-label">${tDual(\'डीएपी की मात्रा (DAP 18:46:0 Dose):\', \'DAP (18:46:0) Dose:\')}</label>'
    ),
    (
        '<input type="text" id="advDap" class="form-control" value="1.0 बोरी (बेसल खुराक)" required>',
        "<input type=" + '"text" id="advDap" class="form-control" value="${tDual(\'1.0 बोरी (बेसल खुराक)\', \'1.0 Bag (Basal application)\')}" required>'
    ),
    (
        '<input type="text" id="advPotash" class="form-control" value="20 kg / एकड़ (बेसल)" required>',
        "<input type=" + '"text" id="advPotash" class="form-control" value="${tDual(\'20 kg / एकड़ (बेसल)\', \'20 kg / Acre (Basal)\')}" required>'
    ),
    (
        '<input type="text" id="advZinc" class="form-control" value="जिंक सल्फेट 21% - 10 kg / एकड़">',
        "<input type=" + '"text" id="advZinc" class="form-control" value="${tDual(\'जिंक सल्फेट 21% - 10 kg / एकड़\', \'Zinc Sulfate 21% - 10 kg / Acre\')}">'
    ),
    (
        '<label class="form-label">सिंचाई एवं अन्य महत्वपूर्ण निर्देश (Irrigation Advisory & Notes):</label>',
        "<label class=" + '"form-label">${tDual(\'सिंचाई एवं अन्य महत्वपूर्ण निर्देश (Irrigation Advisory & Notes):\', \'Irrigation Schedule & Special Instructions:\')}</label>'
    ),
    (
        '<textarea id="advNotes" class="form-control" rows="2">बुवाई के 21 दिन पर पहली सिंचाई करें। डीएपी और जिंक को कभी एक साथ न मिलाएं।</textarea>',
        "<textarea id=" + '"advNotes" class="form-control" rows="2">${tDual(\'बुवाई के 21 दिन पर पहली सिंचाई करें। डीएपी और जिंक को कभी एक साथ न मिलाएं।\', \'First irrigation at 21 days (CRI stage). Never mix DAP and Zinc directly.\')}</textarea>'
    ),
    (
        '<div style="background:#fef3c7; padding:10px; border-radius:var(--radius-sm); font-size:0.8rem; color:#92400e; margin-bottom:14px;">\n          ⚡ यह परामर्श किसान के मोबाइल ऐप पर तुरंत दिखाई देगा और 48h SLA पूरा माना जाएगा। किसान अनुपालन की पुष्टि करेगा।\n        </div>',
        "<div style=" + '"background:#fef3c7; padding:10px; border-radius:var(--radius-sm); font-size:0.8rem; color:#92400e; margin-bottom:14px;">\\n          ⚡ ${tDual(\'यह परामर्श किसान के मोबाइल ऐप पर तुरंत दिखाई देगा और 48h SLA पूरा माना जाएगा।\', \'This prescription will appear immediately on the farmer app, fulfilling the 48h SLA.\')}\\n        </div>'
    ),
    (
        "window.app.showToast('48-घंटे समय सीमा के भीतर वैज्ञानिक परामर्श सफलतापूर्वक जारी किया गया!', 'success');",
        "window.app.showToast(tDual('48-घंटे समय सीमा के भीतर वैज्ञानिक परामर्श सफलतापूर्वक जारी किया गया!', 'Scientific advisory successfully issued within the 48-hour SLA!'), 'success');"
    ),
    (
        '<p style="font-size:0.85rem; color:#475569; margin-bottom:12px;">जारीकर्ता: ${req.advisory.officerName} (${req.advisory.advisoryNumber})</p>',
        "<p style=" + '"font-size:0.85rem; color:#475569; margin-bottom:12px;">${tDual(\'जारीकर्ता:\', \'Issued by:\')} ${req.advisory.officerName} (${req.advisory.advisoryNumber})</p>'
    ),
    (
        '<strong>यूरिया खुराक:</strong> ${req.advisory.ureaBagsPerAcre}<br>',
        "<strong>${tDual('यूरिया खुराक:', 'Urea Dose:')}</strong> ${req.advisory.ureaBagsPerAcre}<br>"
    ),
    (
        '<strong>डीएपी खुराक:</strong> ${req.advisory.dapBagsPerAcre}<br>',
        "<strong>${tDual('डीएपी खुराक:', 'DAP Dose:')}</strong> ${req.advisory.dapBagsPerAcre}<br>"
    ),
    (
        '<strong>पोटाश:</strong> ${req.advisory.potashBagsPerAcre}<br>',
        "<strong>${tDual('पोटाश:', 'Potash:')}</strong> ${req.advisory.potashBagsPerAcre}<br>"
    ),
    (
        '<strong>जिंक:</strong> ${req.advisory.zincSulfateDose}',
        "<strong>${tDual('जिंक:', 'Zinc:')}</strong> ${req.advisory.zincSulfateDose}"
    ),
    (
        '<div style="margin-top:10px; font-size:0.82rem; background:#f8fafc; padding:10px; border-radius:6px;"><strong>निर्देश:</strong> ${req.advisory.scientificRemarks}</div>',
        "<div style=" + '"margin-top:10px; font-size:0.82rem; background:#f8fafc; padding:10px; border-radius:6px;"><strong>${tDual(\'निर्देश:\', \'Instructions:\')}</strong> ${req.advisory.scientificRemarks}</div>'
    ),
    (
        '<button class="btn btn-secondary" onclick="window.app.closeModal()">बंद करें</button>',
        "<button class=" + '"btn btn-secondary" onclick="window.app.closeModal()">${tDual(\'बंद करें\', \'Close\')}</button>'
    ),
    (
        '<button type="button" class="btn btn-secondary" onclick="window.app.closeModal()">रद्द करें</button>',
        "<button type=" + '"button" class="btn btn-secondary" onclick="window.app.closeModal()">${tDual(\'रद्द करें\', \'Cancel\')}</button>'
    ),
    (
        "window.app.openModal(tDual('फसल गुणवत्ता निरीक्षक नियुक्ति', 'Assign Crop Quality Assessor'), `\n      <form onsubmit=\"window.officerPortal.submitAssignCropInspector('${cropId}', event)\">\n        <p style=\"font-size:0.88rem; color:#475569; margin-bottom:14px;\">\n          फसल कटाई लॉट सं. <strong>${cropId}</strong> की गुणवत्ता परीक्षण हेतु अधिकारी नियुक्त करें:\n        </p>\n        <div class=\"form-group\">\n          <label class=\"form-label\">गुणवत्ता निरीक्षक का नाम:</label>",
        "window.app.openModal(tDual('फसल गुणवत्ता निरीक्षक नियुक्ति', 'Assign Crop Quality Assessor'), `\\n      <form onsubmit=\"window.officerPortal.submitAssignCropInspector('${cropId}', event)\">\\n        <p style=\"font-size:0.88rem; color:#475569; margin-bottom:14px;\">\\n          ${tDual('फसल कटाई लॉट सं.', 'Crop Lot ID')} <strong>${cropId}</strong>: ${tDual('गुणवत्ता परीक्षण हेतु अधिकारी नियुक्त करें:', 'assign an official grading inspector:')}\\n        </p>\\n        <div class=\"form-group\">\\n          <label class=\"form-label\">${tDual('गुणवत्ता निरीक्षक का नाम:', 'Select Quality Inspector:')}</label>"
    ),
    (
        '<button type="submit" class="btn btn-primary">परीक्षक नियुक्त करें</button>',
        "<button type=" + '"submit" class="btn btn-primary">${tDual(\'परीक्षक नियुक्त करें\', \'Assign Inspector\')}</button>'
    ),
    (
        "window.app.showToast(`गुणवत्ता परीक्षक ${inspector.split(' ')[0]} नियुक्त किए गए!`, 'success');",
        "window.app.showToast(tDual(`गुणवत्ता परीक्षक ${inspector.split(' ')[0]} नियुक्त किए गए!`, `Quality inspector ${inspector.split(' ')[0]} assigned!`), 'success');"
    ),
    (
        "window.app.openModal(tDual('सरकारी खरीद दर निर्धारण', 'Procurement Rate Quotation Studio'), `\n      <form onsubmit=\"window.officerPortal.submitRateQuote('${cropId}', event)\">\n        <div style=\"background:#f1f8f3; padding:12px; border-radius:var(--radius-md); margin-bottom:14px; font-size:0.84rem;\">\n          <strong>फसल:</strong> ${cr.cropName} (${cr.variety || 'WH-1105'}) | <strong>मात्रा:</strong> ${qty} क्विंटल<br>\n          <strong>मृदा अनुपालन स्थिति:</strong> <span class=\"badge status-optimal\">✅ प्रमाणित मृदा अनुपालन (+₹50/Q बोनस पात्र)</span>\n        </div>",
        "window.app.openModal(tDual('सरकारी खरीद दर निर्धारण', 'Procurement Rate Quotation Studio'), `\\n      <form onsubmit=\"window.officerPortal.submitRateQuote('${cropId}', event)\">\\n        <div style=\"background:#f1f8f3; padding:12px; border-radius:var(--radius-md); margin-bottom:14px; font-size:0.84rem;\">\\n          <strong>${tDual('फसल:', 'Crop:')}</strong> ${cr.cropName} (${cr.variety || 'WH-1105'}) | <strong>${tDual('मात्रा:', 'Quantity:')}</strong> ${qty} ${tDual('क्विंटल', 'Quintals')}<br>\\n          <strong>${tDual('मृदा अनुपालन स्थिति:', 'Soil Compliance Status:')}</strong> <span class=\"badge status-optimal\">✅ ${tDual('प्रमाणित मृदा अनुपालन (+₹50/Q बोनस पात्र)', 'Certified Soil Compliance (+₹50/Q Bonus Eligible)')}</span>\\n        </div>"
    ),
    (
        '<label class="form-label">न्यूनतम समर्थन मूल्य (Base MSP ₹/Q):</label>',
        "<label class=" + '"form-label">${tDual(\'न्यूनतम समर्थन मूल्य (Base MSP ₹/Q):\', \'Base Minimum Support Price (Base MSP ₹/Q):\')}</label>'
    ),
    (
        '<label class="form-label">मृदा स्वास्थ्य अनुपालन प्रोत्साहन (₹/Q):</label>',
        "<label class=" + '"form-label">${tDual(\'मृदा स्वास्थ्य अनुपालन प्रोत्साहन (₹/Q):\', \'Soil Compliance Bonus (₹/Q):\')}</label>'
    ),
    (
        '<div id="liveQuoteTotal" style="font-size:2.2rem; font-weight:800; color:#facc15; font-family:var(--font-mono);">₹${defaultTotal} / क्विंटल</div>',
        "<div id=" + '"liveQuoteTotal" style="font-size:2.2rem; font-weight:800; color:#facc15; font-family:var(--font-mono);">₹${defaultTotal} / ${tDual(\'क्विंटल\', \'Quintal\')}</div>'
    ),
    (
        '<div style="font-size:0.8rem; color:#e2e8f0;">कुल लॉट मूल्य (${qty} क्विंटल): <strong id="liveLotTotal">₹${(defaultTotal * qty).toLocaleString(\'en-IN\')}</strong></div>',
        "<div style=" + '"font-size:0.8rem; color:#e2e8f0;">${tDual(\'कुल लॉट मूल्य\', \'Total Lot Value\')} (${qty} ${tDual(\'क्विंटल\', \'Quintals\')}): <strong id="liveLotTotal">₹${(defaultTotal * qty).toLocaleString(\'en-IN\')}</strong></div>'
    ),
    (
        'if (totalEl) totalEl.innerText = `₹${total} / क्विंटल`;',
        "if (totalEl) totalEl.innerText = `₹${total} / ${tDual('क्विंटल', 'Quintal')}`;"
    ),
    (
        "window.app.showToast(window.tDual('सरकारी खरीद दर किसान ऐप पर सफलतापूर्वक प्रकाशित हुई!', 'Procurement rate declared to farmer app!'), 'success');",
        "window.app.showToast(window.tDual('सरकारी खरीद दर किसान ऐप पर सफलतापूर्वक प्रकाशित हुई!', 'Official procurement rate successfully published to farmer app!'), 'success');"
    ),
    (
        'अभी कोई खरीद इतिहास नहीं है। तुलाई व बिल पूर्ण होने पर विवरण यहाँ सुरक्षित रहेगा।',
        "${tDual('अभी कोई खरीद इतिहास नहीं है। तुलाई व बिल पूर्ण होने पर विवरण यहाँ सुरक्षित रहेगा।', 'No procurement history records yet. Completed weighments & bills will be archived here.')}"
    ),
    (
        "<td>${item.farmerName || '—'} <br><small style=\"color:#64748b;\">${item.mandiLocation || 'नई अनाज मंडी, रोहतक'}</small></td>",
        "<td>${item.farmerName || '—'} <br><small style=\"color:#64748b;\">${item.mandiLocation || tDual('नई अनाज मंडी, रोहतक', 'New Grain Market, Rohtak')}</small></td>"
    ),
    (
        '<td><span class="badge status-optimal">✓ खरीद संपन्न</span></td>',
        "<td><span class=" + '"badge status-optimal">✓ ${tDual(\'खरीद संपन्न\', \'Procurement Completed\')}</span></td>'
    ),

    # Testing Team Portal Hero & Elements
    (
        '<p>परीक्षक: <strong>डॉ. वी. के. वर्मा (वरिष्ठ मृदा विशेषज्ञ)</strong> | क्षेत्रीय कृषि विश्लेषण एवं मृदा परीक्षण लैब, रोहतक (हरियाणा) | मानकीकृत NPK, pH एवं पोषक तत्व विश्लेषण सेल</p>',
        "<p>${tDual('परीक्षक: <strong>डॉ. वी. के. वर्मा (वरिष्ठ मृदा विशेषज्ञ)</strong> | क्षेत्रीय कृषि विश्लेषण एवं मृदा परीक्षण लैब, रोहतक (हरियाणा) | मानकीकृत NPK, pH एवं पोषक तत्व विश्लेषण सेल', 'Tester: <strong>Dr. V. K. Verma (Chief Soil Chemist)</strong> | Regional Agri QA & Soil Testing Laboratory, Rohtak (Haryana) | Standardized NPK, pH & Nutrient Analysis Cell')}</p>"
    ),
    (
        '<div class="lbl">फील्ड रूट क्लस्टर (20km Clusters)</div>',
        "<div class=" + '"lbl">${tDual(\'फील्ड रूट क्लस्टर (20km Clusters)\', \'Field Route Clusters (20km)\')}</div>'
    ),
    (
        '<th>किसान एवं खेत विवरण</th>',
        "<th>${tDual('किसान एवं खेत विवरण', 'Farmer & Plot Details')}</th>"
    ),
    (
        '<th>प्रस्तावित फसल / उप-विभाजन</th>',
        "<th>${tDual('प्रस्तावित फसल / उप-विभाजन', 'Proposed Crop / Parcels')}</th>"
    ),
    (
        '<small style="color:#64748b;">${s.plotName} (बुवाई: ${s.seedingLandAcres || 3.5} / कुल: ${s.totalOwnedLandAcres || 5.0} एकड़)</small>',
        "<small style=" + '"color:#64748b;">${s.plotName} (${tDual(\'बुवाई:\', \'Seeding:\')} ${s.seedingLandAcres || 3.5} / ${tDual(\'कुल:\', \'Total:\')} ${s.totalOwnedLandAcres || 5.0} ${tDual(\'एकड़\', \'Acres\')})</small>'
    ),
    (
        '📄 जमाबंदी PDF देखें',
        "📄 ${tDual('जमाबंदी PDF देखें', 'View Jamabandi PDF')}"
    ),
    (
        "${s.testReport ? '✅ परीक्षण रिपोर्ट तैयार' : '⏳ नमूना प्रक्रिया में'}",
        "${s.testReport ? tDual('✅ परीक्षण रिपोर्ट तैयार', '✅ Test Report Ready') : tDual('⏳ नमूना प्रक्रिया में', '⏳ Sample in Testing')}"
    ),
    (
        'डिजिटल स्वास्थ्य कार्ड देखें',
        "${tDual('डिजिटल स्वास्थ्य कार्ड देखें', 'View Digital SHC')}"
    ),
    (
        '🔬 NPK व pH रिपोर्ट दर्ज करें',
        "🔬 ${tDual('NPK व pH रिपोर्ट दर्ज करें', 'Enter NPK & pH Results')}"
    ),
    (
        '<div style="font-size:0.8rem; color:#64748b; margin-top:4px;">किसान द्वारा नया मिट्टी परीक्षण अनुरोध भेजे जाने के बाद सैंपल यहाँ NPK व pH परीक्षण हेतु उपलब्ध होगा।</div>',
        "<div style=" + '"font-size:0.8rem; color:#64748b; margin-top:4px;">${tDual(\'किसान द्वारा नया मिट्टी परीक्षण अनुरोध भेजे जाने के बाद सैंपल यहाँ NPK व pH परीक्षण हेतु उपलब्ध होगा।\', \'When farmers submit pre-sowing soil test requests, samples will appear here for NPK & pH testing.\')}</div>'
    ),
    (
        '<h3><span>🗺️</span> दैनिक 20 किमी फील्ड निरीक्षण क्लस्टर (20 km Daily Route Clustering)</h3>',
        "<h3><span>🗺️</span> ${tDual('दैनिक 20 किमी फील्ड निरीक्षण क्लस्टर (20 km Daily Route Clustering)', '20 km Daily Route Sampling Clusters')}</h3>"
    ),
    (
        '<small style="color:#64748b;">एक दिन में 20 किमी परिधि के एकाधिक किसानों के खेत का कुशल निरीक्षण व नमूना संग्रह।</small>',
        "<small style=" + '"color:#64748b;">${tDual(\'एक दिन में 20 किमी परिधि के एकाधिक किसानों के खेत का कुशल निरीक्षण व नमूना संग्रह।\', \'Optimized daily route clusters across multiple farms within a 20 km radius for rapid sample intake.\')}</small>'
    ),
    (
        '<span class="badge" style="background:#e0f2fe; color:#0369a1;">दैनिक यात्रा इष्टतमीकरण</span>',
        "<span class=" + '"badge" style="background:#e0f2fe; color:#0369a1;">${tDual(\'दैनिक यात्रा इष्टतमीकरण\', \'Route Optimization\')}</span>'
    ),
    (
        '<span class="badge status-optimal">लैब रिकॉर्ड्स</span>',
        "<span class=" + '"badge status-optimal">${tDual(\'लैब रिकॉर्ड्स\', \'Lab Certified\')}</span>'
    ),
    (
        '<th>प्रमाणपत्र प्रकार</th>',
        "<th>${tDual('प्रमाणपत्र प्रकार', 'Certificate Type')}</th>"
    ),
    (
        '<th>संदर्भ / बिल सं.</th>',
        "<th>${tDual('संदर्भ / बिल सं.', 'Reference / Certificate No')}</th>"
    ),
    (
        '<th>किसान एवं गाँव</th>',
        "<th>${tDual('किसान एवं गाँव', 'Farmer & Village')}</th>"
    ),
    (
        '<th>फसल / नमूना</th>',
        "<th>${tDual('फसल / नमूना', 'Crop / Sample')}</th>"
    ),
    (
        '<th>मात्रा / ग्रेड</th>',
        "<th>${tDual('मात्रा / ग्रेड', 'Parameters')}</th>"
    ),
    (
        '<th>निरीक्षण तिथि</th>',
        "<th>${tDual('निरीक्षण तिथि', 'Test Date')}</th>"
    ),
    (
        '<strong>नमूना सं:</strong> ${requestId} | <strong>किसान:</strong> ${s.farmerName} | <strong>खेत:</strong> ${s.plotName}',
        "<strong>${tDual('नमूना सं:', 'Sample ID:')}</strong> ${requestId} | <strong>${tDual('किसान:', 'Farmer:')}</strong> ${s.farmerName} | <strong>${tDual('खेत:', 'Plot:')}</strong> ${s.plotName}"
    ),
    (
        '<option value="Alluvial Clay Loam (दोमट मिट्टी)">Alluvial Clay Loam (दोमट मिट्टी)</option>',
        "<option value=" + '"Alluvial Clay Loam (दोमट मिट्टी)">${tDual(\'Alluvial Clay Loam (दोमट मिट्टी)\', \'Alluvial Clay Loam (Loamy Soil)\')}</option>'
    ),
    (
        '<option value="Sandy Loam (बलुई दोमट)">Sandy Loam (बलुई दोमट)</option>',
        "<option value=" + '"Sandy Loam (बलुई दोमट)">${tDual(\'Sandy Loam (बलुई दोमट)\', \'Sandy Loam (Sandy Soil)\')}</option>'
    ),
    (
        '<option value="Black Cotton Soil (काली मिट्टी)">Black Cotton Soil (काली मिट्टी)</option>',
        "<option value=" + '"Black Cotton Soil (काली मिट्टी)">${tDual(\'Black Cotton Soil (काली मिट्टी)\', \'Black Cotton Soil (Clayey)\')}</option>'
    ),
    (
        '<label class="form-label">उपलब्ध नाइट्रोजन N (kg/ha):</label>',
        "<label class=" + '"form-label">${tDual(\'उपलब्ध नाइट्रोजन N (kg/ha):\', \'Available Nitrogen N (kg/ha):\')}</label>'
    ),
    (
        '<small style="color:#c2410c;">सामान्य: >280 kg/ha</small>',
        "<small style=" + '"color:#c2410c;">${tDual(\'सामान्य: >280 kg/ha\', \'Optimal: >280 kg/ha\')}</small>'
    ),
    (
        '<label class="form-label">उपलब्ध फॉस्फोरस P (kg/ha):</label>',
        "<label class=" + '"form-label">${tDual(\'उपलब्ध फॉस्फोरस P (kg/ha):\', \'Available Phosphorus P (kg/ha):\')}</label>'
    ),
    (
        '<small style="color:#059669;">सामान्य: 23-56 kg/ha</small>',
        "<small style=" + '"color:#059669;">${tDual(\'सामान्य: 23-56 kg/ha\', \'Optimal: 23-56 kg/ha\')}</small>'
    ),
    (
        '<label class="form-label">उपलब्ध पोटाश K (kg/ha):</label>',
        "<label class=" + '"form-label">${tDual(\'उपलब्ध पोटाश K (kg/ha):\', \'Available Potash K (kg/ha):\')}</label>'
    ),
    (
        '<small style="color:#059669;">सामान्य: 145-335 kg/ha</small>',
        "<small style=" + '"color:#059669;">${tDual(\'सामान्य: 145-335 kg/ha\', \'Optimal: 145-335 kg/ha\')}</small>'
    ),
    (
        '<label class="form-label">जैविक कार्बन (Organic Carbon %):</label>',
        "<label class=" + '"form-label">${tDual(\'जैविक कार्बन (Organic Carbon %):\', \'Organic Carbon (%):\')}</label>'
    ),
    (
        '<label class="form-label">जिंक स्तर (Zinc - ppm):</label>',
        "<label class=" + '"form-label">${tDual(\'जिंक स्तर (Zinc - ppm):\', \'Zinc Level (ppm):\')}</label>'
    ),
    (
        '<div style="background:#e0f2fe; padding:10px; border-radius:var(--radius-sm); font-size:0.8rem; color:#0369a1; margin-bottom:14px;">\n          ⏱️ जैसे ही आप यह रिपोर्ट अपलोड करेंगे, खरीद अधिकारी के पास 48 कार्य घंटों का उलटा काउंटडाउन सक्रिय हो जाएगा।\n        </div>',
        "<div style=" + '"background:#e0f2fe; padding:10px; border-radius:var(--radius-sm); font-size:0.8rem; color:#0369a1; margin-bottom:14px;">\\n          ⏱️ ${tDual(\'जैसे ही आप यह रिपोर्ट अपलोड करेंगे, खरीद अधिकारी के पास 48 कार्य घंटों का उलटा काउंटडाउन सक्रिय हो जाएगा।\', \'Uploading this lab report starts the mandatory 48-working-hour SLA advisory countdown for the procurement officer.\')}\\n        </div>'
    ),
    (
        "window.app.showToast('मृदा परीक्षण रिपोर्ट सफलतापूर्वक अपलोड हुई! 48h SLA शुरू।', 'success');",
        "window.app.showToast(tDual('मृदा परीक्षण रिपोर्ट सफलतापूर्वक अपलोड हुई! 48h SLA शुरू।', 'Soil test report successfully uploaded! 48h SLA countdown started.'), 'success');"
    ),
    (
        '<h4>प्रमाणपत्र सं: ${s.testReport.certificateNo}</h4>',
        "<h4>${tDual('प्रमाणपत्र सं:', 'Certificate No:')} ${s.testReport.certificateNo}</h4>"
    ),
    (
        '<p style="font-size:0.85rem; color:#64748b; margin-bottom:12px;">परीक्षण तिथि: ${new Date(s.testReport.testDate).toLocaleDateString()}</p>',
        "<p style=" + '"font-size:0.85rem; color:#64748b; margin-bottom:12px;">${tDual(\'परीक्षण तिथि:\', \'Test Date:\')} ${new Date(s.testReport.testDate).toLocaleDateString()}</p>'
    ),
    (
        '<span class="param-status status-deficient">कम</span>',
        "<span class=" + '"param-status status-deficient">${tDual(\'कम\', \'Low\')}</span>'
    ),
    (
        '<span class="param-status status-medium">मध्यम</span>',
        "<span class=" + '"param-status status-medium">${tDual(\'मध्यम\', \'Medium\')}</span>'
    ),
    (
        '<span class="param-status status-optimal">पर्याप्त</span>',
        "<span class=" + '"param-status status-optimal">${tDual(\'पर्याप्त\', \'Optimal\')}</span>'
    ),
    (
        '<div class="param-name">मृदा pH</div>',
        "<div class=" + '"param-name">${tDual(\'मृदा pH\', \'Soil pH\')}</div>'
    ),
    (
        '<span class="param-status status-optimal">तटस्थ</span>',
        "<span class=" + '"param-status status-optimal">${tDual(\'तटस्थ\', \'Neutral\')}</span>'
    ),
    (
        'अभी कोई ऐतिहासिक मृदा स्वास्थ्य कार्ड रिकॉर्ड नहीं है।',
        "${tDual('अभी कोई ऐतिहासिक मृदा स्वास्थ्य कार्ड रिकॉर्ड नहीं है।', 'No historical Soil Health Card records yet.')}"
    ),
    (
        '<td><span class="badge status-optimal">SHC मृदा कार्ड</span></td>',
        "<td><span class=" + '"badge status-optimal">${tDual(\'SHC मृदा कार्ड\', \'SHC Soil Card\')}</span></td>'
    ),
    (
        '<td>${item.farmerName} <br><small style="color:#64748b;">खेत: ${item.plotName}</small></td>',
        "<td>${item.farmerName} <br><small style=" + '"color:#64748b;">${tDual(\'खेत:\', \'Plot:\')} ${item.plotName}</small></td>'
    ),
    (
        '<td><span class="badge status-optimal">✓ NPK व pH प्रमाणित</span></td>',
        "<td><span class=" + '"badge status-optimal">✓ ${tDual(\'NPK व pH प्रमाणित\', \'NPK & pH Certified\')}</span></td>'
    ),

    # Warehouse Operator Portal Hero & Elements
    (
        '<h2><span>🏬</span> मंडी गेट, तुलाई एवं भंडारण नियंत्रण कक्ष (Mandi Operations & Silos)</h2>',
        "<h2><span>🏬</span> ${tDual('मंडी गेट, तुलाई एवं भंडारण नियंत्रण कक्ष (Mandi Operations & Silos)', 'Mandi Operations, Weighbridge & Silos Control')}</h2>"
    ),
    (
        '<p>ऑपरेटर: <strong>श्री रविन्द्र नाथ (मंडी सचिव / गोदाम प्रबंधक)</strong> | कृषि उपज मंडी समिति, नई अनाज मंडी, दिल्ली रोड, रोहतक (हरियाणा) | लाइव कतार एवं इलेक्ट्रॉनिक तुलाई तंत्र</p>',
        "<p>${tDual('ऑपरेटर: <strong>श्री रविन्द्र नाथ (मंडी सचिव / गोदाम प्रबंधक)</strong> | कृषि उपज मंडी समिति, नई अनाज मंडी, दिल्ली रोड, रोहतक (हरियाणा) | लाइव कतार एवं इलेक्ट्रॉनिक तुलाई तंत्र', 'Operator: <strong>Sh. Ravindra Nath (Mandi Secretary / Warehouse In-Charge)</strong> | APMC New Grain Market, Delhi Road, Rohtak (Haryana) | Live Queue & Automated Weighbridge')}</p>"
    ),
    (
        '<span style="font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; color:#94a3b8;">मंडी प्रवेश द्वार स्थिति:</span>',
        "<span style=" + '"font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; color:#94a3b8;">${tDual(\'मंडी प्रवेश द्वार स्थिति:\', \'Mandi Gate Status:\')}</span>'
    ),
    (
        '<th>टोकन #</th>',
        "<th>${tDual('टोकन #', 'Token #')}</th>"
    ),
    (
        '<th>वाहन विवरण</th>',
        "<th>${tDual('वाहन विवरण', 'Vehicle Details')}</th>"
    ),
    (
        '<th>कतार स्थिति</th>',
        "<th>${tDual('कतार स्थिति', 'Queue Status')}</th>"
    ),
    (
        '<th>तुलाई व निपटान कार्यवाही</th>',
        "<th>${tDual('तुलाई व निपटान कार्यवाही', 'Weighment & Settlement Action')}</th>"
    ),
    (
        "${t.queuePosition > 0 ? `<br><small style=\"color:#64748b;\">(लाइन में ${t.queuePosition})</small>` : ''}",
        "${t.queuePosition > 0 ? `<br><small style=\"color:#64748b;\">(${tDual('लाइन में', 'In queue:')} ${t.queuePosition})</small>` : ''}"
    ),
    (
        '<div style="font-size:0.8rem; color:#64748b; margin-top:4px;">किसान द्वारा नई अनाज मंडी रोहतक हेतु टोकन बुक करने पर वह यहाँ कतार में प्रदर्शित होगा।</div>',
        "<div style=" + '"font-size:0.8rem; color:#64748b; margin-top:4px;">${tDual(\'किसान द्वारा नई अनाज मंडी रोहतक हेतु टोकन बुक करने पर वह यहाँ कतार में प्रदर्शित होगा।\', \'When a farmer books an e-mandi gate token for Rohtak, it will appear here in the live sequence.\')}</div>'
    ),
    (
        '<div style="margin-top:14px; background:#f8fafc; padding:10px; border-radius:var(--radius-sm); font-size:0.78rem; color:#64748b;">\n              💡 गेहूं साइलो अल्फा में 1260 मीट्रिक टन क्षमता शेष है। नई आवक को साइलो बीटा में डायवर्ट किया जा सकता है।\n            </div>',
        "<div style=" + '"margin-top:14px; background:#f8fafc; padding:10px; border-radius:var(--radius-sm); font-size:0.78rem; color:#64748b;">\\n              💡 ${tDual(\'गेहूं साइलो अल्फा में 1260 मीट्रिक टन क्षमता शेष है। नई आवक को साइलो बीटा में डायवर्ट किया जा सकता है।\', \'Wheat Silo Alpha has remaining capacity. Incoming tractor loads can be routed to Silo Beta.\')}\\n            </div>'
    ),
    (
        '<h3><span>📝</span> गोदाम आवक एवं विक्रय रजिस्टर (Latest 20 Entries - In & Out)</h3>',
        "<h3><span>📝</span> ${tDual('गोदाम आवक एवं विक्रय रजिस्टर (Latest 20 Entries - In & Out)', 'Warehouse Inward & Weighment Ledger (Latest 20 Entries)')}</h3>"
    ),
    (
        '<span class="badge" style="background:#fef3c7; color:#b45309;">डैशबोर्ड अधिकतम 20 प्रविष्टियां</span>',
        "<span class=" + '"badge" style="background:#fef3c7; color:#b45309;">${tDual(\'डैशबोर्ड अधिकतम 20 प्रविष्टियां\', \'Dashboard Max 20 Entries\')}</span>'
    ),
    (
        '<th>टोकन / बिल सं.</th>',
        "<th>${tDual('टोकन / बिल सं.', 'Token / Bill No')}</th>"
    ),
    (
        '<th>वाहन सं.</th>',
        "<th>${tDual('वाहन सं.', 'Vehicle No')}</th>"
    ),
    (
        '<th>मात्रा / वजन</th>',
        "<th>${tDual('मात्रा / वजन', 'Quantity / Weight')}</th>"
    ),
    (
        '<th>तारीख व समय</th>',
        "<th>${tDual('तारीख व समय', 'Date & Time')}</th>"
    ),
    (
        '<h3><span>🏛️</span> गोदाम ऐतिहासिक लेखा (Warehouse History Tab - >20 Entries)</h3>',
        "<h3><span>🏛️</span> ${tDual('गोदाम ऐतिहासिक लेखा (Warehouse History Tab - >20 Entries)', 'Warehouse Archived History (>20 Entries)')}</h3>"
    ),
    (
        '<small style="color:#64748b;">20 से पुरानी सभी आवक व विक्रय प्रविष्टियां तिथि अनुसार यहाँ सुरक्षित रहती हैं।</small>',
        "<small style=" + '"color:#64748b;">${tDual(\'20 से पुरानी सभी आवक व विक्रय प्रविष्टियां तिथि अनुसार यहाँ सुरक्षित रहती हैं।\', \'All historical inward and outward transactions older than the latest 20 entries are archived here.\')}</small>'
    ),
    (
        '<th>बिल / संदर्भ सं.</th>',
        "<th>${tDual('बिल / संदर्भ सं.', 'Bill / Ref No')}</th>"
    ),
    (
        '<th>वाहन विवरण</th>',
        "<th>${tDual('वाहन विवरण', 'Vehicle Details')}</th>"
    ),
    (
        '<th>वजन एवं राशि</th>',
        "<th>${tDual('वजन एवं राशि', 'Weight & Amount')}</th>"
    ),
    (
        '<th>दिनांक व समय</th>',
        "<th>${tDual('दिनांक व समय', 'Date & Time')}</th>"
    ),
    (
        '<th>अंतिम स्थिति</th>',
        "<th>${tDual('अंतिम स्थिति', 'Final Status')}</th>"
    ),
    (
        '🧾 तुलाई पर्ची व DBT वाउचर',
        "🧾 ${tDual('तुलाई पर्ची व DBT वाउचर', 'Weighment Slip & DBT Voucher')}"
    ),
    (
        "window.app.showToast(`टोकन स्थिति अपडेट: ${this.getStatusLabel(nextStatus)}`, 'info');",
        "window.app.showToast(tDual(`टोकन स्थिति अपडेट: ${this.getStatusLabel(nextStatus)}`, `Token status updated: ${this.getStatusLabel(nextStatus)}`), 'info');"
    ),
    (
        "window.kisanVoiceBot.speak(`ध्यान दें! टोकन नंबर ${nextWaiting.tokenNumber}, गाड़ी नंबर ${nextWaiting.vehicleNumber}, किसान भाई ${nextWaiting.farmerName}, कृपया गेट नंबर 2 पर धर्मकांटे के लिए आगे बढ़ें।`);",
        "window.kisanVoiceBot.speak(window.kisanI18n && window.kisanI18n.lang === 'hi' ? `ध्यान दें! टोकन नंबर ${nextWaiting.tokenNumber}, गाड़ी नंबर ${nextWaiting.vehicleNumber}, किसान भाई ${nextWaiting.farmerName}, कृपया गेट नंबर 2 पर आगे बढ़ें।` : `Attention! Token number ${nextWaiting.tokenNumber}, vehicle number ${nextWaiting.vehicleNumber}, farmer ${nextWaiting.farmerName}, please proceed to Gate 2 for weighbridge entry.`);"
    ),
    (
        "window.app.showToast(`📢 टोकन #${nextWaiting.tokenNumber} (${nextWaiting.farmerName}) को प्रवेश के लिए पुकारा गया!`, 'success');",
        "window.app.showToast(tDual(`📢 टोकन #${nextWaiting.tokenNumber} (${nextWaiting.farmerName}) को प्रवेश के लिए पुकारा गया!`, `📢 Token #${nextWaiting.tokenNumber} (${nextWaiting.farmerName}) called to Gate 2!`), 'success');"
    ),
    (
        "window.app.showToast('वर्तमान में कतार में कोई प्रतीक्षारत वाहन नहीं है।', 'info');",
        "window.app.showToast(tDual('वर्तमान में कतार में कोई प्रतीक्षारत वाहन नहीं है।', 'No waiting vehicles in queue at present.'), 'info');"
    ),
    (
        'वाहन <strong>${t.vehicleNumber}</strong> (${t.vehicleType}) धर्मकांटा #1 पर है। कुल सकल वजन दर्ज करें:',
        "${tDual('वाहन', 'Vehicle')} <strong>${t.vehicleNumber}</strong> (${t.vehicleType}) ${tDual('धर्मकांटा #1 पर है। कुल सकल वजन दर्ज करें:', 'is on Weighbridge #1. Enter total gross weight (vehicle + crop) in kg:')}"
    ),
    (
        '<button type="submit" class="btn btn-primary">सकल वजन दर्ज करें</button>',
        "<button type=" + '"submit" class="btn btn-primary">${tDual(\'सकल वजन दर्ज करें\', \'Save Gross Weight\')}</button>'
    ),
    (
        "window.app.openModal('अंतिम तुलाई - खाली वाहन (Tare Weighment & Payment)', `",
        "window.app.openModal(tDual('अंतिम तुलाई - खाली वाहन (Tare Weighment & Payment)', 'Tare Weighment - Empty Vehicle & Payment Voucher'), `"
    ),
    (
        '<button type="submit" class="btn btn-saffron">तुलाई संपन्न व भुगतान वाउचर जारी करें</button>',
        "<button type=" + '"submit" class="btn btn-saffron">${tDual(\'तुलाई संपन्न व भुगतान वाउचर जारी करें\', \'Complete Weighment & Issue DBT Voucher\')}</button>'
    ),
    (
        "window.app.showToast('तुलाई संपन्न! किसान के खाते में DBT भुगतान सलाह प्रेषित।', 'success');",
        "window.app.showToast(tDual('तुलाई संपन्न! किसान के खाते में DBT भुगतान सलाह प्रेषित।', 'Weighment completed! Electronic DBT payment advice dispatched.'), 'success');"
    ),
    (
        "window.app.openModal('इलेक्ट्रॉनिक मंडी तुलाई पर्ची एवं भुगतान पावती (E-Mandi Weighment Slip)', `",
        "window.app.openModal(tDual('इलेक्ट्रॉनिक मंडी तुलाई पर्ची एवं भुगतान पावती (E-Mandi Weighment Slip)', 'Electronic Weighment Slip & DBT Payment Receipt'), `"
    ),
    (
        '<p style="font-size:0.76rem; color:#64748b;">(हरियाणा राज्य कृषि विपणन बोर्ड - डिजिटल खरीद व ई-तुलाई पावती)</p>',
        "<p style=" + '"font-size:0.76rem; color:#64748b;">${tDual(\'(हरियाणा राज्य कृषि विपणन बोर्ड - डिजिटल खरीद व ई-तुलाई पावती)\', \'(Haryana State Agricultural Marketing Board - Official Digital Procurement Slip)\')}</p>'
    ),
    (
        '<span style="font-weight:700; color:#1d4ed8; font-family:var(--font-mono);">बिल सं: ${billNo}</span>',
        "<span style=" + '"font-weight:700; color:#1d4ed8; font-family:var(--font-mono);">${tDual(\'बिल सं:\', \'Bill No:\')} ${billNo}</span>'
    ),
    (
        '<span style="font-weight:700; color:#15803d; font-family:var(--font-mono);">पावती सं: ${voucher}</span>',
        "<span style=" + '"font-weight:700; color:#15803d; font-family:var(--font-mono);">${tDual(\'पावती सं:\', \'Receipt Voucher No:\')} ${voucher}</span>'
    ),
    (
        '<div><strong>किसान का नाम:</strong> ${t.farmerName}</div>',
        "<div><strong>${tDual('किसान का नाम:', 'Farmer Name:')}</strong> ${t.farmerName}</div>"
    ),
    (
        '<div><strong>टोकन सं:</strong> #${t.tokenNumber} (${t.id})</div>',
        "<div><strong>${tDual('टोकन सं:', 'Token No:')}</strong> #${t.tokenNumber} (${t.id})</div>"
    ),
    (
        '<div><strong>वाहन सं:</strong> ${t.vehicleNumber}</div>',
        "<div><strong>${tDual('वाहन सं:', 'Vehicle No:')}</strong> ${t.vehicleNumber}</div>"
    ),
    (
        '<div><strong>फसल:</strong> ${t.cropName}</div>',
        "<div><strong>${tDual('फसल:', 'Crop:')}</strong> ${t.cropName}</div>"
    ),
    (
        '<div><strong>दिनांक:</strong> ${new Date().toLocaleDateString(\'hi-IN\')}</div>',
        "<div><strong>${tDual('दिनांक:', 'Date:')}</strong> ${new Date().toLocaleDateString()}</div>"
    ),
    (
        '<div><strong>समय:</strong> ${new Date().toLocaleTimeString()}</div>',
        "<div><strong>${tDual('समय:', 'Time:')}</strong> ${new Date().toLocaleTimeString()}</div>"
    ),
    (
        '<td style="padding:8px; text-align:right; color:#166534;">${netKg} kg (${netQuintal} क्विंटल)</td>',
        "<td style=" + '"padding:8px; text-align:right; color:#166534;">${netKg} kg (${netQuintal} ${tDual(\'क्विंटल\', \'Quintals\')})</td>'
    ),
    (
        '<td style="padding:6px; text-align:right;">₹${rate} / क्विंटल</td>',
        "<td style=" + '"padding:6px; text-align:right;">₹${rate} / ${tDual(\'क्विंटल\', \'Quintal\')}</td>'
    ),
    (
        '💳 <strong>भुगतान गंतव्य खाता:</strong> ${bank && bank.bankName ? bank.bankName : \'—\'} | खाता सं: •••• ${bank && bank.accountNo ? String(bank.accountNo).slice(-4) : \'—\'} (IFSC: ${bank && bank.ifscCode ? bank.ifscCode : \'—\'}) | लेखा अधिकारी (APMC रोहतक) द्वारा सीधे DBT जारी किया जा रहा है।',
        "💳 <strong>${tDual('भुगतान गंतव्य खाता:', 'Beneficiary Bank Account:')}</strong> ${bank && bank.bankName ? bank.bankName : '—'} | ${tDual('खाता सं:', 'A/C No:')} •••• ${bank && bank.accountNo ? String(bank.accountNo).slice(-4) : '—'} (IFSC: ${bank && bank.ifscCode ? bank.ifscCode : '—'}) | ${tDual('लेखा अधिकारी (APMC रोहतक) द्वारा सीधे DBT जारी किया जा रहा है।', 'Direct Benefit Transfer being processed by APMC Rohtak Accounts Cell.')}"
    ),
    (
        '<button class="btn btn-primary" onclick="window.print()">🖨️ रसीद प्रिंट करें</button>',
        "<button class=" + '"btn btn-primary" onclick="window.print()">🖨️ ${tDual(\'रसीद प्रिंट करें\', \'Print Weighment Slip\')}</button>'
    ),
    (
        'आज अभी कोई धर्मकांटा या गेट एंट्री दर्ज नहीं हुई है।',
        "${tDual('आज अभी कोई धर्मकांटा या गेट एंट्री दर्ज नहीं हुई है।', 'No weighbridge or gate transactions recorded yet today.')}"
    ),
    (
        '${e.netWeightKg ? `<strong>${(e.netWeightKg / 100).toFixed(2)} Q</strong> (₹${(e.finalPayableAmount || 0).toLocaleString(\'en-IN\')})` : \'<span style=\"color:#64748b;\">तुलाई प्रगति पर</span>\'}',
        "${e.netWeightKg ? `<strong>${(e.netWeightKg / 100).toFixed(2)} ${tDual('क्विंटल', 'Q')}</strong> (₹${(e.finalPayableAmount || 0).toLocaleString('en-IN')})` : `<span style=\"color:#64748b;\">${tDual('तुलाई प्रगति पर', 'Weighment in Progress')}</span>`}"
    ),
    (
        '20 से अधिक प्रविष्टियाँ होने पर पुरानी प्रविष्टियाँ यहाँ स्वतः तिथि अनुसार संग्रहीत होंगी।',
        "${tDual('20 से अधिक प्रविष्टियाँ होने पर पुरानी प्रविष्टियाँ यहाँ स्वतः तिथि अनुसार संग्रहीत होंगी।', 'When more than 20 entries exist, older transactions are automatically archived here.')}"
    ),
    (
        "${e.type === 'inward' ? '📥 आवक' : '📤 विक्रय'}",
        "${e.type === 'inward' ? tDual('📥 आवक', '📥 Inward') : tDual('📤 विक्रय', '📤 Outward')}"
    ),
    (
        "window.app.showToast('मंडी गेट डिस्प्ले व कतार सफलतापूर्वक सिंक की गई।', 'info');",
        "window.app.showToast(tDual('मंडी गेट डिस्प्ले व कतार सफलतापूर्वक सिंक की गई।', 'Mandi gate display & queue successfully synced.'), 'info');"
    ),
    # Warehouse statuses
    (
        "case 'waiting': return 'कतार में प्रतीक्षारत';",
        "case 'waiting': return tDual('कतार में प्रतीक्षारत', 'Waiting in Queue');"
    ),
    (
        "case 'gate_entry': return 'गेट 2 प्रवेश';",
        "case 'gate_entry': return tDual('गेट 2 प्रवेश', 'Gate 2 Entry');"
    ),
    (
        "case 'weighbridge_in': return 'प्रथम तुलाई';",
        "case 'weighbridge_in': return tDual('प्रथम तुलाई', 'Gross Weighment');"
    ),
    (
        "case 'unloading': return 'साइलो में खाली';",
        "case 'unloading': return tDual('साइलो में खाली', 'Silo Unloading');"
    ),
    (
        "case 'weighbridge_out': return 'अंतिम तुलाई';",
        "case 'weighbridge_out': return tDual('अंतिम तुलाई', 'Tare Weighment');"
    ),
    (
        "case 'completed': return 'संपन्न / भुगतान';",
        "case 'completed': return tDual('संपन्न / भुगतान', 'Payment Settled');"
    ),

    # Accounts Officer Portal
    (
        '<h2><span>👨‍💼</span> लेखा अधिकारी नियंत्रण कक्ष (Account Officer Desk - DBT Cell)</h2>',
        "<h2><span>👨‍💼</span> ${tDual('लेखा अधिकारी नियंत्रण कक्ष (Account Officer Desk - DBT Cell)', 'Accounts Officer Control Desk (DBT Cell)')}</h2>"
    ),
    (
        '<p>${tDual(\'अधिकारी: <strong>श्री आर. के. गोयल (वरिष्ठ लेखा अधिकारी)</strong> | कृषि उपज मंडी समिति (APMC), नई अनाज मंडी, रोहतक\', \'Officer: <strong>Sh. R. K. Goyal (Senior Accounts Officer)</strong> | APMC New Grain Market, Rohtak\')}</p>',
        "<p>${tDual('अधिकारी: <strong>श्री आर. के. गोयल (वरिष्ठ लेखा अधिकारी)</strong> | कृषि उपज मंडी समिति (APMC), नई अनाज मंडी, रोहतक', 'Officer: <strong>Sh. R. K. Goyal (Senior Accounts Officer)</strong> | APMC New Grain Market, Rohtak (Haryana)')}</p>"
    ),
    (
        '⏳ लंबित भुगतान आवंटन (${pendingPayments.length})',
        "⏳ ${tDual('लंबित भुगतान आवंटन', 'Pending DBT Allotments')} (${pendingPayments.length})"
    ),
    (
        '📜 स्वीकृत भुगतान इतिहास (${paidPayments.length})',
        "📜 ${tDual('स्वीकृत भुगतान इतिहास', 'Disbursement History')} (${paidPayments.length})"
    ),
    (
        'placeholder="बिल संख्या (उदा. BILL-ROH-2026-XXXX) या किसान खोजें..."',
        'placeholder="${tDual(\'बिल संख्या (उदा. BILL-ROH-2026-XXXX) या किसान खोजें...\', \'Search by Bill Number (e.g. BILL-ROH-2026-XXXX) or farmer name...\')}"'
    ),
    (
        '<th>बिल संख्या व टोकन</th>',
        "<th>${tDual('बिल संख्या व टोकन', 'Bill No & Token')}</th>"
    ),
    (
        '<th>किसान एवं मंडी</th>',
        "<th>${tDual('किसान एवं मंडी', 'Farmer & Market')}</th>"
    ),
    (
        '<th>फसल एवं वजन</th>',
        "<th>${tDual('फसल एवं वजन', 'Crop & Weight')}</th>"
    ),
    (
        '<th>दर एवं कुल देय राशि</th>',
        "<th>${tDual('दर एवं कुल देय राशि', 'Rate & Total Payable')}</th>"
    ),
    (
        '<th>नामित बैंक खाता</th>',
        "<th>${tDual('नामित बैंक खाता', 'Beneficiary Bank Account')}</th>"
    ),
    (
        '<small style="color:#64748b;">टोकन: #${p.tokenNumber} (${p.tokenId})</small><br>',
        "<small style=" + '"color:#64748b;">${tDual(\'टोकन:\', \'Token:\')} #${p.tokenNumber} (${p.tokenId})</small><br>'
    ),
    (
        '<small style="color:#64748b;">दिनांक: ${new Date(p.createdDate).toLocaleDateString()}</small>',
        "<small style=" + '"color:#64748b;">${tDual(\'दिनांक:\', \'Date:\')} ${new Date(p.createdDate).toLocaleDateString()}</small>'
    ),
    (
        '<small style="color:#047857;">नई अनाज मंडी, रोहतक</small>',
        "<small style=" + '"color:#047857;">${tDual(\'नई अनाज मंडी, रोहतक\', \'New Grain Market, Rohtak\')}</small>'
    ),
    (
        '<small style="color:#1e293b; font-weight:600;">शुद्ध वजन: ${p.netWeightKg} kg (${p.netQuintals} क्विंटल)</small>',
        "<small style=" + '"color:#1e293b; font-weight:600;">${tDual(\'शुद्ध वजन:\', \'Net Weight:\')} ${p.netWeightKg} kg (${p.netQuintals} ${tDual(\'क्विंटल\', \'Quintals\')})</small>'
    ),
    (
        '<small style="color:#64748b;">दर: ₹${p.ratePerQuintal}/Q</small>',
        "<small style=" + '"color:#64748b;">${tDual(\'दर:\', \'Rate:\')} ₹${p.ratePerQuintal}/Q</small>'
    ),
    (
        "${tDual('✅ भुगतान अंतरित', '✅ Paid')}",
        "✅ ${tDual('भुगतान अंतरित', 'Payment Disbursed')}"
    ),
    (
        '🧾 वाउचर देखें',
        "🧾 ${tDual('वाउचर देखें', 'View Voucher')}"
    ),
    (
        "${tDual('💳 भुगतान जारी करें', '💳 Release DBT')}",
        "💳 ${tDual('भुगतान जारी करें', 'Release Payment')}"
    ),
    (
        "window.app.openModal('किसान प्रत्यक्ष लाभ अंतरण (DBT Payment Allotment & Release)', `",
        "window.app.openModal(tDual('किसान प्रत्यक्ष लाभ अंतरण (DBT Payment Allotment & Release)', 'Direct Benefit Transfer (DBT) Payment Release'), `"
    ),
    (
        '<label class="form-label">किसान का नाम:</label>',
        "<label class=" + '"form-label">${tDual(\'किसान का नाम:\', \'Farmer Name:\')}</label>'
    ),
    (
        '<label class="form-label">फसल एवं शुद्ध मात्रा:</label>',
        "<label class=" + '"form-label">${tDual(\'फसल एवं शुद्ध मात्रा:\', \'Crop & Net Quantity:\')}</label>'
    ),
    (
        '<input type="text" class="form-control" value="${payment.cropName} (${payment.netQuintals} क्विंटल)" readonly style="background:#f1f5f9;">',
        "<input type=" + '"text" class="form-control" value="${payment.cropName} (${payment.netQuintals} ${tDual(\'क्विंटल\', \'Quintals\')})" readonly style="background:#f1f5f9;">'
    ),
    (
        '<label class="form-label">बैंक यूटीआर / लेनदेन सन्दर्भ संख्या (Bank UTR / Transaction Ref No) *:</label>',
        "<label class=" + '"form-label">${tDual(\'बैंक यूटीआर / लेनदेन सन्दर्भ संख्या (Bank UTR / Transaction Ref No) *:\', \'Bank UTR / Transaction Reference No *:\')}</label>'
    ),
    (
        '<small style="color:#64748b;">यह UTR संख्या किसान के मोबाइल ऐप पर ट्रैकर में तुरंत दिखाई देगी।</small>',
        "<small style=" + '"color:#64748b;">${tDual(\'यह UTR संख्या किसान के मोबाइल ऐप पर ट्रैकर में तुरंत दिखाई देगी।\', \'This UTR will immediately appear on the farmer mobile payment tracker.\')}</small>'
    ),
    (
        '<textarea id="accNotes" class="form-control" rows="2">PFMS के माध्यम से रोहतक नई अनाज मंडी खरीद मद से सीधे किसान के खाते में हस्तांतरित।</textarea>',
        "<textarea id=" + '"accNotes" class="form-control" rows="2">${tDual(\'PFMS के माध्यम से रोहतक नई अनाज मंडी खरीद मद से सीधे किसान के खाते में हस्तांतरित।\', \'Disbursed directly from APMC Rohtak procurement allocation to farmer bank account via PFMS.\')}</textarea>'
    ),
    (
        "window.app.showToast(`बिल ${billNumber} का डीबीटी भुगतान (₹${res.totalPayableAmount.toLocaleString('en-IN')}) सफलतापूर्वक जारी किया गया!`, 'success');",
        "window.app.showToast(tDual(`बिल ${billNumber} का डीबीटी भुगतान (₹${res.totalPayableAmount.toLocaleString('en-IN')}) सफलतापूर्वक जारी किया गया!`, `DBT payment for Bill ${billNumber} (₹${res.totalPayableAmount.toLocaleString('en-IN')}) successfully disbursed!`), 'success');"
    ),
    (
        "window.app.showToast('भुगतान जारी करने में त्रुटि हुई।', 'error');",
        "window.app.showToast(tDual('भुगतान जारी करने में त्रुटि हुई।', 'Error releasing payment.'), 'error');"
    ),
    (
        '<div style="font-size:0.8rem; color:#4338ca; font-weight:700; text-transform:uppercase;">हरियाणा सरकार | कृषि विपणन बोर्ड (APMC रोहतक)</div>',
        "<div style=" + '"font-size:0.8rem; color:#4338ca; font-weight:700; text-transform:uppercase;">${tDual(\'हरियाणा सरकार | कृषि विपणन बोर्ड (APMC रोहतक)\', \'Govt. of Haryana | Agricultural Marketing Board (APMC Rohtak)\')}</div>'
    ),
    (
        '<p style="font-size:0.75rem; color:#64748b;">ई-बिल संख्या: <strong style="font-family:var(--font-mono); color:#1e1b4b;">${p.billNumber}</strong> | UTR: <strong style="font-family:var(--font-mono); color:#15803d;">${p.utrNo}</strong></p>',
        "<p style=" + '"font-size:0.75rem; color:#64748b;">${tDual(\'ई-बिल संख्या:\', \'E-Bill No:\')} <strong style="font-family:var(--font-mono); color:#1e1b4b;">${p.billNumber}</strong> | UTR: <strong style="font-family:var(--font-mono); color:#15803d;">${p.utrNo}</strong></p>'
    ),
    (
        '<div>लाभार्थी किसान: <strong>${p.farmerName}</strong></div>',
        "<div>${tDual('लाभार्थी किसान:', 'Beneficiary Farmer:')} <strong>${p.farmerName}</strong></div>"
    ),
    (
        '<div>टोकन सन्दर्भ: #${p.tokenNumber} (${p.tokenId})</div>',
        "<div>${tDual('टोकन सन्दर्भ:', 'Token Ref:')} #${p.tokenNumber} (${p.tokenId})</div>"
    ),
    (
        '<div>उपज / फसल: <strong>${p.cropName}</strong></div>',
        "<div>${tDual('उपज / फसल:', 'Crop / Produce:')} <strong>${p.cropName}</strong></div>"
    ),
    (
        '<div>शुद्ध वजन: <strong>${p.netWeightKg} kg (${p.netQuintals} Q)</strong></div>',
        "<div>${tDual('शुद्ध वजन:', 'Net Weight:')} <strong>${p.netWeightKg} kg (${p.netQuintals} Q)</strong></div>"
    ),
    (
        '<div>खरीद दर: <strong>₹${p.ratePerQuintal} / क्विंटल</strong></div>',
        "<div>${tDual('खरीद दर:', 'Procurement Rate:')} <strong>₹${p.ratePerQuintal} / ${tDual('क्विंटल', 'Quintal')}</strong></div>"
    ),
    (
        '<div>अंतरण दिनांक: <strong>${new Date(p.paymentDate || p.createdDate).toLocaleString()}</strong></div>',
        "<div>${tDual('अंतरण दिनांक:', 'Transfer Date:')} <strong>${new Date(p.paymentDate || p.createdDate).toLocaleString()}</strong></div>"
    ),
    (
        '<div>अधिकृत हस्ताक्षरी: <strong>${p.allottedBy || \'वरिष्ठ लेखा अधिकारी, APMC रोहतक\'}</strong></div>',
        "<div>${tDual('अधिकृत हस्ताक्षरी:', 'Authorized Signatory:')} <strong>${p.allottedBy || (tDual('वरिष्ठ लेखा अधिकारी, APMC रोहतक', 'Senior Accounts Officer, APMC Rohtak'))}</strong></div>"
    ),
    (
        '<div>सुरक्षित डिजिटल रिकॉर्ड: <strong>PFMS / KISAN-SETU-VERIFIED</strong></div>',
        "<div>${tDual('सुरक्षित डिजिटल रिकॉर्ड:', 'Secured Digital Record:')} <strong>PFMS / HARVEST-HUB-VERIFIED</strong></div>"
    ),
    (
        '<button class="btn btn-primary" onclick="window.print()">🖨️ वाउचर प्रिंट करें</button>',
        "<button class=" + '"btn btn-primary" onclick="window.print()">🖨️ ${tDual(\'वाउचर प्रिंट करें\', \'Print Voucher\')}</button>'
    ),

    # App Bootloader toasts & alerts
    (
        "this.showToast(`⚡ SIH त्वरित लॉगिन सफल! स्वागत है, ${user.name}`, 'success');",
        "this.showToast(isHi ? `⚡ SIH त्वरित लॉगिन सफल! स्वागत है, ${user.name}` : `⚡ Demo login successful! Welcome, ${user.name}`, 'success');"
    ),
    (
        "this.showToast(`नमस्ते ${result.user.name.split(' ')[0]}! पोर्टल में आपका स्वागत है।`, 'success');",
        "this.showToast(isHi ? `नमस्ते ${result.user.name.split(' ')[0]}! पोर्टल में आपका स्वागत है।` : `Welcome, ${result.user.name.split(' ')[0]}! Logged in successfully.`, 'success');"
    ),
    (
        "this.showToast(`पंजीकरण सफल! किसान खाता #${newUser.id} सक्रिय हुआ।`, 'success');",
        "this.showToast(isHi ? `पंजीकरण सफल! किसान खाता #${newUser.id} सक्रिय हुआ।` : `Registration successful! Farmer account #${newUser.id} is active.`, 'success');"
    ),
    (
        "if (confirm('क्या आप पोर्टल से लॉगआउट करना चाहते हैं?')) {",
        "if (confirm(window.kisanI18n && window.kisanI18n.currentLang === 'hi' ? 'क्या आप पोर्टल से लॉगआउट करना चाहते हैं?' : 'Are you sure you want to logout?')) {"
    ),
    (
        "this.showToast('आप सफलतापूर्वक लॉगआउट हो गए हैं।', 'info');",
        "this.showToast(window.kisanI18n && window.kisanI18n.currentLang === 'hi' ? 'आप सफलतापूर्वक लॉगआउट हो गए हैं।' : 'You have been logged out successfully.', 'info');"
    ),
    (
        "if (confirm('क्या आप सभी डेटा को डिफ़ॉल्ट डेमो स्थिति में रीसेट करना चाहते हैं? (Reset to clean SIH Demo State?)')) {",
        "if (confirm(window.kisanI18n && window.kisanI18n.currentLang === 'hi' ? 'क्या आप सभी डेटा को डिफ़ॉल्ट डेमो स्थिति में रीसेट करना चाहते हैं?' : 'Do you want to reset all demo data to default clean state?')) {"
    ),
    (
        "this.showToast('डेमो डेटा पुनः रीसेट कर दिया गया।', 'success');",
        "this.showToast(window.kisanI18n && window.kisanI18n.currentLang === 'hi' ? 'डेमो डेटा पुनः रीसेट कर दिया गया।' : 'Demo data has been reset to default state.', 'success');"
    ),
    (
        "this.showToast(`⚡ ${config.demoTitle} ऑटोफिल हो गए (${config.demoEmail})`, 'info');",
        "this.showToast(isHi ? `⚡ ${config.demoTitle} ऑटोफिल हो गए (${config.demoEmail})` : `⚡ ${config.demoTitle} autofilled (${config.demoEmail})`, 'info');"
    ),
    (
        "alert('ℹ️ हार्वेस्ट हब डेमो पोर्टल क्रेडेंशियल सूचना:\\n\\nसभी डेमो उपयोगकर्ताओं का पासवर्ड \"1234567890\" है।\\n\\n• किसान: farmer@demo.com\\n• खरीद अधिकारी: officer@demo.com\\n• लैब टेस्टिंग: testing@demo.com\\n• मंडी संचालक: operator@demo.com\\n• लेखा अधिकारी: accounts@demo.com');",
        "alert(window.kisanI18n && window.kisanI18n.currentLang === 'hi' ? 'ℹ️ हार्वेस्ट हब डेमो पोर्टल क्रेडेंशियल सूचना:\\n\\nसभी डेमो उपयोगकर्ताओं का पासवर्ड \"1234567890\" है।\\n\\n• किसान: farmer@demo.com\\n• खरीद अधिकारी: officer@demo.com\\n• लैब टेस्टिंग: testing@demo.com\\n• मंडी संचालक: operator@demo.com\\n• लेखा अधिकारी: accounts@demo.com' : 'ℹ️ Harvest Hub Demo Portal Credentials:\\n\\nPassword for all demo accounts is \"1234567890\".\\n\\n• Farmer: farmer@demo.com\\n• Procurement Officer: officer@demo.com\\n• Soil Testing Lab: testing@demo.com\\n• Mandi Operator: operator@demo.com\\n• Accounts Officer: accounts@demo.com');"
    )
]

count = 0
for old, new in replacements:
    if old in text:
        text = text.replace(old, new)
        count += 1
    else:
        print('NOT FOUND:', old[:60])

with open('frontend/portal.html', 'w', encoding='utf-8') as f:
    f.write(text)

print(f'Successfully applied {count} out of {len(replacements)} replacements.')
