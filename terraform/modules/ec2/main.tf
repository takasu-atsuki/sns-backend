# NAT ゲートウェイ専用
resource "aws_eip" "nat" {
  vpc = true
}