# 🚀 End-to-End Agentic AI Chatbot

## 🔧 Deployed on AWS EC2 with Jenkins CI/CD Pipeline

⚡ Production Deployment | 🧠 Multi-Agent AI | 🌐 Web-Enabled | 🐳 Dockerized | 🔁 Automated CI/CD

## 🌟 Project Overview

This project is a **production-ready Agentic AI Chatbot system** built using:

*   **LangGraph (StateGraph-based multi-agent workflow)  
    **
*   **Groq LLMs (Llama models)  
    **
*   **Tavily Search API  
    **
*   **Streamlit Frontend  
    **

The entire system is:

✅ Dockerized  
✅ Hosted on **AWS EC2  
**✅ Integrated with **Jenkins CI/CD Pipeline running on EC2  
**✅ Automatically deployed on every GitHub push

# 🏗️ Production Architecture

## 🔹 Infrastructure Setup (AWS)

*   🖥️ **EC2 Instance  
    **
    *   Ubuntu Server  
        
    *   Docker Installed  
        
    *   Jenkins Installed  
        
    *   Git Installed  
        
    *   Security Groups configured (Ports 22, 8080, 8501 open)  
        
*   🔁 **Jenkins running inside EC2  
    **
    *   Configured with GitHub Webhook  
        
    *   Auto-triggers on push  
        
    *   Builds Docker image  
        
    *   Deploys updated container  
        
*   🌐 **Application deployed on EC2 Public IP  
    **
    *   Streamlit exposed on Port 8501  
        
    *   Accessible via:  
        
*   http://<EC2-Public-IP>:8501  
    

# 🧠 AI System Features

## ✨ Multi-Agent Architecture (LangGraph)

Built using **StateGraph workflow orchestration**, where each capability is a modular node:

*   BasicChatbotNode  
    
*   ChatbotWithToolNode  
    
*   AINewsNode  
    

Centralized state management ensures smooth data flow between agents.

## 🤖 Intelligent Modes

### 1️⃣ Basic AI Chatbot

*   Direct Groq LLM interaction  
    
*   Ultra-fast inference  
    
*   Lightweight conversational mode  
    

### 2️⃣ Web-Enabled Chatbot

*   Real-time search using Tavily API  
    
*   Tool-augmented reasoning  
    
*   Context-aware responses  
    

### 3️⃣ AI News Automation

*   Fetches latest AI news  
    
*   Supports Daily / Weekly / Monthly summaries  
    
*   Converts to Markdown format  
    
*   Automatically saves reports inside:  
    

./AINews/

# ⚡ LLM Models Used

*   Llama 3.3–70B  
    
*   Llama 3.1–8B  
    
*   Powered by Groq hardware acceleration  
    

# 🐳 Dockerized Deployment

The entire application is containerized for portability and production reliability.

### 🔹 Build Image

docker build -t agentic-ai-chatbot .

### 🔹 Run Container

docker run -d -p 8501:8501 agentic-ai-chatbot

# 🔁 Jenkins CI/CD Pipeline (Running on EC2)

## ⚙️ CI/CD Flow

1.  Developer pushes code to GitHub  
    
2.  GitHub webhook triggers Jenkins  
    
3.  Jenkins:  
    *   Pulls latest code  
        
    *   Builds Docker image  
        
    *   Stops old container  
        
    *   Runs new container  
        
4.  Updated application goes live automatically  
    

## 📄 Jenkinsfile Overview

Pipeline stages:

*   ✔ Checkout Code  
    
*   ✔ Build Docker Image  
    
*   ✔ Stop Old Container  
    
*   ✔ Run New Container  
    
*   ✔ Verify Deployment  
    

This ensures zero manual deployment effort.

# 🛠️ Tech Stack

| Layer | Technology |
| --- | --- |
| 🧠 Orchestration | LangGraph, LangChain |
| 🤖 LLM | Groq (Llama 3 Models) |
| 🔎 Search | Tavily API |
| 🎨 Frontend | Streamlit |
| 🐍 Backend | Python 3.10 |
| 🐳 Containerization | Docker |
| 🔁 CI/CD | Jenkins (Hosted on EC2) |
| ☁️ Cloud | AWS EC2 |

# 📂 Project Structure

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

# 🌍 Live Deployment

*   Hosted on **AWS EC2  
    **
*   Jenkins running on same EC2 instance  
    
*   Docker container serving Streamlit app  
    
*   Public access via EC2 IP  
    

# 🎯 Why This Project is Production-Grade

✔ Real multi-agent workflow (LangGraph)  
✔ Tool-augmented LLM reasoning  
✔ Fully Dockerized  
✔ Automated CI/CD pipeline  
✔ Cloud deployment on AWS  
✔ Scalable infrastructure-ready design

# 👨‍💻 Author

**Sanjaysai Poloji  
**AI & Systems Engineering Enthusiast  
Cloud | DevOps | Agentic AI | Production Systems