// PERSONA 4 · Pipeline de Jenkins
// Cada vez que alguien sube código, Jenkins corre todo en este orden.
// Requiere en Jenkins: Python 3, el plugin "SonarQube Scanner" y un servidor
// SonarQube configurado con el nombre 'SonarCloud'.

pipeline {
    agent any

    stages {
        stage('Preparar') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements.txt
                    playwright install --with-deps chromium
                '''
            }
        }

        stage('Pruebas unitarias') {
            steps {
                // tarifas.py y validacion.py: no necesitan base de datos ni navegador.
                // --junitxml guarda el resultado para que Jenkins lo muestre.
                sh '. .venv/bin/activate && pytest tests/unitarias --cov=app --cov-report=xml --junitxml=reporte-unitarias.xml'
            }
        }

        stage('SonarQube') {
            steps {
                withSonarQubeEnv('SonarCloud') {
                    sh 'sonar-scanner'
                }
            }
        }

        stage('Navegador (Playwright)') {
            steps {
                // conftest.py levanta la app con una base de datos temporal:
                // no hace falta arrancar el servidor ni crear la base a mano.
                sh '. .venv/bin/activate && pytest tests/e2e --junitxml=reporte-e2e.xml'
            }
        }
    }

    post {
        always { junit allowEmptyResults: true, testResults: 'reporte-*.xml' }
        success { echo 'Todo en verde: el código puede integrarse.' }
        failure { echo 'Algo falló: revisa la etapa en rojo.' }
    }
}
