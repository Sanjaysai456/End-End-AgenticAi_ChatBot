🤖 End-to-End Agentic AI Chatbot with LangGraph
This project is a high-performance, modular Agentic AI Chatbot built using LangGraph, Groq (LLMs), and Tavily API. It features multiple specialized workflows, including a basic chatbot, a web-enabled research assistant, and an automated AI News aggregator and summarizer.

The project is fully containerized and includes a Jenkins CI/CD pipeline for automated deployment.

🌟 Key Features
Multi-Agent Workflows: Built with LangGraph to handle stateful, multi-step agent logic.

Three Modes of Operation:

Basic Chatbot: Direct interaction with Groq LLMs.

Chatbot With Web: Real-time web searching using Tavily API.

AI News Explorer: Fetches latest AI news (Daily/Weekly/Monthly), summarizes them into Markdown, and saves reports locally.

High-Performance LLMs: Powered by Groq (Llama 3.1/3.3) for near-instant response times.

Production Ready: CI/CD integration with Jenkins and Docker.

🏗️ Architecture
The project uses a StateGraph approach where each functionality is a node in the graph:

Nodes: BasicChatbotNode, ChatbotWithToolNode, AINewsNode.

State: Managed via a central State class to pass messages and data between nodes.

Persistence: The AI News workflow automatically saves summaries to the ./AINews/ directory.

🚀 Tech Stack
Orchestration: LangGraph, LangChain

LLMs: Groq (Llama-3.3-70b, Llama-3.1-8b)

Search Engine: Tavily API

Frontend: Streamlit

DevOps: Jenkins, Docker

Language: Python 3.10

🔧 Installation & Setup
1. Clone the Repository
Bash
git clone https://github.com/Sanjaysai456/End-End-AgenticAi_ChatBot.git
cd End-End-AgenticAi_ChatBot
2. Set Up Virtual Environment
Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
3. Environment Variables
Create a .env file or export the following keys:

Bash
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
4. Run the Application
Bash
streamlit run app.py
