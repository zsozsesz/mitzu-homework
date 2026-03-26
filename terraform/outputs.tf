output "data_bucket_name" {
  description = "S3 bucket name – upload the Parquet file here before starting the backend"
  value       = aws_s3_bucket.data.bucket
}

output "ecr_repository_url" {
  description = "ECR repository URL – use this when tagging and pushing the backend image"
  value       = aws_ecr_repository.backend.repository_url
}

output "backend_url" {
  description = "App Runner service URL (HTTPS)"
  value       = "https://${aws_apprunner_service.backend.service_url}"
}

output "frontend_url" {
  description = "Amplify default domain (HTTPS)"
  value       = "https://${var.amplify_branch}.${aws_amplify_app.frontend.default_domain}"
}

output "github_actions_role_arn" {
  description = "Set GitHub secret AWS_ROLE_TO_ASSUME to this ARN"
  value       = aws_iam_role.github_actions_ecr_push.arn
}
