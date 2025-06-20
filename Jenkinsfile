pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
        }
    }

    environment {
        PIP_DISABLE_PIP_VERSION_CHECK = 1
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Pytest') {
            steps {
                sh 'pytest --junitxml=pytest-report.xml'
            }
        }

        stage('Archive test report') {
            steps {
                junit 'pytest-report.xml'
            }
        }
    }
}
