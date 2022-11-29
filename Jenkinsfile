pipeline {
    agent any

    stages {
        stage('Deploy') {
            steps {
                docker compose up --build --detach
            }
        }
    }
}
