pipeline {
        agent {
            docker {
                image 'python:3.11-slim'
            }
        }

        environment {
            PIP_DISABLE_PIP_VERSION_CHECK = 1
            PYTHONPATH = "${WORKSPACE}"
            PIP_CACHE_DIR = "${WORKSPACE}/.pip-cache"
        }

        stages {
            stage('Checkout') {
                steps {
                    checkout scm
                }
            }

            stage('Install dependencies') {
                steps {
                    sh 'python -m pip install --upgrade pip'
                    sh 'python -m pip install --cache-dir=$PIP_CACHE_DIR -r requirements.txt'
                }
            }

            stage('Run Pytest') {
                steps {
                    sh 'pytest --junitxml=pytest-report.xml'
                }
            }
        }

        post {
            always {
                junit 'pytest-report.xml'
                archiveArtifacts artifacts: 'pytest-report.xml', onlyIfSuccessful: true
            }
        }
    }