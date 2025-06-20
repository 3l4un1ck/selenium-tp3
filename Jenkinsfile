pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/3l4un1ck/selenium-tp3.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'pytest --html=reports/unit_tests.html'
            }
        }

        stage('Build & Run App') {
            steps {
                sh 'nohup python app.py &'
                sh 'sleep 5' // attendre le démarrage
            }
        }

        stage('Functional Tests') {
            steps {
                sh 'pytest tests_selenium/ --html=reports/selenium_tests.html'
            }
        }

        stage('Deploy (optionnel)') {
            steps {
                echo 'Déploiement réussi (ex. copie serveur, Docker, etc.)'
            }
        }

        stage('Notify') {
            steps {
                echo 'Envoi de notification possible (Slack, email, etc.)'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/*.html', fingerprint: true
        }
        failure {
            echo 'Build failed!'
        }
    }
}
