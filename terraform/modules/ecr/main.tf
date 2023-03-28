locals {
  imageLifePolicy = {
    "sns_back_app" = 1
    "sns_back_web" = 2
  }
}
resource "aws_ecr_repository" "sns_back_app" {
  name                 = "sns-back-app"
  image_tag_mutability = "MUTABLE"
  encryption_configuration {
    encryption_type = "AES256"
  }
  force_delete = true

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "sns_back_web" {
  name                 = "sns-back-web"
  image_tag_mutability = "MUTABLE"
  encryption_configuration {
    encryption_type = "AES256"
  }
  force_delete = true

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_lifecycle_policy" "foopolicy" {
  for_each = local.imageLifePolicy

  repository = each.value == 1 ? aws_ecr_repository.sns_back_app.name : aws_ecr_repository.sns_back_web.name

  policy = <<EOF
{
    "rules": [
        {
            "rulePriority": 1,
            "description": "Up to 10 images can be stored",
            "selection": {
                "tagStatus": "tagged",
                "tagPrefixList": ["v"],
                "countType": "imageCountMoreThan",
                "countNumber": 10
            },
            "action": {
                "type": "expire"
            }
        }
    ]
}
EOF
}
