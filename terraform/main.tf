provider "aws" {
  region = "us-east-1"
}

resource "aws_eks_cluster" "image_api_cluster" {
  name = "image-api-cluster"
  role_arn = var.eks_role_arn
  version = "1.23"
}

resource "aws_eks_node_group" "image_api_nodes" {
  cluster_name    = aws_eks_cluster.image_api_cluster.name
  node_group_name = "image-api-nodes"
  node_role_arn   = var.node_role_arn
  subnet_ids      = var.subnet_ids
  scaling_config {
    desired_size = 2
    max_size     = 3
    min_size     = 1
  }
}

output "cluster_endpoint" {
  value = aws_eks_cluster.image_api_cluster.endpoint
}

output "cluster_name" {
  value = aws_eks_cluster.image_api_cluster.name
}
