pipeline {
    agent any

    environment {
        PYTEST_REPORT_DIR = 'reports'
        COVERAGE_DIR = 'htmlcov'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out repository...'
                git branch: 'main', url: 'https://github.com/3l4un1ck/selenium-tp3.git'
            }
        }

        stage('Clean Docker Environment') {
            steps {
                echo 'Cleaning up old Docker containers, networks, and images...'
                sh '''
                    docker-compose down -v --remove-orphans || true
                    docker rm -f $(docker ps -aq) 2>/dev/null || true
                    docker rmi -f $(docker images -q selenium-tp3-app) 2>/dev/null || true
                    docker network prune -f || true
                    docker volume prune -f || true
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t selenium-tp3-app .'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh 'docker run --rm -v "$PWD":/app -w /app selenium-tp3-app pip install -r requirements.txt'
                echo 'Running pytest to install dependencies...'
                sh 'docker run --rm -v "$PWD":/app -w /app selenium-tp3-app pytest --cov=todo tests/ --junitxml=test-results.xml '
            }
        }

        // stage('Unit Tests') {
        //     steps {
        //         echo 'Running unit tests with Pytest...'
        //         sh """
        //             mkdir -p ${PYTEST_REPORT_DIR}
        //             mkdir -p ${COVERAGE_DIR}
        //             docker run --rm \
        //                 -v "\${WORKSPACE}/${PYTEST_REPORT_DIR}:/app/${PYTEST_REPORT_DIR}" \
        //                 -v "\${WORKSPACE}/${COVERAGE_DIR}:/app/${COVERAGE_DIR}" \
        //                 selenium-tp3-app \
        //                 python -m pytest \
        //                     --html="/app/${PYTEST_REPORT_DIR}/unit_tests.html" \
        //                     --cov=. \
        //                     --cov-report="html:/app/${COVERAGE_DIR}" \
        //                     --junitxml="/app/${PYTEST_REPORT_DIR}/unit-results.xml" \
        //                     tests/
        //         """
        //     }
        //     post {
        //         always {
        //             junit allowEmptyResults: true, testResults: "${PYTEST_REPORT_DIR}/unit-results.xml"
        //             publishHTML([
        //                 allowMissing: true,
        //                 alwaysLinkToLastBuild: true,
        //                 keepAll: true,
        //                 reportDir: PYTEST_REPORT_DIR,
        //                 reportFiles: 'unit_tests.html',
        //                 reportName: 'Unit Tests Report'
        //             ])
        //             publishHTML([
        //                 allowMissing: true,
        //                 alwaysLinkToLastBuild: true,
        //                 keepAll: true,
        //                 reportDir: COVERAGE_DIR,
        //                 reportFiles: 'index.html',
        //                 reportName: 'Coverage Report'
        //             ])
        //         }
        //     }
        // }

        stage('Start Services') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                echo 'Starting app and Selenium with docker-compose...'
                sh 'docker-compose up -d'
                sh 'sleep 10' // Wait for services to be ready
            }
        }

        // stage('Functional Tests') {
        //     when {
        //         expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
        //     }
        //     steps {
        //         echo 'Running Selenium functional tests...'
        //         sh """
        //             docker run --rm \
        //                 --network selenium-tp3_default \
        //                 -v \$PWD/${PYTEST_REPORT_DIR}:/app/${PYTEST_REPORT_DIR} \
        //                 selenium-tp3-app \
        //                 pytest tests_selenium/ \
        //                     --html=${PYTEST_REPORT_DIR}/selenium_tests.html \
        //                     --junitxml=${PYTEST_REPORT_DIR}/selenium-results.xml
        //         """
        //     }
        //     post {
        //         always {
        //             junit "${PYTEST_REPORT_DIR}/selenium-results.xml"
        //             publishHTML([
        //                 allowMissing: false,
        //                 alwaysLinkToLastBuild: true,
        //                 keepAll: true,
        //                 reportDir: PYTEST_REPORT_DIR,
        //                 reportFiles: 'selenium_tests.html',
        //                 reportName: 'Selenium Tests Report'
        //             ])
        //         }
        //     }
        // }

        stage('Deploy') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                echo 'Deploying application...'
                // Add your deployment steps here
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            sh 'docker-compose down || true'
            archiveArtifacts artifacts: "${PYTEST_REPORT_DIR}/*.html,${COVERAGE_DIR}/**", fingerprint: true
        }
        success {
            emailext (
                subject: "✅ Jenkins Build Success: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    Build succeeded successfully!

                    Unit Tests Report: ${env.BUILD_URL}Unit_20Tests_20Report/
                    Coverage Report: ${env.BUILD_URL}Coverage_20Report/
                    Selenium Tests Report: ${env.BUILD_URL}Selenium_20Tests_20Report/

                    Check complete details at: ${env.BUILD_URL}
                """,
                to: 'm.toho@ecoles-epsi.net'
            )
        }
        failure {
            emailext (
                subject: "❌ Jenkins Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    Build failed!

                    Check details at: ${env.BUILD_URL}
                """,
                to: 'm.toho@ecoles-epsi.net'
            )
        }
    }
}