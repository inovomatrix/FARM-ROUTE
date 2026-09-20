import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/portal.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

replaced = False
for idx in range(len(lines) - 3):
    if "this.activeTab === 'pending'" in lines[idx] and 'मंडी संचालक' in lines[idx+1]:
        lines[idx] = "                      ${this.activeTab === 'pending'\n"
        lines[idx+1] = "                        ? tDual('मंडी संचालक द्वारा खाली गाड़ी की अंतिम तुलाई पूरी करने के बाद बिल संख्या के साथ यहाँ भुगतान आदेश स्वतः प्रदर्शित होगा।', 'Payment orders will appear here automatically with bill numbers after the mandi operator completes final tare weighment.')\n"
        lines[idx+2] = "                        : tDual('लेखा अधिकारी द्वारा डीबीटी भुगतान जारी करने पर सभी रिकॉर्ड यहाँ सहेजे जाएंगे।', 'All payment records will be archived here once the account officer authorizes the DBT transfer.')}\n"
        replaced = True
        print(f"Replaced at line {idx+1}")
        break

if replaced:
    with open('frontend/portal.html', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Successfully replaced account empty state!")
else:
    print("Could not find matching lines")
