import streamlit as st
import json
from pathlib import Path

st.set_page_config(
    page_title="AI Mechanical Help Center",
    page_icon="🤖",
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


st.title("🤖 AI Mechanical Help Center")
st.subheader("Smart Self-Service Assistant")

st.markdown("---")

username = st.text_input("👤 Username")
password = st.text_input("🔒 Password", type="password")

if st.button("✅ Login", use_container_width=True):

    users = load_users()

    if not username.strip() or not password:
        st.error("❌ Please enter Username and Password.")

    elif username not in users:
        st.error("❌ Username not found. Please register first.")

    elif users[username]["password"] != password:
        st.error("❌ Incorrect password.")

    else:
        st.session_state["logged_in"] = True
        st.session_state["username"] = username

        st.success("✅ Login successful!")

        st.switch_page("pages/dashboard.py")


st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    if st.button("📝 Register Here", use_container_width=True):
        st.switch_page("pages/register.py")

with col2:
    if st.button("🔑 Forgot Password", use_container_width=True):
        st.switch_page("pages/forgot_password.py")