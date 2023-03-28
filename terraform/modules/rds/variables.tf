variable "private_subnet" {}
variable "vpc_id" {
  type = string
}

variable "rds_name" {
  type    = string
  default = "sns-rds"
}

variable "db_name" {
  type = string
}

variable "db_user" {
  type = string
}

variable "mysql_version" {
  type    = string
  default = "8.0.32"
}

variable "db_password" {
  type = string
}
