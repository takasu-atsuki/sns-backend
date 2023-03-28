# ロードバランサー
resource "aws_lb" "this" {
  name                       = "sns-back-service-alb"
  internal                   = false
  load_balancer_type         = "application"
  security_groups            = [aws_security_group.sns_service_alb_sg.id]
  subnets                    = [for subnet in var.public_subnet : subnet.id]
  ip_address_type            = "ipv4"
  enable_deletion_protection = false
}

# ロードバランサーのターゲットグループ
resource "aws_lb_target_group" "this" {
  name        = "sns-service-alb-target-group"
  port        = 8080
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    matcher = 200
    path    = "/healthcheck.html"
  }

}

data "aws_caller_identity" "current" {}

# ロードバランサーのリスナー
resource "aws_lb_listener" "this" {
  load_balancer_arn = aws_lb.this.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = var.alb_security_policy
  certificate_arn   = "arn:aws:acm:ap-northeast-1:${data.aws_caller_identity.current.account_id}:certificate/aef90f51-e7ab-477d-aa62-609c315c0a00"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.this.arn
  }
}


# ロードバランサーのセキュリティグループ
resource "aws_security_group" "sns_service_alb_sg" {
  name        = "sns_service_alb_sg"
  description = "Security groups tied to application load balancers tied to services"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [var.ecs_service_security_id]
  }
}