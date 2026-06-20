# 🤖 Persona-Adaptive Customer Support Agent

## Project Overview
This project is an intelligent, retrieval-augmented customer support agent built to dynamically adapt its communication style based on the detected persona of the user. It utilizes a local vector database to ground its responses in factual knowledge base documents and includes a built-in escalation workflow that routes unresolved or low-confidence queries to a human agent, providing a structured handoff summary.

## Tech Stack
* **Language:** Python 3.11+
* **User Interface:** Streamlit (>=1.30.0)
* **LLM / Generation:** Google Gemini (`gemini-2.5-flash`) via `google-genai` SDK
* **Embeddings:** Google Gemini (`gemini-embedding-001`)
* **Vector Database:** ChromaDB (>=0.4.0)
* **Document Parsing:** PyPDF (>=3.0.0)
* **Chunking:** LangChain Text Splitters (`langchain-text-splitters`)

---

## Architecture Diagram
```text
[User Message] 
      │
      ▼
[Persona Classifier] ──▶ Tags User: Technical / Frustrated / Executive
      │
      ▼
[Vector Database] ─────▶ Cosine Similarity Search ──▶ [Top-3 Document Chunks]
      │
      ▼
[Adaptive Prompt Engine] 
      │
      ├─▶ (If Confidence < 0.40) ──▶ [Escalate to Human Agent] ──▶ [Generate JSON Handoff]
      │
      └─▶ (If Confidence ≥ 0.40) ──▶ [Generate Persona-Adaptive Response]