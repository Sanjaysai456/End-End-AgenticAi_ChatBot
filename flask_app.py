import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage

# Load environment variables first
load_dotenv(override=True)

from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder

# ─────────────────────────────────────────────
# Flask App Setup
# ─────────────────────────────────────────────
app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

# ─────────────────────────────────────────────
# Graph Initialization (once at startup)
# ─────────────────────────────────────────────
print("[INIT] Initializing LangGraph Multi-Agent System with Medical RAG...")

# Default Groq model — change here if needed
DEFAULT_MODEL = "llama-3.1-8b-instant"

user_controls_input = {
    "selected_llm": "Groq",
    "selected_groq_model": DEFAULT_MODEL,
}

try:
    llm_config = GroqLLM(user_controls_input=user_controls_input)
    model = llm_config.get_llm_model()
    graph_builder = GraphBuilder(model)
    graph = graph_builder.setup_graph("Multi-Agent System")
    print("[OK] Multi-Agent Graph ready!")
except Exception as e:
    print(f"[ERROR] Failed to initialize graph: {e}")
    graph = None


# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the frontend chat UI."""
    return send_from_directory("frontend", "index.html")


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "graph_ready": graph is not None,
        "model": DEFAULT_MODEL,
    })


@app.route("/chat", methods=["POST"])
def chat():
    """
    Main chat endpoint.

    Request body:
        { "message": "What is diabetes?" }

    Response:
        {
            "response": "...",
            "intent": "medical",
            "agent": "Medical RAG 🏥"
        }
    """
    if graph is None:
        return jsonify({"error": "Graph not initialized. Check server logs."}), 500

    data = request.get_json(force=True)
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Empty message received."}), 400

    try:
        initial_state = {"messages": [HumanMessage(content=user_message)]}
        result = graph.invoke(initial_state)

        intent = result.get("intent", "basic")

        # ── AI News: read from saved markdown file ──
        if intent == "ai_news":
            frequency = result.get("frequency", "daily").lower() or "daily"
            news_path = f"./AINews/{frequency}_summary.md"
            try:
                with open(news_path, "r", encoding="utf-8") as f:
                    response_text = f.read()
            except FileNotFoundError:
                response_text = f"⚠️ News file not found at `{news_path}`. The news may not have been generated yet."
            agent_label = "AI News 📰"

        # ── Medical RAG ──
        elif intent == "medical":
            response_text = _extract_last_ai_message(result)
            agent_label = "Medical RAG 🏥"

        # ── Web Search ──
        elif intent == "web_search":
            response_text = _extract_last_ai_message(result)
            agent_label = "Web Search 🌐"

        # ── Basic Chat ──
        else:
            response_text = _extract_last_ai_message(result)
            agent_label = "Chat Assistant 💬"

        return jsonify({
            "response": response_text,
            "intent": intent,
            "agent": agent_label,
        })

    except Exception as e:
        print(f"[Chat Error] {e}")
        return jsonify({"error": str(e)}), 500


def _extract_last_ai_message(result: dict) -> str:
    """Extract the last AIMessage content from the graph result."""
    messages = result.get("messages", [])
    for message in reversed(messages):
        if isinstance(message, AIMessage) and message.content:
            return message.content
    return "I'm sorry, I couldn't generate a response. Please try again."


# ─────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"[SERVER] Flask running at http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
