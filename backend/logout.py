print("="*70)
print("🤖 AI SMART MECHANICAL HELP CENTER")
print("🔒 LOGOUT")
print("="*70)

name = input("👤 Enter Your Name: ")

print(f"\nHello, {name}!")

choice = input("Do you want to logout? (yes/no): ").lower()

if choice == "yes":
    print("\n🔒 Logging out...")
    print("✅ Logout Successful!")
    print("👋 Thank you for using AI Smart Mechanical Help Center.")
    print("🚗 Have a Safe Journey!")
elif choice == "no":
    print("\n😊 Logout Cancelled.")
    print("You are still logged in.")
else:
    print("\n❌ Invalid Input.")
    print("Please enter 'yes' or 'no'.")