import datetime
import random
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import SoilTestRecord, User, Center

router = APIRouter(prefix="/soil-testing", tags=["Soil Testing & Fertilizer Advisory"])

# -------------------------------------------------------------
# PYDANTIC SCHEMAS
# -------------------------------------------------------------
class SoilTestBookingRequest(BaseModel):
    farmer_id: Optional[str] = "USR-FARMER-01"
    farmer_name: str
    farmer_phone: str
    district: Optional[str] = "Karnal"
    state: Optional[str] = "Haryana"
    village: Optional[str] = "Kachhwa"
    center_id: Optional[str] = "CTR-HR-01"
    center_name: Optional[str] = "Karnal Central Procurement Center"
    lab_name: Optional[str] = None
    booking_date: str
    time_slot: Optional[str] = "10:00 AM – 11:30 AM"
    preferred_slot: Optional[str] = None
    crop_planned: Optional[str] = "Wheat (Grade A)"
    land_area_acres: Optional[float] = 5.0
    soil_type: Optional[str] = "Alluvial Loam"

class SoilTestUpdateRequest(BaseModel):
    record_id: Optional[str] = None
    sample_id: Optional[str] = None
    farmer_phone: Optional[str] = None
    ph: Optional[float] = None
    ph_level: Optional[float] = None
    ec_level: Optional[float] = 0.45
    electrical_conductivity: Optional[float] = None
    organic_carbon_percent: Optional[float] = 0.55
    nitrogen_kg_ha: Optional[float] = 280.0
    phosphorus_kg_ha: Optional[float] = 22.0
    potassium_kg_ha: Optional[float] = 210.0
    zinc_ppm: Optional[float] = 0.55
    sulphur_ppm: Optional[float] = 8.2
    health_status: Optional[str] = "MODERATE"
    status: Optional[str] = "COMPLETED"
    advisory_notes: Optional[str] = ""

