pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main', url: 'https://github.com/Sanjaysai456/End-End-AgenticAi_ChatBot.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ainewsagentic:latest .'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker stop ainews || true
                docker rm ainews || true
                docker run -d \
                  --name ainews \
                  -p 8501:8501 \
                  ainewsagentic:latest
                '''
            }
        }
    }
}
