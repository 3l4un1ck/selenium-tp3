pipeline {
    agent any
        stages {
            stage('Checkout') {
                steps {
                    echo 'Checking out repository...'
                    git 'https://github.com/3l4un1ck/selenium-tp3.git'
                }
            }

            stage('Install Dependencies') {
                steps {
                    echo 'Installing dependencies...'
                    sh 'pip install -r requirements.txt'
                }
            }

            stage('Unit Tests') {
                steps {
                    echo 'Running unit tests...'
                    sh 'pytest --html=reports/unit_tests.html'
                }
            }

            stage('Build & Run App') {
                steps {
                    echo 'Building and running app...'
                    sh 'nohup python app.py &'
                    sh 'sleep 5'
                }
           }

           stage('Functional Tests') {
            steps {
                echo 'Running functional (Selenium) tests...'
                sh 'pytest tests_selenium/ --html=reports/selenium_tests.html'
               }
           }

          stage('Deploy (optionnel)') {
            steps {
                            echo 'Deploying application (optional)...'
                            echo 'Déploiement réussi (ex. copie serveur, Docker, etc.)'
                        }
                    }

                    stage('Notify') {
                        steps {
                            echo 'Sending notification (Slack, email, etc.)...'
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
                    success {
                        emailext (
                            subject: "Jenkins Build Success: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                            body: "Good news! The build succeeded.\n\nCheck details at: ${env.BUILD_URL}",
                            to: 'your_email@example.com'
                        )
                    }
                }
            }