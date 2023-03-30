variable "aws_region" {}
variable "aws_ssl_id" {}
variable "public_subnet" {}

variable "vpc_id" {
  type = string
}
variable "ecs_service_security_id" {
  type = string
}

variable "alb_security_policy" {
  default = "ELBSecurityPolicy-2016-08"
}