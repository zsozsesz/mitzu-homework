resource "aws_amplify_app" "frontend" {
  name        = "${var.app_name}-frontend"
  repository  = "https://github.com/${var.github_repo}"
  oauth_token = var.github_oauth_token
  platform    = "WEB"

  # Pass the App Runner HTTPS URL as a build-time env var
  environment_variables = {
    VITE_API_URL = "https://${aws_apprunner_service.backend.service_url}"
  }

  build_spec = <<-YAML
    version: 1
    applications:
      - appRoot: frontend
        frontend:
          phases:
            preBuild:
              commands:
                - npm ci
            build:
              commands:
                - npm run build
          artifacts:
            baseDirectory: dist
            files:
              - "**/*"
          cache:
            paths:
              - node_modules/**/*
  YAML

  # Rewrite all paths to index.html for client-side routing
  custom_rule {
    source = "</^[^.]+$|\\.(?!(css|gif|ico|jpg|js|png|txt|svg|woff|woff2|ttf|map|json)$)([^.]+$)/>"
    status = "200"
    target = "/index.html"
  }
}

resource "aws_amplify_branch" "main" {
  app_id      = aws_amplify_app.frontend.id
  branch_name = var.amplify_branch
  display_name = replace(var.amplify_branch, "/", "-")

  enable_auto_build = true
  framework         = "React"
  stage             = "PRODUCTION"
}
