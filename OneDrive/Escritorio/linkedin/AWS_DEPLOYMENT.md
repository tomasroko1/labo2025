# AWS Deployment Guide

## GitHub Actions Deployment

This repository uses GitHub Actions to build and deploy the LinkedIn job scraper to AWS ECS.

### Prerequisites

1. **Push this code to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Add GitHub Actions workflow for AWS deployment"
   git push origin main
   ```

2. **Set up GitHub Secrets** (Required for AWS authentication):

   Go to your GitHub repository → Settings → Secrets and variables → Actions → New repository secret

   Add these two secrets:

   - **Name**: `AWS_ACCESS_KEY_ID`
     **Value**: Your AWS Access Key ID (for user proyect-global)
   
   - **Name**: `AWS_SECRET_ACCESS_KEY`
     **Value**: Your AWS Secret Access Key

### How to Deploy

Once the secrets are set up, deployment is automatic!

**Option A: Push to main branch**
```bash
git push origin main
```

**Option B: Manual trigger**
1. Go to GitHub repository → Actions tab
2. Select "Build and Deploy to AWS ECR"
3. Click "Run workflow"

### What the workflow does:

1. ✅ Builds Docker image on GitHub's servers (not your machine)
2. ✅ Pushes image to ECR: `914964735054.dkr.ecr.us-east-1.amazonaws.com/linkedin-job-scraper:latest`
3. ✅ Runs a test ECS task to verify deployment
4. ✅ Your scheduled task will use this image daily at 9:00 AM UTC

### Monitor Deployment

**GitHub Actions**: https://github.com/YOUR_USERNAME/linkedin/actions

**AWS Console**:
- ECS Cluster: https://us-east-1.console.aws.amazon.com/ecs/home?region=us-east-1#/clusters/linkedin-scraper-cluster
- ECR Repository: https://us-east-1.console.aws.amazon.com/ecr/repositories/private/914964735054/linkedin-job-scraper
- CloudWatch Logs: https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/$252Fecs$252Flinkedin-scraper-task

### Troubleshooting

**If the workflow fails:**
1. Check GitHub Actions logs for error details
2. Verify AWS credentials are correct
3. Ensure IAM user has permissions for ECR and ECS

**If ECS task fails:**
```bash
# Check task status
aws ecs list-tasks --cluster linkedin-scraper-cluster

# View logs
aws logs tail /ecs/linkedin-scraper-task --follow
```

### Cost Reminder

- **Monthly cost**: ~$0.25
- **Free tier remaining**: $84.75

## Manual Deployment (Alternative)

If GitHub Actions doesn't work, you can use AWS CloudShell:

1. Open AWS Console → CloudShell (icon in top right)
2. Run:
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 914964735054.dkr.ecr.us-east-1.amazonaws.com
   
   # Clone repo
   git clone https://github.com/YOUR_USERNAME/linkedin.git
   cd linkedin
   
   # Build and push
   docker build -t linkedin-job-scraper .
   docker tag linkedin-job-scraper:latest 914964735054.dkr.ecr.us-east-1.amazonaws.com/linkedin-job-scraper:latest
   docker push 914964735054.dkr.ecr.us-east-1.amazonaws.com/linkedin-job-scraper:latest
   ```
