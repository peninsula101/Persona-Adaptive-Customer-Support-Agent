import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def generate_adaptive_response(user_query: str, persona: str, context_chunks: list) -> dict:
   
    confidence_threshold = 0.15
    best_score = max([chunk["score"] for chunk in context_chunks]) if context_chunks else 0.0

    if best_score < confidence_threshold or len(context_chunks) == 0:
        return {
            "escalated": True,
            "response": "I apologize, but I am unable to locate the precise solution to your request. I am connecting you with a live human support specialist.",
            "handoff_summary": generate_handoff_summary(user_query, persona, context_chunks)
        }

    if persona == "Technical Expert":
        persona_instructions = (
            "You are a Senior Systems Engineer. Provide clear root-cause analysis, "
            "configuration specifications, and precise API pathways or code blocks. "
            "Keep technical descriptions exact and structured."
        )
    elif persona == "Frustrated User":
        persona_instructions = (
            "You are a deeply empathetic, reassuring Customer Care Specialist. "
            "Begin with a warm, genuine validation of their difficulty. Use straightforward, "
            "reassuring, and simple action-oriented bullet steps. Avoid confusing jargon."
        )
    else:  
        persona_instructions = (
            "You are a concise Client Relations Director. Focus on direct business outcomes, "
            "impact summaries, and timelines for resolution. Keep responses extremely "
            "brief, professional, and skip unnecessary configuration details."
        )

    context_text = "\n\n".join([f"Source [{c['source']}]: {c['text']}" for c in context_chunks])
    
    full_system_prompt = (
        f"{persona_instructions}\n\n"
        "CRITICAL RULES:\n"
        "Base your response ONLY on the provided context.\n"
        "Do not hallucinate or assume facts not found in the documents.\n\n"
        f"FACTUAL CONTEXT DOCUMENTS:\n{context_text}"
    )

    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_query,
        config=types.GenerateContentConfig(
            system_instruction=full_system_prompt,
            temperature=0.2
        )
    )

    return {
        "escalated": False,
        "response": response.text,
        "handoff_summary": None
    }

def generate_handoff_summary(user_query: str, persona: str, context_chunks: list) -> str:
    """Compiles detailed, structured JSON handoff data for an escalating support ticket."""
    handoff_data = {
        "persona": persona,
        "detected_issue": user_query[:100] + "...",
        "retrieved_sources": [c["source"] for c in context_chunks],
        "confidence_score": max([c["score"] for c in context_chunks]) if context_chunks else 0.0,
        "recommended_action": "Review retrieved documents and contact the user directly to resolve their specific issue."
    }
    return json.dumps(handoff_data, indent=2)

if __name__ == "__main__":
    test_query = "How do I fix a 401 Unauthorized error?"
    test_persona = "Technical Expert"
    test_chunks = [{
        "source": "api_troubleshooting.md", 
        "text": "If you receive a 401 Unauthorized error, it means your API key is invalid. Navigate to Security > API Keys and Generate a new Bearer Token.", 
        "score": 0.85
    }]

    result = generate_adaptive_response(test_query, test_persona, test_chunks)
    print("\n--- Final Output ---")
    print(result["response"])