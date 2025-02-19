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
                // Run tests using pytest (adjust or remove this stage if you don't have tests)
                sh './venv/bin/python -m pytest'
            }
        }
        
        stage('Deploy') {
            steps {
                // Restart your Flask application via systemd
                // Make sure the Jenkins user can run this command without a password
                sh 'sudo systemctl restart flask_app.service'
            }
        }
    }
    
    post {
        failure {
            echo 'Build or Deployment failed!'
            // You can add additional notification steps here (e.g., email or Slack)
        }
        success {
            echo 'Deployment succeeded!'
        }
    }
}
