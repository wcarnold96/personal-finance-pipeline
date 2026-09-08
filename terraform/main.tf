resource "aws_s3_bucket" "finance_lake" {
  bucket = var.bucket_name

  tags = var.tags
}

provider "aws" {
  region = var.aws_region
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
