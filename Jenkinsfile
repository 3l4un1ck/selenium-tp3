pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out repository...'
                git branch: 'main', url: 'https://github.com/3l4un1ck/selenium-tp3.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t selenium-tp3-app .'
            }
        }

        stage('Start Services') {
            steps {
                echo 'Starting app and Selenium with docker-compose...'
                sh 'docker-compose up -d'
                sh 'sleep 10'
            }
        }

        stage('Unit Tests') {
            steps {
                echo 'Running unit tests in Docker...'
                sh 'docker run --rm -v $PWD/reports:/app/reports selenium-tp3-app pytest --html=reports/unit_tests.html'
            }
        }

        stage('Functional Tests') {
            steps {
                echo 'Running Selenium tests in Docker...'
                sh 'docker run --rm --network selenium-tp3_default -v $PWD/reports:/app/reports selenium-tp3-app pytest tests_selenium/ --html=reports/selenium_tests.html'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application (Docker Compose keeps app running)...'
            }
        }

        stage('Notify') {
            steps {
                echo 'Sending notification (Slack, email, etc.)...'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/*.html', fingerprint: true
            echo 'Stopping and removing Docker containers...'
            sh 'docker-compose down || true'
        }
        failure {
            echo 'Build failed!'
        }
        success {
            emailext (
                subject: "Jenkins Build Success: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Good news! The build succeeded.\n\nCheck details at: ${env.BUILD_URL}",
                to: 'm.toho@ecoles-epsi.net'
            )
        }
    }
}