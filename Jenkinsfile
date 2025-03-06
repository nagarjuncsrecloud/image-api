pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "nagarjuncsrecloud/image-api"
        DOCKER_TAG = "latest"
        KUBE_NAMESPACE = "image-api"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git credentialsId: 'github-ssh', url: 'git@github.com:nagarjuncsrecloud/image-api.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    withDockerRegistry([credentialsId: 'docker-hub', url: '']) {
                        sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    }
                }
            }
        }

        stage('Start Minikube') {
            steps {
                script {
                    sh "minikube start --driver=docker"
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                script {
                    sh "kubectl config use-context minikube"
                    sh "kubectl create namespace ${KUBE_NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -"
                    sh "helm upgrade --install image-api helm/ --namespace ${KUBE_NAMESPACE} --set image.repository=${DOCKER_IMAGE},image.tag=${DOCKER_TAG}"
                }
            }
        }
    }

    post {
        success {
            echo "Deployment Successful!"
        }
        failure {
            echo "Deployment Failed!"
        }
    }
}
