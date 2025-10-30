import streamlit as st
import anthropic
import base64
from PIL import Image
import io
import os
import sys

# Add path to access comprehensive veterinary system
sys.path.append('..')
sys.path.append('../comprehensive_veterinary_drugs_database/production_code')

# Import comprehensive veterinary knowledge system
try:
    from comprehensive_veterinary_drugs_database.production_code.final_95_confidence_standalone import Final95ConfidenceAssistant
    KNOWLEDGE_BASE_AVAILABLE = True
    print("✅ Comprehensive veterinary knowledge base loaded successfully!")
except ImportError as e:
    print(f"⚠️ Knowledge base not available: {e}")
    KNOWLEDGE_BASE_AVAILABLE = False

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

# Initialize comprehensive veterinary knowledge base
@st.cache_resource
def initialize_veterinary_assistant():
    """Initialize the comprehensive veterinary assistant with knowledge base"""
    if KNOWLEDGE_BASE_AVAILABLE:
        try:
            # Set environment variables for the knowledge base
            if "ANTHROPIC_API_KEY" in st.secrets:
                os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]
            if "OPENAI_API_KEY" in st.secrets:
                os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
            if "PINECONE_API_KEY" in st.secrets:
                os.environ["PINECONE_API_KEY"] = st.secrets["PINECONE_API_KEY"]
            
            vet_assistant = Final95ConfidenceAssistant()
            return vet_assistant
        except Exception as e:
            print(f"⚠️ Failed to initialize knowledge base: {e}")
            return None
    return None

# Try to initialize the comprehensive system
vet_assistant = initialize_veterinary_assistant()

