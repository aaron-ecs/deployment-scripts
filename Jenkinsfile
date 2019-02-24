pipeline {
  agent any
  stages {
    stage('Build & Test') {
      steps {
        script {
          checkout scm
          sh 'docker build -t deployment-scripts .'
        }
      }
    }
  }
}