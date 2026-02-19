pipeline {
    agent any

    environment {
        IMAGE_NAME = "sanjaysai/streamlit-app"
        EC2_HOST = "13.232.85.102"
        EC2_USER = "ubuntu"
    }

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main', url: 'https://github.com/Sanjaysai456/End-End-AgenticAi_ChatBot.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t $IMAGE_NAME:latest ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker push $IMAGE_NAME:latest
                    """
                }
            }
        }

stage('Deploy to EC2') {
    steps {
        sh """
        ssh -i C:/jenkins/ec2-key1.pem -o IdentitiesOnly=yes -o StrictHostKeyChecking=no ubuntu@13.232.85.102 "

            docker pull sanjaysai/streamlit-app:latest &&
            docker stop streamlit || true &&
            docker rm streamlit || true &&
            docker run -d -p 8501:8501 --name streamlit sanjaysai/streamlit-app:latest
        "
        """
    }
}

    }
}
