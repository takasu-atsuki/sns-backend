variable "private_subnet" {}
variable "vpc_id" {
  type = string
}
variable "alb_target_group_arn" {
  type = string
}

variable "app_name" {
  type    = string
  default = "sns-back-app"
}

variable "web" {
  type    = string
  default = "sns-back-web"
}