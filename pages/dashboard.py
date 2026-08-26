<<<<<<< HEAD
import streamlit as st
import pandas as pd
from datetime import date, timedelta
import streamlit.components.v1 as components
from pathlib import Path
import base64
import re
import numpy as np
from sklearn.pipeline import Pipeline  # type: ignore[reportMissingModuleSource]
from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore[reportMissingModuleSource]
from sklearn.linear_model import LogisticRegression  # type: ignore[reportMissingModuleSource]
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier  # type: ignore[reportMissingModuleSource]


# ============================================================
# MACHINE LEARNING - VEHICLE FAULT DIAGNOSIS
# ============================================================
# This is a lightweight supervised text-classification model.
# It learns from curated symptom examples and predicts the most
# likely fault from the user's natural-language description.
#
# IMPORTANT:
# For a production-grade project, replace the small curated
# training set below with a larger real-world labelled dataset.

ML_TRAINING_DATA = [
    # Engine Not Starting
    ("bike is not starting engine does not start", "Engine Not Starting"),
    ("self starts but engine does not start", "Engine Not Starting"),
    ("bike won't start", "Engine Not Starting"),
    ("motorcycle not starting", "Engine Not Starting"),
    ("engine cranks but does not start", "Engine Not Starting"),
    ("bike stopped and now it will not start", "Engine Not Starting"),
    ("starter works but engine does not start", "Engine Not Starting"),

    # Battery Problem
    ("battery is weak", "Battery Problem"),
    ("battery discharged", "Battery Problem"),
    ("bike battery is dead", "Battery Problem"),
    ("headlight is dim and battery is weak", "Battery Problem"),
    ("battery not holding charge", "Battery Problem"),
    ("battery voltage is low", "Battery Problem"),
    ("bike has weak battery", "Battery Problem"),

    # Brake Problem
    ("brakes are not working properly", "Brake Problem"),
    ("brake feels weak", "Brake Problem"),
    ("brake pad worn", "Brake Problem"),
    ("brake lever is soft", "Brake Problem"),
    ("braking distance is high", "Brake Problem"),
    ("front brake problem", "Brake Problem"),
    ("rear brake problem", "Brake Problem"),

    # Tyre Problem
    ("tyre is punctured", "Tyre Problem"),
    ("tire has low pressure", "Tyre Problem"),
    ("tyre pressure is low", "Tyre Problem"),
    ("bike tyre is worn", "Tyre Problem"),
    ("wheel feels unstable", "Tyre Problem"),
    ("tyre problem", "Tyre Problem"),

    # Engine Overheating
    ("engine is overheating", "Engine Overheating"),
    ("bike gets very hot", "Engine Overheating"),
    ("engine temperature is high", "Engine Overheating"),
    ("bike overheats in traffic", "Engine Overheating"),
    ("engine becomes too hot", "Engine Overheating"),
    ("overheating problem", "Engine Overheating"),

    # Oil Leakage
    ("oil is leaking", "Oil Leakage"),
    ("engine oil leakage", "Oil Leakage"),
    ("oil dripping from bike", "Oil Leakage"),
    ("oil leak under motorcycle", "Oil Leakage"),
    ("engine is losing oil", "Oil Leakage"),
    ("oil drops under bike", "Oil Leakage"),

    # Chain/Sprocket Problem
    ("chain is loose", "Chain/Sprocket Problem"),
    ("chain makes noise", "Chain/Sprocket Problem"),
    ("sprocket is worn", "Chain/Sprocket Problem"),
    ("chain needs lubrication", "Chain/Sprocket Problem"),
    ("chain and sprocket problem", "Chain/Sprocket Problem"),
    ("chain is making clicking noise", "Chain/Sprocket Problem"),

    # Clutch Problem
    ("clutch is slipping", "Clutch Problem"),
    ("clutch problem", "Clutch Problem"),
    ("clutch is hard", "Clutch Problem"),
    ("clutch lever problem", "Clutch Problem"),
    ("clutch free play problem", "Clutch Problem"),
    ("bike clutch is not working", "Clutch Problem"),

    # Gear Shifting Problem
    ("gear is not shifting", "Gear Shifting Problem"),
    ("gear shifting is hard", "Gear Shifting Problem"),
    ("cannot change gears", "Gear Shifting Problem"),
    ("gear lever problem", "Gear Shifting Problem"),
    ("bike gears are stuck", "Gear Shifting Problem"),
    ("difficulty changing gear", "Gear Shifting Problem"),

    # Poor Mileage
    ("bike mileage is low", "Poor Mileage"),
    ("fuel consumption is high", "Poor Mileage"),
    ("poor fuel economy", "Poor Mileage"),
    ("bike gives low mileage", "Poor Mileage"),
    ("petrol consumption increased", "Poor Mileage"),
    ("mileage has decreased", "Poor Mileage"),

    # Low Pickup
    ("bike has low pickup", "Low Pickup"),
    ("pickup is poor", "Low Pickup"),
    ("bike is slow to accelerate", "Low Pickup"),
    ("acceleration is weak", "Low Pickup"),
    ("motorcycle lacks power", "Low Pickup"),
    ("bike has no pickup", "Low Pickup"),

    # Excessive Smoke
    ("bike is producing too much smoke", "Excessive Smoke"),
    ("black smoke from exhaust", "Excessive Smoke"),
    ("blue smoke from engine", "Excessive Smoke"),
    ("white smoke from exhaust", "Excessive Smoke"),
    ("excessive exhaust smoke", "Excessive Smoke"),
    ("smoke coming from exhaust", "Excessive Smoke"),

    # Strange Noise
    ("strange noise from engine", "Strange Noise"),
    ("engine making unusual noise", "Strange Noise"),
    ("clicking sound from bike", "Strange Noise"),
    ("knocking noise", "Strange Noise"),
    ("rattling noise", "Strange Noise"),
    ("bike is making strange sound", "Strange Noise"),

    # Electrical Problem
    ("headlight is not working", "Electrical Problem"),
    ("indicator is not working", "Electrical Problem"),
    ("electrical problem", "Electrical Problem"),
    ("fuse keeps blowing", "Electrical Problem"),
    ("wiring problem", "Electrical Problem"),
    ("horn is not working", "Electrical Problem"),
]

ML_TEXTS = [x[0] for x in ML_TRAINING_DATA]
ML_LABELS = [x[1] for x in ML_TRAINING_DATA]

@st.cache_resource
def train_fault_model():
    model = Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=1
        )),
        ("classifier", LogisticRegression(
            max_iter=2000,
            class_weight="balanced"
        ))
    ])
    model.fit(ML_TEXTS, ML_LABELS)
    return model

fault_model = train_fault_model()

def clean_problem_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def predict_fault(description):
    cleaned = clean_problem_text(description)
    probabilities = fault_model.predict_proba([cleaned])[0]
    classes = fault_model.classes_
    order = np.argsort(probabilities)[::-1]

    top_predictions = [
        (classes[i], float(probabilities[i]))
        for i in order[:3]
    ]
    return top_predictions

# ============================================================
# ADVANCED ML - VEHICLE HEALTH + PREDICTIVE MAINTENANCE
# ============================================================
# These models learn from a generated labelled training set so the
# Streamlit app works immediately. For the final project, replace
# this training set with a real service/maintenance dataset.

HEALTH_FEATURE_NAMES = [
    "vehicle_age",
    "current_km_10k",
    "days_since_service_180",
    "service_count",
    "recent_fault_count",
    "high_severity_faults"
]

@st.cache_resource
def train_health_model():
    rng = np.random.default_rng(42)
    n = 2500
    age = rng.uniform(0, 15, n)
    km10 = rng.uniform(0, 15, n)
    days = rng.uniform(0, 360, n)
    service_count = rng.integers(0, 16, n)
    faults = rng.integers(0, 8, n)
    high_faults = rng.integers(0, 5, n)

    # Synthetic target representing a reasonable vehicle-health pattern.
    score = (
        100
        - age * 1.7
        - km10 * 2.0
        - np.maximum(days - 45, 0) * 0.045
        + np.minimum(service_count, 12) * 0.9
        - faults * 2.2
        - high_faults * 4.5
        + rng.normal(0, 2.5, n)
    )
    score = np.clip(score, 20, 100)

    X = np.column_stack([age, km10, days, service_count, faults, high_faults])
    model = RandomForestRegressor(
        n_estimators=180,
        random_state=42,
        min_samples_leaf=3,
        n_jobs=-1
    )
    model.fit(X, score)
    return model

@st.cache_resource
def train_maintenance_model():
    rng = np.random.default_rng(123)
    n = 2500
    age = rng.uniform(0, 15, n)
    km10 = rng.uniform(0, 15, n)
    days = rng.uniform(0, 360, n)
    service_count = rng.integers(0, 16, n)
    faults = rng.integers(0, 8, n)
    high_faults = rng.integers(0, 5, n)

    risk_signal = (
        0.25 * age
        + 0.35 * km10
        + 0.012 * np.maximum(days - 30, 0)
        - 0.18 * service_count
        + 0.65 * faults
        + 1.25 * high_faults
        + rng.normal(0, 1.0, n)
    )
    maintenance_needed = (risk_signal > 5.0).astype(int)

    X = np.column_stack([age, km10, days, service_count, faults, high_faults])
    model = RandomForestClassifier(
        n_estimators=180,
        random_state=123,
        class_weight="balanced",
        min_samples_leaf=3,
        n_jobs=-1
    )
    model.fit(X, maintenance_needed)
    return model

health_model = train_health_model()
maintenance_model = train_maintenance_model()

def get_vehicle_ml_features():
    """Build ML features from the user's saved vehicle and service history."""
    info = st.session_state.get("vehicle_info", {})
    current_year = int(info.get("Year", date.today().year))
    current_km = float(info.get("Current KM", 0) or 0)

    history = st.session_state.get("history", [])
    vehicle_company = info.get("Company", "")
    vehicle_model = info.get("Model", "")

    matching_history = [
        h for h in history
        if h.get("Company") == vehicle_company and h.get("Model") == vehicle_model
    ]

    service_count = len(matching_history)
    if matching_history:
        latest = max(matching_history, key=lambda h: h.get("Date", date.min))
        latest_date = latest.get("Date", date.today())
        last_service_km = float(latest.get("KM", 0) or 0)
        days_since_service = max((date.today() - latest_date).days, 0)
        if current_km <= 0:
            current_km = last_service_km
    else:
        last_service_km = 0
        days_since_service = 365

    diagnoses = st.session_state.get("diagnosis_history", [])
    matching_diagnoses = [
        d for d in diagnoses
        if d.get("Company") == vehicle_company and d.get("Model") == vehicle_model
    ]
    recent_diagnoses = matching_diagnoses[-8:]
    high_severity_faults = sum(
        1 for d in recent_diagnoses
        if d.get("Severity") in {"HIGH", "CRITICAL"}
    )

    features = np.array([[
        max(date.today().year - current_year, 0),
        current_km / 10000.0,
        min(days_since_service, 720) / 180.0,
        service_count,
        len(recent_diagnoses),
        high_severity_faults
    ]], dtype=float)

    return features, {
        "current_km": current_km,
        "last_service_km": last_service_km,
        "days_since_service": days_since_service,
        "service_count": service_count,
        "recent_fault_count": len(recent_diagnoses),
        "high_severity_faults": high_severity_faults,
        "vehicle_age": max(date.today().year - current_year, 0),
    }

