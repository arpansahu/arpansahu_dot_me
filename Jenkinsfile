pipeline {
    agent any

    stages {
        stage('Deploy') {
            steps {
                script {
                    sh "docker rm -f arpansahu_dot_me"
                    sh "docker compose up --build --detach"
                }
            }
        }
    }
}
