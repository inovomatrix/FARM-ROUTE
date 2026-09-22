import re
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Commodity, Center, Booking, QueueEntry

router = APIRouter(prefix="/assistant", tags=["Voice Assistant & Farmer Chatbot"])

class AssistantQueryRequest(BaseModel):
    query: str
    language: Optional[str] = "en"
    user_id: Optional[str] = None
    user_role: Optional[str] = "farmer"
    current_page: Optional[str] = None

class AssistantAction(BaseModel):
    label: str
    url: str
    type: str = "link"

class AssistantQueryResponse(BaseModel):
    success: bool
    response: str
    audio_text: str
    category: str
    quick_actions: List[AssistantAction] = []
    suggestions: List[str] = []

# Knowledge base for procurement calendars & schedules
PROCUREMENT_SCHEDULES = {
    "wheat": {
        "crop_name": "Wheat (Grade A)",
        "season": "Rabi 2026",
        "start_date": "1 April 2026",
        "end_date": "15 May 2026",
        "msp": "₹2,275 / Quintal",
        "demo_rate": "₹2,425 / Quintal",
        "moisture": "12.0% Maximum",
        "status": "Active (Procurement Ongoing / Registration Open)"
    },
    "mustard": {
        "crop_name": "Mustard",
        "season": "Rabi 2026",
        "start_date": "15 March 2026",
        "end_date": "30 April 2026",
        "msp": "₹5,650 / Quintal",
        "demo_rate": "₹5,650 / Quintal",
        "moisture": "9.0% Maximum",
        "status": "Active (Intake Started)"
    },
    "gram": {
        "crop_name": "Gram / Chickpea",
        "season": "Rabi 2026",
        "start_date": "1 April 2026",
        "end_date": "15 May 2026",
        "msp": "₹5,440 / Quintal",
        "demo_rate": "₹5,440 / Quintal",
        "moisture": "10.0% Maximum",
        "status": "Active / Scheduled"
    },
    "barley": {
        "crop_name": "Barley",
        "season": "Rabi 2026",
        "start_date": "1 April 2026",
        "end_date": "15 May 2026",
        "msp": "₹1,850 / Quintal",
        "demo_rate": "₹1,980 / Quintal",
        "moisture": "12.0% Maximum",
        "status": "Active / Scheduled"
    },
    "paddy": {
        "crop_name": "Paddy (Common)",
        "season": "Kharif 2026",
        "start_date": "1 October 2026",
        "end_date": "15 November 2026",
        "msp": "₹2,183 / Quintal",
        "demo_rate": "₹2,320 / Quintal",
        "moisture": "17.0% Maximum",
        "status": "Kharif Season Scheduled"
    },
    "bajra": {
        "crop_name": "Bajra (Pearl Millet)",
        "season": "Kharif 2026",
        "start_date": "1 October 2026",
        "end_date": "15 November 2026",
        "msp": "₹2,500 / Quintal",
        "demo_rate": "₹2,625 / Quintal",
        "moisture": "12.0% Maximum",
        "status": "Kharif Season Scheduled"
    },
    "cotton": {
        "crop_name": "Cotton",
        "season": "Kharif 2026",
        "start_date": "15 October 2026",
        "end_date": "31 December 2026",
        "msp": "₹6,620 / Quintal",
        "demo_rate": "₹7,122 / Quintal",
        "moisture": "8.5% Maximum",
        "status": "Kharif Season Scheduled"
    },
    "maize": {
        "crop_name": "Maize",
        "season": "Kharif 2026",
        "start_date": "1 October 2026",
        "end_date": "30 November 2026",
        "msp": "₹2,090 / Quintal",
        "demo_rate": "₹2,225 / Quintal",
        "moisture": "14.0% Maximum",
        "status": "Kharif Season Scheduled"
    },
    "soybean": {
        "crop_name": "Soybean",
        "season": "Kharif 2026",
        "start_date": "15 October 2026",
        "end_date": "30 November 2026",
        "msp": "₹4,892 / Quintal",
        "demo_rate": "₹4,892 / Quintal",
        "moisture": "12.0% Maximum",
        "status": "Kharif Season Scheduled"
    }
}

