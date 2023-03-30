variable "private_subnet" {}
variable "public_subnet" {}
variable "db_password" {}
variable "db_user" {}
variable "db_name" {}
variable "db_port" {}

variable "vpc_id" {
  type = string
}

variable "rds_name" {
  type    = string
  default = "sns-rds"
}

variable "mysql_version" {
  type    = string
  default = "8.0.32"
}


