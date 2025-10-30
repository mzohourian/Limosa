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
    --clinical-primary: #0f4c75;
    --clinical-secondary: #3282b8;
    --clinical-accent: #bbe1fa;
    --clinical-success: #27ae60;
    --clinical-warning: #f39c12;
    --clinical-error: #e74c3c;
    --clinical-text: #2c3e50;
    --clinical-text-light: #7f8c8d;
    --clinical-bg: #ffffff;
    --clinical-bg-light: #f8f9fa;
    --clinical-border: #e9ecef;
    --clinical-shadow: rgba(15, 76, 117, 0.08);
}

/* Global Layout */
.main .block-container {
    padding: 0;
    max-width: 1200px;
    margin: 0 auto;
    background: var(--clinical-bg);
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}
.stDecoration {display: none;}

/* Professional Header */
.clinical-header {
    background: linear-gradient(135deg, var(--clinical-primary) 0%, var(--clinical-secondary) 100%);
    padding: 3rem 2rem;
    text-align: center;
    color: white;
    margin-bottom: 0;
    box-shadow: 0 4px 20px var(--clinical-shadow);
}

.clinical-logo {
    width: 80px;
    height: 80px;
    margin: 0 auto 1.5rem;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.clinical-logo img {
    width: 50px;
    height: 50px;
    filter: brightness(1.2) contrast(1.1);
}

.clinical-title {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0;
    letter-spacing: -0.02em;
}

.clinical-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 1.1rem;
    font-weight: 400;
    opacity: 0.9;
    margin-top: 0.5rem;
}

/* Main Content Area */
.clinical-main {
    padding: 3rem 2rem;
    background: var(--clinical-bg);
}

/* Professional File Upload */
.clinical-upload {
    background: var(--clinical-bg-light);
    border: 2px dashed var(--clinical-border);
    border-radius: 16px;
    padding: 3rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    transition: all 0.3s ease;
}

.clinical-upload:hover {
    border-color: var(--clinical-secondary);
    background: rgba(50, 130, 184, 0.02);
}

.clinical-upload-icon {
    width: 60px;
    height: 60px;
    background: var(--clinical-accent);
    border-radius: 50%;
    margin: 0 auto 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    color: var(--clinical-primary);
}

/* Professional Controls */
.clinical-controls {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    justify-content: center;
}

.clinical-select {
    background: white;
    border: 1px solid var(--clinical-border);
    border-radius: 8px;
    padding: 0.75rem 1rem;
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    color: var(--clinical-text);
    min-width: 150px;
}

/* Chat Interface */
.clinical-chat {
    background: white;
    border-radius: 16px;
    box-shadow: 0 2px 20px var(--clinical-shadow);
    margin-bottom: 2rem;
    overflow: hidden;
}

.clinical-chat-header {
    background: var(--clinical-bg-light);
    padding: 1rem 1.5rem;
    border-bottom: 1px solid var(--clinical-border);
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    color: var(--clinical-text);
    font-size: 0.9rem;
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

/* Chat Input Styling */
div[data-testid="stChatInput"] {
    background: white;
    border: 1px solid var(--clinical-border);
    border-radius: 12px;
    margin: 2rem;
    box-shadow: 0 2px 10px var(--clinical-shadow);
}

div[data-testid="stChatInput"] > div {
    border: none;
    background: transparent;
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

# Professional Header
st.markdown(f"""
<div class="clinical-header">
    <div class="clinical-logo">
        <img src="data:image/png;base64,{logo_base64}" alt="Limosa Logo">
    </div>
    <h1 class="clinical-title">Limosa</h1>
    <p class="clinical-subtitle">AI-Powered Veterinary Diagnostics</p>
</div>
""", unsafe_allow_html=True)

# Main Content Container
st.markdown('<div class="clinical-main">', unsafe_allow_html=True)

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = [{
        'role': 'assistant',
        'content': "Welcome to Limosa. I'm an AI assistant specialized in veterinary diagnostics. Upload medical images for analysis or ask me any veterinary questions."
    }]

# Professional File Upload Section
st.markdown("""
<div class="clinical-upload">
    <div class="clinical-upload-icon">📋</div>
    <h3 style="margin: 0 0 0.5rem 0; color: var(--clinical-text);">Upload Veterinary Image</h3>
    <p style="margin: 0; color: var(--clinical-text-light); font-size: 0.9rem;">
        Drag and drop your X-rays, clinical photos, or diagnostic images here
    </p>
</div>
""", unsafe_allow_html=True)

# Hidden file uploader (styled with CSS)
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="hidden")

# Initialize defaults
species = "Unknown"
analysis_type = "General"

# Professional Controls (when file is uploaded)
if uploaded_file:
    # Display uploaded image professionally
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    
    # Professional controls
    st.markdown("""
    <div class="clinical-controls">
        <div style="text-align: center;">
            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500; color: var(--clinical-text);">Species</label>
        </div>
        <div style="text-align: center;">
            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500; color: var(--clinical-text);">Analysis Focus</label>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        species = st.selectbox("", ["Unknown", "Canine", "Feline", "Equine"], key="species")
    with col2:
        analysis_type = st.selectbox("", ["General", "Radiographic", "Dermatological"], key="analysis")

# Professional Chat Interface
st.markdown("""
<div class="clinical-chat">
    <div class="clinical-chat-header">
        🩺 Veterinary Consultation
    </div>
""", unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.markdown('</div>', unsafe_allow_html=True)  # Close chat container

# Close main content container
st.markdown('</div>', unsafe_allow_html=True)

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