def predict_vehicle_health():
    features, meta = get_vehicle_ml_features()
    score = float(np.clip(health_model.predict(features)[0], 0, 100))
    risk_prob = float(maintenance_model.predict_proba(features)[0][1])
    return score, risk_prob, meta

def health_label(score):
    if score >= 85:
        return "Excellent", "🟢"
    if score >= 70:
        return "Good", "🟢"
    if score >= 50:
        return "Needs Attention", "🟡"
    return "Critical", "🔴"

def maintenance_label(probability):
    if probability >= 0.75:
        return "High Risk", "🔴"
    if probability >= 0.45:
        return "Medium Risk", "🟡"
    return "Low Risk", "🟢"

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Mechanical Help Center",
    page_icon="🏍️",
    layout="wide"
)

# ============================================================
# LOGIN PROTECTION
# ============================================================

if not st.session_state.get("logged_in", False):
    st.warning("⚠️ Please login first.")
    st.switch_page("app.py")

username = st.session_state.get("username", "User")

# ============================================================
# INITIALIZE SERVICE HISTORY
# ============================================================

if "history" not in st.session_state:
    st.session_state["history"] = []

if "diagnosis_history" not in st.session_state:
    st.session_state["diagnosis_history"] = []

vehicle_data = {
    "Hero": {"Splendor": "models/hero_splendor.glb", "HF Deluxe": "models/hero_hf_deluxe.glb", "Passion": "models/hero_passion.glb", "Glamour": "models/hero_glamour.glb", "Xtreme 125R": "models/hero_xtreme_125r.glb"},
    "Honda": {"Shine": "models/honda_shine.glb", "SP 125": "models/honda_sp125.glb", "Unicorn": "models/honda_unicorn.glb", "Activa": "models/honda_activa.glb", "Hornet 2.0": "models/honda_hornet_2.glb"},
    "Bajaj": {"Pulsar 125": "models/bajaj_pulsar_125.glb", "Pulsar 150": "models/bajaj_pulsar_150.glb", "Pulsar NS200": "models/bajaj_pulsar_ns200.glb", "Platina": "models/bajaj_platina.glb", "Avenger": "models/bajaj_avenger.glb"},
    "TVS": {"Apache RTR 160": "models/tvs_apache_rtr_160.glb", "Apache RTR 200": "models/tvs_apache_rtr_200.glb", "Raider": "models/tvs_raider.glb", "Sport": "models/tvs_sport.glb", "Jupiter": "models/tvs_jupiter.glb"},
    "Yamaha": {"FZ": "models/yamaha_fz.glb", "MT-15": "models/yamaha_mt15.glb", "R15": "models/yamaha_r15.glb", "Fascino": "models/yamaha_fascino.glb", "Ray ZR": "models/yamaha_ray_zr.glb"},
    "Suzuki": {"Access 125": "models/suzuki_access_125.glb", "Burgman Street": "models/suzuki_burgman_street.glb", "Gixxer": "models/suzuki_gixxer.glb", "Avenis": "models/suzuki_avenis.glb"},
    "Royal Enfield": {"Classic 350": "models/re_classic_350.glb", "Bullet 350": "models/re_bullet_350.glb", "Hunter 350": "models/re_hunter_350.glb", "Meteor 350": "models/re_meteor_350.glb"},
}



# ============================================================
# HEADER
# ============================================================

st.title("🤖 AI Mechanical Help Center")
st.subheader(
    f"🏍️ Smart Self-Service Assistant for 2-Wheelers | Welcome {username} 👋"
)

st.markdown("---")

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ Menu")

menu = st.sidebar.radio(
    "Select Option",
    [
        "🏠 Home",
        "🏍️ 3D Bike View",
        "🔧 Vehicle Diagnosis",
        "🛠 Maintenance Tips",
        "📋 Service History",
        "❤️ Vehicle Health & Predictive Maintenance",
        "📞 Contact Support",
        "🚪 Logout"
    ]
)

# ============================================================
# HOME
# ============================================================

if menu == "🏠 Home":

    st.header("🏠 Vehicle Information")

    st.success(
        f"Welcome {username}! 🤖 Your AI Mechanical Help Center is ready."
    )

    col1, col2 = st.columns(2)

    with col1:

        company = st.selectbox(
            "🏍️ Vehicle Company",
            list(vehicle_data.keys())
        )

        model = st.selectbox(
            "🏍️ Vehicle Model",
            list(vehicle_data[company].keys())
        )

        year = st.number_input(
            "📅 Manufacturing Year",
            min_value=2000,
            max_value=2026,
            value=2024,
            step=1
        )

    with col2:

        owner = st.text_input(
            "👤 Owner Name"
        )

        number = st.text_input(
            "🔢 Vehicle Number"
        )

        fuel = st.selectbox(
            "⛽ Fuel Type",
            [
                "Petrol",
                "Electric"
            ]
        )

        current_km = st.number_input(
            "🛣️ Current Kilometer",
            min_value=0,
            step=100,
            value=0
        )

    st.markdown("---")

    if st.button(
        "💾 Save Vehicle Information",
        use_container_width=True
    ):

        st.session_state["vehicle_info"] = {
            "Owner": owner,
            "Vehicle Number": number,
            "Company": company,
            "Model": model,
            "Year": year,
            "Fuel": fuel,
            "Current KM": current_km
        }

        st.success(
            "✅ Vehicle information saved successfully!"
        )

    st.info(
        "💡 Select an option from the left menu to use the vehicle services."
    )

# ============================================================
# 3D BIKE VIEW
# ============================================================

elif menu == "🏍️ 3D Bike View":

    st.header("🏍️ 360° 2-Wheeler Viewer")

    st.info(
        "Select your company and model to view the 3D vehicle."
    )

    company = st.selectbox(
        "Select Vehicle Company",
        list(vehicle_data.keys())
    )

    model = st.selectbox(
        "Select Vehicle Model",
        list(vehicle_data[company].keys())
    )

    model_path = vehicle_data[company][model]

    BASE_DIR = Path(__file__).resolve().parent

    model_file = BASE_DIR / model_path

    st.write("📁 3D Model Path:")
    st.code(str(model_file))

    if not model_file.exists():

        st.error("❌ 3D model file not found!")

        st.write("Expected location:")
        st.code(str(model_file))

        st.warning(
            f"Create the folder 'models' beside your dashboard.py "
            f"and place the GLB file for {company} {model} inside it."
        )

    else:

        st.success(
            f"✅ {company} {model} 3D model found!"
        )

        try:

            with open(model_file, "rb") as file:
                model_bytes = file.read()

            model_base64 = base64.b64encode(
                model_bytes
            ).decode("utf-8")

            model_url = (
                "data:model/gltf-binary;base64,"
                + model_base64
            )

            html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<script
type="module"
src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js">
</script>

<style>

html,
body {{
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #eeeeee;
}}

model-viewer {{
    width: 100%;
    height: 650px;
    background: #eeeeee;
    border-radius: 15px;
}}

</style>

</head>

<body>

<model-viewer

src="{model_url}"

camera-controls

auto-rotate

auto-rotate-delay="0"

rotation-per-second="20deg"

shadow-intensity="1"

exposure="1"

camera-orbit="0deg 75deg 3m"

field-of-view="30deg"

interaction-prompt="auto"

loading="eager"

reveal="auto"

alt="{company} {model} 3D Model">

</model-viewer>

</body>

