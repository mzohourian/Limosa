import streamlit as st

st.title("🩺 Limosa - Basic Test")
st.write("If you can see this, Streamlit is working!")

st.write("## Environment Test")
import sys
st.write(f"Python version: {sys.version}")

try:
    import anthropic
    st.success("✅ anthropic imported")
except Exception as e:
    st.error(f"❌ anthropic: {e}")

try:
    import openai
    st.success("✅ openai imported")
except Exception as e:
    st.error(f"❌ openai: {e}")

try:
    import pinecone
    st.success("✅ pinecone imported")
except Exception as e:
    st.error(f"❌ pinecone: {e}")

st.write("## Secrets Test")
try:
    if "ANTHROPIC_API_KEY" in st.secrets:
        st.success("✅ ANTHROPIC_API_KEY available")
    else:
        st.error("❌ ANTHROPIC_API_KEY missing")
except Exception as e:
    st.error(f"❌ Secrets error: {e}")

st.write("✅ **Basic app is working!**")