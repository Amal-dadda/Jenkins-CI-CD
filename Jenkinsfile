pipeline {
    agent any

    environment {
        VENV_DIR   = ".venv"
        HOST       = "0.0.0.0"
        PORT       = "5000"
        APP_MODULE = "app:app"
    }

    // Partie 5 : triggers
    triggers {
        cron('H/5 * * * *')   // build toutes les 5 minutes
        githubPush()          // build à chaque push (webhook GitHub via ngrok)
    }

    stages {

        // Étape 1 : Checkout
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Amal-dadda/Jenkins-CI-CD.git',
                    credentialsId: 'github-token'
            }
        }

        // Étape 2 : Setup Virtual Environment
        stage('Setup Virtual Environment') {
            steps {
                sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    python --version
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest-cov
                '''
            }
        }

        // Étape 3 : Run Tests (Partie 6 : parallel, Partie 7 : when/not/changeset)
        stage('Run Tests') {
            when {
                not { changeset "README.md" }
            }
            parallel {
                stage('Tests - test_app.py') {
                    steps {
                        sh '''
                            . ${VENV_DIR}/bin/activate
                            python -m pytest test_app.py -v \
                                --cov=app --cov-report=term --cov-report=xml
                        '''
                    }
                }
                stage('Tests - test_app_2.py') {
                    steps {
                        sh '''
                            . ${VENV_DIR}/bin/activate
                            python -m pytest test_app_2.py -v
                        '''
                    }
                }
            }
        }

        // Étape 4 : Deploy
        stage('Deploy') {
            steps {
                // empêche Jenkins de tuer gunicorn à la fin du build
                withEnv(['JENKINS_NODE_COOKIE=dontKillMe']) {
                    sh '''#!/bin/bash
                        source ${VENV_DIR}/bin/activate
pkill -f "gunicorn --bind" || true; sleep 1
pkill -f "gunicorn --bind" || true; sleep 1
                        nohup gunicorn --bind ${HOST}:${PORT} ${APP_MODULE} > gunicorn.log 2>&1 &
                        echo "Gunicorn démarré sur http://${HOST}:${PORT}"
                    '''
                }
            }
        }
    }
}
