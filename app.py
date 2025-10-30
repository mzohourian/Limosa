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

# Professional Clinical Interface CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --medical-blue: #4A90E2;
    --medical-blue-light: #E8F4FD;
    --medical-blue-dark: #2E5C8A;
    --snowy-white: #FEFEFE;
    --text-primary: #1a1a1a;
    --text-secondary: #6b6b6b;
    --border-light: #e5e5e5;
    --shadow-light: rgba(74, 144, 226, 0.1);
}

/* Global Layout - Claude Style */
.main .block-container {
    padding: 2rem;
    max-width: 800px;
    margin: 0 auto;
    background: var(--snowy-white);
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}
.stDecoration {display: none;}

/* Claude-style Header */
.claude-header {
    text-align: center;
    padding: 2rem 0 3rem 0;
    background: var(--snowy-white);
    border-bottom: 1px solid var(--border-light);
    margin-bottom: 2rem;
}

.claude-logo {
    width: 120px;
    height: 120px;
    margin: 0 auto 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.claude-logo img {
    width: 100px;
    height: 100px;
}

.claude-title {
    font-family: 'Inter', sans-serif;
    font-size: 2rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0 0 0.5rem 0;
}

.claude-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    font-weight: 400;
    color: var(--text-secondary);
    margin: 0;
}

/* Claude-style Chat Interface */
.claude-chat {
    background: var(--snowy-white);
    margin-bottom: 6rem;
}

/* Messages */
.stChatMessage {
    background: transparent;
    border: none;
    padding: 1.5rem;
    border-bottom: 1px solid var(--clinical-border);
}

.stChatMessage:last-child {
    border-bottom: none;
}

/* Chat Input */
div[data-testid="stChatInput"] {
    background: white;
    border-top: 1px solid var(--clinical-border);
    padding: 1rem 1.5rem;
}

/* Typography */
body, .main, div {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--clinical-text);
    line-height: 1.6;
}

h1, h2, h3 {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    color: var(--clinical-text);
}

/* Responsive Design */
@media (max-width: 768px) {
    .clinical-header {
        padding: 2rem 1rem;
    }
    
    .clinical-main {
        padding: 2rem 1rem;
    }
    
    .clinical-title {
        font-size: 2rem;
    }
    
    .clinical-controls {
        flex-direction: column;
        align-items: center;
    }
}

/* Custom File Uploader Styling */
.stFileUploader {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: pointer;
}

.stFileUploader > div {
    height: 100%;
}

.stFileUploader > div > div {
    height: 100%;
    border: none !important;
    background: transparent !important;
}

/* Position file uploader over custom upload area */
.clinical-upload {
    position: relative;
    cursor: pointer;
}

/* Professional Select Boxes */
.stSelectbox > div > div {
    background: white;
    border: 1px solid var(--clinical-border);
    border-radius: 8px;
    font-family: 'Inter', sans-serif;
}

/* Claude-style Input Area */
.claude-input-container {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: var(--snowy-white);
    border-top: 1px solid var(--border-light);
    padding: 1.5rem;
    z-index: 1000;
}

.claude-input-wrapper {
    max-width: 800px;
    margin: 0 auto;
    position: relative;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.claude-upload-btn {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    border: 1px solid var(--border-light);
    background: var(--snowy-white);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 1.2rem;
    color: var(--text-secondary);
    transition: all 0.2s ease;
}

.claude-upload-btn:hover {
    background: var(--medical-blue-light);
    color: var(--medical-blue);
    border-color: var(--medical-blue);
}

.claude-mic-btn {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    border: 1px solid var(--border-light);
    background: var(--snowy-white);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 1.1rem;
    color: var(--text-secondary);
    transition: all 0.2s ease;
}

.claude-mic-btn:hover {
    background: var(--medical-blue-light);
    color: var(--medical-blue);
    border-color: var(--medical-blue);
}

/* Hide default chat input styling */
div[data-testid="stChatInput"] {
    display: none;
}

/* Professional Status Messages */
.stAlert {
    border-radius: 8px;
    border: none;
    box-shadow: 0 2px 10px var(--clinical-shadow);
}

.stSuccess {
    background: rgba(39, 174, 96, 0.1);
    color: var(--clinical-success);
}

.stError {
    background: rgba(231, 76, 60, 0.1);
    color: var(--clinical-error);
}

.stWarning {
    background: rgba(243, 156, 18, 0.1);
    color: var(--clinical-warning);
}
</style>
""", unsafe_allow_html=True)

# Professional Clinical Interface
# Read and encode logo
with open("limosa.png", "rb") as f:
    logo_data = f.read()
    logo_base64 = base64.b64encode(logo_data).decode()

# Claude-style Header
st.markdown(f"""
<div class="claude-header">
    <div class="claude-logo">
        <img src="data:image/png;base64,{logo_base64}" alt="Limosa Logo">
    </div>
    <h1 class="claude-title">Limosa</h1>
    <p class="claude-subtitle">Veterinary Assistant</p>
</div>
""", unsafe_allow_html=True)

# Initialize chat history (no initial message)
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Initialize defaults for file upload
species = "Unknown"
analysis_type = "General"
uploaded_file = None

# Claude-style Chat Interface
st.markdown('<div class="claude-chat">', unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.markdown('</div>', unsafe_allow_html=True)

# Claude-style Input Area with Upload and Mic buttons
st.markdown("""
<div class="claude-input-container">
    <div class="claude-input-wrapper">
        <div class="claude-upload-btn" title="Upload image">+</div>
        <div style="flex: 1;"></div>
        <div class="claude-mic-btn" title="Voice input">🎤</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Hidden file uploader
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="hidden", key="hidden_uploader")

# Display uploaded image if any
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", width=300)
    
    col1, col2 = st.columns(2)
    with col1:
        species = st.selectbox("Species", ["Unknown", "Canine", "Feline", "Equine"])
    with col2:
        analysis_type = st.selectbox("Analysis Type", ["General", "Radiographic", "Dermatological"])

# Professional Chat Input
if prompt := st.chat_input("Type your veterinary question here..."):
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

