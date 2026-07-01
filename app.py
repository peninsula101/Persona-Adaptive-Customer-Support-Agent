import streamlit as st
import json
from src.classifier import classify_customer_persona
from src.rag_pipeline import LocalRAGPipeline
from src.generator import generate_adaptive_response
import os
from src.rag_pipeline import build_database_from_folder

# --- Manual Database Override ---

if st.sidebar.button("🛠️ Force Rebuild Database"):
    with st.spinner("Rebuilding knowledge base..."):
        from src.rag_pipeline import build_database_from_folder
        build_database_from_folder()
        st.sidebar.success("Database Rebuilt! Please refresh the page.")
# --------------------------------

# --- Database Initialization ---
# When deployed, the chroma_db folder won't exist yet. This builds it automatically.
if not os.path.exists("chroma_db"):
    with st.spinner("First-time setup: Initializing Enterprise Knowledge Base..."):
        build_database_from_folder()

st.set_page_config(page_title="Persona-Adaptive Customer Support Agent", page_icon="🤖", layout="centered")
st.title("🤖 Persona-Adaptive Support Agent")
st.caption("Powered by Gemini, ChromaDB, and Retrieval-Augmented Generation")

@st.cache_resource
def load_database():
    return LocalRAGPipeline()

rag_db = load_database()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing request..."):
            
            persona_data = classify_customer_persona(prompt)
            detected_persona = persona_data.get("persona", "Unknown")
            
            context_chunks = rag_db.retrieve_context(prompt, top_k=3)
            
            final_output = generate_adaptive_response(prompt, detected_persona, context_chunks)
            
            with st.expander(f"🧠 Detected Persona: **{detected_persona}**", expanded=False):
                st.write("**Reasoning:**", persona_data.get("reasoning"))
                st.write("**Retrieved Sources:**")
                if context_chunks:
                    for chunk in context_chunks:
                        st.caption(f"📄 {chunk['source']} (Score: {chunk['score']:.2f})")
                else:
                    st.caption("No relevant documents found.")

            st.markdown(final_output["response"])
            
            if final_output.get("escalated"):
                st.error("🚨 **ESCALATION TRIGGERED: HUMAN HANDOFF REQUIRED**")
                st.json(json.loads(final_output["handoff_summary"]))

    st.session_state.messages.append({"role": "assistant", "content": final_output["response"]})