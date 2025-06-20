pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out repository...'
                git branch: 'main', url: 'https://github.com/3l4un1ck/selenium-tp3.git'
            }
        }
        stage('Install') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Unit Tests') {
            steps {
                sh 'pytest tests/ --html=reports/unit_test_report.html'
            }
        }
        stage('Run App') {
            steps {
                sh 'python app.py &'
                sleep(time: 5, unit: 'SECONDS')
            }
        }
        stage('Functional Tests') {
            steps {
                sh 'pytest selenium_tests/ --html=reports/selenium_report.html'
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'reports/*.html', fingerprint: true
        }
    }
}