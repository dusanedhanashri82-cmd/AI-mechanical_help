import streamlit as st
import json
from pathlib import Path

st.set_page_config(
    page_title="Forgot Password",
    page_icon="🔑",
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


st.title("🔑 Forgot Password")

st.write("Enter your registered username and email.")

st.markdown("---")

username = st.text_input("👤 Username")
email = st.text_input("📧 Registered Email")

if st.button("🔍 Verify Account", use_container_width=True):

    users = load_users()

    if not username.strip() or not email.strip():
        st.error("❌ Please enter Username and Email.")

    elif username not in users:
        st.error("❌ Username not found.")

    elif users[username]["email"] != email:
        st.error("❌ Email does not match the registered account.")

    else:
        st.session_state["reset_user"] = username
        st.success("✅ Account verified successfully!")

        st.session_state["show_reset"] = True


if st.session_state.get("show_reset", False):

    st.markdown("---")

    st.subheader("🔐 Create New Password")

    new_password = st.text_input(
        "New Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm New Password",
        type="password"
    )

    if st.button("🔄 Reset Password", use_container_width=True):

        if not new_password:
            st.error("❌ Enter a new password.")

        elif new_password != confirm_password:
            st.error("❌ Passwords do not match.")

        else:

            users = load_users()

            username = st.session_state["reset_user"]

            users[username]["password"] = new_password

            save_users(users)

            st.success("🎉 Password reset successfully!")

            st.session_state["show_reset"] = False
            st.session_state["reset_user"] = None

            st.info("➡️ Go back to Login.")

if st.button("⬅ Back to Login", use_container_width=True):
    st.switch_page("app.py")