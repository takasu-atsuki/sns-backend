locals {

}

resource "aws_vpc" "this" {
  cidr_block       = "10.0.0.0/16"

  tags = {
    Name = "sns-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.this.id
  enable_dns64 = true
  cidr_block = "10.0.1.0/24"

  tags = {
    Name = "Main"
  }
}