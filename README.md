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

## Objective
●	Detects customer personas from incoming messages <br>
●	Supports at least three personas: <br>
○	Technical Expert <br>
○	Frustrated User <br>
○	Business Executive <br>
●	Retrieves relevant information from a knowledge base
●	Adapts response style and tone according to the detected persona
●	Generates grounded responses using retrieved content
●	Escalates conversations to a human support agent when appropriate
●	Provides a structured handoff summary during escalation
●	Runs end-to-end through a command-line interface or web UI
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
```
---

To Test

Drop these into your Streamlit app one by one:

1. The "Technical Expert" Test
"I keep getting a 401 Unauthorized error when hitting the endpoint. Also, what is the exact X-Signature header validation process for webhook payloads?"

2. The "Business Executive" Test
"What is the guaranteed monthly uptime SLA for our enterprise tier, and what specific service credits are we entitled to if performance drops below 99.99%? Give me the bottom line for our ₹500,000 annual contract."

3. The "Frustrated User" Test
"I was double charged this month because of some stupid system glitch and I am incredibly angry! How do I get my money back right now before I just cancel my subscription?!"

4. The "Escalation Protocol" Test (Human Handoff)
"I am trying to configure an expo-sqlite database for my React Native mobile application and I keep getting a 'directory not found' error on Android. How do I fix this?"
