pipeline {
    agent any

    environment {
        DOCKER_USERNAME = credentials('dockerhub-username')
        DOCKER_PASSWORD = credentials('dockerhub-password')
        SONARQUBE_TOKEN = credentials('sonarqube-token')
        AWS_ACCESS_KEY_ID = credentials('aws-access-key')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-key')
        IMAGE_NAME = "nagarjuncsrecloud/image-api"
        KUBECONFIG_CREDENTIAL_ID = 'kubeconfig-aws'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/nagarjuncsrecloud/image-api.git'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    withSonarQubeEnv('SonarQube') {
                        sh 'sonar-scanner -Dsonar.projectKey=image-api -Dsonar.sources=. -Dsonar.host.url=http://18.188.224.206:9000 -Dsonar.login=$SONARQUBE_TOKEN'
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh './run_tests.sh'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t $IMAGE_NAME .
                    docker tag $IMAGE_NAME $IMAGE_NAME:latest
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('', 'dockerhub-credentials') {
                        sh 'docker push $IMAGE_NAME:latest'
                    }
                }
            }
        }

        stage('Deploy with Helm') {
            steps {
                script {
                    sh '''
                        helm upgrade --install image-api helm/ \
                        --set image.repository=$IMAGE_NAME \
                        --set image.tag=latest
                    '''
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
