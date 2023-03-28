# NATゲートウェイ用
resource "aws_eip" "nat" {
  vpc = true
}