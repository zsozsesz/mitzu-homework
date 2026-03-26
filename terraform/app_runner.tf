resource "aws_apprunner_service" "backend" {
  service_name = "${var.app_name}-backend"

  source_configuration {
    authentication_configuration {
      access_role_arn = aws_iam_role.app_runner_ecr_access.arn
    }

    image_repository {
      image_identifier      = "${aws_ecr_repository.backend.repository_url}:latest"
      image_repository_type = "ECR"

      image_configuration {
        port = "8000"

        runtime_environment_variables = {
          DATA_S3_BUCKET = aws_s3_bucket.data.bucket
          DATA_S3_KEY    = var.data_s3_key
        }
      }
    }

    # App Runner automatically redeploys when the latest image is updated in ECR.
    auto_deployments_enabled = true
  }

  instance_configuration {
    cpu               = var.app_runner_cpu
    memory            = var.app_runner_memory
    instance_role_arn = aws_iam_role.app_runner_instance.arn
  }

  health_check_configuration {
    protocol            = "HTTP"
    path                = "/summary"
    interval            = 10
    timeout             = 5
    healthy_threshold   = 1
    unhealthy_threshold = 5
  }
}
