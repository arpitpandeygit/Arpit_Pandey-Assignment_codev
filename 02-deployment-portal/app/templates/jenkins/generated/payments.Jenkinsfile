pipeline {
  agent any

  stages {
    stage('Build') {
      steps {
        echo 'Building application'
      }
    }

    stage('Test') {
      steps {
        echo 'Running tests'
      }
    }

    stage('Docker Build & Push') {
      steps {
        echo 'Building Docker image for payments'
      }
    }

    stage('Deploy') {
      steps {
        echo 'Deploying payments to Kubernetes'
      }
    }
  }
}
