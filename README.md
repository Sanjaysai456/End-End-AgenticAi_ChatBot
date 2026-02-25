# 🤖 End-to-End Agentic AI Chatbot with LangGraph

⚡ Production-Ready | 🧠 Multi-Agent | 🌐 Web-Enabled | 📰 AI News Automation | 🚀 CI/CD Integrated

## 🌟 Overview

A **high-performance, modular Agentic AI Chatbot** built using **LangGraph**, **Groq LLMs**, and **Tavily Search API**.

This system supports **multi-agent workflows**, real-time web search, and automated AI news summarization — all fully containerized with **Docker** and deployed via **Jenkins CI/CD**.

## 🔥 Key Features

✨ **Multi-Agent Architecture**

*   Built using LangGraph StateGraph  
    
*   Modular and scalable workflow nodes  
    

🤖 **Three Intelligent Modes**

1️⃣ **Basic Chatbot**

*   Direct interaction with Groq LLMs  
    
*   Ultra-fast inference  
    

2️⃣ **Chatbot With Web**

*   Real-time web search via Tavily API  
    
*   Context-aware responses  
    

3️⃣ **AI News Explorer**

*   Fetches latest AI news (Daily / Weekly / Monthly)  
    
*   Auto-summarizes into Markdown  
    
*   Saves reports locally in ./AINews/  
    

⚡ **High-Speed LLMs**

*   Llama 3.3–70B  
    
*   Llama 3.1–8B  
    
*   Powered by Groq hardware acceleration  
    

🚀 **Production Ready**

*   Dockerized environment  
    
*   Jenkins automated pipeline  
    
*   Clean modular codebase  
    

## 🏗️ Architecture

### 🧩 StateGraph-Based Design

Each feature runs as a **node** inside a centralized graph:

*   BasicChatbotNode  
    
*   ChatbotWithToolNode  
    
*   AINewsNode  
    

### 🗂️ Centralized State Management

*   Custom State class  
    
*   Passes messages & metadata between nodes  
    

### 💾 Persistence

*   AI News reports auto-saved in:  
    

./AINews/

## 🛠️ Tech Stack

| Layer | Technology |
| --- | --- |
| 🧠 Orchestration | LangGraph, LangChain |
| 🤖 LLMs | Groq (Llama 3.3-70B, Llama 3.1-8B) |
| 🔎 Search | Tavily API |
| 🎨 Frontend | Streamlit |
| 🐳 DevOps | Docker, Jenkins |
| 🐍 Backend | Python 3.10 |

## 🚀 Installation & Setup

### 1️⃣ Clone Repository

git clone https://github.com/Sanjaysai456/End-End-AgenticAi\_ChatBot.git

cd End-End-AgenticAi\_ChatBot

### 2️⃣ Create Virtual Environment

python -m venv venv

**Activate:**

*   Windows:  
    

venv\\Scripts\\activate

*   Mac/Linux:  
    

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

### 3️⃣ Configure Environment Variables

Create a .env file:

GROQ\_API\_KEY=your\_groq\_key

TAVILY\_API\_KEY=your\_tavily\_key

### 4️⃣ Run Application

streamlit run app.py

## 🐳 Docker Deployment

Build image:

docker build -t agentic-ai-chatbot .

Run container:

docker run -p 8501:8501 agentic-ai-chatbot

## 🔁 CI/CD Pipeline

✔ Jenkins pulls latest GitHub changes  
✔ Builds Docker image  
✔ Runs container automatically  
✔ Ensures production stability

## 📂 Project Structure

├── app.py

├── nodes/

│ ├── basic\_chatbot.py

│ ├── chatbot\_with\_tool.py

│ └── ai\_news.py

├── AINews/

├── Dockerfile

├── Jenkinsfile

├── requirements.txt

└── README.md

## 📌 Why This Project Stands Out

*   True **Agentic workflow architecture  
    **
*   Real-time tool usage inside LLM reasoning  
    
*   Automated AI research pipeline  
    
*   Production-grade deployment setup  
    
*   Clean modular extensible design  
    

## 👨‍💻 Author

**Sanjaysai  
**AI & Systems Engineering Enthusiast