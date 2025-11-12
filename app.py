import streamlit as st
import json
from pathlib import Path

USER_FILE = Path("users.json")

if not USER_FILE.exists():
    with open(USER_FILE, "w") as f:
        json.dump({}, f)

def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def signup(email, password, confirm_password):
    if not email or not password or not confirm_password:
        return "❌ Please fill in all fields."

    if "@" not in email or "." not in email:
        return "⚠️ Invalid email format."

    if password != confirm_password:
        return "🚫 Passwords do not match."

    users = load_users()
    if email in users:
        return "😅 Email already registered. Try logging in."

    users[email] = {"password": password}
    save_users(users)
    return "✅ Signup successful! You can now log in."


def login(email, password):
    users = load_users()

    if email not in users:
        return "❌ No account found with this email."

    if users[email]["password"] != password:
        return "🚫 Incorrect password."

    return "✅ Login successful!"

st.set_page_config(page_title="Threat Predictor", page_icon="🔐", layout="centered")

if "menu" not in st.session_state:
    st.session_state["menu"] = "Home"
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "email" not in st.session_state:
    st.session_state["email"] = None


st.markdown("## 🤔 Threat Predictor")

col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
with col2:
    if st.button("🏠 Home"):
        st.session_state["menu"] = "Home"
with col3:
    if st.button("📝 Signup"):
        st.session_state["menu"] = "Signup"
with col4:
    if st.button("🔑 Login"):
        st.session_state["menu"] = "Login"

menu = st.session_state["menu"]

st.markdown("---")

if menu == "Home":
    st.header("Welcome to Threat Predictor ")
    if st.session_state["logged_in"]:
        st.success(f"Welcome back, {st.session_state['email']}! ")
    st.write("(tag line) Here you can explore data and information about various **threats** .")
    st.info(" Add any kind of site info n also some of the images related to that.")
    
elif menu == "Signup":
    st.header("Create a New Account ")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        result = signup(email, password, confirm_password)
        if "✅" in result:
            st.success(result)
            #st.rerun()
        else:
            st.error(result)
            #st.rerun()

elif menu == "Login":
    if not st.session_state["logged_in"]:
        st.header("Log In to Your Account ")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            result = login(email, password)
            if "✅" in result:
                st.session_state["logged_in"] = True
                st.session_state["email"] = email
                st.success(result)
                st.session_state["menu"] = "Home"
                st.rerun()
            else:
                st.error(result)

    if st.session_state["logged_in"]:
        st.subheader(f"Welcome, {st.session_state['email']}! 🎉")
        st.info("You’re now logged in. Access more features below 👇")
        if st.button("Logout"):
            st.session_state["logged_in"] = False
            st.session_state["email"] = None
            st.session_state["menu"] = "Home"
            st.rerun()

st.markdown("---")
st.caption("<p style='text-align:center; font-size: 18px'> Threat Predictor © 2025 ", unsafe_allow_html= True)
