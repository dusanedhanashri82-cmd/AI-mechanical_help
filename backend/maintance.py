# ============================================================
# AI SMART MECHANICAL HELP CENTER
# VEHICLE MAINTENANCE BACKEND
# ============================================================


# ============================================================
# FUNCTION 1
# GET GENERAL MAINTENANCE TIPS
# ============================================================

def get_general_maintenance_tips():

    tips = [
        "Check tyre pressure every 15 days.",
        "Clean your vehicle regularly.",
        "Keep the battery terminals clean.",
        "Carry a spare tyre and toolkit.",
        "Check all lights before long trips."
    ]

    return tips


# ============================================================
# FUNCTION 2
# GET SERVICE RECOMMENDATIONS
# BASED ON VEHICLE RUNNING KM
# ============================================================

def get_service_recommendations(km):

    km = int(km)

    # --------------------------------------------------------
    # BELOW 5000 KM
    # --------------------------------------------------------

    if km < 5000:

        recommendations = [
            "Your vehicle is relatively new.",
            "Check engine oil and coolant level."
        ]

        service_stage = "Below 5,000 KM"


    # --------------------------------------------------------
    # 5,000 - 10,000 KM
    # --------------------------------------------------------

    elif km < 10000:

        recommendations = [
            "Engine oil change is recommended.",
            "Inspect air filter."
        ]

        service_stage = "5,000 - 10,000 KM"


    # --------------------------------------------------------
    # 10,000 - 20,000 KM
    # --------------------------------------------------------

    elif km < 20000:

        recommendations = [
            "Replace engine oil and oil filter.",
            "Check brake pads and battery."
        ]

        service_stage = "10,000 - 20,000 KM"


    # --------------------------------------------------------
    # 20,000 - 40,000 KM
    # --------------------------------------------------------

    elif km < 40000:

        recommendations = [
            "Replace air filter.",
            "Inspect spark plugs.",
            "Check wheel alignment."
        ]

        service_stage = "20,000 - 40,000 KM"


    # --------------------------------------------------------
    # 40,000 - 60,000 KM
    # --------------------------------------------------------

    elif km < 60000:

        recommendations = [
            "Replace brake fluid.",
            "Check suspension.",
            "Inspect clutch."
        ]

        service_stage = "40,000 - 60,000 KM"


    # --------------------------------------------------------
    # ABOVE 60,000 KM
    # --------------------------------------------------------

    else:

        recommendations = [
            "Complete vehicle inspection is recommended.",
            "Check gearbox, suspension and engine.",
            "Visit an authorized service center."
        ]

        service_stage = "60,000+ KM"


    return {
        "service_stage": service_stage,
        "recommendations": recommendations
    }


# ============================================================
# FUNCTION 3
# GET SAFETY TIPS
# ============================================================

def get_safety_tips():

    safety_tips = [
        "Never ignore warning lights.",
        "Stop driving if the engine overheats.",
        "Do not drive with a fuel leak.",
        "Wear your seat belt at all times."
    ]

    return safety_tips


# ============================================================
# FUNCTION 4
# VALIDATE VEHICLE DETAILS
# ============================================================

def validate_maintenance_details(
    name,
    company,
    model,
    fuel,
    km
):

    errors = []

    # --------------------------------------------------------
    # NAME
    # --------------------------------------------------------

    if not name or not name.strip():

        errors.append(
            "Please enter your name."
        )


    # --------------------------------------------------------
    # COMPANY
    # --------------------------------------------------------

    if not company or not company.strip():

        errors.append(
            "Please enter vehicle company."
        )


    # --------------------------------------------------------
    # MODEL
    # --------------------------------------------------------

    if not model or not model.strip():

        errors.append(
            "Please enter vehicle model."
        )


    # --------------------------------------------------------
    # FUEL
    # --------------------------------------------------------

    if not fuel or not fuel.strip():

        errors.append(
            "Please select fuel type."
        )


    # --------------------------------------------------------
    # KM
    # --------------------------------------------------------

    try:

        km = int(km)

        if km < 0:

            errors.append(
                "Vehicle running KM cannot be negative."
            )

    except:

        errors.append(
            "Vehicle running KM must be a valid number."
        )


    return errors


# ============================================================
# FUNCTION 5
# COMPLETE MAINTENANCE PROCESS
# ============================================================

