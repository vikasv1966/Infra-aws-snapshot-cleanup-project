provider "aws" {
  region = var.region
}

module "snapshot_cleanup" {
  source = "../../modules/snapshot-cleanup"

  name       = var.name
  lambda_zip = var.lambda_zip

  retention_days = var.retention_days
  dry_run        = var.dry_run

  subnets         = var.subnets
  security_groups = var.security_groups
}