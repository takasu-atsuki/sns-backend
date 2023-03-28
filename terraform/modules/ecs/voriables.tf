variable "private_subnet" {}
variable "ecs_task_role" {}
variable "db_name" {}
variable "db_host" {}
variable "db_user" {}
variable "db_pass" {}
variable "db_port" {}
variable "front_url" {}
variable "arrowed_host" {}
variable "aws_access_key_id" {}
variable "aws_secret_access_key" {}
variable "aws_s3_backet_name" {}
variable "debug" {}
variable "secret_key" {}

variable "app_name" {
  type = string
}
variable "web_name" {
  type = string
}
variable "vpc_id" {
  type = string
}
variable "alb_target_group_arn" {
  type = string
}