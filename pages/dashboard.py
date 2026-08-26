import streamlit as st
import pandas as pd
from datetime import date, timedelta
import streamlit.components.v1 as components
from pathlib import Path
import base64


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
            "Fuel": fuel
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

            result = diagnosis_database[problem]

            st.success(
                "✅ Diagnosis Completed"
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
                "🤖 This diagnosis provides possible causes based "
                "on the selected symptom. It is not a substitute "
                "for professional mechanical inspection."
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

        st.switch_page("app.py")