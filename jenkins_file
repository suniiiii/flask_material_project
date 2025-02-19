pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Replace the URL with your repository URL and branch if needed
                git url: 'https://github.com/suniiiii/flask_material_project.git', branch: 'main'
            }
        }
        stage('Set Up Environment') {
            steps {
                // Create a virtual environment and install dependencies
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install --upgrade pip'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                // Run tests if you have any (e.g., using pytest)
                sh './venv/bin/python -m pytest'
            }
        }
        stage('Deploy') {
            steps {
                // Example: Restart your Flask app via systemd or another method.
                // Adjust this step to suit your deployment process.
                sh 'sudo systemctl restart flask_app.service'
            }
        }
    }

    post {
        failure {
            // Notify if the build fails, e.g., email or Slack notifications.
            echo 'Build or Deployment failed!'
        }
        success {
            echo 'Deployment succeeded!'
        }
    }
}
