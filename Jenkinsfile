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
                sh '''
                    python3 -m pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    python3 -m pytest
                '''
            }
        }

        stage('Build') {
            steps {
                sh '''
                    export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
                    export DOCKER_HOST="unix:///Users/anushkadave/.docker/run/docker.sock"
                    export DOCKER_CONFIG="$WORKSPACE/.docker-jenkins"
                    mkdir -p "$DOCKER_CONFIG"
                    printf '{"auths":{}}' > "$DOCKER_CONFIG/config.json"

                    docker build \
                      -t system-health-dashboard:${BUILD_NUMBER} \
                      -t system-health-dashboard:latest .
                '''
            }
        }

        stage('Tag') {
            steps {
                sh '''
                    export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
                    export DOCKER_HOST="unix:///Users/anushkadave/.docker/run/docker.sock"
                    export DOCKER_CONFIG="$WORKSPACE/.docker-jenkins"

                    docker tag system-health-dashboard:${BUILD_NUMBER} \
                      system-health-dashboard:${BUILD_NUMBER}
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
                    export DOCKER_HOST="unix:///Users/anushkadave/.docker/run/docker.sock"
                    export DOCKER_CONFIG="$WORKSPACE/.docker-jenkins"

                    docker rm -f jenkins-health-check 2>/dev/null || true

                    docker run -d \
                      --name jenkins-health-check \
                      -p 5001:5000 \
                      -e ENVIRONMENT=production \
                      system-health-dashboard:${BUILD_NUMBER}

                    sleep 5

                    curl -f http://localhost:5001/health
                    curl -f http://localhost:5001/version
                    curl -f http://localhost:5001/environment

                    docker rm -f jenkins-health-check
                '''
            }
        }
    }

    post {
        always {
            sh '''
                export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
                    export DOCKER_HOST="unix:///Users/anushkadave/.docker/run/docker.sock"
                docker rm -f jenkins-health-check 2>/dev/null || true
            '''
        }
    }
}
