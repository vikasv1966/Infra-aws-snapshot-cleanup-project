
The project automates snapshot maintenance by running a Lambda function on a schedule. It identifies snapshots older than the configured threshold and removes them to help manage storage and costs.



## What Gets Created

- An IAM role with permissions required for snapshot operations
- A Lambda function deployed inside a private subnet
- A scheduled EventBridge rule that invokes the Lambda daily
- Configurable parameters such as retention period and dry-run mode

## Infrastructure Details

The Terraform module is responsible for:
- Creating the Lambda function and IAM role
- Attaching necessary permissions
- Configuring the scheduled trigger
- Associating the Lambda with VPC settings (subnets and security groups)

Each environment (dev/prod) references the same module with its own configuration.

## Requirements

- Terraform installed locally  
- AWS CLI configured with appropriate credentials  

'''bash
aws configure

## build the lambda
cd build
bash package.sh

## Deploy to Development
cd infra/terraform/envs/dev
terraform init
terraform apply

## Deploy to Prod
cd infra/terraform/envs/prod
terraform init
terraform apply