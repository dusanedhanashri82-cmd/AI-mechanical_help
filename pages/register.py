import streamlit as st
import json
from pathlib import Path

st.set_page_config(
    page_title="Register",
    page_icon="📝",
    layout="centered"
)

USERS_FILE = Path("users.json")


def load_users():
    if not USERS_FILE.exists():
        return {}

    try:
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    except:
        return {}


def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)


st.title("📝 Create New Account")

st.write("Register to use AI Mechanical Help Center.")

st.markdown("---")

fullname = st.text_input("👤 Full Name")
email = st.text_input("📧 Email")
mobile = st.text_input("📱 Mobile Number")
username = st.text_input("👤 Username")
password = st.text_input("🔒 Password", type="password")
confirm_password = st.text_input(
    "🔒 Confirm Password",
    type="password"
)

if st.button("✅ Register", use_container_width=True):

    users = load_users()

    if not fullname.strip():
        st.error("❌ Please enter your Full Name.")

    elif not email.strip():
        st.error("❌ Please enter your Email.")

    elif not mobile.strip():
        st.error("❌ Please enter your Mobile Number.")

    elif not username.strip():
        st.error("❌ Please enter your Username.")

    elif not password:
        st.error("❌ Please enter your Password.")

    elif not confirm_password:
        st.error("❌ Please confirm your Password.")

    elif password != confirm_password:
        st.error("❌ Passwords do not match.")

    elif username in users:
        st.error("❌ Username already exists.")

    else:

        users[username] = {
            "fullname": fullname,
            "email": email,
            "mobile": mobile,
            "password": password
        }

        save_users(users)

        st.success("🎉 Registration Successful!")
        st.info("➡️ Now go back to Login and login with your account.")

if st.button("⬅ Back to Login", use_container_width=True):
    st.switch_page("app.py")