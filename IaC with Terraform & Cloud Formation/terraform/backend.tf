terraform {
  backend "s3" {
    bucket = "tf-states-766766276947"
    key    = "episode2/terraform.tfstate"
    region = "eu-west-1"
    dynamodb_table = "terraform-locks"
    encrypt = true
  }
}