</html>
"""

            components.html(
                html,
                height=700,
                scrolling=False
            )

            st.info(
                "🖱️ Drag = Rotate | 🔍 Scroll = Zoom | 🔄 Auto-rotate = ON"
            )

        except Exception as e:

            st.error(
                "❌ Error loading the 3D model"
            )

            st.exception(e)

# ============================================================
# VEHICLE DIAGNOSIS
# ============================================================

elif menu == "🔧 Vehicle Diagnosis":

    st.header("🔧 AI Vehicle Diagnosis")
    st.write("Describe your vehicle problem and get possible causes and recommended actions.")

    # --------------------------------------------------------
    # VEHICLE DATA
    # --------------------------------------------------------

    diagnosis_vehicle_data = {

        "Hero": [
            "Splendor",
            "HF Deluxe",
            "Passion",
            "Glamour",
            "Xtreme 125R"
        ],

        "Honda": [
            "Shine",
            "SP 125",
            "Unicorn",
            "Activa",
            "Hornet 2.0"
        ],

        "Bajaj": [
            "Pulsar 125",
            "Pulsar 150",
            "Pulsar NS200",
            "Platina",
            "Avenger"
        ],

        "TVS": [
            "Apache RTR 160",
            "Apache RTR 200",
            "Raider",
            "Sport",
            "Jupiter"
        ],

        "Yamaha": [
            "FZ",
            "MT-15",
            "R15",
            "Fascino",
            "Ray ZR"
        ],

        "Suzuki": [
            "Access 125",
            "Burgman Street",
            "Gixxer",
            "Avenis"
        ],

        "Royal Enfield": [
            "Classic 350",
            "Bullet 350",
            "Hunter 350",
            "Meteor 350"
        ]
    }

    # --------------------------------------------------------
    # VEHICLE SELECTION
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        company = st.selectbox(
            "🏍️ Vehicle Company",
            list(diagnosis_vehicle_data.keys()),
            key="diagnosis_company"
        )

        model = st.selectbox(
            "🏍️ Vehicle Model",
            diagnosis_vehicle_data[company],
            key="diagnosis_model"
        )

    with col2:

        year = st.number_input(
            "📅 Manufacturing Year",
            min_value=2000,
            max_value=2026,
            value=2024,
            step=1,
            key="diagnosis_year"
        )

        problem = st.selectbox(
            "⚠️ Select Vehicle Problem",
            [
                "Engine Not Starting",
                "Battery Problem",
                "Brake Problem",
                "Tyre Problem",
                "Engine Overheating",
                "Oil Leakage",
                "Chain/Sprocket Problem",
                "Clutch Problem",
                "Gear Shifting Problem",
                "Poor Mileage",
                "Low Pickup",
                "Excessive Smoke",
                "Strange Noise",
                "Electrical Problem",
                "Other"
            ],
            key="diagnosis_problem"
        )

    # --------------------------------------------------------
    # PROBLEM DESCRIPTION
    # --------------------------------------------------------

    description = st.text_area(
        "📝 Describe Your Problem",
        placeholder="Example: Bike is not starting, starter is working but engine is not starting...",
        height=130,
        key="diagnosis_description"
    )

    # --------------------------------------------------------
    # DIAGNOSIS DATABASE
    # --------------------------------------------------------

    diagnosis_database = {

        "Engine Not Starting": {

            "causes": [
                "Weak or discharged battery",
                "Fuel supply problem",
                "Spark plug problem",
                "Engine kill switch may be OFF",
                "Starter motor or ignition problem"
            ],

            "checks": [
                "Check battery voltage",
                "Check fuel level",
                "Check spark plug",
                "Check engine kill switch",
                "Check starter motor"
            ],

            "solution": [
                "Charge or replace the battery if required",
                "Check fuel supply",
                "Clean or replace the spark plug",
                "Keep the engine kill switch in RUN position",
                "Contact a mechanic if the starter motor has a fault"
            ],

            "severity": "HIGH"
        },

        "Battery Problem": {

            "causes": [
                "Battery discharged",
                "Loose battery terminals",
                "Battery is old",
                "Charging system problem"
            ],

            "checks": [
                "Check battery voltage",
                "Check battery terminals",
                "Check charging voltage",
                "Check battery age"
            ],

            "solution": [
                "Charge the battery",
                "Clean and tighten terminals",
                "Check alternator/charging system",
                "Replace battery if it is damaged"
            ],

            "severity": "MEDIUM"
        },

        "Brake Problem": {

            "causes": [
                "Brake pad/shoe worn",
                "Low brake fluid",
                "Brake cable problem",
                "Brake system adjustment required"
            ],

            "checks": [
                "Inspect brake pads",
                "Check brake fluid",
                "Check brake lever/pedal",
                "Check brake cable"
            ],

            "solution": [
                "Replace worn brake pads",
                "Top up or replace brake fluid as specified",
                "Adjust or replace brake cable",
                "Have the brake system inspected by a mechanic"
            ],

            "severity": "CRITICAL"
        },

        "Tyre Problem": {

            "causes": [
                "Low tyre pressure",
                "Puncture",
                "Tyre wear",
                "Wheel alignment problem"
            ],

            "checks": [
                "Check tyre pressure",
                "Inspect tyre for puncture",
                "Check tread depth",
                "Inspect wheel alignment"
            ],

            "solution": [
                "Set correct tyre pressure",
                "Repair puncture if possible",
                "Replace badly worn tyre",
                "Check wheel alignment"
            ],

            "severity": "HIGH"
        },

        "Engine Overheating": {

            "causes": [
                "Low engine oil",
                "Cooling system problem",
                "Engine running under excessive load",
                "Blocked air flow"
            ],

            "checks": [
                "Check engine oil level",
                "Check cooling system",
                "Check for unusual engine noise",
                "Check air flow"
            ],

            "solution": [
                "Maintain correct engine oil level",
                "Allow the engine to cool",
                "Check cooling system",
                "Contact a mechanic if overheating continues"
            ],

            "severity": "HIGH"
        },

        "Oil Leakage": {

            "causes": [
                "Loose drain bolt",
                "Damaged oil seal",
                "Gasket leakage",
                "Engine component leakage"
            ],

            "checks": [
                "Identify leakage location",
                "Check drain bolt",
                "Check oil seals",
                "Check engine gasket"
            ],

            "solution": [
                "Tighten loose fasteners where appropriate",
                "Replace damaged seals",
                "Replace damaged gasket",
                "Check oil level and repair the leak"
            ],

            "severity": "HIGH"
        },

        "Chain/Sprocket Problem": {

            "causes": [
                "Chain too loose",
                "Chain too tight",
                "Poor lubrication",
                "Worn sprocket"
            ],

            "checks": [
                "Check chain slack",
                "Inspect sprocket teeth",
                "Check chain lubrication",
                "Check chain condition"
            ],

            "solution": [
                "Adjust chain slack",
                "Lubricate the chain",
                "Replace worn chain/sprocket",
                "Perform regular chain maintenance"
            ],

            "severity": "MEDIUM"
        },

        "Clutch Problem": {

            "causes": [
                "Incorrect clutch adjustment",
                "Worn clutch plates",
                "Clutch cable problem",
                "Low/incorrect engine oil"
            ],

            "checks": [
                "Check clutch free play",
                "Check clutch cable",
                "Check clutch operation",
                "Inspect clutch plates if required"
            ],

            "solution": [
                "Adjust clutch free play",
                "Lubricate or replace cable",
                "Replace worn clutch components",
                "Use the manufacturer-recommended oil"
            ],

            "severity": "MEDIUM"
        },

        "Gear Shifting Problem": {

            "causes": [
                "Clutch adjustment problem",
                "Low or incorrect oil",
                "Gear linkage problem",
                "Internal transmission problem"
            ],

            "checks": [
                "Check clutch operation",
                "Check engine oil",
                "Inspect gear lever/linkage",
                "Check for abnormal noises"
            ],

            "solution": [
                "Adjust clutch",
                "Check and replace oil if necessary",
                "Inspect gear linkage",
                "Consult a qualified mechanic for internal faults"
            ],

            "severity": "HIGH"
        },

        "Poor Mileage": {

            "causes": [
                "Dirty air filter",
                "Incorrect tyre pressure",
                "Poor riding conditions",
                "Spark plug problem",
                "Fuel system problem"
            ],

            "checks": [
                "Check air filter",
                "Check tyre pressure",
                "Inspect spark plug",
                "Check fuel system"
            ],

            "solution": [
                "Clean or replace air filter",
                "Maintain correct tyre pressure",
                "Service spark plug",
                "Check fuel system"
            ],

            "severity": "MEDIUM"
        },

        "Low Pickup": {

            "causes": [
                "Dirty air filter",
                "Spark plug problem",
                "Clutch slipping",
                "Fuel delivery problem"
            ],

            "checks": [
                "Check air filter",
                "Check spark plug",
                "Check clutch",
                "Check fuel system"
            ],

            "solution": [
                "Clean or replace air filter",
                "Clean or replace spark plug",
                "Inspect clutch",
                "Service fuel system"
            ],

            "severity": "MEDIUM"
        },

        "Excessive Smoke": {

            "causes": [
                "Engine oil burning",
                "Air filter problem",
                "Fuel mixture problem",
                "Engine wear"
            ],

            "checks": [
                "Identify smoke color",
                "Check engine oil level",
                "Check air filter",
                "Check engine condition"
            ],

            "solution": [
                "Check oil level",
                "Service air filter",
                "Inspect fuel system",
                "Get engine inspected if smoke continues"
            ],

            "severity": "HIGH"
        },

        "Strange Noise": {

            "causes": [
                "Loose component",
                "Low engine oil",
                "Chain problem",
                "Engine component wear"
            ],

            "checks": [
                "Identify noise location",
                "Check engine oil",
                "Check chain",
                "Inspect loose components"
            ],

            "solution": [
                "Tighten loose components",
                "Maintain correct oil level",
                "Adjust/lubricate chain",
                "Get the vehicle inspected if noise continues"
            ],

            "severity": "HIGH"
        },

        "Electrical Problem": {

            "causes": [
                "Blown fuse",
                "Weak battery",
                "Loose wiring",
                "Faulty switch"
            ],

            "checks": [
                "Check battery",
                "Check fuses",
                "Inspect wiring",
                "Check switches"
            ],

            "solution": [
                "Charge or replace battery",
                "Replace blown fuse with correct rating",
                "Repair loose wiring",
                "Get electrical system inspected"
            ],

            "severity": "MEDIUM"
        },

        "Other": {

            "causes": [
                "Problem requires additional inspection"
            ],

            "checks": [
                "Describe the symptoms clearly",
                "Check for unusual sounds, smells or warning lights"
            ],

            "solution": [
                "Consult a qualified mechanic for detailed inspection"
            ],

            "severity": "UNKNOWN"
        }
    }

    # --------------------------------------------------------
    # DIAGNOSE BUTTON
    # --------------------------------------------------------

    if st.button(
        "🔧 Diagnose Vehicle",
        use_container_width=True,
        type="primary"
    ):

        if not description.strip():

            st.warning(
                "⚠️ Please describe your vehicle problem first."
            )

        else:

            # ========================================================
            # ML PREDICTION
            # ========================================================
            ml_predictions = predict_fault(description)
            ml_problem, ml_confidence = ml_predictions[0]

            # Keep the existing rule-based database for explanations,
            # checks and solutions. ML decides the most likely fault.
            if ml_problem in diagnosis_database:
                result = diagnosis_database[ml_problem]
            else:
                result = diagnosis_database[problem]

            # Store diagnosis so the health and predictive-maintenance models
            # can use recent faults as additional vehicle-health signals.
            st.session_state["diagnosis_history"].append({
                "Date": date.today(),
                "Company": company,
                "Model": model,
                "Problem": ml_problem,
                "Confidence": ml_confidence,
                "Severity": result.get("severity", "UNKNOWN")
            })

            st.success("✅ ML Diagnosis Completed")

            # ------------------------------------------------
            # ML RESULT
            # ------------------------------------------------
            st.subheader("🤖 Machine Learning Diagnosis")

            ml_col1, ml_col2 = st.columns(2)

            with ml_col1:
                st.metric(
                    "Predicted Problem",
                    ml_problem
                )

            with ml_col2:
                st.metric(
                    "ML Confidence",
                    f"{ml_confidence * 100:.1f}%"
                )

            if ml_confidence >= 0.75:
                st.success(
                    f"🎯 High-confidence ML prediction: **{ml_problem}**"
                )
            elif ml_confidence >= 0.50:
                st.warning(
                    f"⚠️ Moderate-confidence ML prediction: **{ml_problem}**. "
                    "A physical inspection is recommended."
                )
            else:
                st.info(
                    f"ℹ️ ML prediction: **{ml_problem}** with low confidence. "
                    "Please provide more detailed symptoms."
                )

            # Show top 3 ML predictions
            st.write("### 🔎 Top ML Predictions")
            for rank, (predicted_problem, probability) in enumerate(
                ml_predictions, start=1
            ):
                st.write(
                    f"**{rank}. {predicted_problem}** — "
                    f"{probability * 100:.1f}%"
                )
                st.progress(min(max(probability, 0.0), 1.0))

            # Compare the user's selected problem with the ML result.
            if problem != ml_problem:
                st.warning(
                    f"⚠️ Your selected problem is **{problem}**, but the "
                    f"ML model detected **{ml_problem}** from the description. "
                    "The detailed diagnosis below is based on the ML prediction."
                )

            # ------------------------------------------------
            # VEHICLE INFORMATION
            # ------------------------------------------------

            st.subheader("🏍️ Vehicle Information")

            st.write(
                f"**Vehicle:** {company} {model}"
            )

            st.write(
                f"**Manufacturing Year:** {year}"
            )

            st.write(
                f"**Problem:** {problem}"
            )

            st.write(
                f"**Description:** {description}"
            )

            # ------------------------------------------------
            # SEVERITY
            # ------------------------------------------------

            severity = result["severity"]

            if severity == "CRITICAL":

                st.error(
                    "🚨 Severity: CRITICAL — Avoid riding until the brake problem is inspected."
                )

            elif severity == "HIGH":

                st.warning(
                    "⚠️ Severity: HIGH — Vehicle inspection is recommended soon."
                )

            elif severity == "MEDIUM":

                st.info(
                    "🟡 Severity: MEDIUM — Check the listed components."
                )

            else:

                st.info(
                    "ℹ️ Severity: UNKNOWN — Further inspection is required."
                )

            # ------------------------------------------------
            # POSSIBLE CAUSES
            # ------------------------------------------------

            st.subheader("🔍 Possible Causes")

            for cause in result["causes"]:
                st.write("• " + cause)

            # ------------------------------------------------
            # CHECK THESE FIRST
            # ------------------------------------------------

            st.subheader("🛠️ Recommended Checks")

            for check in result["checks"]:
                st.write("☑️ " + check)

            # ------------------------------------------------
            # RECOMMENDED ACTION
            # ------------------------------------------------

            st.subheader("💡 Recommended Action")

            for solution in result["solution"]:
                st.write("🔧 " + solution)

            # ------------------------------------------------
            # FINAL MESSAGE
            # ------------------------------------------------

            st.info(
                "🤖 This diagnosis uses a supervised Machine Learning "
                "text-classification model trained on curated vehicle "
                "symptom examples. The ML prediction is combined with "
                "the application's mechanical knowledge base. It is "
                "not a substitute for professional mechanical inspection."
            )

# ============================================================
# MAINTENANCE TIPS
# ============================================================

elif menu == "🛠 Maintenance Tips":

    st.header("🛠 2-Wheeler Maintenance Tips")

    company = st.selectbox(
        "Select Company",
        list(vehicle_data.keys()),
        key="maintenance_company"
    )

    model = st.selectbox(
        "Select Model",
        list(vehicle_data[company].keys()),
        key="maintenance_model"
    )

    st.success(
        f"Maintenance Guide: {company} {model}"
    )

    tips = [

        "🛢️ Check and replace engine oil at the recommended interval.",

        "🛞 Check tyre pressure regularly.",

        "⛓️ Inspect and lubricate the chain regularly.",

        "🔋 Check battery condition and terminals.",

        "🛑 Check brake pads/shoes and brake fluid.",

        "💡 Check headlights, indicators and brake lights.",

        "⚙️ Check clutch and gear operation.",

        "⛽ Keep the fuel system clean.",

        "🔧 Follow the manufacturer's service schedule.",

        "🏍️ Do not ignore unusual sounds, vibrations or smoke."

    ]

    for tip in tips:
        st.write(tip)

# ============================================================
# SERVICE HISTORY
# ============================================================

elif menu == "📋 Service History":

    st.header("📋 2-Wheeler Service History")

    col1, col2 = st.columns(2)

    with col1:

        owner = st.text_input(
            "👤 Owner Name",
            key="service_owner"
        )

        company = st.selectbox(
            "🏍️ Vehicle Company",
            list(vehicle_data.keys()),
            key="service_company"
        )

        model = st.selectbox(
            "🏍️ Vehicle Model",
            list(vehicle_data[company].keys()),
            key="service_model"
        )

        year = st.number_input(
            "📅 Manufacturing Year",
            min_value=2000,
            max_value=2026,
            value=2024,
            key="service_year"
        )

    with col2:

        service_no = st.text_input(
            "🔢 Service Number"
        )

        km = st.number_input(
            "🛣️ Current Kilometer",
            min_value=0,
            step=100
        )

        service_date = st.date_input(
            "📅 Service Date"
        )

        service_type = st.selectbox(
            "🔧 Service Type",
            [
                "General Service",
                "Engine Oil Change",
                "Brake Service",
                "Battery Check",
                "Chain Adjustment",
                "Chain & Sprocket Replacement",
                "Tyre Replacement",
                "Clutch Service",
                "Air Filter Replacement",
                "Spark Plug Replacement",
                "Wheel Alignment"
            ]
        )

    cost = st.number_input(
        "💰 Service Cost (₹)",
        min_value=0,
        step=100
    )

    notes = st.text_area(
        "📝 Mechanic Notes"
    )

    if st.button(
        "💾 Save Service Record",
        use_container_width=True
    ):

        next_date = (
            service_date +
            timedelta(days=180)
        )

        next_km = km + 5000

        st.session_state["history"].append(
            {
                "Owner": owner,
                "Company": company,
                "Model": model,
                "Year": year,
                "Service No": service_no,
                "Date": service_date,
                "Service": service_type,
                "KM": km,
                "Cost": cost,
                "Notes": notes,
                "Next Date": next_date,
                "Next KM": next_km
            }
        )

        st.success(
            "✅ Service Record Saved Successfully!"
        )

    if len(st.session_state["history"]) > 0:

        st.subheader(
            "📜 Previous Service History"
        )

        df = pd.DataFrame(
            st.session_state["history"]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        latest = st.session_state["history"][-1]

        st.subheader(
            "⏰ Next Service Reminder"
        )

        st.info(
            f"""
