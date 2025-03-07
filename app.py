import streamlit as st
import secrets
import string
from zxcvbn import zxcvbn
import time

# Initialize session state variables
if "password_history" not in st.session_state:
    st.session_state["password_history"] = []
if "password" not in st.session_state:
    st.session_state["password"] = ""

# Function to generate a password
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

# Function to get strength label
def get_strength_meter(score):
    colors = ["🔴 Very Weak", "🟠 Weak", "🟡 Moderate", "🟢 Strong", "💪 Very Strong"]
    return colors[score]

# Function to reset password field
def reset_password():
    st.session_state["password"] = ""  # ✅ Reset password only

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

    # User Password Input (Handles Manual Typing)
    password_input = st.text_input(
        "🔐 Type or Generate a Password:", 
        value=st.session_state["password"], 
        key="password_input"
    )

    # Update session state when user types a password
    if password_input != st.session_state["password"]:
        st.session_state["password"] = password_input  # ✅ Proper session state update

    # Check password strength
    if password_input:
        score, feedback = check_password_strength(password_input)
        strength_label = get_strength_meter(score)

        # Color-based strength feedback
        st.markdown(f"**Strength:** {strength_label}")
        if feedback['suggestions']:
            with st.expander("💡 Tips to Improve Your Password"):
                for suggestion in feedback['suggestions']:
                    st.write(f"- {suggestion}")

    col1, col2 = st.columns([1, 1])

    # Generate Password Button
    if col1.button("🎲 Generate Password", use_container_width=True):
        with st.spinner("Generating a secure password..."):
            time.sleep(1)
            new_password = generate_password(length, use_digits, use_special)
            st.session_state["password"] = new_password  # ✅ Store generated password

        if len(new_password) >= 16:
            st.balloons()

    # Clear Password Button
    if col2.button("🗑️ Clear Password", use_container_width=True, on_click=reset_password):
        pass  # ✅ This now resets the password safely

    # Display Password
    if st.session_state["password"]:
        st.markdown("### ✨ Your Secure Password:")
        st.text_input("🔑 Generated Password", value=st.session_state["password"], disabled=True)

    # Sidebar: Security Tips
    st.sidebar.markdown("### 🔐 Pro Security Tips")
    st.sidebar.info("""
    - ✅ Use at least **12-16 characters** for max security.
    - 🔄 Avoid **reusing passwords**.
    - 🔥 Mix uppercase, lowercase, numbers, and symbols.
    - 🛑 Never share your passwords!
    - 🔑 Consider using a **password manager**.
    """)

    # Footer
    st.markdown("<hr>", unsafe_allow_html=True)
    st.caption("🔐 Stay secure with our fun & interactive password generator!")

# Run the app
if __name__ == "__main__":
    main()
