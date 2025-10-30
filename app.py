import streamlit as st
import anthropic
import base64
from PIL import Image
import io
import os
import sys

# Add current directory and subdirectories to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'comprehensive_veterinary_drugs_database', 'production_code'))

# Import Enhanced Veterinary Assistant v4.0 system
COMPREHENSIVE_SYSTEM_AVAILABLE = False

try:
    from enhanced_veterinary_assistant_v4 import EnhancedVeterinaryAssistantV4
    COMPREHENSIVE_SYSTEM_AVAILABLE = True
    print("✅ Enhanced Veterinary Assistant v4.0 loaded successfully!")
    print("   💉 CRI Calculation Engine")
    print("   🧠 Principle-Based Knowledge Retrieval")
    print("   🧬 Pharmacological Reasoning Engine") 
    print("   🧮 Mathematical Calculation Validation")
    print("   📚 Complete Knowledge Base (5,039 chunks)")
except ImportError as e:
    print(f"⚠️ Enhanced Veterinary Assistant v4.0 not available: {e}")
    COMPREHENSIVE_SYSTEM_AVAILABLE = False

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

# Initialize Enhanced Veterinary Assistant v4.0 (single initialization)
enhanced_vet_assistant = None

if COMPREHENSIVE_SYSTEM_AVAILABLE:
    try:
        # Set environment variables for all systems
        if "ANTHROPIC_API_KEY" in st.secrets:
            os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]
        if "OPENAI_API_KEY" in st.secrets:
            os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
        if "PINECONE_API_KEY" in st.secrets:
            os.environ["PINECONE_API_KEY"] = st.secrets["PINECONE_API_KEY"]
        
        # Single initialization of Enhanced Veterinary Assistant v4.0
        print("🔄 Initializing Enhanced Veterinary Assistant v4.0...")
        enhanced_vet_assistant = EnhancedVeterinaryAssistantV4()
        print("✅ Enhanced Veterinary Assistant v4.0 initialized successfully!")
        
    except Exception as e:
        print(f"⚠️ Failed to initialize Enhanced Veterinary Assistant v4.0: {e}")
        enhanced_vet_assistant = None

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

# Header with Enhanced Veterinary Assistant v4.0 status
if enhanced_vet_assistant:
    kb_status = "🎯 **Enhanced Veterinary Assistant v4.0 Active**<br/>💉 CRI Engine | 🧠 Principle Retrieval | 🧬 Pharma Reasoning | 🧮 Math Validation | 📚 5,039 Chunks"
else:
    kb_status = "⚠️ Basic Knowledge Only (Enhanced v4.0 System Unavailable)"

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
            with st.spinner("🔍 Processing with Enhanced Veterinary Assistant v4.0..."):
                try:
                    if enhanced_vet_assistant and COMPREHENSIVE_SYSTEM_AVAILABLE:
                        # Use Enhanced Veterinary Assistant v4.0 with all engines
                        print(f"🎯 Using Enhanced Veterinary Assistant v4.0 for query: {prompt[:50]}...")
                        
                        # Query using comprehensive safety v4 method
                        v4_response = enhanced_vet_assistant.query_with_comprehensive_safety_v4(prompt)
                        
                        if v4_response and 'answer' in v4_response:
                            response_text = v4_response['answer']
                            
                            # Add system metadata and capabilities used
                            metadata_lines = []
                            
                            # Confidence and grounding
                            if 'confidence' in v4_response:
                                confidence = v4_response['confidence']
                                metadata_lines.append(f"🎯 **Confidence:** {confidence:.1%}")
                            
                            if 'grounding_score' in v4_response:
                                grounding = v4_response['grounding_score']
                                metadata_lines.append(f"📚 **Knowledge Base Grounding:** {grounding:.1f}%")
                            
                            # Safety features activated
                            safety = v4_response.get('safety_analysis', {})
                            activated_features = []
                            if safety.get('cri_engine_override'):
                                activated_features.append("💉 CRI Calculation Engine")
                            if safety.get('principle_based_retrieval_performed'):
                                activated_features.append("🧠 Principle-Based Retrieval")
                            if safety.get('interaction_analysis_performed'):
                                activated_features.append("🧬 Drug Interaction Analysis")
                            if safety.get('calculation_validation_performed'):
                                activated_features.append("🧮 Mathematical Validation")
                            
                            if activated_features:
                                metadata_lines.append("**Safety Systems Activated:** " + " | ".join(activated_features))
                            
                            # CRI calculation results
                            cri_calc = v4_response.get('cri_calculation', {})
                            if cri_calc and cri_calc.get('performed'):
                                metadata_lines.append(f"💉 **CRI Calculation:** Total runtime {cri_calc.get('total_run_time_hours', 0):.1f} hours")
                            
                            # Add metadata if available
                            if metadata_lines:
                                response_text += f"\n\n---\n**📊 System Analysis:**\n" + "\n".join(metadata_lines)
                                
                            # Add professional disclaimer
                            response_text += f"\n\n✅ **Enhanced Veterinary Assistant v4.0** - Based on comprehensive veterinary knowledge base with mathematical validation and safety analysis."
                            
                        else:
                            response_text = "I'm having trouble accessing the Enhanced Veterinary Assistant v4.0 system. Let me provide a basic response."
                    else:
                        # Fallback to enhanced Claude system if v4.0 unavailable
                        print("⚠️ Using fallback Claude system (Enhanced v4.0 not available)")
                        
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
                        response_text += "\n\n*Note: Response based on Claude's general veterinary knowledge (Enhanced v4.0 system not available)*"
                    
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                    
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})