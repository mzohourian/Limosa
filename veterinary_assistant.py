#!/usr/bin/env python3
"""
Professional Veterinary AI Assistant - Standalone Web Application
Claude-inspired minimal design for veterinary image analysis and consultation
"""

import streamlit as st
import os
import json
import base64
import time
from typing import Dict, List, Any, Optional
from pathlib import Path
import anthropic
from dotenv import load_dotenv
from datetime import datetime
from PIL import Image
import io

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="Limosa - Veterinary AI Assistant",
    page_icon="🦆",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Limosa - AI-Powered Veterinary Diagnostics for Modern Clinics"
    }
)

class VeterinaryAIAssistant:
    """Professional Veterinary AI Assistant with Claude-style interface"""
    
    def __init__(self):
        self.anthropic_client = None
        self.initialize_ai_client()
        self.setup_custom_css()
        
    def initialize_ai_client(self):
        """Initialize Anthropic AI client"""
        # Try to get API key from Streamlit secrets first, then environment
        api_key = None
        
        # Check Streamlit secrets (for Streamlit Cloud)
        try:
            api_key = st.secrets["ANTHROPIC_API_KEY"]
        except:
            # Fallback to environment variable (for local development)
            api_key = os.getenv('ANTHROPIC_API_KEY')
        
        if api_key:
            self.anthropic_client = anthropic.Anthropic(api_key=api_key)
        else:
            st.error("⚠️ API key not configured. Please set ANTHROPIC_API_KEY in Streamlit secrets or environment variables.")
    
    def setup_custom_css(self):
        """Apply Claude-inspired professional styling"""
        st.markdown("""
        <style>
        /* Claude-inspired color scheme with veterinary theme */
        :root {
            --primary-color: #2E7D32;        /* Forest Green */
            --secondary-color: #4CAF50;      /* Light Green */
            --accent-color: #FF7043;         /* Orange accent */
            --background: #FAFAFA;           /* Light gray background */
            --surface: #FFFFFF;              /* White surfaces */
            --text-primary: #212121;         /* Dark gray text */
            --text-secondary: #757575;       /* Medium gray text */
            --border: #E0E0E0;              /* Light border */
            --success: #4CAF50;             /* Success green */
            --warning: #FF9800;             /* Warning orange */
            --error: #F44336;               /* Error red */
        }
        
        /* Main container styling */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        
        /* Header styling */
        .vet-header {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 4px 20px rgba(46, 125, 50, 0.15);
        }
        
        .vet-title {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }
        
        .vet-subtitle {
            font-size: 1.1rem;
            opacity: 0.9;
            font-weight: 400;
        }
        
        /* Chat interface styling */
        .chat-container {
            background: var(--surface);
            border-radius: 12px;
            border: 1px solid var(--border);
            min-height: 500px;
            margin-bottom: 1rem;
            overflow: hidden;
        }
        
        .chat-header {
            background: var(--background);
            padding: 1rem 1.5rem;
            border-bottom: 1px solid var(--border);
            font-weight: 600;
            color: var(--text-primary);
        }
        
        .chat-messages {
            padding: 1rem;
            max-height: 400px;
            overflow-y: auto;
        }
        
        /* Message styling */
        .message {
            margin-bottom: 1rem;
            padding: 1rem;
            border-radius: 8px;
            max-width: 80%;
        }
        
        .message.user {
            background: var(--primary-color);
            color: white;
            margin-left: auto;
        }
        
        .message.assistant {
            background: var(--background);
            color: var(--text-primary);
            border: 1px solid var(--border);
        }
        
        /* Upload area styling */
        .upload-area {
            background: var(--surface);
            border: 2px dashed var(--border);
            border-radius: 12px;
            padding: 2rem;
            text-align: center;
            margin: 1rem 0;
            transition: all 0.3s ease;
        }
        
        .upload-area:hover {
            border-color: var(--secondary-color);
            background: rgba(76, 175, 80, 0.02);
        }
        
        /* Button styling */
        .stButton > button {
            background: var(--primary-color);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .stButton > button:hover {
            background: var(--secondary-color);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(46, 125, 50, 0.3);
        }
        
        /* Analysis results styling */
        .analysis-result {
            background: var(--surface);
            border-radius: 12px;
            border: 1px solid var(--border);
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }
        
        .analysis-header {
            color: var(--primary-color);
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        /* Image preview styling */
        .image-preview {
            border-radius: 8px;
            border: 1px solid var(--border);
            overflow: hidden;
            margin: 1rem 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        /* Professional badges */
        .professional-badge {
            background: var(--accent-color);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 16px;
            font-size: 0.85rem;
            font-weight: 500;
            display: inline-block;
            margin: 0.2rem;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--background);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--border);
            border-radius: 3px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--text-secondary);
        }
        </style>
        """, unsafe_allow_html=True)
    
    def render_header(self):
        """Render professional header"""
        st.markdown("""
        <div class="vet-header">
            <div class="vet-title">🦆 Limosa</div>
            <div class="vet-subtitle">AI-Powered Veterinary Diagnostics • Empowering Modern Veterinary Clinics • Instant Image Analysis</div>
        </div>
        """, unsafe_allow_html=True)
    
    def validate_veterinary_image(self, uploaded_file) -> bool:
        """Validate uploaded veterinary image"""
        if uploaded_file is None:
            return False
        
        # Check file size (max 20MB for medical images)
        if uploaded_file.size > 20 * 1024 * 1024:
            st.error("🏥 Image file too large. Please upload images smaller than 20MB.")
            return False
        
        # Check file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/tiff', 'image/bmp']
        if uploaded_file.type not in allowed_types:
            st.error("🏥 Unsupported image format. Please upload JPEG, PNG, WebP, TIFF, or BMP images.")
            return False
        
        # Advanced validation
        try:
            uploaded_file.seek(0)
            with Image.open(uploaded_file) as img:
                width, height = img.size
                
                if width < 100 or height < 100:
                    st.error("🏥 Image resolution too low for clinical analysis. Please use higher resolution images.")
                    return False
                
                if width > 10000 or height > 10000:
                    st.warning("⚠️ Very high resolution image. Processing may take longer.")
                
                if width < 500 or height < 500:
                    st.warning("⚠️ Low resolution detected. For best analysis, use images ≥500x500 pixels.")
        
        except Exception as e:
            st.error(f"🏥 Invalid image file: {str(e)}")
            return False
        finally:
            uploaded_file.seek(0)
        
        return True
    
    def encode_image_to_base64(self, uploaded_file) -> str:
        """Convert uploaded image to base64"""
        try:
            uploaded_file.seek(0)
            image_bytes = uploaded_file.read()
            return base64.b64encode(image_bytes).decode('utf-8')
        except Exception as e:
            st.error(f"Error encoding image: {str(e)}")
            return None
        finally:
            uploaded_file.seek(0)
    
    def analyze_veterinary_image(self, query: str, image_data: str, analysis_context: Dict) -> str:
        """Analyze veterinary image using Claude 3.5 Haiku"""
        try:
            if not self.anthropic_client:
                return "⚠️ AI service not available. Please check configuration."
            
            # Build professional veterinary prompt
            system_prompt = self.build_veterinary_prompt(analysis_context)
            user_prompt = f"""Please analyze this veterinary image with the following context:

**Analysis Focus:** {analysis_context.get('focus', 'General veterinary assessment')}
**Species:** {analysis_context.get('species', 'Unknown')}
**Clinical Context:** {analysis_context.get('clinical_notes', 'None provided')}

**User Question:** {query}

Please provide a comprehensive veterinary analysis following professional guidelines."""
            
            # Detect image format
            try:
                decoded_data = base64.b64decode(image_data)
                image_format = "image/jpeg"  # Default
                
                if decoded_data.startswith(b'\\x89PNG'):
                    image_format = "image/png"
                elif decoded_data.startswith(b'\\xff\\xd8\\xff'):
                    image_format = "image/jpeg"
                elif decoded_data.startswith(b'RIFF') and b'WEBP' in decoded_data[:12]:
                    image_format = "image/webp"
            except:
                image_format = "image/jpeg"
            
            # Call Claude for analysis
            start_time = datetime.now()
            
            response = self.anthropic_client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=2000,
                temperature=0.1,
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": image_format,
                                "data": image_data
                            }
                        }
                    ]
                }]
            )
            
            end_time = datetime.now()
            analysis_time = (end_time - start_time).total_seconds()
            
            # Format professional response
            analysis_text = response.content[0].text
            return self.format_professional_response(analysis_text, analysis_context, analysis_time)
            
        except Exception as e:
            error_msg = str(e)
            if "not_found_error" in error_msg or "404" in error_msg:
                return "⚠️ **AI Model Temporarily Unavailable**\\n\\nThe analysis service is currently updating. Please try again in a few moments."
            elif "rate_limit" in error_msg.lower():
                return "⚠️ **Service Busy**\\n\\nHigh demand detected. Please wait a moment and try again."
            else:
                return f"⚠️ **Analysis Error**\\n\\nUnable to process the image: {error_msg}"
    
    def build_veterinary_prompt(self, context: Dict) -> str:
        """Build professional veterinary analysis prompt"""
        focus = context.get('focus', 'General veterinary assessment')
        species = context.get('species', 'Unknown')
        
        base_prompt = f"""You are a highly experienced veterinary radiologist and clinical diagnostician specializing in {species.lower()} medicine with expertise in:

- Veterinary radiology and diagnostic imaging
- Clinical pathology and laboratory medicine  
- Emergency and critical care medicine
- Anatomical and physiological assessment

ANALYSIS FOCUS: {focus}

PROFESSIONAL GUIDELINES:
1. Provide detailed, clinically relevant observations
2. Use systematic approach: Observation → Assessment → Recommendations
3. Include differential diagnoses when appropriate
4. Maintain professional medical terminology
5. Note limitations of image-based assessment

RESPONSE FORMAT:
- **Clinical Observations**: Detailed findings
- **Professional Assessment**: Medical interpretation
- **Recommendations**: Next steps or considerations
- **Limitations**: Acknowledge assessment boundaries

Always conclude with appropriate medical disclaimer."""
        
        return base_prompt
    
    def format_professional_response(self, analysis: str, context: Dict, response_time: float) -> str:
        """Format analysis in professional presentation"""
        focus = context.get('focus', 'General veterinary assessment')
        species = context.get('species', 'Unknown')
        
        response = f"""
<div class="analysis-result">
<div class="analysis-header">
🩺 Professional Veterinary Analysis
</div>

**📋 Analysis Type:** {focus}  
**🐾 Species:** {species}  
**⏱️ Analysis Time:** {response_time:.2f}s  
**🔬 AI Model:** Claude 3.5 Haiku Vision

---

{analysis}

---

**🦆 Powered by Limosa** - AI-driven veterinary diagnostics for modern clinics  
**⚠️ Professional Disclaimer:** This analysis supports clinical decision-making but does not replace professional veterinary examination and clinical correlation.
</div>
"""
        return response
    
    def render_demo_banner(self):
        """Render MVP demo banner"""
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FF7043, #FFB74D); color: white; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem; text-align: center;">
            <strong>🚀 MVP Demo</strong> • Experience AI-powered veterinary diagnostics • Designed for modern veterinary clinics
        </div>
        """, unsafe_allow_html=True)
    
    def render_main_interface(self):
        """Render the main chat and analysis interface"""
        # Initialize session state
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
            # Add welcome message
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': """Welcome to **Limosa**! 🦆 

