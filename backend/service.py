import pandas as pd
from datetime import datetime, timedelta
def get_service_data():
    return "Service Data"
print("=" * 70)
print("🚗 AI SMART MECHANICAL HELP CENTER")
print("📋 VEHICLE SERVICE HISTORY")
print("=" * 70)

service_history = []

while True:

    print("\n1. Add Service Record")
    print("2. View Service History")
    print("3. Next Service Reminder")
    print("4. Exit")

    choice = input("\nEnter Choice: ")

    if choice == "1":

        owner = input("Owner Name: ")
        company = input("Vehicle Company: ")
        model = input("Vehicle Model: ")
        vehicle_no = input("Vehicle Number: ")

        km = int(input("Current Kilometer: "))

        service_type = input("Service Type: ")

        cost = float(input("Service Cost (₹): "))

        notes = input("Mechanic Notes: ")

        service_date = datetime.today().date()

        next_service_date = service_date + timedelta(days=180)
        next_service_km = km + 10000

        record = {
            "Owner": owner,
            "Company": company,
            "Model": model,
            "Vehicle No": vehicle_no,
            "Service Date": service_date,
            "Service Type": service_type,
            "KM": km,
            "Cost": cost,
            "Notes": notes,
            "Next Service Date": next_service_date,
            "Next Service KM": next_service_km
        }

        service_history.append(record)

        print("\n✅ Service Record Saved Successfully!")

    elif choice == "2":

        if len(service_history) == 0:
            print("\nNo Service Records Found.")

        else:
            df = pd.DataFrame(service_history)
            print("\nSERVICE HISTORY")
            print(df)

    elif choice == "3":

        if len(service_history) == 0:
            print("\nNo Service Record Available.")

        else:

            latest = service_history[-1]

            print("\nNEXT SERVICE REMINDER")
            print("-" * 50)
            print("Vehicle :", latest["Company"], latest["Model"])
            print("Vehicle Number :", latest["Vehicle No"])
            print("Next Service Date :", latest["Next Service Date"])
            print("Next Service KM :", latest["Next Service KM"], "KM")
            print("Recommended Service : Engine Oil + General Inspection")

            today = datetime.today().date()

            remaining = (latest["Next Service Date"] - today).days

            if remaining <= 30:
                print("\n⚠ Reminder: Your next service is due in", remaining, "days.")
            else:
                print("\n✅", remaining, "days remaining for next service.")

    elif choice == "4":

        print("\nThank you for using AI Smart Mechanical Help Center.")
        break

    else:
        print("\n❌ Invalid Choice")