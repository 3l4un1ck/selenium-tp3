pipeline {
    agent any

    environment {
        PYTEST_REPORT_DIR = 'reports'
        COVERAGE_DIR = 'htmlcov'
    }

    stages {
        stage('Checkout') {
            steps {
                echo '📥 Clonage du dépôt...'
                git branch: 'main', url: 'https://github.com/3l4un1ck/selenium-tp3.git'
            }
        }

        stage('Clean Docker') {
            steps {
                echo '🧹 Nettoyage Docker...'
                sh '''
                    docker-compose down -v --remove-orphans || true
                    docker rm -f $(docker ps -aq) 2>/dev/null || true
                    docker rmi -f $(docker images -q selenium-tp3-app) 2>/dev/null || true
                    docker network prune -f || true
                    docker volume prune -f || true
                '''
            }
        }

        stage('Build Image') {
            steps {
                echo '🐳 Construction de l\'image Docker...'
                sh 'docker build -t selenium-tp3-app .'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '📦 Installation des dépendances...'
                sh 'docker run --rm -v "$PWD":/app -w /app selenium-tp3-app pip install -r requirements.txt'
            }
        }

        stage('Unit Tests') {
            steps {
                echo '🧪 Lancement des tests unitaires...'
                sh """
                    mkdir -p ${PYTEST_REPORT_DIR}
                    mkdir -p ${COVERAGE_DIR}
                    docker run --rm \
                        -v "\$PWD:/app" \
                        -w /app \
                        selenium-tp3-app \
                        pytest tests/ \
                            --html=${PYTEST_REPORT_DIR}/unit_tests.html \
                            --cov=. \
                            --cov-report="html:${COVERAGE_DIR}" \
                            --junitxml=${PYTEST_REPORT_DIR}/unit-results.xml
                """
            }
            post {
                always {
                    junit "${PYTEST_REPORT_DIR}/unit-results.xml"
                    publishHTML([
                        reportDir: PYTEST_REPORT_DIR,
                        reportFiles: 'unit_tests.html',
                        reportName: 'Unit Tests Report',
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true
                    ])
                    publishHTML([
                        reportDir: COVERAGE_DIR,
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report',
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true
                    ])
                }
            }
        }

        stage('Start App and Selenium') {
            steps {
                echo '🚀 Démarrage des services Flask + Selenium...'
                sh 'docker-compose up -d'
                echo '⏳ Attente de 10s pour la disponibilité des services...'
                sh 'sleep 10'
            }
        }

        stage('Functional Tests') {
            steps {
                echo '🧪 Lancement des tests fonctionnels avec Selenium...'
                sh """
                    docker run --rm \
                        --network selenium-tp3_default \
                        -v \$PWD:/app \
                        -w /app \
                        selenium-tp3-app \
                        pytest tests_selenium/ \
                            --html=${PYTEST_REPORT_DIR}/selenium_tests.html \
                            --junitxml=${PYTEST_REPORT_DIR}/selenium-results.xml
                """
            }
            post {
                always {
                    junit "${PYTEST_REPORT_DIR}/selenium-results.xml"
                    publishHTML([
                        reportDir: PYTEST_REPORT_DIR,
                        reportFiles: 'selenium_tests.html',
                        reportName: 'Selenium Tests Report',
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true
                    ])
                }
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Déploiement fictif terminé (placeholder).'
            }
        }
    }

    post {
        always {
            echo '🧼 Nettoyage final...'
            sh 'docker-compose down || true'
            archiveArtifacts artifacts: "${PYTEST_REPORT_DIR}/*.html,${COVERAGE_DIR}/**", fingerprint: true
        }

        success {
            emailext (
                subject: "✅ Build Success – ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
🎉 Le build a réussi !

🔗 [Unit Tests Report](${env.BUILD_URL}Unit_20Tests_20Report/)
🔗 [Coverage Report](${env.BUILD_URL}Coverage_20Report/)
🔗 [Selenium Tests Report](${env.BUILD_URL}Selenium_20Tests_20Report/)

📂 Détail complet : ${env.BUILD_URL}
""",
                to: 'm.toho@ecoles-epsi.net'
            )
        }

        failure {
            emailext (
                subject: "❌ Build Failed – ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
⚠️ Le build a échoué !

📂 Détail complet : ${env.BUILD_URL}
""",
                to: 'm.toho@ecoles-epsi.net'
            )
        }
    }
}
