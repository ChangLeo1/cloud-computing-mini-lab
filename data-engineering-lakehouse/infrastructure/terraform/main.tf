terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" { region = var.aws_region }

resource "aws_s3_bucket" "lake" { bucket = var.bucket_name }

resource "aws_s3_bucket_versioning" "lake" {
  bucket = aws_s3_bucket.lake.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_glue_catalog_database" "energy" { name = "energy_lakehouse" }

resource "aws_cloudwatch_log_group" "pipeline" {
  name              = "/energy-lakehouse/pipeline"
  retention_in_days = 14
}

resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "energy-lakehouse-lambda-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 0
  dimensions = { FunctionName = "energy-file-validator" }
}

resource "aws_ecr_repository" "fargate_ingestion" { name = "energy-ingestion" }

output "bucket_name" { value = aws_s3_bucket.lake.bucket }