🏍️ Vehicle: {latest['Company']} {latest['Model']}

📅 Manufacturing Year: {latest['Year']}

📅 Next Service Date: {latest['Next Date']}

🛣️ Next Service KM: {latest['Next KM']} KM

💰 Last Service Cost: ₹{latest['Cost']}
"""
        )

# ============================================================
# VEHICLE HEALTH + PREDICTIVE MAINTENANCE
# ============================================================

elif menu == "❤️ Vehicle Health & Predictive Maintenance":

    st.header("❤️ AI Vehicle Health & Predictive Maintenance")
    st.write(
        "Machine Learning estimates your vehicle health and maintenance risk "
        "using vehicle age, kilometer usage, service history and recent diagnosis results."
    )

    vehicle_info = st.session_state.get("vehicle_info", {})

    if not vehicle_info:
        st.warning("⚠️ Please save your vehicle information from the Home page first.")
        st.info("Go to 🏠 Home → enter your vehicle details → click Save Vehicle Information.")
    else:
        health_score, maintenance_probability, meta = predict_vehicle_health()
        label, icon = health_label(health_score)
        risk_label, risk_icon = maintenance_label(maintenance_probability)

        # --------------------------------------------------------
        # VEHICLE SUMMARY
        # --------------------------------------------------------
        st.subheader("🏍️ Vehicle Summary")
        summary_cols = st.columns(4)
        summary_cols[0].metric("Vehicle", f"{vehicle_info.get('Company', '')} {vehicle_info.get('Model', '')}")
        summary_cols[1].metric("Vehicle Age", f"{meta['vehicle_age']} years")
        summary_cols[2].metric("Current KM", f"{meta['current_km']:,.0f}")
        summary_cols[3].metric("Services Recorded", meta["service_count"])

        st.markdown("---")

        # --------------------------------------------------------
        # ML VEHICLE HEALTH SCORE
        # --------------------------------------------------------
        st.subheader("🤖 ML Vehicle Health Score")
        health_cols = st.columns([1, 1, 2])
        with health_cols[0]:
            st.metric("Health Score", f"{health_score:.0f}/100")
        with health_cols[1]:
            st.metric("Condition", f"{icon} {label}")
        with health_cols[2]:
            st.progress(int(round(health_score)), text=f"Vehicle Health: {health_score:.0f}%")

        if health_score >= 85:
            st.success("🟢 Your vehicle is in excellent condition based on the available data.")
        elif health_score >= 70:
            st.success("🟢 Your vehicle is in good condition. Continue regular maintenance.")
        elif health_score >= 50:
            st.warning("🟡 Your vehicle needs attention. Check upcoming maintenance items.")
        else:
            st.error("🔴 Your vehicle shows a high maintenance need. Professional inspection is recommended.")

        # --------------------------------------------------------
        # PREDICTIVE MAINTENANCE
        # --------------------------------------------------------
        st.subheader("🔮 Predictive Maintenance")
        risk_cols = st.columns(3)
        risk_cols[0].metric("Maintenance Risk", f"{maintenance_probability * 100:.1f}%")
        risk_cols[1].metric("Risk Level", f"{risk_icon} {risk_label}")
        risk_cols[2].metric("Days Since Service", meta["days_since_service"])
        st.progress(
            int(round(maintenance_probability * 100)),
            text=f"ML Maintenance Risk: {maintenance_probability * 100:.1f}%"
        )

        if maintenance_probability >= 0.75:
            st.error("🔴 Predictive alert: maintenance should be scheduled soon.")
        elif maintenance_probability >= 0.45:
            st.warning("🟡 Predictive alert: maintenance may be required soon.")
        else:
            st.success("🟢 Predictive alert: no immediate maintenance risk detected from the available data.")

        # --------------------------------------------------------
        # NEXT SERVICE ESTIMATE
        # --------------------------------------------------------
        st.subheader("📅 Next Service Prediction")
        if meta["service_count"] > 0:
            latest_service = max(
                [
                    h for h in st.session_state["history"]
                    if h.get("Company") == vehicle_info.get("Company")
                    and h.get("Model") == vehicle_info.get("Model")
                ],
                key=lambda h: h.get("Date", date.min)
            )
            estimated_date = latest_service.get("Next Date", date.today() + timedelta(days=180))
            estimated_km = float(latest_service.get("Next KM", meta["current_km"] + 5000))
        else:
            estimated_date = date.today() + timedelta(days=180)
            estimated_km = meta["current_km"] + 5000

        due_cols = st.columns(2)
        due_cols[0].metric("Recommended Date", str(estimated_date))
        due_cols[1].metric("Recommended KM", f"{estimated_km:,.0f} KM")

        if meta["days_since_service"] > 180 or (
            meta["last_service_km"] > 0 and meta["current_km"] - meta["last_service_km"] >= 5000
        ):
            st.warning("⏰ Your vehicle may already be due for service based on the latest service record.")

        # --------------------------------------------------------
        # ML INPUT SIGNALS
        # --------------------------------------------------------
        st.subheader("📊 ML Health Factors")
        factor_df = pd.DataFrame([
            {"Factor": "Vehicle Age", "Value": f"{meta['vehicle_age']} years"},
            {"Factor": "Current Usage", "Value": f"{meta['current_km']:,.0f} KM"},
            {"Factor": "Days Since Service", "Value": str(meta['days_since_service'])},
            {"Factor": "Recorded Services", "Value": str(meta['service_count'])},
            {"Factor": "Recent Diagnosed Faults", "Value": str(meta['recent_fault_count'])},
            {"Factor": "High/Critical Faults", "Value": str(meta['high_severity_faults'])},
        ])
        st.dataframe(factor_df, use_container_width=True, hide_index=True)

        st.info(
            "🤖 ML note: the current app uses a built-in labelled training set so the feature works immediately. "
            "For a final academic/production version, replace it with a larger real-world 2-wheeler service and fault dataset."
        )

# ============================================================
# CONTACT SUPPORT
# ============================================================

elif menu == "📞 Contact Support":

    st.header("📞 Contact Support")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📧 Email Support")

        st.write(
            "support@aimechanical.com"
        )

    with col2:

        st.subheader("📱 Phone Support")

        st.write(
            "+91 9876543210"
        )

    st.markdown("---")

    st.info(
        "For emergency vehicle problems, contact a qualified "
        "mechanic or authorized service center."
    )

# ============================================================
# LOGOUT
# ============================================================

elif menu == "🚪 Logout":

    st.warning(
        "🚪 Are you sure you want to logout?"
    )

    if st.button(
        "🚪 Logout Now",
        use_container_width=True
    ):

        st.session_state["logged_in"] = False
        st.session_state["username"] = None

        st.success(
            "✅ Logged out successfully!"
        )

=======
import streamlit as st
import pandas as pd
from datetime import date, timedelta
import streamlit.components.v1 as components
from pathlib import Path
import base64
import re
import numpy as np
from sklearn.pipeline import Pipeline  # type: ignore[reportMissingModuleSource]
from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore[reportMissingModuleSource]
from sklearn.linear_model import LogisticRegression  # type: ignore[reportMissingModuleSource]
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier  # type: ignore[reportMissingModuleSource]


# ============================================================
# MACHINE LEARNING - VEHICLE FAULT DIAGNOSIS
# ============================================================
# This is a lightweight supervised text-classification model.
# It learns from curated symptom examples and predicts the most
# likely fault from the user's natural-language description.
#
# IMPORTANT:
# For a production-grade project, replace the small curated
# training set below with a larger real-world labelled dataset.

ML_TRAINING_DATA = [
    # Engine Not Starting
    ("bike is not starting engine does not start", "Engine Not Starting"),
    ("self starts but engine does not start", "Engine Not Starting"),
    ("bike won't start", "Engine Not Starting"),
    ("motorcycle not starting", "Engine Not Starting"),
    ("engine cranks but does not start", "Engine Not Starting"),
    ("bike stopped and now it will not start", "Engine Not Starting"),
    ("starter works but engine does not start", "Engine Not Starting"),

    # Battery Problem
    ("battery is weak", "Battery Problem"),
    ("battery discharged", "Battery Problem"),
    ("bike battery is dead", "Battery Problem"),
    ("headlight is dim and battery is weak", "Battery Problem"),
    ("battery not holding charge", "Battery Problem"),
    ("battery voltage is low", "Battery Problem"),
    ("bike has weak battery", "Battery Problem"),

    # Brake Problem
    ("brakes are not working properly", "Brake Problem"),
    ("brake feels weak", "Brake Problem"),
    ("brake pad worn", "Brake Problem"),
    ("brake lever is soft", "Brake Problem"),
    ("braking distance is high", "Brake Problem"),
    ("front brake problem", "Brake Problem"),
    ("rear brake problem", "Brake Problem"),

    # Tyre Problem
    ("tyre is punctured", "Tyre Problem"),
    ("tire has low pressure", "Tyre Problem"),
    ("tyre pressure is low", "Tyre Problem"),
    ("bike tyre is worn", "Tyre Problem"),
    ("wheel feels unstable", "Tyre Problem"),
    ("tyre problem", "Tyre Problem"),

    # Engine Overheating
    ("engine is overheating", "Engine Overheating"),
    ("bike gets very hot", "Engine Overheating"),
    ("engine temperature is high", "Engine Overheating"),
    ("bike overheats in traffic", "Engine Overheating"),
    ("engine becomes too hot", "Engine Overheating"),
    ("overheating problem", "Engine Overheating"),

    # Oil Leakage
    ("oil is leaking", "Oil Leakage"),
    ("engine oil leakage", "Oil Leakage"),
    ("oil dripping from bike", "Oil Leakage"),
    ("oil leak under motorcycle", "Oil Leakage"),
    ("engine is losing oil", "Oil Leakage"),
    ("oil drops under bike", "Oil Leakage"),

    # Chain/Sprocket Problem
    ("chain is loose", "Chain/Sprocket Problem"),
    ("chain makes noise", "Chain/Sprocket Problem"),
    ("sprocket is worn", "Chain/Sprocket Problem"),
    ("chain needs lubrication", "Chain/Sprocket Problem"),
    ("chain and sprocket problem", "Chain/Sprocket Problem"),
    ("chain is making clicking noise", "Chain/Sprocket Problem"),

    # Clutch Problem
    ("clutch is slipping", "Clutch Problem"),
    ("clutch problem", "Clutch Problem"),
    ("clutch is hard", "Clutch Problem"),
    ("clutch lever problem", "Clutch Problem"),
    ("clutch free play problem", "Clutch Problem"),
    ("bike clutch is not working", "Clutch Problem"),

    # Gear Shifting Problem
    ("gear is not shifting", "Gear Shifting Problem"),
    ("gear shifting is hard", "Gear Shifting Problem"),
    ("cannot change gears", "Gear Shifting Problem"),
    ("gear lever problem", "Gear Shifting Problem"),
    ("bike gears are stuck", "Gear Shifting Problem"),
    ("difficulty changing gear", "Gear Shifting Problem"),

    # Poor Mileage
    ("bike mileage is low", "Poor Mileage"),
    ("fuel consumption is high", "Poor Mileage"),
    ("poor fuel economy", "Poor Mileage"),
    ("bike gives low mileage", "Poor Mileage"),
    ("petrol consumption increased", "Poor Mileage"),
    ("mileage has decreased", "Poor Mileage"),

    # Low Pickup
    ("bike has low pickup", "Low Pickup"),
    ("pickup is poor", "Low Pickup"),
    ("bike is slow to accelerate", "Low Pickup"),
    ("acceleration is weak", "Low Pickup"),
    ("motorcycle lacks power", "Low Pickup"),
    ("bike has no pickup", "Low Pickup"),

    # Excessive Smoke
    ("bike is producing too much smoke", "Excessive Smoke"),
    ("black smoke from exhaust", "Excessive Smoke"),
    ("blue smoke from engine", "Excessive Smoke"),
    ("white smoke from exhaust", "Excessive Smoke"),
    ("excessive exhaust smoke", "Excessive Smoke"),
    ("smoke coming from exhaust", "Excessive Smoke"),

    # Strange Noise
    ("strange noise from engine", "Strange Noise"),
    ("engine making unusual noise", "Strange Noise"),
    ("clicking sound from bike", "Strange Noise"),
    ("knocking noise", "Strange Noise"),
    ("rattling noise", "Strange Noise"),
    ("bike is making strange sound", "Strange Noise"),

    # Electrical Problem
    ("headlight is not working", "Electrical Problem"),
    ("indicator is not working", "Electrical Problem"),
    ("electrical problem", "Electrical Problem"),
    ("fuse keeps blowing", "Electrical Problem"),
    ("wiring problem", "Electrical Problem"),
    ("horn is not working", "Electrical Problem"),
]

ML_TEXTS = [x[0] for x in ML_TRAINING_DATA]
ML_LABELS = [x[1] for x in ML_TRAINING_DATA]

@st.cache_resource
def train_fault_model():
    model = Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=1
        )),
        ("classifier", LogisticRegression(
            max_iter=2000,
            class_weight="balanced"
        ))
    ])
    model.fit(ML_TEXTS, ML_LABELS)
    return model

fault_model = train_fault_model()

def clean_problem_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def predict_fault(description):
    cleaned = clean_problem_text(description)
    probabilities = fault_model.predict_proba([cleaned])[0]
    classes = fault_model.classes_
    order = np.argsort(probabilities)[::-1]

    top_predictions = [
        (classes[i], float(probabilities[i]))
        for i in order[:3]
    ]
    return top_predictions

# ============================================================
# ADVANCED ML - VEHICLE HEALTH + PREDICTIVE MAINTENANCE
# ============================================================
# These models learn from a generated labelled training set so the
# Streamlit app works immediately. For the final project, replace
# this training set with a real service/maintenance dataset.

HEALTH_FEATURE_NAMES = [
    "vehicle_age",
    "current_km_10k",
    "days_since_service_180",
    "service_count",
    "recent_fault_count",
    "high_severity_faults"
]

@st.cache_resource
def train_health_model():
    rng = np.random.default_rng(42)
    n = 2500
    age = rng.uniform(0, 15, n)
    km10 = rng.uniform(0, 15, n)
    days = rng.uniform(0, 360, n)
    service_count = rng.integers(0, 16, n)
    faults = rng.integers(0, 8, n)
    high_faults = rng.integers(0, 5, n)

    # Synthetic target representing a reasonable vehicle-health pattern.
    score = (
        100
        - age * 1.7
        - km10 * 2.0
        - np.maximum(days - 45, 0) * 0.045
        + np.minimum(service_count, 12) * 0.9
        - faults * 2.2
        - high_faults * 4.5
        + rng.normal(0, 2.5, n)
    )
    score = np.clip(score, 20, 100)

    X = np.column_stack([age, km10, days, service_count, faults, high_faults])
    model = RandomForestRegressor(
        n_estimators=180,
        random_state=42,
        min_samples_leaf=3,
        n_jobs=-1
    )
    model.fit(X, score)
    return model

@st.cache_resource
def train_maintenance_model():
    rng = np.random.default_rng(123)
    n = 2500
    age = rng.uniform(0, 15, n)
    km10 = rng.uniform(0, 15, n)
    days = rng.uniform(0, 360, n)
    service_count = rng.integers(0, 16, n)
    faults = rng.integers(0, 8, n)
    high_faults = rng.integers(0, 5, n)

    risk_signal = (
        0.25 * age
        + 0.35 * km10
        + 0.012 * np.maximum(days - 30, 0)
        - 0.18 * service_count
        + 0.65 * faults
        + 1.25 * high_faults
        + rng.normal(0, 1.0, n)
    )
    maintenance_needed = (risk_signal > 5.0).astype(int)

    X = np.column_stack([age, km10, days, service_count, faults, high_faults])
    model = RandomForestClassifier(
        n_estimators=180,
        random_state=123,
        class_weight="balanced",
        min_samples_leaf=3,
        n_jobs=-1
    )
    model.fit(X, maintenance_needed)
    return model

health_model = train_health_model()
maintenance_model = train_maintenance_model()

def get_vehicle_ml_features():
    """Build ML features from the user's saved vehicle and service history."""
    info = st.session_state.get("vehicle_info", {})
    current_year = int(info.get("Year", date.today().year))
    current_km = float(info.get("Current KM", 0) or 0)

    history = st.session_state.get("history", [])
    vehicle_company = info.get("Company", "")
    vehicle_model = info.get("Model", "")

    matching_history = [
        h for h in history
        if h.get("Company") == vehicle_company and h.get("Model") == vehicle_model
    ]

    service_count = len(matching_history)
    if matching_history:
        latest = max(matching_history, key=lambda h: h.get("Date", date.min))
        latest_date = latest.get("Date", date.today())
        last_service_km = float(latest.get("KM", 0) or 0)
        days_since_service = max((date.today() - latest_date).days, 0)
        if current_km <= 0:
            current_km = last_service_km
    else:
        last_service_km = 0
        days_since_service = 365

    diagnoses = st.session_state.get("diagnosis_history", [])
    matching_diagnoses = [
        d for d in diagnoses
        if d.get("Company") == vehicle_company and d.get("Model") == vehicle_model
    ]
    recent_diagnoses = matching_diagnoses[-8:]
    high_severity_faults = sum(
        1 for d in recent_diagnoses
        if d.get("Severity") in {"HIGH", "CRITICAL"}
    )

    features = np.array([[
        max(date.today().year - current_year, 0),
        current_km / 10000.0,
        min(days_since_service, 720) / 180.0,
        service_count,
        len(recent_diagnoses),
        high_severity_faults
    ]], dtype=float)

    return features, {
        "current_km": current_km,
        "last_service_km": last_service_km,
        "days_since_service": days_since_service,
        "service_count": service_count,
        "recent_fault_count": len(recent_diagnoses),
        "high_severity_faults": high_severity_faults,
        "vehicle_age": max(date.today().year - current_year, 0),
    }

