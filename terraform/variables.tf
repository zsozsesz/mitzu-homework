variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "eu-west-1"
}

variable "app_name" {
  description = "Short application name used to name resources"
  type        = string
  default     = "nyc-taxi-dashboard"
}

variable "github_repo" {
  description = "GitHub repository in owner/name format (e.g. acme/nyc-taxi-dashboard)"
  type        = string
}

variable "github_oauth_token" {
  description = "Deprecated fallback token for legacy Amplify OAuth GitHub connections"
  type        = string
  default     = null
  sensitive   = true
}

variable "github_access_token" {
  description = "GitHub personal access token used by Amplify GitHub App access"
  type        = string
  default     = null
  sensitive   = true
}

variable "github_actions_branch" {
  description = "Git branch allowed to assume the GitHub Actions AWS role"
  type        = string
  default     = "feat/deployment"
}

variable "create_github_actions_oidc_provider" {
  description = "Whether Terraform should create the shared GitHub Actions OIDC provider in IAM"
  type        = bool
  default     = true
}

variable "github_actions_oidc_provider_arn" {
  description = "Existing GitHub Actions OIDC provider ARN to use when create_github_actions_oidc_provider is false"
  type        = string
  default     = null
}

variable "amplify_branch" {
  description = "Git branch that Amplify deploys from"
  type        = string
  default     = "main"
}

variable "app_runner_cpu" {
  description = "vCPU units for App Runner (256|512|1024|2048|4096 or 0.25 vCPU|0.5 vCPU|1 vCPU|2 vCPU|4 vCPU)"
  type        = string
  default     = "0.5 vCPU"
}

variable "app_runner_memory" {
  description = "Memory for App Runner (512|1024|2048|3072|4096|6144|8192|10240|12288 or 0.5 GB|1 GB|2 GB|...)"
  type        = string
  default     = "1 GB"
}

variable "data_s3_key" {
  description = "S3 object key of the Parquet file inside the data bucket (e.g. yellow_tripdata_2024-01.parquet)"
  type        = string
  default     = "yellow_tripdata_2024-01.parquet"
}
