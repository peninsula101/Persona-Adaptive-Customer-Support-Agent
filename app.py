import streamlit as st
import json
from src.classifier import classify_customer_persona
from src.rag_pipeline import LocalRAGPipeline
from src.generator import generate_adaptive_response

# --- Streamlit Page Setup ---
st.set_page_config(page_title="Adsparkx AI Support", page_icon="🤖", layout="centered")
st.title("🤖 Persona-Adaptive Support Agent")
st.caption("Powered by Gemini, ChromaDB, and Retrieval-Augmented Generation")

# --- Initialize RAG Database (Runs once per session) ---
@st.cache_resource
def load_database():
    return LocalRAGPipeline()

rag_db = load_database()

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat Input & AI Processing ---
if prompt := st.chat_input("How can I help you today?"):
    # 1. Display User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing request..."):
            
            # 2. Detect Persona
            persona_data = classify_customer_persona(prompt)
            detected_persona = persona_data.get("persona", "Unknown")
            
            # 3. Retrieve Context from Database
            context_chunks = rag_db.retrieve_context(prompt, top_k=3)
            
            # 4. Generate Adaptive Response
            final_output = generate_adaptive_response(prompt, detected_persona, context_chunks)
            
            # --- UI Display ---
            # Show the "thinking" steps in an expandable box
            with st.expander(f"🧠 Detected Persona: **{detected_persona}**", expanded=False):
                st.write("**Reasoning:**", persona_data.get("reasoning"))
                st.write("**Retrieved Sources:**")
                if context_chunks:
                    for chunk in context_chunks:
                        st.caption(f"📄 {chunk['source']} (Score: {chunk['score']:.2f})")
                else:
                    st.caption("No relevant documents found.")

            # Show the final AI response
            st.markdown(final_output["response"])
            
            # Handle Escalation UI
            if final_output.get("escalated"):
                st.error("🚨 **ESCALATION TRIGGERED: HUMAN HANDOFF REQUIRED**")
                st.json(json.loads(final_output["handoff_summary"]))

    # Save AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": final_output["response"]})