import json
from langchain_core.messages import HumanMessage, SystemMessage
from src.langgraphagenticai.state.state import State

class RouterNode:
    def __init__(self, llm):
        self.llm = llm

    def process(self, state: State) -> dict:
        """
        Analyzes the user's input and routes to the correct intent.
        """
        messages = state.get("messages", [])
        if not messages:
            return {"intent": "basic", "frequency": ""}
        
        last_message = messages[-1].content
        
        system_prompt = """You are an intelligent routing supervisor for a multi-agent system.
Your job is to analyze the user's input and classify their intent into exactly one of these categories:
1. "ai_news" - The user is asking to fetch, get, or read AI news. Also extract the frequency (e.g., "Daily", "Weekly", "Monthly"). If no frequency is mentioned, default to "Daily".
2. "web_search" - The user is asking a factual question or something that requires searching the web for real-time information (e.g., weather, current events, recent data, sports scores, stock prices).
3. "medical" - The user is asking anything related to medicine, health, diseases, symptoms, treatments, medications, anatomy, medical conditions, disorders, syndromes, drugs, surgery, or any health-related topic. Examples: "What is diabetes?", "symptoms of pneumonia", "how is cancer treated?", "what is hypertension?"
4. "basic" - The user is just chatting, greeting, or asking general knowledge questions that don't require external tools, news, or medical knowledge.

Output your response strictly as a JSON object with the following keys:
- "intent": string (must be one of "ai_news", "web_search", "medical", "basic")
- "frequency": string (if intent is "ai_news", use "Daily", "Weekly", or "Monthly". Otherwise empty string "")

Example Outputs:
{"intent": "ai_news", "frequency": "Weekly"}
{"intent": "medical", "frequency": ""}
{"intent": "web_search", "frequency": ""}
{"intent": "basic", "frequency": ""}
"""
        
        try:
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=last_message)
            ])
            
            content = response.content
            # Clean up potential markdown formatting like ```json ... ```
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:-3].strip()
            elif content.startswith("```"):
                content = content[3:-3].strip()
                
            parsed_result = json.loads(content)
            intent = parsed_result.get("intent", "basic")
            frequency = parsed_result.get("frequency", "")
            
            # Ensure frequency matches what ai_news_node expects (capitalized)
            if frequency:
                frequency = frequency.capitalize()
            
            return {"intent": intent, "frequency": frequency}
            
        except Exception as e:
            print(f"Error in router node: {e}")
            # Fallback to basic chat
            return {"intent": "basic", "frequency": ""}
