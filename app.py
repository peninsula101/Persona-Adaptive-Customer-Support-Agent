import streamlit as st
import json
import os
from src.classifier import classify_customer_persona
from src.rag_pipeline import LocalRAGPipeline, build_database_from_folder
from src.generator import generate_adaptive_response

# --- Page Configuration (Must be first Streamlit command) ---
st.set_page_config(page_title="Persona-Adaptive Customer Support Agent", page_icon="🤖", layout="centered")

# --- Manual Database Override ---
if st.sidebar.button("🛠️ Force Rebuild Database"):
    with st.spinner("Rebuilding knowledge base..."):
        build_database_from_folder()
        st.sidebar.success("Database Rebuilt! Please refresh the page.")
# --------------------------------

# --- Database Initialization ---
if not os.path.exists("chroma_db"):
    with st.spinner("First-time setup: Initializing Enterprise Knowledge Base..."):
        build_database_from_folder()

st.title("🤖 Persona-Adaptive Support Agent")
st.caption("Powered by Gemini, ChromaDB, and Retrieval-Augmented Generation")

@st.cache_resource
def load_database():
    return LocalRAGPipeline()

rag_db = load_database()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display message history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- INTERACTIVE PROMPT SUGGESTIONS GUIDE ---
st.markdown("### 💡 What you can ask me")
st.caption("Click any example prompt below to automatically populate the agent and test multi-domain RAG retrieval:")

col1, col2 = st.columns(2)

# Temporary trigger variable
clicked_prompt = None

with col1:
    st.markdown("**🏍️ TVS Jupiter Vehicle Manual**")
    if st.button("🔧 When should I change the engine oil?"):
        clicked_prompt = "According to the manual, what is the recommended schedule and procedure for changing the engine oil?"
    if st.button("🛞 What is the recommended tire pressure?"):
        clicked_prompt = "What is the recommended front and rear tire pressure for the 2-wheeler?"

with col2:
    st.markdown("**💻 Enterprise API & SLAs**")
    if st.button("⚠️ I keep getting a 401 Unauthorized error"):
        clicked_prompt = "I keep getting a 401 Unauthorized error when hitting the endpoint. How do I fix this?"
    if st.button("📜 Explain the webhook validation"):
        clicked_prompt = "What is the exact X-Signature header validation process for webhook payloads?"

st.markdown("---")

# Capture either the live chat input or the suggestion chip selection
chat_prompt = st.chat_input("How can I help you today?")
prompt = chat_prompt if chat_prompt else clicked_prompt

if prompt:
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