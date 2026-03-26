terraform {
  required_version = ">= 1.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Uncomment and configure to store state remotely
  # backend "s3" {
  #   bucket = "your-terraform-state-bucket"
  #   key    = "nyc-taxi-dashboard/terraform.tfstate"
  #   region = "us-east-1"
  # }
}

provider "aws" {
  region = var.aws_region
}
