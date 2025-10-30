import streamlit as st
import anthropic
import base64
from PIL import Image
import io

# Configure page
st.set_page_config(
    page_title="Limosa",
    page_icon="🩺",
    layout="centered"
)

# Get API key from secrets
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    client = anthropic.Anthropic(api_key=api_key)
except:
    st.error("API key not configured")
    st.stop()

# Minimal CSS like Claude
st.markdown("""
<style>
.main .block-container {
    padding-top: 2rem;
    max-width: 720px;
    margin: 0 auto;
}

/* Hide all Streamlit UI elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}
.stDecoration {display: none;}

/* Clean typography */
.main h1 {
    font-size: 1.5rem;
    font-weight: 500;
    color: #1a1a1a;
    margin-bottom: 0.5rem;
    text-align: center;
}

/* Minimal chat interface */
.stChatMessage {
    background: transparent;
    border: none;
    padding: 0.5rem 0;
}

/* Clean file uploader */
.stFileUploader {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1rem;
}

/* Clean selectboxes */
.stSelectbox {
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# Simple header
st.markdown("# Limosa")

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = [{
        'role': 'assistant',
        'content': "I'm an AI assistant specialized in veterinary diagnostics. Upload an image and ask me about it, or ask me any veterinary questions."
    }]

# File upload section
uploaded_file = st.file_uploader("Upload veterinary image", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    st.image(uploaded_file, width=300)
    
    col1, col2 = st.columns(2)
    with col1:
        species = st.selectbox("Species", ["Unknown", "Canine", "Feline", "Equine"])
    with col2:
        analysis_type = st.selectbox("Focus", ["General", "Radiographic", "Dermatological"])

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about veterinary cases..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        if uploaded_file:
            with st.spinner("🔬 Analyzing veterinary image..."):
                try:
                    # Convert image to base64
                    uploaded_file.seek(0)
                    image_bytes = uploaded_file.read()
                    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
                    
                    # Call Claude
                    response = client.messages.create(
                        model="claude-3-5-haiku-20241022",
                        max_tokens=1500,
                        temperature=0.1,
                        system=f"You are a veterinary diagnostician analyzing a {species} image with focus on {analysis_type}. Provide professional medical insights.",
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": f"Please analyze this veterinary image: {prompt}"},
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": "image/jpeg",
                                        "data": encoded_image
                                    }
                                }
                            ]
                        }]
                    )
                    
                    analysis = response.content[0].text
                    formatted_response = f"""**Analysis for {species}** ({analysis_type})

{analysis}

*This analysis supports clinical decision-making but does not replace professional veterinary examination.*"""
                    
                    st.markdown(formatted_response)
                    st.session_state.messages.append({"role": "assistant", "content": formatted_response})
                    
                except Exception as e:
                    error_msg = f"⚠️ Analysis error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
        else:
            with st.spinner("Thinking..."):
                try:
                    response = client.messages.create(
                        model="claude-3-5-haiku-20241022",
                        max_tokens=1000,
                        temperature=0.1,
                        system="You are a veterinary assistant. Provide helpful, professional responses about veterinary medicine.",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    
                    response_text = response.content[0].text
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                    
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

