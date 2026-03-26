# Deployment Plan

This document describes how the application could be deployed on AWS in a simple, production-like way without introducing unnecessary infrastructure complexity.

## Goals

The deployment approach should:

- keep the architecture simple
- support separate frontend and backend deployment
- use managed AWS services where possible
- avoid unnecessary operational overhead
- remain appropriate for the scope of a small assignment project

## High-Level Architecture

The application consists of three main parts:

- **Frontend**: React + TypeScript dashboard
- **Backend**: FastAPI service
- **Data**: local Parquet file loaded into memory at backend startup

High-level request flow:

1. User opens the frontend application
2. Frontend sends HTTP requests to the backend API
3. Backend processes requests using in-memory data loaded at startup
4. Backend returns aggregated data for dashboard visualizations

## Frontend Deployment

The frontend would be deployed using **AWS Amplify Hosting**.

### Why Amplify

AWS Amplify Hosting is a good fit because it provides:

- GitHub integration
- automatic build and deployment
- managed HTTPS
- CDN-backed frontend delivery
- minimal setup effort

This is appropriate for a small frontend application where the goal is to keep deployment straightforward.

### Deployment Flow

1. Connect the GitHub repository to Amplify
2. Configure Amplify to build only the frontend directory
3. On each approved release event, Amplify builds and deploys the frontend
4. Amplify serves the static site through its managed hosting layer

### Monorepo Consideration

Because the frontend and backend are stored in the same repository, Amplify should be configured to use the frontend subdirectory as the application root. This allows the frontend to be deployed independently without affecting the backend.

## Backend Deployment

The backend would be deployed using **AWS App Runner**.

### Why App Runner

AWS App Runner is a strong fit for this project because:

- it is well suited for a small HTTP API
- it supports containerized deployment
- it provides managed HTTPS and scaling
- it requires less setup than ECS + Fargate
- it keeps the deployment model simple and easy to explain

### Deployment Flow

1. Package the backend as a Docker container
2. Push the image to Amazon ECR
3. Configure AWS App Runner to deploy the container image
4. Expose the backend as a managed HTTPS API service

## Data Handling

The backend uses a local Parquet file as the data source.

### Runtime Strategy

At application startup, the backend:

- reads the Parquet file
- parses and preprocesses required fields
- derives analytical fields such as hour and date
- filters invalid rows
- stores the processed dataset in memory

The API then performs request-time calculations on the in-memory dataset.

### Why No Database

A database was intentionally not introduced because:

- the dataset is small enough for in-memory use
- the project does not require persistence
- the assignment favors simplicity and decision-making over infrastructure complexity
- adding a database would increase setup and operational overhead without clear benefit

## Environment Configuration

The following configuration would be handled through environment variables:

- backend API base URL for the frontend
- runtime environment settings
- file path or data source configuration for backend startup
- container/runtime settings for cloud deployment

No sensitive secret management is required for the current scope, but AWS-native secret storage could be introduced if needed in a larger production setup.

## CI/CD Approach

The preferred workflow is to use GitHub as the source of truth for deployments.

### Frontend

The frontend is deployed through Amplify's GitHub integration. Once Terraform has connected the repository and branch, Amplify automatically rebuilds and deploys the frontend for that branch.

### Backend

The backend deployment flow is:

1. GitHub Actions builds the backend Docker image
2. The image is pushed to Amazon ECR using a stable tag (e.g. `latest` or `prod`)
3. AWS App Runner is configured with automatic deployments enabled and watches the ECR image tag
4. When the `latest` image changes, App Runner automatically deploys the new backend image

This keeps frontend and backend deployment independent while still supporting a clean monorepo workflow.

## GitHub Workflow Requirements

The GitHub Actions pipeline assumes the Terraform resources already exist and only needs AWS credentials so it can push the backend image to ECR.

Configure one of these authentication options as repository secrets:

- `AWS_ROLE_TO_ASSUME` for GitHub OIDC authentication, or
- `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` as a fallback

The workflow is aligned to the Terraform defaults in this repo:

- region: `eu-west-1`
- ECR repository: `nyc-taxi-dashboard-backend`
- App Runner service: `nyc-taxi-dashboard-backend`
- Amplify app: `nyc-taxi-dashboard-frontend`
- Amplify deployment branch: `feat/deployment`

Terraform now creates the GitHub Actions IAM role for ECR pushes. After `terraform apply`, you can fetch the role ARN with:

- `terraform output -raw github_actions_role_arn`

Then store that value in the GitHub repository secret:

- `AWS_ROLE_TO_ASSUME`

By default, the role trusts only this repository and branch:

- repository: `zsozsesz/mitzu-homework`
- branch: `feat/deployment`

If the GitHub OIDC provider already exists in your AWS account, set:

- `create_github_actions_oidc_provider = false`
- `github_actions_oidc_provider_arn = "arn:aws:iam::<account-id>:oidc-provider/token.actions.githubusercontent.com"`

## Handling Terraform Secrets

Do not keep `github_access_token` in a tracked Terraform file.

For local Terraform usage, prefer an environment variable:

- `export TF_VAR_github_access_token="..."`

If you want a file-based local override, use an ignored file such as:

- `terraform/secrets.auto.tfvars`

For new GitHub-based Amplify apps, Terraform should use Amplify's `accessToken` flow, not legacy `oauthToken`. AWS documents that this requires:

1. Installing the regional Amplify GitHub App on the repository
2. Providing a GitHub personal access token with `admin:repo_hook`

For this repository in `eu-west-1`, install the GitHub App here:

- `https://github.com/apps/aws-amplify-eu-west-1/installations/new`

Then provide the token to Terraform as `TF_VAR_github_access_token`.

## Scaling Considerations

This architecture is intentionally simple, but it has a few known tradeoffs.

### Frontend

The frontend scales well because it is a static application served through managed hosting/CDN infrastructure.

### Backend

The backend can scale horizontally through App Runner, but each new instance repeats startup-time data loading and preprocessing.

This means:

- startup time increases due to preprocessing
- each instance duplicates the same in-memory dataset
- preprocessing work is repeated across instances instead of being centralized

These tradeoffs are acceptable for this assignment because the dataset is relatively small and expected traffic is limited.

## Alternative Considered

### ECS + Fargate

ECS + Fargate was considered for backend deployment.

It would provide:

- greater control over service configuration
- more flexibility for multi-service environments
- a model closer to full container orchestration

However, it was not selected because:

- it adds more setup complexity
- it introduces concepts that are unnecessary for a single small API
- App Runner provides a simpler and more appropriate deployment model for this use case

### S3 + CloudFront for Frontend

S3 + CloudFront was also considered for frontend hosting.

This is a valid option, but Amplify was preferred because:

- it simplifies GitHub-based deployment
- it reduces manual setup
- it provides an easier managed workflow for a small project

## Summary

The selected deployment approach is:

- **Frontend**: AWS Amplify Hosting
- **Backend**: AWS App Runner
- **Container Registry**: Amazon ECR
- **Data Storage**: local Parquet file loaded into memory at startup
- **Database**: not used

This deployment model prioritizes simplicity, clarity, and managed services while remaining realistic and appropriate for the size of the assignment.