# -------------------------------------------------------------
# CROP AGRONOMIC ADVISORY ENGINE
# -------------------------------------------------------------
CROP_ADVISORY_DB = {
    "wheat": {
        "crop_name": "Wheat (Grade A)",
        "ideal_ph": "6.5 – 7.8",
        "fertilizers": [
            {
                "name": "DAP (Di-Ammonium Phosphate)",
                "per_acre_kg": 55,
                "application_timing": "At Sowing - Basal Dressing",
                "purpose": "Phosphorus supply for early root development and active tillering."
            },
            {
                "name": "Urea (46% N)",
                "per_acre_kg": 110,
                "application_timing": "Two equal splits (1st split at 21 days with 1st irrigation; 2nd split at 45 days)",
                "purpose": "Supports vegetative plant growth and maximum tiller count."
            },
            {
                "name": "MOP (Muriate of Potash)",
                "per_acre_kg": 20,
                "application_timing": "At Sowing (Basal)",
                "purpose": "Stem strengthening, disease resistance, and optimum grain filling."
            },
            {
                "name": "Zinc Sulphate 33%",
                "per_acre_kg": 6,
                "application_timing": "Applied separately with 1st irrigation",
                "purpose": "Prevents Khaira disease, chlorosis, and yellowing of wheat leaves."
            }
        ],
        "pesticides": [
            {
                "name": "Propiconazole 25% EC (Tilt)",
                "dosage_per_acre": "200 ml in 200 liters of water",
                "target_pest": "Yellow Rust and Karnal Bunt",
                "safety_interval": "Spray in the evening as soon as early foliar symptoms appear."
            },
            {
                "name": "Imidacloprid 17.8% SL (Confidor)",
                "dosage_per_acre": "60 ml in 150 liters of water",
                "target_pest": "Aphids / Chepa",
                "safety_interval": "Apply in Dec-Jan when aphid count exceeds 5-10 insects per earhead."
            }
        ],
        "when_not_to_use": [
            "❌ **Never apply Urea after flowering or heading**: Causes crop lodging, shriveled grains, and invites fungal blights.",
            "❌ **Never mix DAP and Zinc Sulphate together**: Mixing forms insoluble Zinc Phosphate, locking both nutrients from the plant.",
            "❌ **Do not broadcast Urea in dry soil or scorching afternoon sun**: Leads to volatile ammonia loss and severe leaf scorching.",
            "❌ **Do not apply Nitrogen when heavy rain is forecast**: Nitrogen washes away through surface runoff and deep leaching."
        ]
    },
    "mustard": {
        "crop_name": "Mustard",
        "ideal_ph": "6.0 – 7.5",
        "fertilizers": [
            {
                "name": "DAP (Di-Ammonium Phosphate)",
                "per_acre_kg": 35,
                "application_timing": "Basal at sowing",
                "purpose": "Strong taproot establishment and early branching."
            },
            {
                "name": "Urea",
                "per_acre_kg": 50,
                "application_timing": "At first irrigation (30-35 days after sowing)",
                "purpose": "Promotes vigorous branching prior to flower initiation."
            },
            {
                "name": "Bentonite Sulphur 90%",
                "per_acre_kg": 10,
                "application_timing": "Incorporate into soil at sowing",
                "purpose": "Crucial for increasing mustard oil content by 2-3%."
            }
        ],
        "pesticides": [
            {
                "name": "Dimethoate 30% EC (Rogor) or Thiamethoxam 25% WG",
                "dosage_per_acre": "250 ml or 40g per acre",
                "target_pest": "Mustard Aphid (Lipaphis erysimi)",
                "safety_interval": "Spray promptly during cloudy overcast weather in Dec-Jan."
            },
            {
                "name": "Mancozeb 75% WP (Dithane M-45)",
                "dosage_per_acre": "600g in 200 liters of water",
                "target_pest": "White Rust and Alternaria Leaf Spot",
                "safety_interval": "Spray in the morning after morning dew has evaporated."
            }
        ],
        "when_not_to_use": [
            "❌ **Never apply Urea during full flowering**: Attracts severe aphid attacks and delays pod maturation.",
            "❌ **Do not apply excessive Sulphur without prior soil testing**: Excess Sulphur can induce unwanted soil acidification.",
            "❌ **Never broadcast granular fertilizer over dew-drenched leaves**: Granules stick to leaves and burn foliage."
        ]
    },
    "paddy": {
        "crop_name": "Paddy (Common / Basmati)",
        "ideal_ph": "6.0 – 7.2",
        "fertilizers": [
            {
                "name": "DAP",
                "per_acre_kg": 40,
                "application_timing": "At puddling / final field preparation",
                "purpose": "Early root establishment and active tillering."
            },
            {
                "name": "Urea",
                "per_acre_kg": 90,
                "application_timing": "Three equal splits (7, 21, and 42 days after transplanting)",
                "purpose": "Uniform vegetative canopy growth and productive tillers."
            },
            {
                "name": "Zinc Sulphate 33%",
                "per_acre_kg": 6,
                "application_timing": "15-20 days after transplanting with Urea",
                "purpose": "Effective prevention of Khaira physiological disorder in rice."
            }
        ],
        "pesticides": [
            {
                "name": "Cartap Hydrochloride 4G (Padan)",
                "dosage_per_acre": "7.5 kg per acre in standing water",
                "target_pest": "Stem Borer and Leaf Folder",
                "safety_interval": "Apply 25-30 days after transplanting."
            },
            {
                "name": "Streptocycline (6g) + Copper Oxychloride (500g)",
                "dosage_per_acre": "In 200 liters of water per acre",
                "target_pest": "Bacterial Leaf Blight (BLB)",
                "safety_interval": "Spray immediately upon seeing yellow-white streaks on leaf margins."
            }
        ],
        "when_not_to_use": [
            "❌ **Never broadcast Urea in more than 5 cm of standing water**: Leads to extensive leaching loss. Drain field to thin layer first.",
            "❌ **Never apply fertilizer while draining the field**: Nutrients will be carried out into irrigation drains.",
            "❌ **Do not apply Urea after panicle emergence**: Causes neck blast and black discolored kernels."
        ]
    },
    "cotton": {
        "crop_name": "Cotton",
        "ideal_ph": "6.5 – 8.0",
        "fertilizers": [
            {
                "name": "DAP",
                "per_acre_kg": 40,
                "application_timing": "Band placement in rows at sowing",
                "purpose": "Root penetration and sturdy main stem."
            },
            {
                "name": "Urea",
                "per_acre_kg": 95,
                "application_timing": "Three splits (1st weeding, flowering, and early boll formation)",
                "purpose": "Maximizes boll retention and individual boll weight."
            },
            {
                "name": "Magnesium Sulphate",
                "per_acre_kg": 10,
                "application_timing": "At early boll formation stage",
                "purpose": "Prevents Red Leaf Disease and premature senescence."
            }
        ],
        "pesticides": [
            {
                "name": "Flonicamid 50% WG (Ulala)",
                "dosage_per_acre": "80g in 150 liters of water",
                "target_pest": "Whitefly and Jassids",
                "safety_interval": "Spray when sucking pests cross Economic Threshold Levels (ETL)."
            },
            {
                "name": "Spinetoram 11.7% SC",
                "dosage_per_acre": "170 ml per acre",
                "target_pest": "Pink Bollworm (Pectinophora gossypiella)",
                "safety_interval": "Spray when rosette flowers or green boll damage appears."
            }
        ],
        "when_not_to_use": [
            "❌ **Never apply Urea during excessive vegetative rank growth**: Promotes leaf shedding, boll drop, and invites heavy whitefly infestation.",
            "❌ **Do not apply fertilizers under waterlogged conditions**: Wait until excess water is removed to avoid root rot.",
            "❌ **Never tank-mix pesticides and fertilizers without scientific agronomic advice**."
        ]
    },
    "gram": {
        "crop_name": "Gram / Chickpea",
        "ideal_ph": "6.0 – 7.8",
        "fertilizers": [
            {
                "name": "DAP",
                "per_acre_kg": 30,
                "application_timing": "Basal at sowing",
                "purpose": "Initial nitrogen and phosphorus for rhizobial root nodule development."
            },
            {
                "name": "Gypsum",
                "per_acre_kg": 50,
                "application_timing": "During final land preparation",
                "purpose": "Supplies Sulphur and Calcium for bright, plump pulse grains."
            }
        ],
        "pesticides": [
            {
                "name": "Emamectin Benzoate 5% SG (Proclaim)",
                "dosage_per_acre": "100g in 150 liters of water",
                "target_pest": "Gram Pod Borer (Helicoverpa armigera)",
                "safety_interval": "Spray at pod initiation when small larvae appear."
            }
        ],
        "when_not_to_use": [
            "❌ **Never top-dress Urea on standing chickpea crops**: As a legume, chickpea fixes atmospheric nitrogen. Top-dressing halts nodulation and causes excessive vegetative growth with zero pod set.",
            "❌ **Do not apply nitrogen fertilizers in wilt-infected plots**: Excess nitrogen accelerates fungal spreading."
        ]
    },
    "bajra": {
        "crop_name": "Bajra (Pearl Millet)",
        "ideal_ph": "6.5 – 8.5",
        "fertilizers": [
            {
                "name": "DAP",
                "per_acre_kg": 30,
                "application_timing": "At sowing",
                "purpose": "Root anchorage and drought resilience."
            },
            {
                "name": "Urea",
                "per_acre_kg": 45,
                "application_timing": "After 1st rain or irrigation (25-30 days)",
                "purpose": "Promotes tillering and longer earheads."
            }
        ],
        "pesticides": [
            {
                "name": "Chlorpyrifos 20% EC",
                "dosage_per_acre": "1 liter per acre with irrigation",
                "target_pest": "Termites and Shoot Fly",
                "safety_interval": "Apply at sowing or with the first irrigation."
            }
        ],
        "when_not_to_use": [
            "❌ **Never apply Urea during severe drought or moisture stress**: Fertilizing dry soil burns roots and dries out the crop.",
            "❌ **Do not apply fertilizers during the earhead ripening stage**."
        ]
    }
}

