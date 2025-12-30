variable "cidr_block" {
  description = "The CIDR block for the cyber-vpc"
  type        = string
}

variable "subnet_a_cidr" {
  description = "The CIDR block for subnet A"
  type        = string
}

variable "az_subnet_a" {
  description = "The availability zone for subnet A"
  type        = string
}

variable "sg_name" {
  description = "The name of the security group allowing mutual SSH"
  type        = string
}
variable "key_pair_name" {
  description = "The name of the key pair to use for EC2 instances"
  type        = string 
}

variable "ami_id" {
  description = "The AMI ID for the EC2 instances"
  type        = string
}

variable "instance_type" {
  description = "The instance type for the EC2 instances"
  type        = string 
}

variable "region" {
  description = "AWS Region"
  type        = string
}