def predict_vehicle_health():
    features, meta = get_vehicle_ml_features()
    score = float(np.clip(health_model.predict(features)[0], 0, 100))
    risk_prob = float(maintenance_model.predict_proba(features)[0][1])
    return score, risk_prob, meta

def health_label(score):
    if score >= 85:
        return "Excellent", "🟢"
    if score >= 70:
        return "Good", "🟢"
    if score >= 50:
        return "Needs Attention", "🟡"
    return "Critical", "🔴"

def maintenance_label(probability):
    if probability >= 0.75:
        return "High Risk", "🔴"
    if probability >= 0.45:
        return "Medium Risk", "🟡"
    return "Low Risk", "🟢"

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Mechanical Help Center",
    page_icon="🏍️",
    layout="wide"
)

# ============================================================
# LOGIN PROTECTION
# ============================================================

if not st.session_state.get("logged_in", False):
    st.warning("⚠️ Please login first.")
    st.switch_page("app.py")

username = st.session_state.get("username", "User")

# ============================================================
# INITIALIZE SERVICE HISTORY
# ============================================================

if "history" not in st.session_state:
    st.session_state["history"] = []

if "diagnosis_history" not in st.session_state:
    st.session_state["diagnosis_history"] = []

vehicle_data = {
    "Hero": {"Splendor": "models/hero_splendor.glb", "HF Deluxe": "models/hero_hf_deluxe.glb", "Passion": "models/hero_passion.glb", "Glamour": "models/hero_glamour.glb", "Xtreme 125R": "models/hero_xtreme_125r.glb"},
    "Honda": {"Shine": "models/honda_shine.glb", "SP 125": "models/honda_sp125.glb", "Unicorn": "models/honda_unicorn.glb", "Activa": "models/honda_activa.glb", "Hornet 2.0": "models/honda_hornet_2.glb"},
    "Bajaj": {"Pulsar 125": "models/bajaj_pulsar_125.glb", "Pulsar 150": "models/bajaj_pulsar_150.glb", "Pulsar NS200": "models/bajaj_pulsar_ns200.glb", "Platina": "models/bajaj_platina.glb", "Avenger": "models/bajaj_avenger.glb"},
    "TVS": {"Apache RTR 160": "models/tvs_apache_rtr_160.glb", "Apache RTR 200": "models/tvs_apache_rtr_200.glb", "Raider": "models/tvs_raider.glb", "Sport": "models/tvs_sport.glb", "Jupiter": "models/tvs_jupiter.glb"},
    "Yamaha": {"FZ": "models/yamaha_fz.glb", "MT-15": "models/yamaha_mt15.glb", "R15": "models/yamaha_r15.glb", "Fascino": "models/yamaha_fascino.glb", "Ray ZR": "models/yamaha_ray_zr.glb"},
    "Suzuki": {"Access 125": "models/suzuki_access_125.glb", "Burgman Street": "models/suzuki_burgman_street.glb", "Gixxer": "models/suzuki_gixxer.glb", "Avenis": "models/suzuki_avenis.glb"},
    "Royal Enfield": {"Classic 350": "models/re_classic_350.glb", "Bullet 350": "models/re_bullet_350.glb", "Hunter 350": "models/re_hunter_350.glb", "Meteor 350": "models/re_meteor_350.glb"},
}



