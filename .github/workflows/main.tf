terraform {
  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 5.0"
    }
  }
}

provider "github" {
  token = var.github_token
}

resource "github_repository" "image-api" {
  name        = "image-api"
  description = "This repo is managed by Terraform"
  visibility  = "public"
}