def detect_crop_key(text: str) -> Optional[str]:
    t = text.lower()
    if any(w in t for w in ["wheat", "gehu", "gehun"]):
        return "wheat"
    if any(w in t for w in ["mustard", "sarson", "sarsho"]):
        return "mustard"
    if any(w in t for w in ["gram", "chana", "chickpea"]):
        return "gram"
    if any(w in t for w in ["barley", "jau"]):
        return "barley"
    if any(w in t for w in ["paddy", "rice", "dhan", "chawal", "basmati"]):
        return "paddy"
    if any(w in t for w in ["bajra", "millet"]):
        return "bajra"
    if any(w in t for w in ["cotton", "kapas"]):
        return "cotton"
    if any(w in t for w in ["maize", "makka", "corn"]):
        return "maize"
    if any(w in t for w in ["soybean", "soya"]):
        return "soybean"
    return None

DISTRICT_TRANSLITERATIONS = {
    "karnal": "karnal",
    "ambala": "ambala",
    "rohtak": "rohtak",
    "jhajjar": "jhajjar",
    "sonipat": "sonipat",
    "panipat": "panipat",
    "hisar": "hisar",
    "bhiwani": "bhiwani",
    "jind": "jind",
    "rewari": "rewari",
    "sirsa": "sirsa",
    "kaithal": "kaithal",
    "kurukshetra": "kurukshetra",
    "fatehabad": "fatehabad",
    "indore": "indore",
    "bhopal": "bhopal",
    "patiala": "patiala",
}

def detect_district_or_center(text: str, centers: List[Center]) -> Optional[Center]:
    t = text.lower()
    for name, en_name in DISTRICT_TRANSLITERATIONS.items():
        if name in t or en_name in t:
            for c in centers:
                if c.district.lower() == en_name:
                    return c
    for c in centers:
        if c.district.lower() in t or c.name.lower() in t:
            return c
    return None

