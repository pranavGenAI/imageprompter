import streamlit as st
import PIL.Image
import google.generativeai as genai
import time
import hashlib

# Streamlit Configuration
st.set_page_config(page_title="Image Prompter", page_icon="🎨", layout="wide")
background_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Underwater Bubble Background</title>
    <style>
        body {
            margin: 0;
            overflow: hidden;
            background: linear-gradient(45deg, #161d20 5%, #161d29 47.5%,#161d53 ,#161d52 95%);
         }
        canvas {
            display: block;
        }
    </style>
</head>
<body>
    <canvas id="bubblefield"></canvas>
    <script>
        // Setup canvas
        const canvas = document.getElementById('bubblefield');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        // Arrays to store bubbles
        let bubbles = [];
        const numBubbles = 100;
        const glowDuration = 1000; // Glow duration in milliseconds

        // Function to initialize bubbles
        function initializeBubbles() {
            for (let i = 0; i < numBubbles; i++) {
                bubbles.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    radius: Math.random() * 5 + 2, // Adjusted smaller bubble size
                    speedX: Math.random() * 0.5 - 0.25, // Adjusted slower speed
                    speedY: Math.random() * 0.5 - 0.25, // Adjusted slower speed
                    glow: false,
                    glowStart: 0
                });
            }
        }

        // Draw function
        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Draw bubbles
            for (let i = 0; i < numBubbles; i++) {
                let bubble = bubbles[i];

                // Calculate glow intensity based on time elapsed since glow started
                let glowIntensity = 0;
                if (bubble.glow) {
                    let elapsedTime = Date.now() - bubble.glowStart;
                    glowIntensity = 0.8 * (1 - elapsedTime / glowDuration); // Decreasing glow intensity over time
                    if (elapsedTime >= glowDuration) {
                        bubble.glow = false; // Reset glow state after glow duration
                    }
                }

                ctx.beginPath();
                ctx.arc(bubble.x, bubble.y, bubble.radius, 0, Math.PI * 2);

                // Set glow effect if bubble should glow
                if (glowIntensity > 0) {
                    let gradient = ctx.createRadialGradient(bubble.x, bubble.y, 0, bubble.x, bubble.y, bubble.radius);
                    gradient.addColorStop(0, `rgba(255, 255, 255, ${glowIntensity})`);
                    gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');
                    ctx.fillStyle = gradient;
                } else {
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.1)'; // Adjusted bubble transparency to 70%
                }
                
                ctx.fill();

                // Move bubbles based on speed
                bubble.x += bubble.speedX;
                bubble.y += bubble.speedY;

                // Wrap bubbles around edges of canvas
                if (bubble.x < -bubble.radius) {
                    bubble.x = canvas.width + bubble.radius;
                }
                if (bubble.x > canvas.width + bubble.radius) {
                    bubble.x = -bubble.radius;
                }
                if (bubble.y < -bubble.radius) {
                    bubble.y = canvas.height + bubble.radius;
                }
                if (bubble.y > canvas.height + bubble.radius) {
                    bubble.y = -bubble.radius;
                }
            }
            
            requestAnimationFrame(draw);
        }

        // Mouse move event listener to move bubbles towards cursor
        canvas.addEventListener('mousemove', function(event) {
            let mouseX = event.clientX;
            let mouseY = event.clientY;
            for (let i = 0; i < numBubbles; i++) {
                let bubble = bubbles[i];
                let dx = mouseX - bubble.x;
                let dy = mouseY - bubble.y;
                let distance = Math.sqrt(dx * dx + dy * dy);
                if (distance < 50) {
                    bubble.speedX = dx * 0.01;
                    bubble.speedY = dy * 0.01;
                    if (!bubble.glow) {
                        bubble.glow = true;
                        bubble.glowStart = Date.now();
                    }
                }
            }
        });

        // Start animation
        initializeBubbles();
        draw();

        // Resize canvas on window resize
        window.addEventListener('resize', function() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            initializeBubbles();  // Reinitialize bubbles on resize
        });
    </script>
</body>
</html>
"""

# Embed the HTML code into the Streamlit app
st.components.v1.html(background_html, height=1000)
st.markdown("""
<style>
    iframe {
        position: fixed;
        left: 0;
        right: 0;
        top: 0;
        bottom: 0;
        border: none;
        height: 100%;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)
st.markdown(
    """
    <style>
        .stAppHeader.st-emotion-cache-h4xjwg.e10jh26i0 {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("GenAI Image Prompter")
# Configure Google Generative AI with the API key
GOOGLE_API_KEY = "AIzaSyAAuinhF4VsJ8jwwQrntVQAsqxVhkUgfhQ"
genai.configure(api_key=GOOGLE_API_KEY)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Define users and hashed passwords
users = {
    "ankur.d.shrivastav": hash_password("ankur123"),
    "sashank.vaibhav.allu": hash_password("sashank123"),
    "shivananda.mallya": hash_password("shiv123"),
    "m.venkata.kesava": hash_password("mahendra123"),
    "pranav.baviskar": hash_password("pranav123"),
    "nehal.s": hash_password("nehal123")
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
    col1, col2, col3 = st.columns([6,1, 10])

    with col1:
        uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if uploaded_image:
            st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)

    with col3:
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
