variable "aws_region" {
  description = "The AWS region to deploy resources in."
  type        = string
  default     = "us-east-1" # You can change this default
}

variable "project_name" {
  description = "A unique name for the project, used for resource naming."
  type        = string
  default     = "linkedin-scraper"
}

variable "notion_token" {
  description = "Notion Integration Token for API access."
  type        = string
  sensitive   = true # Mark as sensitive to prevent logging
}

variable "notion_database_id" {
  description = "The ID of the Notion database to sync job data to."
  type        = string
  sensitive   = true # Mark as sensitive to prevent logging
}

variable "ecr_repository_name" {
  description = "Name for the ECR repository."
  type        = string
  default     = "linkedin-job-scraper"
}

variable "container_port" {
  description = "Port the container listens on (if any). Not used for this script but good practice for containers."
  type        = number
  default     = 80
}

variable "fargate_cpu" {
  description = "The number of CPU units reserved for the Fargate task."
  type        = number
  default     = 512 # 0.5 vCPU
}

variable "fargate_memory" {
  description = "The amount of memory (in MiB) reserved for the Fargate task."
  type        = number
  default     = 1024 # 1 GB
}

variable "schedule_expression" {
  description = "The cron expression for scheduling the Fargate task (e.g., cron(0 9 * * ? *))."
  type        = string
  default     = "cron(0 9 * * ? *)" # Every day at 09:00 AM UTC
}
