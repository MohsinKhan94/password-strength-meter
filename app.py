import streamlit as st
import secrets
import string
import time
import pyperclip
from zxcvbn import zxcvbn

# Store password history
if "password_history" not in st.session_state:
    st.session_state["password_history"] = []
if "password" not in st.session_state:
    st.session_state["password"] = ""
if "password_input" not in st.session_state:
    st.session_state["password_input"] = ""

# Function to generate a strong password
def generate_password(length=12, use_digits=True, use_special=True):
    characters = string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

# Function to check password strength
def check_password_strength(password):
    result = zxcvbn(password)
    return result['score'], result['feedback']

# Function to style the strength meter with colors
def get_strength_meter(score):
    colors = ["🔴 Very Weak", "🟠 Weak", "🟡 Moderate", "🟢 Strong", "💪 Very Strong"]
    return colors[score]

# Function to copy password to clipboard
def copy_password():
    pyperclip.copy(st.session_state["password"])

# Function to reset everything
def reset_app():
    st.session_state.clear()

# Main function
def main():
    st.set_page_config(page_title="🔒 Password Generator", page_icon="🔑", layout="wide")

    # Sidebar Settings
    st.sidebar.title("⚙️ Settings")
    length = st.sidebar.slider("🔢 Password Length", min_value=8, max_value=32, value=12)
    use_digits = st.sidebar.checkbox("🔢 Include Digits", value=True)
    use_special = st.sidebar.checkbox("🔣 Include Special Characters", value=True)

    # Title & Description
    st.title("🔑 Ultimate Password Generator")
    st.markdown("### Secure, Fun, and Interactive! 🚀")
    st.markdown("<hr>", unsafe_allow_html=True)

    # User Password Input for Live Strength Meter
    password_input = st.text_input("🔐 Type or Generate a Password:", key="password_input")

    if password_input:
        score, feedback = check_password_strength(password_input)
        strength_label = get_strength_meter(score)
        st.markdown(f"**Strength:** {strength_label}")
        
        if feedback['suggestions']:
            with st.expander("💡 Tips to Improve Your Password"):
                for suggestion in feedback['suggestions']:
                    st.write(f"- {suggestion}")

    # Generate Password Button
    if st.button("🎲 Generate Password"):
        with st.spinner("Generating a secure password..."):
            time.sleep(1)
            new_password = generate_password(length, use_digits, use_special)
            st.session_state["password"] = new_password
            st.session_state["password_history"].append(new_password)

        if len(new_password) >= 16:
            st.balloons()

    # Display Generated Password
    if st.session_state["password"]:
        st.markdown("### ✨ Your Secure Password:")
        st.text_input("🔑 Generated Password", value=st.session_state["password"], disabled=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("📋 Copy to Clipboard"):
                copy_password()
                st.success("✅ Password copied!")

        with col2:
            if st.button("❌ Reset"):
                reset_app()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.caption("🔐 Stay secure with our fun & interactive password generator!")

# Run the app
if __name__ == "__main__":
    main()
