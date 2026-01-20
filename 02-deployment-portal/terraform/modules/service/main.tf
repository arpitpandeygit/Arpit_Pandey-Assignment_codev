variable "service_name" {
  type = string
}

module "ecr" {
  source       = "../ecr"
  service_name = var.service_name
}

module "iam" {
  source       = "../iam"
  service_name = var.service_name
}

