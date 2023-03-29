# # s3
# resource "aws_s3_bucket" "this" {
#   bucket        = "sns-media-backet"
#   force_destroy = true
# }

# data "aws_caller_identity" "current" {}

# # バケットポリシーとバケット紐付け
# resource "aws_s3_bucket_policy" "this" {
#   bucket = aws_s3_bucket.this.id
#   policy = data.aws_iam_policy_document.s3_backet_policy.json
# }

# # バケットポリシー
# data "aws_iam_policy_document" "s3_backet_policy" {
#   statement {
#     sid = "public-open"
#     principals {
#       type        = "AWS"
#       identifiers = ["*"]
#     }

#     actions = [
#       "s3:PutObject",
#       "s3:GetObject",
#       "s3:ListBucket",
#     ]

#     resources = [
#       aws_s3_bucket.this.arn,
#       "${aws_s3_bucket.this.arn}/*",
#     ]
#   }
#   statement {
#     sid = "owner-open"
#     principals {
#       type        = "AWS"
#       identifiers = [data.aws_caller_identity.current.arn]
#     }

#     actions = [
#       "s3:*"
#     ]

#     resources = [
#       aws_s3_bucket.this.arn,
#       "${aws_s3_bucket.this.arn}/*"
#     ]
#   }
# }

# resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
#   bucket                = aws_s3_bucket.this.id
#   expected_bucket_owner = data.aws_caller_identity.current.account_id

#   rule {
#     bucket_key_enabled = true
#   }
# }
# s3
resource "aws_s3_bucket" "this" {
  bucket        = "sns-media-backet"
  force_destroy = true
}

data "aws_caller_identity" "current" {}

# バケットポリシーとバケット紐付け
resource "aws_s3_bucket_policy" "this" {
  bucket = aws_s3_bucket.this.id
  policy = data.aws_iam_policy_document.s3_backet_policy.json
}

# バケットポリシー
data "aws_iam_policy_document" "s3_backet_policy" {
  statement {
    sid = "public-open"
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }

    actions = [
      "s3:PutObject",
      "s3:GetObject",
      "s3:ListBucket",
    ]

    resources = [
      aws_s3_bucket.this.arn,
      "${aws_s3_bucket.this.arn}/*",
    ]
  }
  statement {
    sid = "owner-open"
    principals {
      type        = "AWS"
      identifiers = [data.aws_caller_identity.current.arn]
    }

    actions = [
      "s3:*"
    ]

    resources = [
      aws_s3_bucket.this.arn,
      "${aws_s3_bucket.this.arn}/*"
    ]
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  bucket                = aws_s3_bucket.this.id
  expected_bucket_owner = data.aws_caller_identity.current.account_id

  rule {
    bucket_key_enabled = true
  }
}
