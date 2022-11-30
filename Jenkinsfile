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
                                        "Email": "admin@arpansahu.me",
                                        "Name": "Mailjet Pilot"
                                },
                                "To": [
                                        {
                                                "Email": "arpanrocks95@gmail.com",
                                                "Name": "passenger 1"
                                        }
                                ],
                                "Subject": "Your email flight plan!",
                                "TextPart": "Dear passenger 1, welcome to Mailjet! May the delivery force be with you!",
                                "HTMLPart": "<h3>Dear passenger 1, welcome to <a>Mailjet</a>!</h3><br />May the delivery force be with you!"
                        }
                ]
            }'"""
        }
    }
}