# ============================================================
# HEADER
# ============================================================

st.title("🤖 AI Mechanical Help Center")
st.subheader(
    f"🏍️ Smart Self-Service Assistant for 2-Wheelers | Welcome {username} 👋"
)

st.markdown("---")

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ Menu")

menu = st.sidebar.radio(
    "Select Option",
    [
        "🏠 Home",
        "🏍️ 3D Bike View",
        "🔧 Vehicle Diagnosis",
        "🛠 Maintenance Tips",
        "📋 Service History",
        "❤️ Vehicle Health & Predictive Maintenance",
        "📞 Contact Support",
        "🚪 Logout"
    ]
)

# ============================================================
# HOME
# ============================================================

if menu == "🏠 Home":

    st.header("🏠 Vehicle Information")

    st.success(
        f"Welcome {username}! 🤖 Your AI Mechanical Help Center is ready."
    )

    col1, col2 = st.columns(2)

    with col1:

        company = st.selectbox(
            "🏍️ Vehicle Company",
            list(vehicle_data.keys())
        )

        model = st.selectbox(
            "🏍️ Vehicle Model",
            list(vehicle_data[company].keys())
        )

        year = st.number_input(
            "📅 Manufacturing Year",
            min_value=2000,
            max_value=2026,
            value=2024,
            step=1
        )

    with col2:

        owner = st.text_input(
            "👤 Owner Name"
        )

        number = st.text_input(
            "🔢 Vehicle Number"
        )

        fuel = st.selectbox(
            "⛽ Fuel Type",
            [
                "Petrol",
                "Electric"
            ]
        )

        current_km = st.number_input(
            "🛣️ Current Kilometer",
            min_value=0,
            step=100,
            value=0
        )

    st.markdown("---")

    if st.button(
        "💾 Save Vehicle Information",
        use_container_width=True
    ):

        st.session_state["vehicle_info"] = {
            "Owner": owner,
            "Vehicle Number": number,
            "Company": company,
            "Model": model,
            "Year": year,
            "Fuel": fuel,
            "Current KM": current_km
        }

        st.success(
            "✅ Vehicle information saved successfully!"
        )

    st.info(
        "💡 Select an option from the left menu to use the vehicle services."
    )

# ============================================================
# 3D BIKE VIEW
# ============================================================

elif menu == "🏍️ 3D Bike View":

    st.header("🏍️ 360° 2-Wheeler Viewer")

    st.info(
        "Select your company and model to view the 3D vehicle."
    )

    company = st.selectbox(
        "Select Vehicle Company",
        list(vehicle_data.keys())
    )

    model = st.selectbox(
        "Select Vehicle Model",
        list(vehicle_data[company].keys())
    )

    model_path = vehicle_data[company][model]

    BASE_DIR = Path(__file__).resolve().parent

    model_file = BASE_DIR / model_path

    st.write("📁 3D Model Path:")
    st.code(str(model_file))

    if not model_file.exists():

        st.error("❌ 3D model file not found!")

        st.write("Expected location:")
        st.code(str(model_file))

        st.warning(
            f"Create the folder 'models' beside your dashboard.py "
            f"and place the GLB file for {company} {model} inside it."
        )

    else:

        st.success(
            f"✅ {company} {model} 3D model found!"
        )

        try:

            with open(model_file, "rb") as file:
                model_bytes = file.read()

            model_base64 = base64.b64encode(
                model_bytes
            ).decode("utf-8")

            model_url = (
                "data:model/gltf-binary;base64,"
                + model_base64
            )

            html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<script
type="module"
src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js">
</script>

<style>

html,
body {{
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #eeeeee;
}}

model-viewer {{
    width: 100%;
    height: 650px;
    background: #eeeeee;
    border-radius: 15px;
}}

</style>

</head>

<body>

<model-viewer

src="{model_url}"

camera-controls

auto-rotate

auto-rotate-delay="0"

rotation-per-second="20deg"

shadow-intensity="1"

exposure="1"

camera-orbit="0deg 75deg 3m"

field-of-view="30deg"

interaction-prompt="auto"

loading="eager"

reveal="auto"

alt="{company} {model} 3D Model">

</model-viewer>

</body>

