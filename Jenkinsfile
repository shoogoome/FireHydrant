pipeline {
    agent any

    stages {
        stage('update deploy file') {
            steps {
                sh 'cp /var/jenkins_home/deploy/firehydrant/deploy.sh .'
            }
        }
        stage('update code and build') {
            steps {
                sh 'chmod 700 ./deploy.sh'
                sh './deploy.sh'
            }
        }
    }
}