I'm your AI-powered veterinary diagnostic assistant, designed specifically for modern veterinary clinics.

**What I can help with:**
- 🔬 **X-ray Analysis** - Upload radiographs for instant interpretation
- 📸 **Clinical Photos** - Analyze skin conditions, wounds, and abnormalities  
- 🔬 **Microscopy** - Evaluate cytology and histopathology images
- 🩺 **General Consultation** - Answer veterinary questions and provide guidance

**For the best analysis:**
1. Upload your veterinary image
2. Select the appropriate species and analysis focus
3. Add any relevant clinical notes
4. Ask your specific question

Ready to revolutionize your diagnostic workflow? Upload an image and let's get started! 💫"""
            })
        
        # Create main layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            st.markdown('<div class="chat-header">💬 Veterinary Consultation</div>', unsafe_allow_html=True)
            
            # Display chat history
            chat_container = st.container()
            with chat_container:
                for message in st.session_state.chat_history:
                    if message['role'] == 'user':
                        st.markdown(f"""
                        <div class="message user">
                            <strong>You:</strong> {message['content']}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="message assistant">
                            <strong>Limosa:</strong><br>
                            {message['content']}
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Chat input
            user_query = st.chat_input("Ask about veterinary cases, upload images for analysis...")
        
        with col2:
            st.markdown("### 📸 Image Analysis")
            
            # Image upload
            uploaded_file = st.file_uploader(
                "Upload veterinary image",
                type=['png', 'jpg', 'jpeg', 'webp', 'tiff', 'bmp'],
                help="X-rays, clinical photos, microscopy, ultrasounds"
            )
            
            # Analysis options
            if uploaded_file:
                st.markdown("**📋 Analysis Options**")
                
                analysis_focus = st.selectbox(
                    "Analysis Focus:",
                    ["General assessment", "Radiographic interpretation", "Dermatological evaluation", 
                     "Emergency findings", "Surgical assessment", "Microscopic examination"]
                )
                
                species = st.selectbox(
                    "Species:",
                    ["Unknown", "Canine (Dog)", "Feline (Cat)", "Equine (Horse)", 
                     "Bovine (Cattle)", "Small mammals", "Exotic/Wildlife"]
                )
                
                clinical_notes = st.text_area(
                    "Clinical Notes:",
                    placeholder="Patient history, symptoms, concerns...",
                    height=100
                )
                
                # Image preview
                if self.validate_veterinary_image(uploaded_file):
                    st.markdown('<div class="image-preview">', unsafe_allow_html=True)
                    st.image(uploaded_file, caption=f"📋 {uploaded_file.name}", use_column_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
        
        # Process user query
        if user_query:
            # Add user message
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_query
            })
            
            # Generate response
            if uploaded_file and self.validate_veterinary_image(uploaded_file):
                # Image analysis
                image_data = self.encode_image_to_base64(uploaded_file)
                if image_data:
                    analysis_context = {
                        'focus': analysis_focus,
                        'species': species,
                        'clinical_notes': clinical_notes
                    }
                    
                    with st.spinner("🔬 Analyzing veterinary image..."):
                        response = self.analyze_veterinary_image(user_query, image_data, analysis_context)
                    
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': response
                    })
            else:
                # Text-only consultation
                response = "I'm ready to help with veterinary questions. For image analysis, please upload a veterinary image (X-ray, clinical photo, etc.) and I'll provide detailed professional analysis."
                
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': response
                })
            
            st.rerun()
    
    def render_footer(self):
        """Render professional footer"""
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

def main():
    """Main application entry point"""
    app = VeterinaryAIAssistant()
    
    # Render application
    app.render_header()
    app.render_demo_banner()
    app.render_main_interface() 
    app.render_footer()

if __name__ == "__main__":
    main()