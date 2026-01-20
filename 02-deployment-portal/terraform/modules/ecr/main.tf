variable "service_name" {
  type = string
}

resource "aws_ecr_repository" "this" {
  name = var.service_name
}

