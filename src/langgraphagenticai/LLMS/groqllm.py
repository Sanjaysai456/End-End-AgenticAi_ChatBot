import os
from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input

    def get_llm_model(self):
        try:
            selected_groq_model = self.user_controls_input["selected_groq_model"]

            # Get API key from environment
            groq_api_key = os.getenv("GROQ_API_KEY")

            if not groq_api_key:
                raise ValueError("GROQ_API_KEY not found in environment variables")

            # No need to pass api_key manually
            llm = ChatGroq(
                model=selected_groq_model
            )

            return llm

        except Exception as e:
            raise ValueError(f"Error occurred while initializing Groq LLM: {e}")