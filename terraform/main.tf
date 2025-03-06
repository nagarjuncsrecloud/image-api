provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_deployment" "image_api" {
  metadata {
    name = "image-api"
  }

  spec {
    replicas = 3
    selector {
      match_labels = {
        app = "image-api"
      }
    }
    template {
      metadata {
        labels = {
          app = "image-api"
        }
      }
      spec {
        container {
          name  = "image-api"
          image = "nagarjuncsrecloud/image-api:latest"

          port {
            container_port = 8000
          }

          env_from {
            secret_ref {
              name = "api-secrets"
            }
          }

          env {
            name  = "ENV"
            value = "production"
          }

          liveness_probe {
            http_get {
              path = "/health"
              port = 8000
            }
            initial_delay_seconds = 5
            period_seconds        = 10
          }

          readiness_probe {
            http_get {
              path = "/health"
              port = 8000
            }
            initial_delay_seconds = 3
            period_seconds        = 5
          }

          resources {
            limits = {
              cpu    = "500m"
              memory = "512Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "256Mi"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "image_api_service" {
  metadata {
    name = "image-api-service"
  }

  spec {
    selector = {
      app = "image-api"
    }

    port {
      protocol    = "TCP"
      port        = 80
      target_port = 8000
    }

    type = "NodePort"
  }
}

resource "kubernetes_deployment" "sonarqube" {
  metadata {
    name = "sonarqube"
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "sonarqube"
      }
    }
    template {
      metadata {
        labels = {
          app = "sonarqube"
        }
      }
      spec {
        container {
          image = "sonarqube:latest"
          name  = "sonarqube"
          port {
            container_port = 9000
          }
        }
      }
    }
  }
}
