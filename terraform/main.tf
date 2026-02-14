# AWS VPC for our Fargate Task
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.project_name}-vpc"
  }
}

# Public Subnets for the VPC
resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.${count.index}.0/24"
  map_public_ip_on_launch = true
  availability_zone       = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "${var.project_name}-public-subnet-${count.index}"
  }
}

# Internet Gateway for public subnet access
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project_name}-igw"
  }
}

# Route Table for public subnet
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${var.project_name}-public-rt"
  }
}

# Associate Route Table with Public Subnets
resource "aws_route_table_association" "public" {
  count          = length(aws_subnet.public)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# Security Group for Fargate Task
resource "aws_security_group" "fargate_sg" {
  vpc_id      = aws_vpc.main.id
  name        = "${var.project_name}-fargate-sg"
  description = "Allow outbound internet access for Fargate task"

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-fargate-sg"
  }
}

# Data source for availability zones
data "aws_availability_zones" "available" {
  state = "available"
}

# ECR Repository
resource "aws_ecr_repository" "app" {
  name                 = var.ecr_repository_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "${var.project_name}-ecr"
  }
}

# IAM Role for ECS Task Execution (allows ECS to pull images and send logs)
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "${var.project_name}-ecs-task-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# IAM Role for the ECS Task (allows the container to perform actions, e.g., Notion API calls)
resource "aws_iam_role" "ecs_task_role" {
  name = "${var.project_name}-ecs-task-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

# CloudWatch Log Group for ECS Task
resource "aws_cloudwatch_log_group" "app_logs" {
  name              = "/ecs/${var.project_name}-task"
  retention_in_days = 7 # Adjust as needed

  tags = {
    Name = "${var.project_name}-logs"
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-cluster"

  tags = {
    Name = "${var.project_name}-cluster"
  }
}

# ECS Task Definition
resource "aws_ecs_task_definition" "app" {
  family                   = "${var.project_name}-task"
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn # Assign the task role

  container_definitions = jsonencode([
    {
      name      = var.project_name,
      image     = "${aws_ecr_repository.app.repository_url}:latest",
      cpu       = var.fargate_cpu,
      memory    = var.fargate_memory,
      essential = true,
      environment = [
        {
          name  = "NOTION_TOKEN",
          value = var.notion_token
        },
        {
          name  = "NOTION_DATABASE_ID",
          value = var.notion_database_id
        },
        {
          name  = "RAPIDAPI_KEY",
          value = var.rapidapi_key
        }
      ],
      logConfiguration = {
        logDriver = "awslogs",
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.app_logs.name,
          "awslogs-region"        = var.aws_region,
          "awslogs-stream-prefix" = "ecs"
        }
      },
      # If your script were a server, you'd define portMappings here
      # portMappings = [
      #   {
      #     containerPort = var.container_port,
      #     hostPort      = var.container_port,
      #     protocol      = "tcp"
      #   }
      # ]
    }
  ])

  tags = {
    Name = "${var.project_name}-task"
  }
}

# EventBridge Rule to schedule the Fargate task
resource "aws_cloudwatch_event_rule" "schedule" {
  name                = "${var.project_name}-schedule"
  description         = "Schedule for the LinkedIn job scraper Fargate task"
  schedule_expression = var.schedule_expression
  is_enabled          = true

  tags = {
    Name = "${var.project_name}-schedule"
  }
}

# IAM role for EventBridge to invoke ECS tasks
resource "aws_iam_role" "eventbridge_ecs_role" {
  name = "${var.project_name}-eventbridge-ecs-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "events.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "eventbridge_ecs_policy" {
  name = "${var.project_name}-eventbridge-ecs-policy"
  role = aws_iam_role.eventbridge_ecs_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "ecs:RunTask",
        ],
        Effect = "Allow",
        Resource = [
          aws_ecs_task_definition.app.arn,
          # Need to specify specific cluster if not using all
          "arn:aws:ecs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:cluster/${aws_ecs_cluster.main.name}"
        ]
      },
      {
        Action = [
          "iam:PassRole",
        ],
        Effect = "Allow",
        Resource = [
          aws_iam_role.ecs_task_execution_role.arn,
          aws_iam_role.ecs_task_role.arn
        ]
      }
    ]
  })
}

# EventBridge Target to trigger the Fargate task
resource "aws_cloudwatch_event_target" "run_fargate_task" {
  rule     = aws_cloudwatch_event_rule.schedule.name
  arn      = aws_ecs_cluster.main.arn
  role_arn = aws_iam_role.eventbridge_ecs_role.arn
  input = jsonencode({
    "containerOverrides" : [],
    "cpu" : var.fargate_cpu,
    "memory" : var.fargate_memory,
    "taskDefinition" : aws_ecs_task_definition.app.family,
    "cluster" : aws_ecs_cluster.main.name,
    "group" : "ecs-event-triggered", # Optional: Group tasks triggered by EventBridge
    "launchType" : "FARGATE",
    "networkConfiguration" : {
      "awsvpcConfiguration" : {
        "subnets" : aws_subnet.public[*].id,
        "assignPublicIp" : "ENABLED",
        "securityGroups" : [aws_security_group.fargate_sg.id]
      }
    }
  })
  ecs_target {
    task_definition_arn = aws_ecs_task_definition.app.arn
    task_count          = 1
    launch_type         = "FARGATE"
    network_configuration {
      subnets          = aws_subnet.public[*].id
      assign_public_ip = true
      security_groups  = [aws_security_group.fargate_sg.id]
    }
    platform_version = "LATEST"
  }
}

# Data source for AWS account ID
data "aws_caller_identity" "current" {}
