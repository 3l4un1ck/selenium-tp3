pipeline {
    agent any

    environment {
        DOCKER_BUILDKIT = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                echo '📥 Cloning repository...'
                git branch: 'main', url: 'https://github.com/3l4un1ck/selenium-tp3.git'
            }
        }

        stage('Build & Test') {
            steps {
                echo '🚀 Running execute.sh...'
                sh 'chmod +x ./execute.sh'
                sh './execute.sh'
            }
        }

        stage('Publish Reports') {
            steps {
                echo '📝 Archiving reports...'
                publishHTML (target: [
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'unit_test_report.html',
                    reportName: 'Unit Test Report'
                ])
            }
        }
    }

    post {
        always {
            echo '🧹 Cleaning up...'
            sh 'docker-compose down || true'
        }
    }
}
