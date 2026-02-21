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
🐳 Docker Deployment
To run the application using Docker:

Bash
# Build the image
docker build -t agentic-chatbot .

# Run the container
docker run -p 8501:8501 agentic-chatbot
⛓️ CI/CD Pipeline (Jenkins)
The project includes a Jenkinsfile that automates the following steps:

Clone Repo: Pulls the latest code from the main branch.

Build: Creates a Docker image labeled sanjaysai/streamlit-app.

Push: Authenticates with Docker Hub and pushes the latest image.

Note: Ensure you have configured dockerhub-creds in your Jenkins Credentials Provider.

📝 Usage Guide
Select LLM: Choose "Groq" and provide your API key.

Choose Usecase:

Basic: Standard AI chat.

Chatbot with Web: Ask questions about current events (uses Tavily).

AI News: Select "Daily" or "Weekly" and click "Fetch" to generate a summarized AI report.
