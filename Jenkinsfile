pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Clone the repository from GitHub
                git url: 'https://github.com/suniiiii/flask_material_project.git', branch: 'main'
            }
        }
        
        stage('Set Up Environment') {
            steps {
                // Create a virtual environment, upgrade pip, and install dependencies
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install --upgrade pip'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    // Run tests using pytest and capture the exit code
                    def result = sh(script: './venv/bin/python -m pytest', returnStatus: true)
                    if (result == 5) {
                        echo "No tests collected. Continuing pipeline."
                    } else if (result != 0) {
                        error "Tests failed with exit code ${result}."
                    } else {
                        echo "Tests passed successfully."
                    }
                }
            }
        }
        
        stage('Deploy') {
            steps {
                // Restart the Flask application using systemd (ensure Jenkins has passwordless sudo)
                sh 'sudo systemctl restart flask_app.service'
            }
        }
    }
    
    post {
        failure {
            echo 'Build or Deployment failed!'
            // Additional notifications (email, Slack, etc.) can be added here
        }
        success {
            echo 'Deployment succeeded!'
        }
    }
}
