pipeline {
    agent any

    environment {
        APP_NAME = "agentic-ai"
        GROQ_API_KEY = credentials('GROQ_API_KEY')
        TAVILY_API_KEY = credentials('TAVILY_API_KEY')
    }

    stages {

        stage('Clone') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Sanjaysai456/End-End-AgenticAi_ChatBot.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $APP_NAME .'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker stop $APP_NAME || true'
                sh 'docker rm $APP_NAME || true'
            }
        }

        stage('Run New Container') {
            steps {
                sh '''
                docker run -d \
                -p 8501:8501 \
                -e GROQ_API_KEY=$GROQ_API_KEY \
                -e TAVILY_API_KEY=$TAVILY_API_KEY \
                --name $APP_NAME \
                $APP_NAME
                '''
            }
        }
    }
}