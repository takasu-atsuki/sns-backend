variable "private_subnet" {}
variable "ecs_task_role" {}
variable "app_name" {}
variable "web_name" {}
variable "vpc_id" {
  type = string
}
variable "alb_target_group_arn" {
  type = string
}