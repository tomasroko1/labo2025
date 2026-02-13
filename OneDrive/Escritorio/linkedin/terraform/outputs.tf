output "ecr_repository_url" {
  description = "The URL of the ECR repository."
  value       = aws_ecr_repository.app.repository_url
}

output "ecs_cluster_name" {
  description = "The name of the ECS cluster."
  value       = aws_ecs_cluster.main.name
}

output "ecs_task_definition_arn" {
  description = "The ARN of the ECS task definition."
  value       = aws_ecs_task_definition.app.arn
}

output "cloudwatch_log_group_name" {
  description = "The name of the CloudWatch Log Group for the Fargate task."
  value       = aws_cloudwatch_log_group.app_logs.name
}