# Medical Blue and Snowy White CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global styles */
.main .block-container {
    padding: 0;
    max-width: 800px;
    margin: 0 auto;
    background: #FEFEFE;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

/* Body background */
body {
    background-color: #FEFEFE !important;
}

/* Header */
.limosa-header {
    text-align: center;
    padding: 3rem 2rem 2rem 2rem;
    background: #FEFEFE;
    border-bottom: 1px solid #e5e5e5;
}

.limosa-logo {
    width: 150px;
    height: 150px;
    margin: 0 auto 1.5rem auto;
    display: flex;
    align-items: center;
    justify-content: center;
}

.limosa-logo img {
    width: 140px;
    height: 140px;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* Force remove Streamlit image backgrounds */
div[data-testid="stImage"] {
    background: transparent !important;
}

div[data-testid="stImage"] > img {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

.limosa-title {
    font-family: 'Inter', sans-serif;
    font-size: 2.5rem;
    font-weight: 600;
    color: #1a1a1a;
    margin: 0 0 0.5rem 0;
}

.limosa-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 1.1rem;
    font-weight: 400;
    color: #6b6b6b;
    margin: 0;
}

/* Chat area */
.chat-container {
    padding: 2rem;
    background: #FEFEFE;
    min-height: 400px;
}

/* Chat messages */
.stChatMessage {
    background: transparent;
    padding: 1rem 0;
    border: none;
}

/* Input area styling */
.input-area {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #FEFEFE;
    border-top: 1px solid #e5e5e5;
    padding: 1.5rem;
    z-index: 1000;
}

.input-wrapper {
    max-width: 800px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: white;
    border: 1px solid #e5e5e5;
    border-radius: 12px;
    padding: 0.5rem;
    box-shadow: 0 2px 10px rgba(74, 144, 226, 0.1);
}

.upload-btn {
    width: 36px;
    height: 36px;
    background: white;
    border: 1px solid #e5e5e5;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 1.2rem;
    color: #6b6b6b;
    transition: all 0.2s ease;
}

.upload-btn:hover {
    background: #E8F4FD;
    border-color: #4A90E2;
    color: #4A90E2;
}

.mic-btn {
    width: 36px;
    height: 36px;
    background: white;
    border: 1px solid #e5e5e5;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 1rem;
    color: #6b6b6b;
    transition: all 0.2s ease;
}

.mic-btn:hover {
    background: #E8F4FD;
    border-color: #4A90E2;
    color: #4A90E2;
}

/* Chat input field - style the default Streamlit input */
div[data-testid="stChatInput"] {
    margin: 2rem;
    background: white;
    border: 1px solid #e5e5e5;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(74, 144, 226, 0.1);
}

div[data-testid="stChatInput"] > div {
    border: none;
    background: transparent;
}

div[data-testid="stChatInput"] input {
    padding-left: 3.5rem !important;
    padding-right: 3.5rem !important;
}

.stChatInputContainer {
    position: relative;
}

/* Add buttons to input area */
.stChatInputContainer::before {
    content: "+";
    position: absolute;
    left: 0.75rem;
    top: 50%;
    transform: translateY(-50%);
    width: 32px;
    height: 32px;
    background: white;
    border: 1px solid #e5e5e5;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 1.1rem;
    color: #6b6b6b;
    z-index: 10;
}

.stChatInputContainer::after {
    content: "🎤";
    position: absolute;
    right: 0.75rem;
    top: 50%;
    transform: translateY(-50%);
    width: 32px;
    height: 32px;
    background: white;
    border: 1px solid #e5e5e5;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 0.9rem;
    z-index: 10;
}

/* File uploader */
.stFileUploader {
    display: none;
}

/* Select boxes */
.stSelectbox {
    margin: 0.5rem 0;
}

/* Medical blue accents */
.medical-accent {
    color: #4A90E2;
}

/* Uploaded image styling */
.uploaded-image {
    text-align: center;
    margin: 1rem 0;
    padding: 1rem;
    background: #E8F4FD;
    border-radius: 12px;
    border: 1px solid #4A90E2;
}

</style>
""", unsafe_allow_html=True)

# Load and encode logo
with open("limosa.png", "rb") as f:
    logo_data = f.read()
    logo_base64 = base64.b64encode(logo_data).decode()

# Header with knowledge base status
kb_status = "🎯 **Comprehensive Knowledge Base Active** (Plumb, Ettinger, Veterinary Textbooks)" if vet_assistant else "⚠️ Basic Knowledge Only"

st.markdown(f"""
<div class="limosa-header">
    <div class="limosa-logo">
        <img src="data:image/png;base64,{logo_base64}" alt="Limosa Logo">
    </div>
    <h1 class="limosa-title">Limosa</h1>
    <p class="limosa-subtitle">Veterinary Assistant</p>
    <div style="margin-top: 1rem; font-size: 0.85rem; color: #4A90E2;">
        {kb_status}
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize chat history - NO INITIAL MESSAGE
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.markdown('</div>', unsafe_allow_html=True)

# File upload (hidden)
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="hidden", key="file_upload")

# Initialize defaults
species = "Unknown"
analysis_type = "General"

# Show uploaded image and controls if file is uploaded
if uploaded_file:
    st.markdown('<div class="uploaded-image">', unsafe_allow_html=True)
    st.image(uploaded_file, caption="Uploaded Image", width=400)
    
    col1, col2 = st.columns(2)
    with col1:
        species = st.selectbox("Species", ["Unknown", "Canine", "Feline", "Equine"])
    with col2:
        analysis_type = st.selectbox("Analysis Type", ["General", "Radiographic", "Dermatological"])
    
    st.markdown('</div>', unsafe_allow_html=True)

# Chat input (this creates the text box)
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
            with st.spinner("🔍 Searching comprehensive veterinary knowledge base..."):
                try:
                    if vet_assistant and KNOWLEDGE_BASE_AVAILABLE:
                        # Use comprehensive veterinary knowledge base with Pinecone + textbooks
                        print(f"🎯 Using comprehensive knowledge base for query: {prompt[:50]}...")
                        
                        # Query the comprehensive system
                        kb_response = vet_assistant.query_with_high_confidence(prompt)
                        
                        if kb_response and 'answer' in kb_response:
                            response_text = kb_response['answer']
                            
                            # Add knowledge base attribution
                            if 'sources' in kb_response and kb_response['sources']:
                                response_text += f"\n\n**📚 Sources from veterinary textbooks and databases**"
                            
                            # Add confidence indicator if available
                            if 'confidence' in kb_response:
                                confidence = kb_response['confidence']
                                if confidence > 0.9:
                                    response_text += f"\n\n✅ **High confidence response** (based on Plumb, Ettinger, and comprehensive veterinary databases)"
                                elif confidence > 0.7:
                                    response_text += f"\n\n⚠️ **Moderate confidence response** - consider additional consultation"
                        else:
                            # Fallback to basic response
                            response_text = "I'm having trouble accessing the comprehensive knowledge base. Let me provide a basic response."
                    else:
                        # Fallback to enhanced Claude system if knowledge base unavailable
                        print("⚠️ Using fallback Claude system (knowledge base not available)")
                        
                        veterinary_system = """You are an expert veterinary diagnostician with comprehensive knowledge of:

• Veterinary pharmacology and drug dosages (including Plumb's Veterinary Drug Handbook)
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
                        response_text += "\n\n*Note: Response based on Claude's general veterinary knowledge (comprehensive knowledge base not available)*"
                    
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                    
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})