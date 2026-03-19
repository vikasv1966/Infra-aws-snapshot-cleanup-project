variable "region" {
  default = "us-east-1"
}

variable "name" {
  default = "snapshot-cleanup-prod"
}

variable "lambda_zip" {
  default = "../../../lambda.zip"
}

variable "retention_days" {
  default = "365"
}

variable "dry_run" {
  default = "false"
}

variable "subnets" {
  type = list(string)
}

variable "security_groups" {
  type = list(string)
}