# RDS
resource "aws_db_instance" "this" {
  allocated_storage      = 10
  identifier             = var.rds_name
  storage_type           = "gp2"
  db_name                = var.db_name
  engine                 = "mysql"
  engine_version         = var.mysql_version
  instance_class         = "db.t2.micro"
  username               = var.db_user
  password               = var.db_password
  max_allocated_storage  = 0
  multi_az               = false
  network_type           = "IPV4"
  db_subnet_group_name   = aws_db_subnet_group.this.name
  vpc_security_group_ids = [aws_security_group.rds_security_group.id]
  skip_final_snapshot    = true
}

# サブネットグループ
resource "aws_db_subnet_group" "this" {

  name       = "sns-rds-subnet-groups"
  subnet_ids = [for subnet in var.private_subnet : subnet.id]

  tags = {
    Name = "sns_private_rdb_subnet_group"
  }
}

data "aws_vpc" "selected" {
  id = var.vpc_id
}

# セキュリティグループ
resource "aws_security_group" "rds_security_group" {
  name   = "sns-rds-sg"
  vpc_id = var.vpc_id

  ingress {
    from_port   = var.db_port
    to_port     = var.db_port
    protocol    = "tcp"
    # cidr_blocks = [data.aws_vpc.selected.cidr_block]
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}