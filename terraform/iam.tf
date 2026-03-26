# GitHub Actions OIDC provider for assuming the ECR push role.
# AWS ignores the thumbprint for GitHub's OIDC endpoint, but the API still expects a value.
resource "aws_iam_openid_connect_provider" "github_actions" {
  count = var.create_github_actions_oidc_provider ? 1 : 0

  url = "https://token.actions.githubusercontent.com"

  client_id_list = [
    "sts.amazonaws.com"
  ]

  thumbprint_list = [
    "ffffffffffffffffffffffffffffffffffffffff"
  ]
}

locals {
  github_actions_oidc_provider_arn = var.create_github_actions_oidc_provider ? aws_iam_openid_connect_provider.github_actions[0].arn : var.github_actions_oidc_provider_arn
}

data "aws_iam_policy_document" "github_actions_assume_role" {
  statement {
    effect = "Allow"

    actions = [
      "sts:AssumeRoleWithWebIdentity"
    ]

    principals {
      type        = "Federated"
      identifiers = [local.github_actions_oidc_provider_arn]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:${var.github_repo}:ref:refs/heads/${var.github_actions_branch}"]
    }
  }
}

resource "aws_iam_role" "github_actions_ecr_push" {
  name               = "${var.app_name}-github-actions-ecr-push"
  assume_role_policy = data.aws_iam_policy_document.github_actions_assume_role.json
}

data "aws_iam_policy_document" "github_actions_ecr_push" {
  statement {
    effect = "Allow"

    actions = [
      "ecr:GetAuthorizationToken"
    ]

    resources = ["*"]
  }

  statement {
    effect = "Allow"

    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:CompleteLayerUpload",
      "ecr:InitiateLayerUpload",
      "ecr:PutImage",
      "ecr:UploadLayerPart"
    ]

    resources = [aws_ecr_repository.backend.arn]
  }
}

resource "aws_iam_role_policy" "github_actions_ecr_push" {
  name   = "${var.app_name}-github-actions-ecr-push"
  role   = aws_iam_role.github_actions_ecr_push.id
  policy = data.aws_iam_policy_document.github_actions_ecr_push.json
}

# Access role – allows App Runner to pull images from ECR
resource "aws_iam_role" "app_runner_ecr_access" {
  name = "${var.app_name}-app-runner-ecr-access"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "build.apprunner.amazonaws.com" }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "app_runner_ecr_access" {
  role       = aws_iam_role.app_runner_ecr_access.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
}

# Instance role – assumed by the running container at runtime
resource "aws_iam_role" "app_runner_instance" {
  name = "${var.app_name}-app-runner-instance"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "tasks.apprunner.amazonaws.com" }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

# Allow the running container to read objects from the data bucket
resource "aws_iam_role_policy" "app_runner_s3_read" {
  name = "${var.app_name}-s3-read"
  role = aws_iam_role.app_runner_instance.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["s3:GetObject", "s3:ListBucket"]
        Resource = [
          aws_s3_bucket.data.arn,
          "${aws_s3_bucket.data.arn}/*"
        ]
      }
    ]
  })
}
