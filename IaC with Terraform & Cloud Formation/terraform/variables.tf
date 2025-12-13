variable "cidr_block" {
  description = "The CIDR block for the cyber-vpc"
  type        = string
  default     = "10.10.0.0/16"
}

variable "subnet_a_cidr" {
  description = "The CIDR block for subnet A"
  type        = string
  default     = "10.10.1.0/24"
}

variable "az_subnet_a" {
  description = "The availability zone for subnet A"
  type        = string
  default     = "eu-west-1a"
}

variable "subnet_b_cidr" {
  description = "The CIDR block for subnet A"
  type        = string
  default     = "10.10.2.0/24"
}

variable "az_subnet_b" {
  description = "The availability zone for subnet A"
  type        = string
  default     = "eu-west-1b"
}

variable "sg_name" {
  description = "The name of the security group allowing mutual SSH"
  type        = string
  default     = "mutual-ssh"
}
variable "key_pair_name" {
  description = "The name of the key pair to use for EC2 instances"
  type        = string
  default     = "nodes-connect"
  
}

variable "ami_id" {
  description = "The AMI ID for the EC2 instances"
  type        = string
  default     = "ami-09c54d172e7aa3d9a" # Amazon Linux 2 AMI (HVM), SSD Volume Type in eu-west-1
}

variable "instance_type" {
  description = "The instance type for the EC2 instances"
  type        = string
  default     = "t3.micro"
  
}