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

/* Logo styling */
.logo-container {
    text-align: center;
    margin-bottom: 2rem;
}

/* Remove gray background from images */
.main img {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

div[data-testid="stImage"] > img {
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# Header with logo
# Read and encode logo
with open("limosa.png", "rb") as f:
    logo_data = f.read()
    logo_base64 = base64.b64encode(logo_data).decode()

st.markdown(f"""
<div class="logo-container" style="text-align: center; margin-bottom: 2rem;">
    <img src="data:image/png;base64,{logo_base64}" 
         style="width: 100px; height: auto; background: transparent !important; border: none !important;">
    <h1 style="margin-top: 1rem; margin-bottom: 0; font-size: 1.5rem; font-weight: 500; color: #1a1a1a;">Limosa</h1>
</div>
""", unsafe_allow_html=True)

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = [{
        'role': 'assistant',
        'content': "I'm an AI assistant specialized in veterinary diagnostics. Upload an image and ask me about it, or ask me any veterinary questions."
    }]

# File upload section
uploaded_file = st.file_uploader("Upload veterinary image", type=['png', 'jpg', 'jpeg'])

# Initialize defaults
species = "Unknown"
analysis_type = "General"

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
                    
                    # Enhanced veterinary image analysis system prompt
                    image_system = f"""You are an expert veterinary radiologist and diagnostician analyzing a {species} image with {analysis_type} focus.

ANALYSIS FRAMEWORK:
• Technical Quality: Image positioning, exposure, artifacts
• Anatomical Structures: Normal vs. abnormal findings
• Pathological Changes: Detailed description of abnormalities
• Differential Diagnosis: List most likely conditions
• Clinical Significance: Immediate vs. follow-up concerns
• Recommendations: Additional imaging, treatment, monitoring

SPECIES-SPECIFIC CONSIDERATIONS:
- {species}-specific normal anatomical variations
- Common conditions in {species}
- Age-related changes expected
- Emergency conditions requiring immediate intervention

FOCUS AREAS for {analysis_type}:
{"• Radiographic: Bone density, joint spaces, soft tissue contrast, organ silhouettes, gas patterns" if analysis_type == "Radiographic" else ""}
{"• Dermatological: Lesion morphology, distribution, secondary changes, differential patterns" if analysis_type == "Dermatological" else ""}
{"• General: Overall assessment with emphasis on most significant findings" if analysis_type == "General" else ""}

Provide structured, professional analysis suitable for veterinary case records."""
                    
                    # Call Claude
                    response = client.messages.create(
                        model="claude-3-5-haiku-20241022",
                        max_tokens=2000,
                        temperature=0.1,
                        system=image_system,
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": f"Please provide detailed veterinary analysis: {prompt}"},
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
                    # Enhanced veterinary system prompt with built-in knowledge
                    veterinary_system = """You are an expert veterinary diagnostician with comprehensive knowledge of:

• Veterinary pharmacology and drug dosages
• Emergency medicine (GDV/bloat, shock, trauma)
• Diagnostic imaging (X-rays, ultrasound)
• Clinical pathology and laboratory values
• Surgical procedures and techniques
• Species-specific conditions (canine, feline, equine)
• Infectious diseases and parasitology
• Toxicology and poisoning management

Provide professional, evidence-based veterinary advice. Always include:
- Specific dosage calculations when relevant
- Safety considerations and contraindications
- Emergency protocols when applicable
- Differential diagnosis considerations
- Appropriate follow-up recommendations

Use metric units (mg/kg) and provide ranges when appropriate. Always emphasize the need for hands-on examination and veterinary supervision."""
                    
                    response = client.messages.create(
                        model="claude-3-5-haiku-20241022",
                        max_tokens=1500,
                        temperature=0.1,
                        system=veterinary_system,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    
                    response_text = response.content[0].text
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                    
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

