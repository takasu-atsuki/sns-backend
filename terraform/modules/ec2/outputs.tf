output "elasticIp" {
  description = "Associated with NatGateWay"
  value       = aws_eip.nat.id
}