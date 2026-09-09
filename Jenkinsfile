pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install') {
            steps {
                sh 'python3 -m pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh 'python3 -m pytest'
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t system-health-dashboard .'
            }
        }

        stage('Tag') {
            steps {
                sh 'docker tag system-health-dashboard system-health-dashboard:${BUILD_NUMBER}'
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    docker rm -f jenkins-health-check 2>/dev/null || true
                    docker run -d --name jenkins-health-check -p 5001:5000 system-health-dashboard:${BUILD_NUMBER}
                    sleep 5
                    curl -f http://localhost:5001/health
                    docker rm -f jenkins-health-check
                '''
            }
        }
    }
}
