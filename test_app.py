#!/usr/bin/env python3
"""
Minimal test version to diagnose deployment issues
"""

import streamlit as st
import sys
import os

st.set_page_config(page_title="Limosa Test", page_icon="🩺")

st.title("🩺 Limosa Deployment Test")

st.write("✅ Streamlit is working")

# Test basic imports
try:
    import anthropic
    st.write("✅ Anthropic library imported")
except Exception as e:
    st.error(f"❌ Anthropic import failed: {e}")

try:
    import openai
    st.write("✅ OpenAI library imported")
except Exception as e:
    st.error(f"❌ OpenAI import failed: {e}")

try:
    import pinecone
    st.write("✅ Pinecone library imported")
except Exception as e:
    st.error(f"❌ Pinecone import failed: {e}")

# Test path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
st.write(f"📁 Current directory: {current_dir}")

# Test Enhanced v4.0 import
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'comprehensive_veterinary_drugs_database', 'production_code'))

try:
    from enhanced_veterinary_assistant_v4 import EnhancedVeterinaryAssistantV4
    st.write("✅ Enhanced Veterinary Assistant v4.0 imported successfully")
except Exception as e:
    st.error(f"❌ Enhanced v4.0 import failed: {e}")
    st.code(str(e))

# Test API keys
api_keys_status = {}
for key in ["ANTHROPIC_API_KEY", "OPENAI_API_KEY", "PINECONE_API_KEY"]:
    try:
        if key in st.secrets:
            api_keys_status[key] = "✅ Available"
        else:
            api_keys_status[key] = "❌ Missing"
    except:
        api_keys_status[key] = "❌ Secrets not accessible"

st.write("🔑 API Keys Status:")
for key, status in api_keys_status.items():
    st.write(f"  {key}: {status}")

st.write("---")
st.write("**Next Steps:** Based on this test, we can identify what's preventing the main app from loading.")