@router.post("/query", response_model=AssistantQueryResponse)
def process_assistant_query(req: AssistantQueryRequest, db: Session = Depends(get_db)):
    q = req.query.strip()
    q_lower = q.lower()

    # Load db commodities and centers
    commodities = db.query(Commodity).all()
    centers = db.query(Center).all()

    # -------------------------------------------------------------
    # 1. GREETINGS & INTRO
    # -------------------------------------------------------------
    if re.search(r"^(hello|hi|hey|greetings|good morning|good afternoon|good evening|kisan vani|who are you|help)", q_lower):
        resp_text = (
            "**Welcome Farmer! 🙏 I am Kisan Vani, your digital agricultural assistant.**\n\n"
            "I can assist you with:\n"
            "• 🌾 **Minimum Support Prices (MSP) & Benchmark Mandi Rates**\n"
            "• 📅 **Official Government Procurement Schedules & Dates**\n"
            "• 📍 **Nearby Procurement Centers & Live Yard Congestion**\n"
            "• ⚡ **Digital Tokens & Weighbridge Slot Booking Guidance**\n"
            "• 💳 **Payment (DBT) Status Tracking & Grievance Redressal**\n\n"
            "You can type your query or click the microphone to speak."
        )
        audio_text = "Welcome Farmer! I am Kisan Vani. You can ask me about crop MSP rates, government procurement schedules, nearby mandis, and digital slot bookings."
        return AssistantQueryResponse(
            success=True,
            response=resp_text,
            audio_text=audio_text,
            category="general",
            quick_actions=[
                AssistantAction(label="🌾 Crop Rates & MSP", url="farmer/centers.html"),
                AssistantAction(label="📅 Procurement Calendar", url="#dates"),
                AssistantAction(label="📍 Procurement Centers", url="farmer/centers.html"),
                AssistantAction(label="⚡ Book a Slot", url="farmer/booking.html")
            ],
            suggestions=[
                "What is the MSP rate for wheat?",
                "When does mustard procurement start?",
                "How congested is Karnal mandi?",
                "How do I book a token?"
            ]
        )

    # -------------------------------------------------------------
    # 2. PROCUREMENT STARTING DATES & SCHEDULES
    # -------------------------------------------------------------
    date_keywords = ["date", "dates", "schedule", "start", "starting date", "start date", "when does", "when will", "procurement start", "season"]
    crop_found = detect_crop_key(q_lower)

    if any(k in q_lower for k in date_keywords) or (crop_found and any(w in q_lower for w in ["buy", "procure", "procurement", "mandi when"])):
        if crop_found and crop_found in PROCUREMENT_SCHEDULES:
            sc = PROCUREMENT_SCHEDULES[crop_found]
            resp_text = (
                f"📅 **Official Procurement Schedule for {sc['crop_name']} ({sc['season']})**:\n\n"
                f"• **Procurement Start Date:** **{sc['start_date']}**\n"
                f"• **Procurement End Date:** **{sc['end_date']}**\n"
                f"• **Minimum Support Price (MSP):** **{sc['msp']}**\n"
                f"• **Benchmark Market Rate:** {sc['demo_rate']}\n"
                f"• **Maximum Permissible Moisture:** {sc['moisture']}\n"
                f"• **Current Status:** {sc['status']}\n\n"
                f"💡 *Advice: Before heading to the mandi, please book a digital token and time slot on KisanSetu to eliminate long queue waiting times.*"
            )
            audio_text = f"Government procurement for {sc['crop_name']} runs from {sc['start_date']} to {sc['end_date']}. The minimum support price is {sc['msp']} and maximum permissible moisture is {sc['moisture']}."
            return AssistantQueryResponse(
                success=True,
                response=resp_text,
                audio_text=audio_text,
                category="procurement_dates",
                quick_actions=[
                    AssistantAction(label=f"⚡ Book Slot for {sc['crop_name']}", url=f"farmer/booking.html?crop={crop_found}"),
                    AssistantAction(label="📍 View Procurement Centers", url="farmer/centers.html")
                ],
                suggestions=[
                    "What is the MSP rate for wheat?",
                    "When does mustard procurement start?",
                    "What are the operating hours?",
                    "What documents are required?"
                ]
            )
        else:
            # Overall Procurement Calendar
            resp_text = (
                "📅 **Official Procurement Calendar 2026 (Starting Dates & Schedules)**:\n\n"
                "🌾 **Rabi Harvest Procurement:**\n"
                "• **Mustard:** 15 March 2026 to 30 April 2026 (MSP: ₹5,650/Q)\n"
                "• **Wheat:** 1 April 2026 to 15 May 2026 (MSP: ₹2,275/Q)\n"
                "• **Gram / Chickpea:** 1 April 2026 to 15 May 2026 (MSP: ₹5,440/Q)\n"
                "• **Barley:** 1 April 2026 to 15 May 2026 (MSP: ₹1,850/Q)\n\n"
                "🌾 **Kharif Harvest Procurement:**\n"
                "• **Paddy:** 1 October 2026 to 15 November 2026 (MSP: ₹2,183/Q)\n"
                "• **Bajra:** 1 October 2026 to 15 November 2026 (MSP: ₹2,500/Q)\n"
                "• **Cotton:** 15 October 2026 to 31 December 2026 (MSP: ₹6,620/Q)\n"
                "• **Maize:** 1 October 2026 to 30 November 2026 (MSP: ₹2,090/Q)\n"
                "• **Soybean:** 15 October 2026 to 30 November 2026 (MSP: ₹4,892/Q)\n\n"
                "🕒 **Operating Hours:** 09:00 AM to 05:00 PM (Monday to Saturday)."
            )
            audio_text = "For Rabi crops, mustard procurement begins on 15 March, and wheat, gram, and barley begin on 1 April 2026. Paddy and bajra procurement begins on 1 October."
            return AssistantQueryResponse(
                success=True,
                response=resp_text,
                audio_text=audio_text,
                category="procurement_dates",
                quick_actions=[
                    AssistantAction(label="⚡ Book Delivery Slot", url="farmer/booking.html"),
                    AssistantAction(label="📍 Nearby Centers", url="farmer/centers.html")
                ],
                suggestions=[
                    "When does wheat procurement start?",
                    "What is the MSP rate for mustard?",
                    "What documents do I need to bring?"
                ]
            )

    # -------------------------------------------------------------
    # 3. CROP PRICES & MSP RATES
    # -------------------------------------------------------------
    price_keywords = ["price", "rate", "cost", "msp", "floor price", "per quintal", "how much rate", "rates"]
    if any(k in q_lower for k in price_keywords) or crop_found:
        if crop_found:
            matched_comm = next((c for c in commodities if crop_found in c.name.lower() or crop_found in (c.name_english or "").lower()), None)
            if matched_comm:
                c_name = matched_comm.name_english or matched_comm.name
                c_msp = matched_comm.msp_per_quintal
                c_demo = matched_comm.demo_rate
                c_moist = matched_comm.moisture_max_percent
                resp_text = (
                    f"🌾 **Official Price Details for {c_name}**:\n\n"
                    f"• **Government MSP Floor Price:** **₹{c_msp:,.2f} / Quintal**\n"
                    f"• **Current Benchmark Mandi Rate:** ₹{c_demo:,.2f} / Quintal\n"
                    f"• **Maximum Permissible Moisture:** **{c_moist}%**\n"
                    f"• **Category:** {matched_comm.category}\n"
                    f"• **Season:** {matched_comm.season}\n\n"
                    f"ℹ️ *Moisture Norms: If your produce moisture is {c_moist}% or below, you receive 100% full MSP without quality deductions. Payments are disbursed directly to your bank account via DBT within 48-72 hours.*"
                )
                audio_text = f"The official MSP rate for {c_name} is {int(c_msp)} rupees per quintal, with a maximum permissible moisture limit of {c_moist} percent."
                return AssistantQueryResponse(
                    success=True,
                    response=resp_text,
                    audio_text=audio_text,
                    category="prices",
                    quick_actions=[
                        AssistantAction(label=f"⚡ Book Slot for {c_name}", url=f"farmer/booking.html?crop={crop_found}"),
                        AssistantAction(label="📍 Check Center Rates", url="farmer/centers.html")
                    ],
                    suggestions=[
                        f"When does {c_name} procurement start?",
                        "What if moisture is higher than limit?",
                        "How long does payment take?",
                        "View rates for other crops"
                    ]
                )

        # General Rates List
        lines = []
        for com in commodities[:6]:
            cname = com.name_english or com.name
            lines.append(f"• **{cname}:** MSP **₹{com.msp_per_quintal:,.0f}** / Quintal (Moisture limit: {com.moisture_max_percent}%)")

        resp_text = (
            "🌾 **Current Official Minimum Support Prices (MSP 2026)**:\n\n"
            + "\n".join(lines)
            + "\n\n"
            "• **Payment System:** Direct Benefit Transfer (DBT) credited within 48-72 hours after electronic weighment.\n"
            "• **Deduction Policy:** 100% full floor rate is guaranteed if moisture content complies with FAQ norms."
        )
        audio_text = "Current government MSP rates are 2275 rupees for wheat, 5650 rupees for mustard, 2183 rupees for paddy, and 2500 rupees per quintal for bajra."
        return AssistantQueryResponse(
            success=True,
            response=resp_text,
            audio_text=audio_text,
            category="prices",
            quick_actions=[
                AssistantAction(label="🌾 View All Crops & Centers", url="farmer/centers.html"),
                AssistantAction(label="⚡ Book Slot Online", url="farmer/booking.html")
            ],
            suggestions=[
                "What is the wheat rate?",
                "What is the mustard rate?",
                "What is the gram rate?",
                "What is the cotton rate?"
            ]
        )

    # -------------------------------------------------------------
    # 4. CENTERS & LIVE QUEUE / CONGESTION
    # -------------------------------------------------------------
    center_keywords = ["center", "mandi", "yard", "queue", "line", "crowd", "wait", "waiting", "wait time", "traffic", "congestion", "how busy"]
    if any(k in q_lower for k in center_keywords):
        matched_c = detect_district_or_center(q_lower, centers)
        if matched_c:
            load_label = {"low": "Low Load (Fast Track)", "medium": "Moderate Load (Standard Buffer)", "high": "Heavy Congestion (Slow Intake)"}.get(matched_c.load_status, "Normal")
            resp_text = (
                f"📍 **{matched_c.name} ({matched_c.district}, {matched_c.state})**:\n\n"
                f"• **Address:** {matched_c.address}\n"
                f"• **Operating Hours:** {matched_c.operating_hours}\n"
                f"• **Current Queue Status:** **{load_label}**\n"
                f"• **Vehicles in Yard:** {matched_c.current_queue_vehicles} vehicles\n"
                f"• **Estimated Wait Time:** Approximately **{matched_c.estimated_wait_minutes} minutes**\n"
                f"• **Daily Intake Capacity:** {matched_c.daily_capacity_mt} MT\n"
                f"• **Primary Commodity:** {matched_c.commodity}\n\n"
                f"⚡ *Tip: You can book an online delivery slot at this facility to reserve your queue priority.*"
            )
            audio_text = f"{matched_c.name} currently has {matched_c.current_queue_vehicles} vehicles in yard, with an estimated wait time of approximately {matched_c.estimated_wait_minutes} minutes."
            return AssistantQueryResponse(
                success=True,
                response=resp_text,
                audio_text=audio_text,
                category="centers",
                quick_actions=[
                    AssistantAction(label="⚡ Book Token at This Center", url=f"farmer/booking.html?centerId={matched_c.id}"),
                    AssistantAction(label="📊 View Live Queue Status", url=f"farmer/queue.html?centerId={matched_c.id}")
                ],
                suggestions=[
                    "How do I book a delivery slot?",
                    "How do I get my token pass?",
                    "What is the wheat price?"
                ]
            )

        # Overview of active centers
        c_lines = []
        for c in centers[:4]:
            load_label = "Low Congestion" if c.load_status == "low" else ("Moderate" if c.load_status == "medium" else "Heavy Congestion")
            c_lines.append(f"• **{c.name} ({c.district}):** {c.current_queue_vehicles} vehicles in yard • Wait ~{c.estimated_wait_minutes} mins ({load_label})")

        resp_text = (
            "📍 **Key Procurement Centers (Live Queue Telemetry Overview)**:\n\n"
            + "\n".join(c_lines)
            + "\n\n"
            "💡 You can specify any district (e.g. 'Karnal', 'Ambala', 'Rohtak', 'Hisar') to check live queue telemetry for that yard."
        )
        audio_text = "Major procurement yards in Karnal, Ambala, Rohtak, and Sonipat are operating normally. Speak or type any district name to inspect live queue status."
        return AssistantQueryResponse(
            success=True,
            response=resp_text,
            audio_text=audio_text,
            category="centers",
            quick_actions=[
                AssistantAction(label="📍 View All 15+ Procurement Centers", url="farmer/centers.html"),
                AssistantAction(label="⚡ Live Queue Monitor", url="farmer/queue.html")
            ],
            suggestions=[
                "Check status of Karnal center",
                "How busy is Ambala center?",
                "Rohtak procurement center status"
            ]
        )

    # -------------------------------------------------------------
    # 5. HOW TO BOOK SLOT / TOKEN PASS
    # -------------------------------------------------------------
    booking_keywords = ["booking", "book", "slot", "token", "pass", "how to book", "how do i book", "receipt", "qr pass"]
    if any(k in q_lower for k in booking_keywords):
        resp_text = (
            "⚡ **How to Book a Digital Token & Delivery Slot on KisanSetu**:\n\n"
            "1. **Log in:** Sign in to the Farmer Portal with your registered mobile number.\n"
            "2. **Choose Center:** Select 'Procurement Centers' and pick the nearest facility in your district.\n"
            "3. **Select Crop & Quantity:** Specify your commodity (Wheat, Mustard, etc.) and estimated quintals.\n"
            "4. **Pick Delivery Time Window:** Select your preferred date and time slot (e.g., 10:00 AM – 11:00 AM).\n"
            "5. **Generate Pass:** Confirm to instantly generate your **Digital Token (e.g., KS-TKN-1011)** and cryptographically signed QR pass!\n\n"
            "📱 *At the mandi gate, present this digital token or QR code on your phone for immediate fast-track check-in.*"
        )
        audio_text = "To book a delivery slot, choose a procurement center on the portal, select your crop and delivery date, and confirm your vehicle number to generate your digital pass."
        return AssistantQueryResponse(
            success=True,
            response=resp_text,
            audio_text=audio_text,
            category="booking",
            quick_actions=[
                AssistantAction(label="⚡ Book a Slot Now", url="farmer/booking.html"),
                AssistantAction(label="📋 View My Bookings", url="farmer/bookings.html"),
                AssistantAction(label="🎫 View Digital Token Pass", url="farmer/token.html")
            ],
            suggestions=[
                "How can I cancel a booking?",
                "What do I need to present at the gate?",
                "What is the wheat price?",
                "How do I track live queue position?"
            ]
        )

    # -------------------------------------------------------------
    # 6. MANDI ARRIVAL & WEIGHBRIDGE PROCESS
    # -------------------------------------------------------------
    arrival_keywords = ["gate", "process", "arrival", "arrived", "weighbridge", "scale", "workflow", "steps", "intake"]
    if any(k in q_lower for k in arrival_keywords):
        resp_text = (
            "🚛 **Procurement & Weighment Process at the Mandi Yard**:\n\n"
            "1. **Gate Verification & Security Check-In:** Present your digital token pass or QR code at the entry terminal.\n"
            "2. **Gross Weighing (Scale 1):** Loaded tractor-trolley weight is recorded on the electronic weighbridge.\n"
            "3. **Assay Moisture Testing:** Quality team collects a grain sample and measures moisture content.\n"
            "4. **Unloading Bay:** Grain is unloaded at your assigned warehouse shed or silo bay.\n"
            "5. **Tare Weighing (Scale 2):** Empty vehicle is weighed to calculate certified net crop weight.\n"
            "6. **Statutory e-JForm Issuance:** Digital receipt is generated with price and dockage details."
        )
        audio_text = "When arriving at the mandi, scan your digital token at the gate, proceed to Gross Scale 1, complete moisture testing, unload at your assigned bay, weigh empty at Scale 2, and receive your digital e-JForm receipt."
        return AssistantQueryResponse(
            success=True,
            response=resp_text,
            audio_text=audio_text,
            category="process",
            quick_actions=[
                AssistantAction(label="⚡ Live Queue Telemetry", url="farmer/queue.html"),
                AssistantAction(label="🧾 View Sales History & Receipts", url="farmer/sales-history.html")
            ],
            suggestions=[
                "What if moisture is higher than limit?",
                "When will payment be credited?",
                "How do I submit a grievance?"
            ]
        )

    # -------------------------------------------------------------
    # 7. PAYMENT, DBT & BANK TRANSFERS
    # -------------------------------------------------------------
    payment_keywords = ["payment", "dbt", "bank", "money", "transfer", "payout", "when will i get paid", "account", "credit"]
    if any(k in q_lower for k in payment_keywords):
        resp_text = (
            "💳 **Direct Benefit Transfer (DBT) Payment Process & Timeline**:\n\n"
            "• **Disbursement Window:** Proceeds are transferred directly into your registered bank account within **48 to 72 hours** of e-JForm generation.\n"
            "• **Mechanism:** Aadhaar-enabled Direct Benefit Transfer (DBT) via PFMS/Public Financial Management System.\n"
            "• **Bank Verification:** Ensure your bank account is Aadhaar-seeded and active for DBT payouts.\n"
            "• **Tracking:** Visit 'Sales History' in your Farmer Portal to inspect transaction UTR reference numbers and payment statuses.\n\n"
            "⚠️ *If payment is not credited after 72 business hours, you can lodge an escalated grievance directly on the platform.*"
        )
        audio_text = "Sales proceeds are transferred via DBT directly to your Aadhaar-linked bank account within 48 to 72 hours of digital receipt issuance."
        return AssistantQueryResponse(
            success=True,
            response=resp_text,
            audio_text=audio_text,
            category="payment",
            quick_actions=[
                AssistantAction(label="🌾 View Sales History & DBT", url="farmer/sales-history.html"),
                AssistantAction(label="⚖️ File Payment Grievance", url="farmer/complaints.html")
            ],
            suggestions=[
                "How do I file a grievance?",
                "How do I update my bank details?",
                "What is the wheat MSP rate?"
            ]
        )

    # -------------------------------------------------------------
    # 8. REQUIRED DOCUMENTS
    # -------------------------------------------------------------
    doc_keywords = ["document", "documents", "checklist", "what to bring", "aadhaar", "papers", "id proof"]
    if any(k in q_lower for k in doc_keywords):
        resp_text = (
            "📋 **Farmer Document Checklist for Mandi Procurement**:\n\n"
            "1. **Aadhaar Card:** For farmer identity verification.\n"
            "2. **Land Records (Jamabandi / Fard / Girdawari):** For registered acreage and crop verification.\n"
            "3. **Bank Passbook Copy:** Showing bank account number and IFSC code.\n"
            "4. **Digital Token Pass:** SMS message, printed pass, or mobile QR code from KisanSetu.\n"
            "5. **Vehicle Registration / Driver Info:** Tractor-trolley registration number."
        )
        audio_text = "Please bring your Aadhaar Card, land record fard or jamabandi, bank passbook copy, and your KisanSetu digital token QR pass on your mobile phone."
        return AssistantQueryResponse(
            success=True,
            response=resp_text,
            audio_text=audio_text,
            category="documents",
            quick_actions=[
                AssistantAction(label="⚡ Book Delivery Token", url="farmer/booking.html"),
                AssistantAction(label="👤 View Farmer Profile", url="farmer/dashboard.html#profile-summary")
            ],
            suggestions=[
                "How do I book a delivery slot?",
                "What is the wheat floor price?",
                "When does mustard procurement start?"
            ]
        )

    # -------------------------------------------------------------
    # 9. COMPLAINTS & GRIEVANCE REDRESSAL
    # -------------------------------------------------------------
    complaint_keywords = ["complaint", "grievance", "issue", "problem", "dispute", "help", "fraud", "irregularity", "delay"]
    if any(k in q_lower for k in complaint_keywords):
        resp_text = (
            "⚖️ **KisanSetu Grievance Redressal System**:\n\n"
            "If you experience any operational difficulties (payment delays, incorrect moisture deductions, weighbridge discrepancies, or staff misconduct):\n\n"
            "• **Multi-Tier Escalation:** Grievances automatically escalate from Mandi Operator to District Administrative Officer, and up to State Super Admin if unresolved.\n"
            "• **Resolution Timeframe:** Mandatory turnaround resolution within 24 to 48 hours.\n"
            "• **Tracking:** You receive a unique tracking reference (e.g. CMP-2026-001) for live timeline updates."
        )
        audio_text = "For issues such as payment delays or weight discrepancies, you can file a grievance directly on the portal. Cases are resolved within 24 to 48 hours."
        return AssistantQueryResponse(
            success=True,
            response=resp_text,
            audio_text=audio_text,
            category="complaints",
            quick_actions=[
                AssistantAction(label="⚖️ File New Grievance", url="farmer/complaints.html"),
                AssistantAction(label="🔍 Track Grievance Status", url="farmer/complaints.html")
            ],
            suggestions=[
                "What if payment is not received?",
                "What are the moisture deduction norms?",
                "What is the superintendent helpline?"
            ]
        )

    # -------------------------------------------------------------
    # 10. MOISTURE DEDUCTION RULES
    # -------------------------------------------------------------
    moisture_keywords = ["moisture", "damp", "wet", "water content", "deduction", "faq"]
    if any(k in q_lower for k in moisture_keywords):
        resp_text = (
            "💧 **Moisture Standards & Fair Average Quality (FAQ) Norms**:\n\n"
            "• **Wheat:** Maximum **12.0%** moisture permissible. Full MSP guaranteed at or below 12%.\n"
            "• **Mustard:** Maximum **9.0%** moisture limit (oil content also tested).\n"
            "• **Paddy:** Maximum **17.0%** moisture limit.\n"
            "• **Bajra:** Maximum **12.0%** moisture limit.\n"
            "• **Cotton:** Maximum **8.5%** moisture limit.\n\n"
            "💡 *Tip: Sun-dry your harvested crop for 1-2 days before transporting to the mandi. Excess moisture causes dockage deductions or lot rejection.*"
        )
        audio_text = "Permissible moisture limits are 12 percent for wheat, 9 percent for mustard, and 17 percent for paddy. Ensure your crop is properly dried before delivery."
        return AssistantQueryResponse(
            success=True,
            response=resp_text,
            audio_text=audio_text,
            category="moisture",
            quick_actions=[
                AssistantAction(label="🌾 View Crop Standards", url="farmer/centers.html"),
                AssistantAction(label="⚡ Book Delivery Slot", url="farmer/booking.html")
            ],
            suggestions=[
                "What is the wheat MSP rate?",
                "When does mustard procurement start?",
                "How does the weighbridge scale operate?"
            ]
        )

    # -------------------------------------------------------------
    # 11. SOIL TESTING & FERTILIZER ADVISORY
    # -------------------------------------------------------------
    soil_keywords = ["soil", "soil test", "fertilizer", "urea", "dap", "pesticide", "potash", "zinc", "when not to use", "dosage"]
    if any(k in q_lower for k in soil_keywords):
        resp_text = (
            "🧪 **Soil Testing & Scientific Fertilizer Advisory**:\n\n"
            "1. **Book Soil Test:** You can schedule a soil sample testing appointment at your local mandi laboratory.\n"
            "2. **Soil Health Card:** Quantifies soil pH, Organic Carbon, Nitrogen (N), Phosphorus (P), Potassium (K), and Zinc levels.\n"
            "3. **Crop Dosage Schedules:** e.g., Wheat requires 110 kg Urea + 55 kg DAP + 6 kg Zinc per acre; Mustard requires 50 kg Urea + 35 kg DAP + 10 kg Sulphur.\n\n"
            "⚠️ **Crucial Rules - When NOT to use fertilizers:**\n"
            "• ❌ **Never apply Urea after flowering/heading stage**: Causes severe crop lodging and disease susceptibility.\n"
            "• ❌ **Never mix DAP and Zinc Sulphate**: Forms insoluble Zinc Phosphate, rendering both nutrients unusable.\n"
            "• ❌ **Never top-dress Urea on standing chickpea crops**: Legumes fix atmospheric nitrogen; extra nitrogen inhibits root nodules.\n"
            "• ❌ **Never broadcast Urea on dry soil in harsh sun**: Ammonia evaporates rapidly and scorches foliage."
        )
        audio_text = "Soil testing reveals precise nutrient requirements. Never apply urea after flowering, and do not mix DAP with zinc sulphate."
        return AssistantQueryResponse(
            success=True,
            response=resp_text,
            audio_text=audio_text,
            category="soil_testing",
            quick_actions=[
                AssistantAction(label="🧪 Book Soil Testing Appointment", url="farmer/soil-testing.html"),
                AssistantAction(label="📋 View My Soil Health Card", url="farmer/soil-testing.html#health-card")
            ],
            suggestions=[
                "What fertilizer dosage is recommended for wheat?",
                "Which pesticide should I spray for mustard aphids?",
                "How do I book a soil test appointment?",
                "When should I not apply fertilizers?"
            ]
        )

    # -------------------------------------------------------------
    # 12. DEFAULT INTELLIGENT FALLBACK
    # -------------------------------------------------------------
    fallback_resp = (
        f"🌾 **Kisan Vani AI Assistance**\n\n"
        f"Regarding your query **'{q}'**:\n"
        f"• **Current Crop MSP Rates:** Wheat ₹2,275/Q, Mustard ₹5,650/Q, Gram ₹5,440/Q, Paddy ₹2,183/Q, Bajra ₹2,500/Q.\n"
        f"• **Procurement Schedules:** Mustard procurement active from 15 March; Wheat and Gram active from 1 April 2026.\n"
        f"• **Queue Priority:** Reserve your delivery time window online to avoid yard wait times.\n\n"
        f"Please select from the options below or ask a more specific question."
    )
    fallback_audio = "Welcome! You can ask me about crop MSP rates, procurement schedules, nearby procurement centers, and digital delivery token bookings."

    return AssistantQueryResponse(
        success=True,
        response=fallback_resp,
        audio_text=fallback_audio,
        category="general",
        quick_actions=[
            AssistantAction(label="🌾 Crop Rates & MSP", url="farmer/centers.html"),
            AssistantAction(label="📅 Procurement Calendar", url="#dates"),
            AssistantAction(label="📍 Procurement Centers", url="farmer/centers.html"),
            AssistantAction(label="⚡ Book a Slot", url="farmer/booking.html"),
            AssistantAction(label="⚖️ File a Grievance", url="farmer/complaints.html")
        ],
        suggestions=[
            "What is the MSP rate for wheat?",
            "When does mustard procurement start?",
            "How congested is Karnal mandi?",
            "How do I book a delivery token?",
            "How long does payment take?"
        ]
    )
