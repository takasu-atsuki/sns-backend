variable "vpc_id" {
  type = string
}
variable "ecs_service_security_id" {
  type = string
}

variable "public_subnet" {}

variable "alb_security_policy" {
  default = "ELBSecurityPolicy-2016-08"
}