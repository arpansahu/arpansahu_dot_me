pipeline {
    agent any

    stages {
        stage('Deploy') {
            steps {
                script {
                    docker compose up --build --detach
                }
            }
        }
    }
}
