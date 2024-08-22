"""
Author: Ali Vijdaan
Description: LLM Summarizaiton functions
"""

import google.generativeai as genai
import openai
from dotenv import load_dotenv
import os


load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

model = genai.GenerativeModel('gemini-1.5-flash')

def get_response(prompt, image):

    response = model.generate_content(
        [prompt, image],
        generation_config= genai.GenerationConfig(
            temperature=0.5,
            top_k=5
        )
    )

    return response

openai_api_key = os.getenv("OPEN_AI_KEY")
client = openai.OpenAI(api_key=openai_api_key)

# Note: Add OPEN AI Chat Completion Prompt


