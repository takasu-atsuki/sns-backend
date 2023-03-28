output "private_subnet" {
  value = aws_subnet.private
}

output "public_subnet" {
  value = aws_subnet.public
}

output "vpc_id" {
  description = "vpc紐付けのため"
  value       = aws_vpc.this.id
}