def get_maintenance_tips(
    name,
    company,
    model,
    fuel,
    km
):

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    errors = validate_maintenance_details(
        name,
        company,
        model,
        fuel,
        km
    )


    # --------------------------------------------------------
    # IF ERROR
    # --------------------------------------------------------

    if errors:

        return {
            "success": False,
            "errors": errors,
            "vehicle": None,
            "general_tips": [],
            "service_recommendations": [],
            "safety_tips": []
        }


    # --------------------------------------------------------
    # CONVERT KM
    # --------------------------------------------------------

    km = int(km)


    # --------------------------------------------------------
    # GET GENERAL TIPS
    # --------------------------------------------------------

    general_tips = (
        get_general_maintenance_tips()
    )


    # --------------------------------------------------------
    # GET SERVICE RECOMMENDATIONS
    # --------------------------------------------------------

    service_data = (
        get_service_recommendations(km)
    )


    # --------------------------------------------------------
    # GET SAFETY TIPS
    # --------------------------------------------------------

    safety_tips = (
        get_safety_tips()
    )


    # --------------------------------------------------------
    # VEHICLE DETAILS
    # --------------------------------------------------------

    vehicle = {

        "name": name,

        "company": company,

        "model": model,

        "fuel": fuel,

        "km": km
    }


    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    return {

        "success": True,

        "errors": [],

        "vehicle": vehicle,

        "general_tips": general_tips,

        "service_stage":
            service_data["service_stage"],

        "service_recommendations":
            service_data["recommendations"],

        "safety_tips":
            safety_tips
    }


# ============================================================
# FUNCTION 6
# FORMAT MAINTENANCE REPORT
# ============================================================

def format_maintenance_report(result):

    if not result["success"]:

        return "Maintenance report could not be generated."


    vehicle = result["vehicle"]


    report = f"""
======================================================================
🛠 AI SMART MECHANICAL HELP CENTER
🚗 VEHICLE MAINTENANCE REPORT
======================================================================

👤 Owner Name : {vehicle['name']}
🏢 Company    : {vehicle['company']}
🚗 Model      : {vehicle['model']}
⛽ Fuel Type  : {vehicle['fuel']}
🛣️ Running KM : {vehicle['km']} KM


🔧 AI MAINTENANCE TIPS
----------------------------------------------------------------------

"""


    # --------------------------------------------------------
    # GENERAL TIPS
    # --------------------------------------------------------

    for tip in result["general_tips"]:

        report += (
            "✅ " + tip + "\n"
        )


    # --------------------------------------------------------
    # SERVICE RECOMMENDATIONS
    # --------------------------------------------------------

    report += f"""

📋 SERVICE RECOMMENDATIONS
----------------------------------------------------------------------

Service Stage: {result['service_stage']}

"""


    for recommendation in (
        result["service_recommendations"]
    ):

        report += (
            "• " + recommendation + "\n"
        )


    # --------------------------------------------------------
    # SAFETY TIPS
    # --------------------------------------------------------

    report += """

⚠️ SAFETY TIPS
----------------------------------------------------------------------

"""


    for safety in result["safety_tips"]:

        report += (
            "• " + safety + "\n"
        )


    report += """

======================================================================
✅ Thank you for using AI Smart Mechanical Help Center!
======================================================================
"""


    return report


# ============================================================
# TEST BACKEND
# ============================================================

if __name__ == "__main__":

    print("=" * 70)

    print(
        "🛠 AI SMART MECHANICAL HELP CENTER"
    )

    print(
        "🚗 VEHICLE MAINTENANCE BACKEND"
    )

    print("=" * 70)


    # --------------------------------------------------------
    # SAMPLE DATA
    # --------------------------------------------------------

    name = "Test User"

    company = "Hero"

    model = "Splendor Plus"

    fuel = "Petrol"

    km = 12500


    # --------------------------------------------------------
    # GET MAINTENANCE RESULT
    # --------------------------------------------------------

    result = get_maintenance_tips(

        name=name,

        company=company,

        model=model,

        fuel=fuel,

        km=km
    )


    # --------------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------------

    if result["success"]:

        print(
            format_maintenance_report(
                result
            )
        )

    else:

        print(
            "❌ Errors:"
        )

        for error in result["errors"]:

            print(
                "•",
                error
            )