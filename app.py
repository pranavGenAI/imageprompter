import streamlit as st
import PIL.Image
import google.generativeai as genai
import time
import hashlib

# Streamlit Configuration
st.set_page_config(page_title="Image Prompter", page_icon="🎨", layout="wide")

# Configure Google Generative AI with the API key
GOOGLE_API_KEY = "AIzaSyCNX1H0w4y7dJPlwqvrxiW1OjAMf4dkFp0"
genai.configure(api_key=GOOGLE_API_KEY)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Define users and hashed passwords
users = {
    "ankur.d.shrivastav": hash_password("ankur123"),
    "sashank.vaibhav.allu": hash_password("sashank123"),
    "shivananda.mallya": hash_password("shiv123"),
    "pranav.baviskar": hash_password("pranav123")
}

def login():
    """Login Functionality"""
    col1, col2 = st.columns([0.3, 0.7])
    with col1:
        st.title("Login")
        username = st.text_input("Username", label_visibility="collapsed")
        password = st.text_input("Password", type="password", label_visibility="collapsed")
        
        if st.button("Sign in"):
            hashed_password = hash_password(password)
            if username in users and users[username] == hashed_password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid username or password")

def logout():
    """Logout Functionality"""
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("Logged out successfully!")
    st.rerun()

def generate_content(image, user_question):
    """Generate content using Generative AI"""
    max_retries = 10
    delay = 10
    retry_count = 0

    while retry_count < max_retries:
        try:
            model = genai.GenerativeModel('gemini-1.5-pro')
            prompt = f"""
            You are an intelligent AI assistant. Analyze the provided image and answer the user's question.
            Format the response in Markdown with clear headings, bullet points, and bold/italicized text where appropriate.
            User Question: {user_question}
            """
            response = model.generate_content([prompt, image], stream=True)
            response.resolve()
            return response.text

        except Exception as e:
            st.error(f"Error occurred: {str(e)}")
            retry_count += 1
            if retry_count == max_retries:
                st.error("Max retries reached. Server might be unavailable.")
            time.sleep(delay)

    return None

def main():
    """Main Application Logic"""
    col1, col2 = st.columns([1, 2])

    with col1:
        uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if uploaded_image:
            st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)

    with col2:
        st.write("Enter your prompt here")
        user_question = st.text_input("", label_visibility="collapsed")
        
        if uploaded_image and user_question:
            if st.button("Submit"):
                with st.spinner("Extracting data..."):
                    image = PIL.Image.open(uploaded_image)
                    extracted_data = generate_content(image, user_question)
                    if extracted_data:
                        st.markdown(extracted_data)  # Render the AI response in Markdown
                    else:
                        st.error("Failed to extract data. Please try again.")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if st.session_state.logged_in:
    col1, col2, col3 = st.columns([10, 10, 1.5])
    with col3:
        if st.button("Logout"):
            logout()
    main()
else:
    login()
