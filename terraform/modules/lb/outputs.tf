output "alb_target_group_arn" {
  value = aws_lb_target_group.this.arn
}

output "alb_security_group" {
  value = aws_security_group.sns_service_alb_sg.id
}

output "alb" {
  value = aws_lb.this
}