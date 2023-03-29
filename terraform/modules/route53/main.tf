data "aws_route53_zone" "selected" {
  name = var.dns_name
}

# ロードバランサーを既存のドメイン登録
resource "aws_route53_record" "this" {
  zone_id = data.aws_route53_zone.selected.zone_id
  name    = var.dns_name
  type    = "A"

  alias {
    name                   = var.alb.dns_name
    zone_id                = var.alb.zone_id
    evaluate_target_health = true
  }
}

# data "aws_route53_zone" "selected" {
#   name = var.dns_name
# }

# # ロードバランサーを既存のドメイン登録
# resource "aws_route53_record" "this" {
#   zone_id = data.aws_route53_zone.selected.zone_id
#   name    = var.dns_name
#   type    = "A"

#   alias {
#     name                   = var.alb.dns_name
#     zone_id                = var.alb.zone_id
#     evaluate_target_health = true
#   }
# }