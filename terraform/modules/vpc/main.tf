locals {
  subnetPubOrgs = {
    "ap-northeast-1a" = "10.0.1.0/24"
    "ap-northeast-1c" = "10.0.2.0/24"
    "ap-northeast-1d" = "10.0.3.0/24"
  }
  subnetPriOrgs = {
    "ap-northeast-1a" = "10.0.4.0/24"
    "ap-northeast-1c" = "10.0.5.0/24"
    "ap-northeast-1d" = "10.0.6.0/24"
  }
}

# vpc
resource "aws_vpc" "this" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "sns-vpc"
  }
}

# パブリックサブネット
resource "aws_subnet" "public" {
  for_each = local.subnetPubOrgs

  vpc_id            = aws_vpc.this.id
  cidr_block        = each.value
  availability_zone = each.key

  tags = {
    Name = "sns-public-subnet-${each.key}"
  }

}

# プライベートサブネット
resource "aws_subnet" "private" {
  for_each = local.subnetPriOrgs

  vpc_id            = aws_vpc.this.id
  cidr_block        = each.value
  availability_zone = each.key

  tags = {
    Name = "sns-private-subnet-${each.key}"
  }
}

# インターネットゲートウェイ
resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id

  tags = {
    Name = "sns-vpc-internet-gateway"
  }
}

# ルートテーブル
# パブリック
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.this.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.this.id
  }

  tags = {
    Name = "sns-public-subnet-route-table"
  }
}

# プライベート
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.this.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_nat_gateway.private.id
  }

  tags = {
    Name = "sns-private-subnet-route-table"
  }
}

# サブネットとルートテーブル関連付け
# パブリック
resource "aws_route_table_association" "public" {
  for_each = aws_subnet.public

  subnet_id      = each.value.id
  route_table_id = aws_route_table.public.id
}

# プライベート
resource "aws_route_table_association" "private" {
  for_each = aws_subnet.private

  subnet_id      = each.value.id
  route_table_id = aws_route_table.private.id
}

# NAT ゲートウェイ
resource "aws_nat_gateway" "private" {
  allocation_id = var.elasticIp
  subnet_id     = aws_subnet.public["ap-northeast-1a"].id

  tags = {
    Name = "sns-private-subnet-nat-gateway"
  }

  depends_on = [aws_internet_gateway.this]
}