import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def classify_customer_persona(user_message: str) -> dict:
    """Analyzes the user's message and classifies it into one of the three target personas."""
    
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))

    system_instruction = (
        "You are an advanced classification engine. Your task is to analyze the "
        "sentiment, vocabulary, and tone of an incoming support message and classify "
        "it into exactly one of three customer personas: \n"
        "1. 'Technical Expert': Uses jargon, asks about APIs/code/configs.\n"
        "2. 'Frustrated User': Uses emotional language, exclamation marks, or mentions urgency.\n"
        "3. 'Business Executive': Focuses on business impact, ROI, timelines, and brevity.\n\n"
        "Provide your evaluation strictly in the requested JSON structure."
    )

    response_schema = {
        "type": "OBJECT",
        "properties": {
            "persona": {
                "type": "STRING",
                "enum": ["Technical Expert", "Frustrated User", "Business Executive"]
            },
            "confidence": {"type": "NUMBER"},
            "reasoning": {"type": "STRING"}
        },
        "required": ["persona", "confidence", "reasoning"]
    }

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            response_schema=response_schema,
            temperature=0.1
        )
    )
    
    return json.loads(response.text)

if __name__ == "__main__":
    test_msg = "Our production API key stopped working with a 401 Unauthorized block. Check our logs immediately."
    result = classify_customer_persona(test_msg)
    print(json.dumps(result, indent=2))