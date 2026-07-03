from google import genai
from google.genai import types, errors
import streamlit as st

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    import os
    API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

def classify_customer_persona(prompt: str) -> str:
    """
    Classifies the user's prompt into a distinct persona using Gemini.
    Includes fallback error handling to prevent app crashes during cloud API timeouts.
    """
    system_instruction = """
    You are an expert customer support routing AI. Analyze the user's message and categorize their persona into EXACTLY ONE of the following labels:
    - Technical Expert
    - Executive / Decision Maker
    - Frustrated User
    - Neutral User

    Return ONLY the exact label string without any markdown, bullet points, or extra text.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=genai.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1,
            )
        )
        cleaned_persona = response.text.strip()
        return {
            "persona": cleaned_persona,
            "reasoning": response.text  # Full reasoning for transparency
        }
    except (errors.ServerError, errors.APIError, Exception) as e:
        print(f"⚠️ Cloud API hiccup during persona detection ({type(e).__name__}): {e}")
        return {"persona": "Neutral User"}
