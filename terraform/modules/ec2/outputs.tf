# NATゲートウェイのElasticIP
output "elasticIp" {
  value = aws_eip.nat.id
}