pipeline {
  agent any

  stages {

    stage('Clone Repo') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Image') {
      steps {
        sh 'docker build -t ainews:latest .'
      }
    }

    stage('Run Streamlit Container') {
      steps {
        sh '''
        docker stop ainews || true
        docker rm ainews || true
        docker run -d -p 8501:8501 --name ainews ainews:latest
        '''
      }
    }
  }
}
