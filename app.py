#!/usr/bin/env python3
"""
Limosa - Enhanced Veterinary Assistant v4.0 Web Interface
Simplified deployment version for diagnosing issues
"""

import streamlit as st
import os
import sys
import base64

# Configure page
st.set_page_config(
    page_title="Limosa",
    page_icon="🩺",
    layout="centered"
)

# Simple CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.main .block-container {
    padding: 0;
    max-width: 800px;
    margin: 0 auto;
    background: #FEFEFE;
}

body {
    background-color: #FEFEFE !important;
}

.limosa-header {
    text-align: center;
    padding: 3rem 2rem 2rem 2rem;
    background: #FEFEFE;
    border-bottom: 1px solid #e5e5e5;
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
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class="limosa-header">
    <h1 class="limosa-title">Limosa</h1>
    <p class="limosa-subtitle">Veterinary Assistant</p>
</div>
""", unsafe_allow_html=True)

# System status check
st.write("## 🔧 System Diagnostic")

# Check API keys
api_keys_status = {}
for key in ["ANTHROPIC_API_KEY", "OPENAI_API_KEY", "PINECONE_API_KEY"]:
    try:
        if key in st.secrets:
            api_keys_status[key] = "✅ Available"
        else:
            api_keys_status[key] = "❌ Missing"
    except:
        api_keys_status[key] = "❌ Secrets not accessible"

st.write("### API Keys Status:")
for key, status in api_keys_status.items():
    st.write(f"  **{key}**: {status}")

# Test Enhanced v4.0 import
st.write("### Enhanced Veterinary Assistant v4.0 Import Test:")

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'comprehensive_veterinary_drugs_database', 'production_code'))

try:
    st.write("🔄 Attempting to import Enhanced Veterinary Assistant v4.0...")
    from enhanced_veterinary_assistant_v4 import EnhancedVeterinaryAssistantV4
    st.success("✅ Enhanced Veterinary Assistant v4.0 imported successfully!")
    
    # Try to initialize
    try:
        st.write("🔄 Attempting to initialize Enhanced v4.0...")
        assistant = EnhancedVeterinaryAssistantV4()
        st.success("✅ Enhanced Veterinary Assistant v4.0 initialized successfully!")
        st.success("🎯 **System Ready** - Enhanced v4.0 with comprehensive knowledge base is active!")
        
        # Show test query option
        if st.button("🧪 Test with Cephalexin Query"):
            with st.spinner("Testing Enhanced v4.0..."):
                query = "What is the correct dose of cephalexin for a 24 kg Labrador with skin infection?"
                response = assistant.query_with_comprehensive_safety_v4(query)
                
                if response and 'answer' in response:
                    st.success(f"✅ Test successful! Confidence: {response.get('confidence', 0):.1%}")
                    st.write("**Response Preview:**")
                    st.write(response['answer'][:200] + "...")
                else:
                    st.error("❌ Test failed - no response generated")
        
    except Exception as e:
        st.error(f"❌ Enhanced v4.0 initialization failed: {e}")
        st.write(f"Error type: {type(e).__name__}")
        
except ImportError as e:
    st.error(f"❌ Import failed: {e}")
    st.write("**Missing module details:**")
    st.code(str(e))
except Exception as e:
    st.error(f"❌ Other error: {e}")
    st.write(f"Error type: {type(e).__name__}")

# Show file structure
st.write("### File Structure Check:")
if os.path.exists(current_dir):
    files = os.listdir(current_dir)
    st.write(f"**Current directory ({current_dir}) contains:**")
    for file in sorted(files):
        if file.endswith('.py') or file.endswith('.json') or os.path.isdir(os.path.join(current_dir, file)):
            st.write(f"  - {file}")

# Show comprehensive database status
db_path = os.path.join(current_dir, 'comprehensive_veterinary_drugs_database', 'production_code')
if os.path.exists(db_path):
    st.write(f"**Database directory ({db_path}) contains:**")
    db_files = os.listdir(db_path)
    for file in sorted(db_files):
        if file.endswith('.py') or file.endswith('.json'):
            st.write(f"  - {file}")
else:
    st.error("❌ Database directory not found!")

st.write("---")
st.write("**This diagnostic app helps identify why the Enhanced Veterinary Assistant v4.0 isn't loading on Streamlit Cloud.**")