</html>
"""

            components.html(
                html,
                height=700,
                scrolling=False
            )

            st.info(
                "🖱️ Drag = Rotate | 🔍 Scroll = Zoom | 🔄 Auto-rotate = ON"
            )

        except Exception as e:

            st.error(
                "❌ Error loading the 3D model"
            )

            st.exception(e)

# ============================================================
# VEHICLE DIAGNOSIS
# ============================================================

elif menu == "🔧 Vehicle Diagnosis":

    st.header("🔧 AI Vehicle Diagnosis")
    st.write("Describe your vehicle problem and get possible causes and recommended actions.")

    # --------------------------------------------------------
    # VEHICLE DATA
    # --------------------------------------------------------

    diagnosis_vehicle_data = {

        "Hero": [
            "Splendor",
            "HF Deluxe",
            "Passion",
            "Glamour",
            "Xtreme 125R"
        ],

        "Honda": [
            "Shine",
            "SP 125",
            "Unicorn",
            "Activa",
            "Hornet 2.0"
        ],

        "Bajaj": [
            "Pulsar 125",
            "Pulsar 150",
            "Pulsar NS200",
            "Platina",
            "Avenger"
        ],

        "TVS": [
            "Apache RTR 160",
            "Apache RTR 200",
            "Raider",
            "Sport",
            "Jupiter"
        ],

        "Yamaha": [
            "FZ",
            "MT-15",
            "R15",
            "Fascino",
            "Ray ZR"
        ],

        "Suzuki": [
            "Access 125",
            "Burgman Street",
            "Gixxer",
            "Avenis"
        ],

        "Royal Enfield": [
            "Classic 350",
            "Bullet 350",
            "Hunter 350",
            "Meteor 350"
        ]
    }

    # --------------------------------------------------------
    # VEHICLE SELECTION
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        company = st.selectbox(
            "🏍️ Vehicle Company",
            list(diagnosis_vehicle_data.keys()),
            key="diagnosis_company"
        )

        model = st.selectbox(
            "🏍️ Vehicle Model",
            diagnosis_vehicle_data[company],
            key="diagnosis_model"
        )

    with col2:

        year = st.number_input(
            "📅 Manufacturing Year",
            min_value=2000,
            max_value=2026,
            value=2024,
            step=1,
            key="diagnosis_year"
        )

        problem = st.selectbox(
            "⚠️ Select Vehicle Problem",
            [
                "Engine Not Starting",
                "Battery Problem",
                "Brake Problem",
                "Tyre Problem",
                "Engine Overheating",
                "Oil Leakage",
                "Chain/Sprocket Problem",
                "Clutch Problem",
                "Gear Shifting Problem",
                "Poor Mileage",
                "Low Pickup",
                "Excessive Smoke",
                "Strange Noise",
                "Electrical Problem",
                "Other"
            ],
            key="diagnosis_problem"
        )

    # --------------------------------------------------------
    # PROBLEM DESCRIPTION
    # --------------------------------------------------------

    description = st.text_area(
        "📝 Describe Your Problem",
        placeholder="Example: Bike is not starting, starter is working but engine is not starting...",
        height=130,
        key="diagnosis_description"
    )

    # --------------------------------------------------------
    # DIAGNOSIS DATABASE
    # --------------------------------------------------------

    diagnosis_database = {

        "Engine Not Starting": {

            "causes": [
                "Weak or discharged battery",
                "Fuel supply problem",
                "Spark plug problem",
                "Engine kill switch may be OFF",
                "Starter motor or ignition problem"
            ],

            "checks": [
                "Check battery voltage",
                "Check fuel level",
                "Check spark plug",
                "Check engine kill switch",
                "Check starter motor"
            ],

            "solution": [
                "Charge or replace the battery if required",
                "Check fuel supply",
                "Clean or replace the spark plug",
                "Keep the engine kill switch in RUN position",
                "Contact a mechanic if the starter motor has a fault"
            ],

            "severity": "HIGH"
        },

        "Battery Problem": {

            "causes": [
                "Battery discharged",
                "Loose battery terminals",
                "Battery is old",
                "Charging system problem"
            ],

            "checks": [
                "Check battery voltage",
                "Check battery terminals",
                "Check charging voltage",
                "Check battery age"
            ],

            "solution": [
                "Charge the battery",
                "Clean and tighten terminals",
                "Check alternator/charging system",
                "Replace battery if it is damaged"
            ],

            "severity": "MEDIUM"
        },

        "Brake Problem": {

            "causes": [
                "Brake pad/shoe worn",
                "Low brake fluid",
                "Brake cable problem",
                "Brake system adjustment required"
            ],

            "checks": [
                "Inspect brake pads",
                "Check brake fluid",
                "Check brake lever/pedal",
                "Check brake cable"
            ],

            "solution": [
                "Replace worn brake pads",
                "Top up or replace brake fluid as specified",
                "Adjust or replace brake cable",
                "Have the brake system inspected by a mechanic"
            ],

            "severity": "CRITICAL"
        },

        "Tyre Problem": {

            "causes": [
                "Low tyre pressure",
                "Puncture",
                "Tyre wear",
                "Wheel alignment problem"
            ],

            "checks": [
                "Check tyre pressure",
                "Inspect tyre for puncture",
                "Check tread depth",
                "Inspect wheel alignment"
            ],

            "solution": [
                "Set correct tyre pressure",
                "Repair puncture if possible",
                "Replace badly worn tyre",
                "Check wheel alignment"
            ],

            "severity": "HIGH"
        },

        "Engine Overheating": {

            "causes": [
                "Low engine oil",
                "Cooling system problem",
                "Engine running under excessive load",
                "Blocked air flow"
            ],

            "checks": [
                "Check engine oil level",
                "Check cooling system",
                "Check for unusual engine noise",
                "Check air flow"
            ],

            "solution": [
                "Maintain correct engine oil level",
                "Allow the engine to cool",
                "Check cooling system",
                "Contact a mechanic if overheating continues"
            ],

            "severity": "HIGH"
        },

        "Oil Leakage": {

            "causes": [
                "Loose drain bolt",
                "Damaged oil seal",
                "Gasket leakage",
                "Engine component leakage"
            ],

            "checks": [
                "Identify leakage location",
                "Check drain bolt",
                "Check oil seals",
                "Check engine gasket"
            ],

            "solution": [
                "Tighten loose fasteners where appropriate",
                "Replace damaged seals",
                "Replace damaged gasket",
                "Check oil level and repair the leak"
            ],

            "severity": "HIGH"
        },

        "Chain/Sprocket Problem": {

            "causes": [
                "Chain too loose",
                "Chain too tight",
                "Poor lubrication",
                "Worn sprocket"
            ],

            "checks": [
                "Check chain slack",
                "Inspect sprocket teeth",
                "Check chain lubrication",
                "Check chain condition"
            ],

            "solution": [
                "Adjust chain slack",
                "Lubricate the chain",
                "Replace worn chain/sprocket",
                "Perform regular chain maintenance"
            ],

            "severity": "MEDIUM"
        },

        "Clutch Problem": {

            "causes": [
                "Incorrect clutch adjustment",
                "Worn clutch plates",
                "Clutch cable problem",
                "Low/incorrect engine oil"
            ],

            "checks": [
                "Check clutch free play",
                "Check clutch cable",
                "Check clutch operation",
                "Inspect clutch plates if required"
            ],

            "solution": [
                "Adjust clutch free play",
                "Lubricate or replace cable",
                "Replace worn clutch components",
                "Use the manufacturer-recommended oil"
            ],

            "severity": "MEDIUM"
        },

        "Gear Shifting Problem": {

            "causes": [
                "Clutch adjustment problem",
                "Low or incorrect oil",
                "Gear linkage problem",
                "Internal transmission problem"
            ],

            "checks": [
                "Check clutch operation",
                "Check engine oil",
                "Inspect gear lever/linkage",
                "Check for abnormal noises"
            ],

            "solution": [
                "Adjust clutch",
                "Check and replace oil if necessary",
                "Inspect gear linkage",
                "Consult a qualified mechanic for internal faults"
            ],

            "severity": "HIGH"
        },

        "Poor Mileage": {

            "causes": [
                "Dirty air filter",
                "Incorrect tyre pressure",
                "Poor riding conditions",
                "Spark plug problem",
                "Fuel system problem"
            ],

            "checks": [
                "Check air filter",
                "Check tyre pressure",
                "Inspect spark plug",
                "Check fuel system"
            ],

            "solution": [
                "Clean or replace air filter",
                "Maintain correct tyre pressure",
                "Service spark plug",
                "Check fuel system"
            ],

            "severity": "MEDIUM"
        },

        "Low Pickup": {

            "causes": [
                "Dirty air filter",
                "Spark plug problem",
                "Clutch slipping",
                "Fuel delivery problem"
            ],

            "checks": [
                "Check air filter",
                "Check spark plug",
                "Check clutch",
                "Check fuel system"
            ],

            "solution": [
                "Clean or replace air filter",
                "Clean or replace spark plug",
                "Inspect clutch",
                "Service fuel system"
            ],

            "severity": "MEDIUM"
        },

        "Excessive Smoke": {

            "causes": [
                "Engine oil burning",
                "Air filter problem",
                "Fuel mixture problem",
                "Engine wear"
            ],

            "checks": [
                "Identify smoke color",
                "Check engine oil level",
                "Check air filter",
                "Check engine condition"
            ],

            "solution": [
                "Check oil level",
                "Service air filter",
                "Inspect fuel system",
                "Get engine inspected if smoke continues"
            ],

            "severity": "HIGH"
        },

        "Strange Noise": {

            "causes": [
                "Loose component",
                "Low engine oil",
                "Chain problem",
                "Engine component wear"
            ],

            "checks": [
                "Identify noise location",
                "Check engine oil",
                "Check chain",
                "Inspect loose components"
            ],

            "solution": [
                "Tighten loose components",
                "Maintain correct oil level",
                "Adjust/lubricate chain",
                "Get the vehicle inspected if noise continues"
            ],

            "severity": "HIGH"
        },

        "Electrical Problem": {

            "causes": [
                "Blown fuse",
                "Weak battery",
                "Loose wiring",
                "Faulty switch"
            ],

            "checks": [
                "Check battery",
                "Check fuses",
                "Inspect wiring",
                "Check switches"
            ],

            "solution": [
                "Charge or replace battery",
                "Replace blown fuse with correct rating",
                "Repair loose wiring",
                "Get electrical system inspected"
            ],

            "severity": "MEDIUM"
        },

        "Other": {

            "causes": [
                "Problem requires additional inspection"
            ],

            "checks": [
                "Describe the symptoms clearly",
                "Check for unusual sounds, smells or warning lights"
            ],

            "solution": [
                "Consult a qualified mechanic for detailed inspection"
            ],

            "severity": "UNKNOWN"
        }
    }

    # --------------------------------------------------------
    # DIAGNOSE BUTTON
    # --------------------------------------------------------

    if st.button(
        "🔧 Diagnose Vehicle",
        use_container_width=True,
        type="primary"
    ):

        if not description.strip():

            st.warning(
                "⚠️ Please describe your vehicle problem first."
            )

        else:

            # ========================================================
            # ML PREDICTION
            # ========================================================
            ml_predictions = predict_fault(description)
            ml_problem, ml_confidence = ml_predictions[0]

            # Keep the existing rule-based database for explanations,
            # checks and solutions. ML decides the most likely fault.
            if ml_problem in diagnosis_database:
                result = diagnosis_database[ml_problem]
            else:
                result = diagnosis_database[problem]

            # Store diagnosis so the health and predictive-maintenance models
            # can use recent faults as additional vehicle-health signals.
            st.session_state["diagnosis_history"].append({
                "Date": date.today(),
                "Company": company,
                "Model": model,
                "Problem": ml_problem,
                "Confidence": ml_confidence,
                "Severity": result.get("severity", "UNKNOWN")
            })

            st.success("✅ ML Diagnosis Completed")

            # ------------------------------------------------
            # ML RESULT
            # ------------------------------------------------
            st.subheader("🤖 Machine Learning Diagnosis")

            ml_col1, ml_col2 = st.columns(2)

            with ml_col1:
                st.metric(
                    "Predicted Problem",
                    ml_problem
                )

            with ml_col2:
                st.metric(
                    "ML Confidence",
                    f"{ml_confidence * 100:.1f}%"
                )

            if ml_confidence >= 0.75:
                st.success(
                    f"🎯 High-confidence ML prediction: **{ml_problem}**"
                )
            elif ml_confidence >= 0.50:
                st.warning(
                    f"⚠️ Moderate-confidence ML prediction: **{ml_problem}**. "
                    "A physical inspection is recommended."
                )
            else:
                st.info(
                    f"ℹ️ ML prediction: **{ml_problem}** with low confidence. "
                    "Please provide more detailed symptoms."
                )

            # Show top 3 ML predictions
            st.write("### 🔎 Top ML Predictions")
            for rank, (predicted_problem, probability) in enumerate(
                ml_predictions, start=1
            ):
                st.write(
                    f"**{rank}. {predicted_problem}** — "
                    f"{probability * 100:.1f}%"
                )
                st.progress(min(max(probability, 0.0), 1.0))

            # Compare the user's selected problem with the ML result.
            if problem != ml_problem:
                st.warning(
                    f"⚠️ Your selected problem is **{problem}**, but the "
                    f"ML model detected **{ml_problem}** from the description. "
                    "The detailed diagnosis below is based on the ML prediction."
                )

            # ------------------------------------------------
            # VEHICLE INFORMATION
            # ------------------------------------------------

            st.subheader("🏍️ Vehicle Information")

            st.write(
                f"**Vehicle:** {company} {model}"
            )

            st.write(
                f"**Manufacturing Year:** {year}"
            )

            st.write(
                f"**Problem:** {problem}"
            )

            st.write(
                f"**Description:** {description}"
            )

            # ------------------------------------------------
            # SEVERITY
            # ------------------------------------------------

            severity = result["severity"]

            if severity == "CRITICAL":

                st.error(
                    "🚨 Severity: CRITICAL — Avoid riding until the brake problem is inspected."
                )

            elif severity == "HIGH":

                st.warning(
                    "⚠️ Severity: HIGH — Vehicle inspection is recommended soon."
                )

            elif severity == "MEDIUM":

                st.info(
                    "🟡 Severity: MEDIUM — Check the listed components."
                )

            else:

                st.info(
                    "ℹ️ Severity: UNKNOWN — Further inspection is required."
                )

            # ------------------------------------------------
            # POSSIBLE CAUSES
            # ------------------------------------------------

            st.subheader("🔍 Possible Causes")

            for cause in result["causes"]:
                st.write("• " + cause)

            # ------------------------------------------------
            # CHECK THESE FIRST
            # ------------------------------------------------

            st.subheader("🛠️ Recommended Checks")

            for check in result["checks"]:
                st.write("☑️ " + check)

            # ------------------------------------------------
            # RECOMMENDED ACTION
            # ------------------------------------------------

            st.subheader("💡 Recommended Action")

            for solution in result["solution"]:
                st.write("🔧 " + solution)

            # ------------------------------------------------
            # FINAL MESSAGE
            # ------------------------------------------------

            st.info(
                "🤖 This diagnosis uses a supervised Machine Learning "
                "text-classification model trained on curated vehicle "
                "symptom examples. The ML prediction is combined with "
                "the application's mechanical knowledge base. It is "
                "not a substitute for professional mechanical inspection."
            )

# ============================================================
# MAINTENANCE TIPS
# ============================================================

elif menu == "🛠 Maintenance Tips":

    st.header("🛠 2-Wheeler Maintenance Tips")

    company = st.selectbox(
        "Select Company",
        list(vehicle_data.keys()),
        key="maintenance_company"
    )

    model = st.selectbox(
        "Select Model",
        list(vehicle_data[company].keys()),
        key="maintenance_model"
    )

    st.success(
        f"Maintenance Guide: {company} {model}"
    )

    tips = [

        "🛢️ Check and replace engine oil at the recommended interval.",

        "🛞 Check tyre pressure regularly.",

        "⛓️ Inspect and lubricate the chain regularly.",

        "🔋 Check battery condition and terminals.",

        "🛑 Check brake pads/shoes and brake fluid.",

        "💡 Check headlights, indicators and brake lights.",

        "⚙️ Check clutch and gear operation.",

        "⛽ Keep the fuel system clean.",

        "🔧 Follow the manufacturer's service schedule.",

        "🏍️ Do not ignore unusual sounds, vibrations or smoke."

    ]

    for tip in tips:
        st.write(tip)

# ============================================================
# SERVICE HISTORY
# ============================================================

elif menu == "📋 Service History":

    st.header("📋 2-Wheeler Service History")

    col1, col2 = st.columns(2)

    with col1:

        owner = st.text_input(
            "👤 Owner Name",
            key="service_owner"
        )

        company = st.selectbox(
            "🏍️ Vehicle Company",
            list(vehicle_data.keys()),
            key="service_company"
        )

        model = st.selectbox(
            "🏍️ Vehicle Model",
            list(vehicle_data[company].keys()),
            key="service_model"
        )

        year = st.number_input(
            "📅 Manufacturing Year",
            min_value=2000,
            max_value=2026,
            value=2024,
            key="service_year"
        )

    with col2:

        service_no = st.text_input(
            "🔢 Service Number"
        )

        km = st.number_input(
            "🛣️ Current Kilometer",
            min_value=0,
            step=100
        )

        service_date = st.date_input(
            "📅 Service Date"
        )

        service_type = st.selectbox(
            "🔧 Service Type",
            [
                "General Service",
                "Engine Oil Change",
                "Brake Service",
                "Battery Check",
                "Chain Adjustment",
                "Chain & Sprocket Replacement",
                "Tyre Replacement",
                "Clutch Service",
                "Air Filter Replacement",
                "Spark Plug Replacement",
                "Wheel Alignment"
            ]
        )

    cost = st.number_input(
        "💰 Service Cost (₹)",
        min_value=0,
        step=100
    )

    notes = st.text_area(
        "📝 Mechanic Notes"
    )

    if st.button(
        "💾 Save Service Record",
        use_container_width=True
    ):

        next_date = (
            service_date +
            timedelta(days=180)
        )

        next_km = km + 5000

        st.session_state["history"].append(
            {
                "Owner": owner,
                "Company": company,
                "Model": model,
                "Year": year,
                "Service No": service_no,
                "Date": service_date,
                "Service": service_type,
                "KM": km,
                "Cost": cost,
                "Notes": notes,
                "Next Date": next_date,
                "Next KM": next_km
            }
        )

        st.success(
            "✅ Service Record Saved Successfully!"
        )

    if len(st.session_state["history"]) > 0:

        st.subheader(
            "📜 Previous Service History"
        )

        df = pd.DataFrame(
            st.session_state["history"]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        latest = st.session_state["history"][-1]

        st.subheader(
            "⏰ Next Service Reminder"
        )

        st.info(
            f"""
