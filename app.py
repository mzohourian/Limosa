import streamlit as st
import anthropic
import base64
from PIL import Image
import io

# Configure page
st.set_page_config(
    page_title="Limosa - Veterinary AI Assistant",
    page_icon="🦆",
    layout="wide"
)

# Get API key from secrets
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    client = anthropic.Anthropic(api_key=api_key)
except:
    st.error("API key not configured")
    st.stop()

# Custom CSS
st.markdown("""
<style>
.main .block-container {
    padding-top: 2rem;
    max-width: 1200px;
}
.vet-header {
    background: linear-gradient(135deg, #2E7D32, #4CAF50);
    color: white;
    padding: 2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    text-align: center;
}
.vet-title {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}
.vet-subtitle {
    font-size: 1.1rem;
    opacity: 0.9;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="vet-header">
    <div class="vet-title">🦆 Limosa</div>
    <div class="vet-subtitle">AI-Powered Veterinary Diagnostics • Empowering Modern Veterinary Clinics</div>
</div>
""", unsafe_allow_html=True)

# Demo banner
st.markdown("""
<div style="background: linear-gradient(135deg, #FF7043, #FFB74D); color: white; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem; text-align: center;">
    <strong>🚀 MVP Demo</strong> • Experience AI-powered veterinary diagnostics • Designed for modern veterinary clinics
</div>
""", unsafe_allow_html=True)

# Main interface
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 💬 Veterinary Consultation")
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = [{
            'role': 'assistant',
            'content': """Welcome to **Limosa**! 🦆 

I'm your AI-powered veterinary diagnostic assistant, designed specifically for modern veterinary clinics.

**What I can help with:**
- 🔬 **X-ray Analysis** - Upload radiographs for instant interpretation
- 📸 **Clinical Photos** - Analyze skin conditions, wounds, and abnormalities  
- 🩺 **General Consultation** - Answer veterinary questions and provide guidance

Ready to revolutionize your diagnostic workflow? Upload an image and let's get started! 💫"""
        }]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

with col2:
    st.markdown("### 📸 Image Analysis")
    
    uploaded_file = st.file_uploader(
        "Upload veterinary image",
        type=['png', 'jpg', 'jpeg'],
        help="X-rays, clinical photos, etc."
    )
    
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        species = st.selectbox(
            "Species:",
            ["Unknown", "Canine (Dog)", "Feline (Cat)", "Equine (Horse)"]
        )
        
        analysis_type = st.selectbox(
            "Analysis Focus:",
            ["General assessment", "Radiographic interpretation", "Dermatological evaluation"]
        )

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
                    formatted_response = f"""🩺 **Professional Veterinary Analysis**

**Species:** {species}  
**Analysis Type:** {analysis_type}

{analysis}

---
**🦆 Powered by Limosa** - AI-driven veterinary diagnostics for modern clinics  
**⚠️ Professional Disclaimer:** This analysis supports clinical decision-making but does not replace professional veterinary examination."""
                    
                    st.markdown(formatted_response)
                    st.session_state.messages.append({"role": "assistant", "content": formatted_response})
                    
                except Exception as e:
                    error_msg = f"⚠️ Analysis error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
        else:
            response_text = "I'm ready to help with veterinary questions. For image analysis, please upload a veterinary image and I'll provide detailed professional analysis."
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🦆 Limosa**")
    st.markdown("AI-powered veterinary diagnostics")

with col2:
    st.markdown("**🏥 For Veterinary Clinics**")
    st.markdown("Enhancing diagnostic capabilities")

with col3:
    st.markdown("**💡 MVP Demo**")
    st.markdown("Experience the future of veterinary AI")