def _calculate_crop_advisory(crop_key: str, land_area_acres: float, soil_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    key = "wheat"
    ck = crop_key.lower()
    for k in CROP_ADVISORY_DB:
        if k in ck:
            key = k
            break

    crop_info = CROP_ADVISORY_DB[key]
    acres = max(0.5, float(land_area_acres))

    # Calculate exact fertilizer bags & totals for the land area
    fertilizer_list = []
    for f in crop_info["fertilizers"]:
        total_kg = round(f["per_acre_kg"] * acres, 1)
        bags_50kg = round(total_kg / 50.0, 1)
        bags_45kg = round(total_kg / 45.0, 1)  # Urea standard bag is 45kg in India
        is_urea = "urea" in f["name"].lower()
        bag_count = bags_45kg if is_urea else bags_50kg
        bag_weight = 45 if is_urea else 50

        # Adjust recommendation if soil test data is available
        adjustment_note = "Standard Scientific Recommended Dosage"
        if soil_data:
            n_val = soil_data.get("nitrogen_kg_ha", 240)
            p_val = soil_data.get("phosphorus_kg_ha", 16.5)
            k_val = soil_data.get("potassium_kg_ha", 210)
            ph = soil_data.get("ph_level", 7.2)

            if is_urea:
                if n_val > 500:
                    total_kg = round(total_kg * 0.75, 1)
                    bag_count = round(total_kg / bag_weight, 1)
                    adjustment_note = "⚠️ High soil nitrogen (>500 kg/ha); Urea dosage reduced by 25%."
                elif n_val < 200:
                    total_kg = round(total_kg * 1.15, 1)
                    bag_count = round(total_kg / bag_weight, 1)
                    adjustment_note = "ℹ️ Low soil nitrogen (<200 kg/ha); 15% extra Urea recommended."
            elif "DAP" in f["name"]:
                if p_val > 25:
                    total_kg = round(total_kg * 0.8, 1)
                    bag_count = round(total_kg / bag_weight, 1)
                    adjustment_note = "⚠️ High available phosphorus; DAP dosage reduced by 20%."
            elif "MOP" in f["name"]:
                if k_val > 280:
                    total_kg = round(total_kg * 0.5, 1)
                    bag_count = round(total_kg / bag_weight, 1)
                    adjustment_note = "ℹ️ High available potassium (>280 kg/ha); MOP reduced by 50%."

        fertilizer_list.append({
            "fertilizer_name": f["name"],
            "dose_per_acre": f"{f['per_acre_kg']} kg/acre",
            "total_quantity_kg": total_kg,
            "total_bags": f"{bag_count} bags ({bag_weight} kg per bag)",
            "timing": f["application_timing"],
            "purpose": f["purpose"],
            "adjustment_note": adjustment_note
        })

    # Pesticide dosage
    pesticide_list = []
    for p in crop_info["pesticides"]:
        pesticide_list.append({
            "name": p["name"],
            "dosage_per_acre": p["dosage_per_acre"],
            "target_pest": p["target_pest"],
            "safety_interval": p["safety_interval"]
        })

    urea_bags_50kg = 0.0
    dap_bags_50kg = 0.0
    mop_bags_50kg = 0.0
    for f in fertilizer_list:
        fname = f["fertilizer_name"].lower()
        if "urea" in fname:
            urea_bags_50kg = round(f["total_quantity_kg"] / 50.0, 1)
        elif "dap" in fname:
            dap_bags_50kg = round(f["total_quantity_kg"] / 50.0, 1)
        elif "mop" in fname or "potash" in fname:
            mop_bags_50kg = round(f["total_quantity_kg"] / 50.0, 1)

    fertilizers_dict = {
        "urea_50kg_bags": urea_bags_50kg,
        "dap_50kg_bags": dap_bags_50kg,
        "mop_50kg_bags": mop_bags_50kg,
        "items": fertilizer_list
    }

    return {
        "crop_key": key,
        "crop_display_name": crop_info["crop_name"],
        "land_area_acres": acres,
        "ideal_ph_range": crop_info["ideal_ph"],
        "fertilizers": fertilizers_dict,
        "fertilizer_recommendations": fertilizer_list,
        "pesticides_schedule": pesticide_list,
        "pesticide_recommendations": pesticide_list,
        "when_not_to_use": crop_info["when_not_to_use"],
        "when_not_to_use_fertilizers": crop_info["when_not_to_use"]
    }

# -------------------------------------------------------------
# API ENDPOINTS
# -------------------------------------------------------------

@router.get("/advisory")
def get_crop_advisory(
    crop: str = "Wheat",
    land_area: Optional[float] = None,
    acres: Optional[float] = None,
    farmer_phone: Optional[str] = None,
    ph: Optional[float] = None,
    n: Optional[float] = None,
    p: Optional[float] = None,
    k: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """
    Compute real-time crop fertilizer dosage, pesticides, and "When NOT to use" restrictions
    """
    effective_acres = acres if acres is not None else (land_area if land_area is not None else 1.0)
    soil_data = None
    if farmer_phone:
        clean_p = farmer_phone.replace(" ", "").replace("+91", "").strip()
        rec = db.query(SoilTestRecord).filter(
            (SoilTestRecord.farmer_phone == clean_p) | (SoilTestRecord.farmer_id == clean_p)
        ).order_by(SoilTestRecord.created_at.desc()).first()
        if rec and rec.status == "COMPLETED":
            soil_data = {
                "ph_level": rec.ph_level,
                "nitrogen_kg_ha": rec.nitrogen_kg_ha,
                "phosphorus_kg_ha": rec.phosphorus_kg_ha,
                "potassium_kg_ha": rec.potassium_kg_ha
            }

    if not soil_data and (ph is not None or n is not None or p is not None or k is not None):
        soil_data = {
            "ph_level": ph or 7.2,
            "nitrogen_kg_ha": n or 240.0,
            "phosphorus_kg_ha": p or 16.5,
            "potassium_kg_ha": k or 210.0
        }

    adv = _calculate_crop_advisory(crop, effective_acres, soil_data)
    return {
        "success": True,
        "advisory": adv,
        "fertilizers": adv["fertilizers"],
        "pesticides_schedule": adv["pesticides_schedule"],
        "when_not_to_use_fertilizers": adv["when_not_to_use_fertilizers"]
    }

@router.post("/book")
def book_soil_testing_slot(req: SoilTestBookingRequest, db: Session = Depends(get_db)):
    """
    Farmer books a soil testing appointment and sample submission slot
    """
    clean_phone = req.farmer_phone.replace(" ", "").replace("+91", "").strip()
    record_id = f"ST-2026-{random.randint(1000, 9999)}"
    sample_id = f"SMP-HR-{random.randint(5000, 9999)}"

    # Create new booking entry
    record = SoilTestRecord(
        id=record_id,
        sample_id=sample_id,
        farmer_id=req.farmer_id or f"USR-FARMER-{clean_phone[-4:]}",
        farmer_name=req.farmer_name,
        farmer_phone=clean_phone,
        district=req.district or "Karnal",
        state=req.state or "Haryana",
        village=req.village or "Kachhwa",
        center_id=req.center_id or "CTR-HR-01",
        center_name=req.lab_name or req.center_name or "Karnal Central Procurement Center",
        booking_date=req.booking_date,
        time_slot=req.preferred_slot or req.time_slot or "10:00 AM – 11:30 AM",
        crop_planned=req.crop_planned or "Wheat (Grade A)",
        land_area_acres=req.land_area_acres,
        soil_type=req.soil_type or "Alluvial Loam",
        status="BOOKED",
        ph_level=7.2,
        ec_level=0.45,
        organic_carbon_percent=0.52,
        nitrogen_kg_ha=240.0,
        phosphorus_kg_ha=16.5,
        potassium_kg_ha=210.0,
        zinc_ppm=0.55,
        sulphur_ppm=8.2,
        health_status="PENDING_TEST",
        advisory_notes="Soil health card report will be issued within 24-48 hours after sample submission at the lab.",
        created_at=datetime.datetime.utcnow(),
        tested_at=datetime.datetime.utcnow()
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "success": True,
        "sample_id": record.sample_id,
        "message": "Soil testing slot booked successfully!",
        "booking": {
            "record_id": record.id,
            "sample_id": record.sample_id,
            "farmer_name": record.farmer_name,
            "center_name": record.center_name,
            "date": record.booking_date,
            "time_slot": record.time_slot,
            "crop": record.crop_planned,
            "land_area": record.land_area_acres,
            "status": record.status
        }
    }

@router.get("/farmer/{farmer_id_or_phone}")
def get_farmer_soil_status(farmer_id_or_phone: str, crop_override: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Check: Did farmer have soil testing done or not?
    Returns active Soil Health Card, test values, and tailored crop fertilizer/pesticide advisory.
    """
    clean_val = farmer_id_or_phone.replace(" ", "").replace("+91", "").strip()

    # Search by phone or ID - prefer COMPLETED record if available so farmer gets lab advisory
    records = db.query(SoilTestRecord).filter(
        (SoilTestRecord.farmer_phone == clean_val) |
        (SoilTestRecord.farmer_id == clean_val) |
        (SoilTestRecord.farmer_phone.like(f"%{clean_val}%"))
    ).order_by(SoilTestRecord.created_at.desc()).all()

    if not records:
        return {
            "success": True,
            "has_soil_test": False,
            "tested": False,
            "is_completed": False,
            "status": "NOT_DONE",
            "test_status": "NOT_DONE",
            "status_label": "Soil Testing NOT Done",
            "message": "No registered soil test record found for this farmer. Please book an appointment slot."
        }

    record = next((r for r in records if r.status == "COMPLETED"), records[0])

    target_crop = crop_override or record.crop_planned
    soil_data = {
        "ph_level": record.ph_level,
        "organic_carbon_percent": record.organic_carbon_percent,
        "nitrogen_kg_ha": record.nitrogen_kg_ha,
        "phosphorus_kg_ha": record.phosphorus_kg_ha,
        "potassium_kg_ha": record.potassium_kg_ha,
        "zinc_ppm": record.zinc_ppm,
        "sulphur_ppm": record.sulphur_ppm
    }

    advisory = _calculate_crop_advisory(target_crop, record.land_area_acres, soil_data)
    is_completed = record.status == "COMPLETED"
    test_status = "Completed" if is_completed else ("In Progress" if record.status in ["BOOKED", "SAMPLE_COLLECTED", "IN_PROGRESS", "IN_TESTING"] else record.status)

    return {
        "success": True,
        "has_soil_test": True,
        "tested": is_completed,
        "is_completed": is_completed,
        "status": record.status,
        "test_status": test_status,
        "record_id": record.id,
        "sample_id": record.sample_id,
        "farmer_name": record.farmer_name,
        "farmer_phone": record.farmer_phone,
        "district": record.district,
        "center_name": record.center_name,
        "test_date": record.tested_at.strftime("%d-%m-%Y") if record.tested_at else record.booking_date,
        "crop_planned": target_crop,
        "land_area_acres": record.land_area_acres,
        "soil_type": record.soil_type,
        "status_label": "Soil Testing Completed" if is_completed else "Sample In Lab / In Progress",
        "soil_health_card": {
            "ph_level": record.ph_level,
            "ph_status": "Neutral" if 6.5 <= record.ph_level <= 7.8 else ("Acidic" if record.ph_level < 6.5 else "Alkaline"),
            "ec_level": record.ec_level,
            "organic_carbon_percent": record.organic_carbon_percent,
            "oc_status": "Medium" if record.organic_carbon_percent >= 0.5 else "Low",
            "nitrogen_kg_ha": record.nitrogen_kg_ha,
            "n_status": "Low" if record.nitrogen_kg_ha < 280 else ("Medium" if record.nitrogen_kg_ha <= 560 else "High"),
            "phosphorus_kg_ha": record.phosphorus_kg_ha,
            "p_status": "Medium" if 10 <= record.phosphorus_kg_ha <= 25 else ("Low" if record.phosphorus_kg_ha < 10 else "High"),
            "potassium_kg_ha": record.potassium_kg_ha,
            "k_status": "Medium" if 110 <= record.potassium_kg_ha <= 280 else ("Low" if record.potassium_kg_ha < 110 else "High"),
            "zinc_ppm": record.zinc_ppm,
            "zinc_status": "Deficient" if record.zinc_ppm < 0.6 else "Sufficient",
            "sulphur_ppm": record.sulphur_ppm,
            "health_grade": record.health_status
        },
        "latest_record": {
            "sample_id": record.sample_id,
            "lab_name": record.center_name,
            "test_date": record.tested_at.strftime("%d-%m-%Y") if record.tested_at else record.booking_date,
            "overall_health_grade": record.health_status or "A",
            "ph": record.ph_level,
            "nitrogen_kg_ha": record.nitrogen_kg_ha,
            "phosphorus_kg_ha": record.phosphorus_kg_ha,
            "potassium_kg_ha": record.potassium_kg_ha,
            "organic_carbon_percent": record.organic_carbon_percent,
            "electrical_conductivity": record.ec_level,
            "zinc_ppm": record.zinc_ppm,
            "sulphur_ppm": record.sulphur_ppm
        },
        "advisory": advisory
    }

@router.get("/records")
def list_soil_test_records(
    q: Optional[str] = None,
    status: Optional[str] = None,
    district: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Operator and Admin search across all farmer soil test records
    """
    query = db.query(SoilTestRecord)
    if q:
        clean_q = q.strip()
        query = query.filter(
            (SoilTestRecord.farmer_name.ilike(f"%{clean_q}%")) |
            (SoilTestRecord.farmer_phone.ilike(f"%{clean_q}%")) |
            (SoilTestRecord.sample_id.ilike(f"%{clean_q}%")) |
            (SoilTestRecord.id.ilike(f"%{clean_q}%"))
        )
    if status:
        query = query.filter(SoilTestRecord.status == status.strip().upper())
    if district:
        query = query.filter(SoilTestRecord.district.ilike(f"%{district.strip()}%"))

    records = query.order_by(SoilTestRecord.created_at.desc()).all()

    formatted = []
    for r in records:
        formatted.append({
            "record_id": r.id,
            "sample_id": r.sample_id,
            "farmer_name": r.farmer_name,
            "farmer_phone": r.farmer_phone,
            "district": r.district,
            "center_name": r.center_name,
            "crop_planned": r.crop_planned,
            "land_area": r.land_area_acres,
            "status": r.status,
            "ph": r.ph_level,
            "nitrogen": r.nitrogen_kg_ha,
            "phosphorus": r.phosphorus_kg_ha,
            "potassium": r.potassium_kg_ha,
            "date": r.booking_date,
            "health_status": r.health_status
        })

    return {
        "success": True,
        "total": len(formatted),
        "data": formatted
    }

@router.post("/update-report")
def update_soil_test_report(req: SoilTestUpdateRequest, db: Session = Depends(get_db)):
    """
    Operator records laboratory testing values and marks soil health card as completed
    """
    lookup_id = (req.record_id or req.sample_id or "").strip()
    record = None

    if lookup_id:
        record = db.query(SoilTestRecord).filter(
            (SoilTestRecord.id == lookup_id) |
            (SoilTestRecord.sample_id == lookup_id)
        ).first()

    if not record and req.farmer_phone:
        clean_phone = req.farmer_phone.replace(" ", "").replace("+91", "").strip()
        record = db.query(SoilTestRecord).filter(
            (SoilTestRecord.farmer_phone == clean_phone) |
            (SoilTestRecord.farmer_phone.like(f"%{clean_phone}%"))
        ).order_by(SoilTestRecord.created_at.desc()).first()

    if not record:
        # Create a new completed record if none existed
        import uuid
        farmer_phone = (req.farmer_phone or "9876543210").strip()
        farmer = db.query(User).filter(User.phone == farmer_phone).first()
        record = SoilTestRecord(
            id=f"STR-{uuid.uuid4().hex[:8].upper()}",
            sample_id=req.sample_id or f"SHC-2026-{random.randint(1000, 9999)}",
            farmer_id=farmer.id if farmer else "USR-FARMER-01",
            farmer_name=farmer.name if farmer else "Farmer",
            farmer_phone=farmer_phone,
            district="Karnal",
            state="Haryana",
            center_name="Karnal Central Soil Testing Lab",
            booking_date=datetime.datetime.utcnow().strftime("%Y-%m-%d"),
            crop_planned="Wheat (Grade A)",
            land_area_acres=2.5,
            soil_type="Alluvial Loam"
        )
        db.add(record)

    ph_val = req.ph if req.ph is not None else (req.ph_level if req.ph_level is not None else 7.2)
    ec_val = req.electrical_conductivity if req.electrical_conductivity is not None else (req.ec_level if req.ec_level is not None else 0.45)

    record.ph_level = ph_val
    record.ec_level = ec_val
    record.organic_carbon_percent = req.organic_carbon_percent if req.organic_carbon_percent is not None else 0.55
    record.nitrogen_kg_ha = req.nitrogen_kg_ha if req.nitrogen_kg_ha is not None else 280.0
    record.phosphorus_kg_ha = req.phosphorus_kg_ha if req.phosphorus_kg_ha is not None else 22.0
    record.potassium_kg_ha = req.potassium_kg_ha if req.potassium_kg_ha is not None else 210.0
    record.zinc_ppm = req.zinc_ppm if req.zinc_ppm is not None else 0.55
    record.sulphur_ppm = req.sulphur_ppm if req.sulphur_ppm is not None else 8.2
    record.health_status = req.health_status or "GOOD"
    record.status = "COMPLETED"
    record.tested_at = datetime.datetime.utcnow()
    record.advisory_notes = req.advisory_notes or "Testing completed. Follow scientific dosage recommendations."

    db.commit()
    db.refresh(record)

    return {
        "success": True,
        "message": "Soil testing report updated successfully!",
        "record_id": record.id,
        "sample_id": record.sample_id,
        "status": record.status
    }
