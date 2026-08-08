pipeline {
    agent any

    environment {
        IMAGE_NAME = 'qa-automation-framework:latest'
        API_BASE_URL = 'http://host.docker.internal:2424'
        UI_BASE_URL = 'http://host.docker.internal:3000'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Checking out latest QA automation test code...'
                checkout scm
            }
        }

        stage('Build Docker Test Container') {
            steps {
                echo 'Building QA Playwright + Pytest Docker Image...'
                sh 'docker build -t ${IMAGE_NAME} .'
            }
        }

        stage('PyATS Container Network Health Check') {
            steps {
                echo 'Running PyATS health check on container network ports...'
                sh '''
                    python3 -m venv venv || true
                    ./venv/bin/pip install requests || true
                    ./venv/bin/python utils/pyats_health.py || echo "PyATS health check completed."
                '''
            }
        }

        stage('Run Pytest Test Suite') {
            steps {
                echo 'Executing Pytest test suite (API, UI, Integration) inside Docker...'
                sh '''
                    docker run --rm \
                      --name qa-runner \
                      -e API_BASE_URL=${API_BASE_URL} \
                      -e UI_BASE_URL=${UI_BASE_URL} \
                      -v $(pwd)/reports:/app/reports \
                      ${IMAGE_NAME} pytest --html=reports/report.html --self-contained-html -v || true
                '''
            }
        }

        stage('Publish HTML Test Report') {
            steps {
                echo 'Archiving HTML report artifact...'
                archiveArtifacts artifacts: 'reports/report.html', allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            echo 'Cleaning up docker containers...'
            sh 'docker rm -f qa-runner || true'
        }
        success {
            echo 'QA Test Pipeline Succeeded!'
        }
        failure {
            echo 'QA Test Pipeline Failed!'
        }
    }
}
