print("="*70)
print("🤖 AI SMART MECHANICAL HELP CENTER")
print("🚗 VEHICLE DIAGNOSIS SYSTEM")
print("="*70)

# -------------------------------
# User Details
# -------------------------------

name = input("👤 Enter Your Name: ")
company = input("🏢 Enter Vehicle Company: ")
model = input("🚗 Enter Vehicle Model: ")
year = input("📅 Manufacturing Year: ")
fuel = input("⛽ Fuel Type (Petrol/Diesel/CNG/Electric): ")
km = input("🛣️ Vehicle Running (KM): ")

print("\n" + "="*70)
print("VEHICLE DETAILS")
print("="*70)

print("Owner Name :", name)
print("Company    :", company)
print("Model      :", model)
print("Year       :", year)
print("Fuel Type  :", fuel)
print("Running KM :", km)

print("\nDescribe your vehicle problem.")
problem = input("💬 Problem: ").lower()

print("\n🤖 AI is analyzing your vehicle...")
print("Please wait...\n")

# -------------------------------
# Vehicle Diagnosis
# -------------------------------

fault = ""
repair = ""
time = ""
confidence = ""

if "not start" in problem or "start" in problem:
    fault = "Battery Discharged / Starter Motor Problem"
    repair = """• Check battery terminals
• Check battery voltage
• Try jump-starting
• Check starter motor"""
    time = "30 Minutes"
    confidence = "95%"

elif "overheat" in problem:
    fault = "Engine Overheating"
    repair = """• Stop the vehicle
• Allow engine to cool
• Check coolant
• Check radiator fan"""
    time = "40 Minutes"
    confidence = "96%"

elif "brake" in problem:
    fault = "Brake Pad Worn"
    repair = """• Check brake pads
• Check brake fluid
• Replace worn brake pads"""
    time = "1 Hour"
    confidence = "94%"

elif "battery" in problem:
    fault = "Battery Charging Problem"
    repair = """• Check battery
• Check alternator
• Replace battery if required"""
    time = "30 Minutes"
    confidence = "93%"

elif "oil" in problem:
    fault = "Low Engine Oil"
    repair = """• Check oil level
• Refill engine oil
• Inspect oil leakage"""
    time = "20 Minutes"
    confidence = "95%"

elif "tyre" in problem or "tire" in problem:
    fault = "Flat Tyre"
    repair = """• Replace spare tyre
• Check tyre pressure
• Repair puncture"""
    time = "20 Minutes"
    confidence = "98%"

elif "ac" in problem:
    fault = "AC Cooling Problem"
    repair = """• Check AC gas
• Check compressor
• Clean AC filter"""
    time = "45 Minutes"
    confidence = "92%"

elif "steering" in problem:
    fault = "Wheel Alignment Problem"
    repair = """• Check alignment
• Balance wheels
• Inspect suspension"""
    time = "1 Hour"
    confidence = "90%"

elif "headlight" in problem or "light" in problem:
    fault = "Headlight Fuse/Bulb Failure"
    repair = """• Check fuse
• Replace bulb
• Inspect wiring"""
    time = "20 Minutes"
    confidence = "91%"

elif "fuel" in problem:
    fault = "Fuel Leakage"
    repair = """• Stop the engine
• Do not smoke
• Contact service centre"""
    time = "Immediate"
    confidence = "99%"

elif "smoke" in problem:
    fault = "Engine Internal Problem"
    repair = """• Stop driving
• Check coolant
• Visit service centre"""
    time = "2 Hours"
    confidence = "94%"

elif "gear" in problem:
    fault = "Gearbox Problem"
    repair = """• Check transmission oil
• Inspect clutch
• Visit service centre"""
    time = "2 Hours"
    confidence = "92%"

else:
    fault = "Problem Not Identified"
    repair = """• Please describe the issue in more detail.
• Visit the nearest authorized service centre."""
    time = "Unknown"
    confidence = "70%"

# -------------------------------
# Diagnosis Report
# -------------------------------

print("="*70)
print("🤖 AI VEHICLE DIAGNOSIS REPORT")
print("="*70)

print("👤 Customer :", name)
print("🚗 Vehicle  :", company, model)
print("📅 Year     :", year)
print("⛽ Fuel     :", fuel)
print("🛣️ Running  :", km, "KM")

print("\n🔍 Possible Fault:")
print(fault)

print("\n🛠️ Repair Steps:")
print(repair)

print("\n⏱️ Estimated Repair Time :", time)
print("📊 AI Confidence         :", confidence)

print("\n⚠️ Safety Advice")
print("----------------------------")
print("• Drive carefully if the issue is minor.")
print("• Stop the vehicle immediately if there is overheating or fuel leakage.")
print("• Visit an authorized service centre if the issue continues.")

print("\n📞 Service Centre : +91 9876543210")
print("🚑 Roadside Help  : 1800-123-4567")

print("\n✅ Thank you for using AI Smart Mechanical Help Center.")