🏍️ Vehicle: {latest['Company']} {latest['Model']}

📅 Manufacturing Year: {latest['Year']}

📅 Next Service Date: {latest['Next Date']}

🛣️ Next Service KM: {latest['Next KM']} KM

💰 Last Service Cost: ₹{latest['Cost']}
"""
        )

# ============================================================
# VEHICLE HEALTH + PREDICTIVE MAINTENANCE
# ============================================================

elif menu == "❤️ Vehicle Health & Predictive Maintenance":

    st.header("❤️ AI Vehicle Health & Predictive Maintenance")
    st.write(
        "Machine Learning estimates your vehicle health and maintenance risk "
        "using vehicle age, kilometer usage, service history and recent diagnosis results."
    )

    vehicle_info = st.session_state.get("vehicle_info", {})

    if not vehicle_info:
        st.warning("⚠️ Please save your vehicle information from the Home page first.")
        st.info("Go to 🏠 Home → enter your vehicle details → click Save Vehicle Information.")
    else:
        health_score, maintenance_probability, meta = predict_vehicle_health()
        label, icon = health_label(health_score)
        risk_label, risk_icon = maintenance_label(maintenance_probability)

        # --------------------------------------------------------
        # VEHICLE SUMMARY
        # --------------------------------------------------------
        st.subheader("🏍️ Vehicle Summary")
        summary_cols = st.columns(4)
        summary_cols[0].metric("Vehicle", f"{vehicle_info.get('Company', '')} {vehicle_info.get('Model', '')}")
        summary_cols[1].metric("Vehicle Age", f"{meta['vehicle_age']} years")
        summary_cols[2].metric("Current KM", f"{meta['current_km']:,.0f}")
        summary_cols[3].metric("Services Recorded", meta["service_count"])

        st.markdown("---")

        # --------------------------------------------------------
        # ML VEHICLE HEALTH SCORE
        # --------------------------------------------------------
        st.subheader("🤖 ML Vehicle Health Score")
        health_cols = st.columns([1, 1, 2])
        with health_cols[0]:
            st.metric("Health Score", f"{health_score:.0f}/100")
        with health_cols[1]:
            st.metric("Condition", f"{icon} {label}")
        with health_cols[2]:
            st.progress(int(round(health_score)), text=f"Vehicle Health: {health_score:.0f}%")

        if health_score >= 85:
            st.success("🟢 Your vehicle is in excellent condition based on the available data.")
        elif health_score >= 70:
            st.success("🟢 Your vehicle is in good condition. Continue regular maintenance.")
        elif health_score >= 50:
            st.warning("🟡 Your vehicle needs attention. Check upcoming maintenance items.")
        else:
            st.error("🔴 Your vehicle shows a high maintenance need. Professional inspection is recommended.")

        # --------------------------------------------------------
        # PREDICTIVE MAINTENANCE
        # --------------------------------------------------------
        st.subheader("🔮 Predictive Maintenance")
        risk_cols = st.columns(3)
        risk_cols[0].metric("Maintenance Risk", f"{maintenance_probability * 100:.1f}%")
        risk_cols[1].metric("Risk Level", f"{risk_icon} {risk_label}")
        risk_cols[2].metric("Days Since Service", meta["days_since_service"])
        st.progress(
            int(round(maintenance_probability * 100)),
            text=f"ML Maintenance Risk: {maintenance_probability * 100:.1f}%"
        )

        if maintenance_probability >= 0.75:
            st.error("🔴 Predictive alert: maintenance should be scheduled soon.")
        elif maintenance_probability >= 0.45:
            st.warning("🟡 Predictive alert: maintenance may be required soon.")
        else:
            st.success("🟢 Predictive alert: no immediate maintenance risk detected from the available data.")

        # --------------------------------------------------------
        # NEXT SERVICE ESTIMATE
        # --------------------------------------------------------
        st.subheader("📅 Next Service Prediction")
        if meta["service_count"] > 0:
            latest_service = max(
                [
                    h for h in st.session_state["history"]
                    if h.get("Company") == vehicle_info.get("Company")
                    and h.get("Model") == vehicle_info.get("Model")
                ],
                key=lambda h: h.get("Date", date.min)
            )
            estimated_date = latest_service.get("Next Date", date.today() + timedelta(days=180))
            estimated_km = float(latest_service.get("Next KM", meta["current_km"] + 5000))
        else:
            estimated_date = date.today() + timedelta(days=180)
            estimated_km = meta["current_km"] + 5000

        due_cols = st.columns(2)
        due_cols[0].metric("Recommended Date", str(estimated_date))
        due_cols[1].metric("Recommended KM", f"{estimated_km:,.0f} KM")

        if meta["days_since_service"] > 180 or (
            meta["last_service_km"] > 0 and meta["current_km"] - meta["last_service_km"] >= 5000
        ):
            st.warning("⏰ Your vehicle may already be due for service based on the latest service record.")

        # --------------------------------------------------------
        # ML INPUT SIGNALS
        # --------------------------------------------------------
        st.subheader("📊 ML Health Factors")
        factor_df = pd.DataFrame([
            {"Factor": "Vehicle Age", "Value": f"{meta['vehicle_age']} years"},
            {"Factor": "Current Usage", "Value": f"{meta['current_km']:,.0f} KM"},
            {"Factor": "Days Since Service", "Value": str(meta['days_since_service'])},
            {"Factor": "Recorded Services", "Value": str(meta['service_count'])},
            {"Factor": "Recent Diagnosed Faults", "Value": str(meta['recent_fault_count'])},
            {"Factor": "High/Critical Faults", "Value": str(meta['high_severity_faults'])},
        ])
        st.dataframe(factor_df, use_container_width=True, hide_index=True)

        st.info(
            "🤖 ML note: the current app uses a built-in labelled training set so the feature works immediately. "
            "For a final academic/production version, replace it with a larger real-world 2-wheeler service and fault dataset."
        )

# ============================================================
# CONTACT SUPPORT
# ============================================================

elif menu == "📞 Contact Support":

    st.header("📞 Contact Support")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📧 Email Support")

        st.write(
            "support@aimechanical.com"
        )

    with col2:

        st.subheader("📱 Phone Support")

        st.write(
            "+91 9876543210"
        )

    st.markdown("---")

    st.info(
        "For emergency vehicle problems, contact a qualified "
        "mechanic or authorized service center."
    )

# ============================================================
# LOGOUT
# ============================================================

elif menu == "🚪 Logout":

    st.warning(
        "🚪 Are you sure you want to logout?"
    )

    if st.button(
        "🚪 Logout Now",
        use_container_width=True
    ):

        st.session_state["logged_in"] = False
        st.session_state["username"] = None

        st.success(
            "✅ Logged out successfully!"
        )

>>>>>>> 0069cd2fe8e4cdbb17dc0a6a482adaa93713a609
        st.switch_page("app.py")