locals {
  imageLifePolicy = {
    "app" = 1
    "web" = 2
  }
}
resource "aws_ecr_repository" "app" {
  name                 = var.ecr_repository_back
  image_tag_mutability = "MUTABLE"
  encryption_configuration {
    encryption_type = "AES256"
  }
  force_delete = true

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "web" {
  name                 = var.ecr_repository_back_web
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

  repository = each.value == 1 ? aws_ecr_repository.app.name : aws_ecr_repository.web.name

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

