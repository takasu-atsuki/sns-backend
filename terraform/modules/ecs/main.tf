# クラスター
resource "aws_ecs_cluster" "this" {
  name = "sns"
}

data "aws_ecr_repository" "app" {
  name = var.app_name
}

data "aws_ecr_repository" "web" {
  name = var.web_name
}

data "aws_caller_identity" "current" {}
data "aws_ecs_task_definition" "new" {
  task_definition = aws_ecs_task_definition.this.family
}

# タスク定義
resource "aws_ecs_task_definition" "this" {
  family                   = "sns-app"
  execution_role_arn       = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.ecs_task_role}"
  task_role_arn            = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.ecs_task_role}"
  cpu                      = ".25 vCPU"
  memory                   = ".5 GB"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  container_definitions = jsonencode([
    {
      name      = var.app_name
      image     = "${data.aws_ecr_repository.app.repository_url}:latest"
      essential = true
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
          appProtocol   = "http"
        }
      ]
      secrets = [
        {
          name : "SQL_NAME"
          valueFrom : var.db_name
        },
        {
          name : "SQL_HOST"
          valueFrom : var.db_host
        },
        {
          name : "SQL_USER"
          valueFrom : var.db_user
        },
        {
          name : "SQL_PASSWORD"
          valueFrom : var.db_pass
        },
        {
          name : "SQL_PORT"
          valueFrom : var.db_port
        },
        {
          name : "FRONT_URI"
          valueFrom : var.front_url
        },
        {
          name : "ALLOWED_HOSTS"
          valueFrom : var.arrowed_host
        },
        {
          name : "AWS_ACCESS_KEYID"
          valueFrom : var.aws_access_key_id
        },
        {
          name : "AWS_SECRET_ACCESS_KEY"
          valueFrom : var.aws_secret_access_key
        },
        {
          name : "AWS_S3_BACKET_NAME"
          valueFrom : var.aws_s3_backet_name
        },
        {
          name : "DEBUG"
          valueFrom : var.debug
        },
        {
          name : "SECRET_KEY"
          valueFrom : var.secret_key
        }
      ]
    },
    {
      name      = var.web_name
      image     = "${data.aws_ecr_repository.web.repository_url}:latest"
      essential = true
      portMappings = [
        {
          containerPort = 8080
          hostPort      = 8080
          appProtocol   = "http"
        }
      ]
    }
  ])
  # container_definitions    = file("${path.module}/files/sns_task.json")
  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }

  task_definition = data.aws_ecs_task_definition.new.arn
}

# サービス
resource "aws_ecs_service" "this" {
  name                   = "sns-back-service"
  cluster                = aws_ecs_cluster.this.id
  task_definition        = aws_ecs_task_definition.this.arn
  desired_count          = 1
  enable_execute_command = true
  force_new_deployment   = true
  launch_type            = "FARGATE"
  platform_version       = "LATEST"
  scheduling_strategy    = "REPLICA"

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  network_configuration {
    subnets          = [for subnet in var.private_subnet : subnet.id]
    security_groups  = [aws_security_group.sns_back_sg.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = var.alb_target_group_arn
    container_name   = var.web_name
    container_port   = 8080
  }
}

data "aws_vpc" "selected" {
  id = var.vpc_id
}

# ECSのセキュリティグループ
resource "aws_security_group" "sns_back_sg" {
  name   = "sns-back-sg"
  vpc_id = var.vpc_id

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = [data.aws_vpc.selected.cidr_block]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}


