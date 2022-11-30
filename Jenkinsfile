pipeline {
    agent any
    stages {
        stage('Production') {
            steps {
                script {
                    sh "docker compose up --build --detach"
                }
            }
        }
    }
    post {
        success {
            sh """curl -s \
            -X POST \
            --user $MAIL_JET_API_KEY:$MAIL_JET_API_SECRET \
            https://api.mailjet.com/v3.1/send \
            -H "Content-Type:application/json" \
            -d '{
                "Messages":[
                        {
                                "From": {
                                        "Email": $MAIL_JET_EMAIL_ADDRESS,
                                        "Name": "ArpanSahuOne Jenkins Notification"
                                },
                                "To": [
                                        {
                                                "Email": $MY_EMAIL_ADDRESS,
                                                "Name": "arpan sahu"
                                        }
                                ],
                                "Subject": "arpansahu_dot_me deployed succcessfully",
                                "TextPart": "Hola arpan, your project arpansahu_dot_me is now deployed",
                                "HTMLPart": "<h3>Hola arpan, your project arpansahu_dot_me is now deployed </h3> <br> <p> Build Name: ${currentBuild.fullDisplayName} <br> Build URL: ${env.BUILD_URL}</p>"
                        }
                ]
            }'"""
        }
    }
}
