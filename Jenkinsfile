pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        script {
          sh 'rm artifact.zip'
          zip zipFile: 'artifact.zip', archive: false
        }
      }
    }
    stage('Publish S3') {
      steps {
        script {
          sh 'pip3 install boto3'
          sh 'python3 publish_to_s3.py aaron-codedeploy-bucket user-exercises-rest/latest'
        }
      }
    }
  }
}