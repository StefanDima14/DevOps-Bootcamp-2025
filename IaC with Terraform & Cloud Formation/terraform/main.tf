/*
VPC names cyber-vpc
cidr: 10.10.0.0/16
private subnetA: 10.10.1.0/24 eu-west-1a
private subnetB: 10.10.2.0/24 eu-west-1b
security group: allow ssh from the subnets

ec2 instances:
- t3.micro
- ami: amazon linux 2 AMI (HVM), SSD Volume Type
- key pair: nodes-connect
- sg: the one created above
- no public ip
*/

resource "aws_vpc" "cyber_vpc" {
  cidr_block = var.cidr_block
  tags = {
    Name = "cyber-vpc"
  }
}

resource "aws_subnet" "subnet_a" {
  vpc_id            = aws_vpc.cyber_vpc.id
  cidr_block        = var.subnet_a_cidr
  availability_zone = var.az_subnet_a
  tags = {
    Name = "cyber-subnet-a"
  }
}

resource "aws_subnet" "subnet_b" {
  vpc_id            = aws_vpc.cyber_vpc.id
  cidr_block        = var.subnet_b_cidr
  availability_zone = var.az_subnet_b
  tags = {
    Name = "cyber-subnet-b"
  }
}

# Security Group allowing SSH from the subnets
resource "aws_security_group" "mutual_ssh" {
  name        = var.sg_name
  description = "Allow SSH access from the defined subnets"
  vpc_id      = aws_vpc.cyber_vpc.id
  tags = {
    Name = var.sg_name
  }
}

# Inboud rule to allow SSH from subnet A
resource "aws_vpc_security_group_ingress_rule" "allow_ssh_from_subnet_a" {
  security_group_id = aws_security_group.mutual_ssh.id
  cidr_ipv4        = var.subnet_a_cidr
  from_port        = 22
  to_port          = 22
  ip_protocol      = "tcp"
}
# Inboud rule to allow SSH from subnet B
resource "aws_vpc_security_group_ingress_rule" "allow_ssh_from_subnet_b" {
  security_group_id = aws_security_group.mutual_ssh.id
  cidr_ipv4        = var.subnet_b_cidr
  from_port        = 22
  to_port          = 22
  ip_protocol      = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "allow_all_outbound" {
  security_group_id = aws_security_group.mutual_ssh.id
  cidr_ipv4      = "0.0.0.0/0"
  from_port        = 0
  to_port          = 0
  ip_protocol      = "-1"
  
}
# key pair for EC2 instances
resource "aws_key_pair" "nodes_connect" {
  key_name   = var.key_pair_name
  public_key = file("${path.module}/nodes_connect.pub")
}
# EC2 Instance in Subnet A

resource "aws_instance" "node_a" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.subnet_a.id
  vpc_security_group_ids = [aws_security_group.mutual_ssh.id]
  key_name               = aws_key_pair.nodes_connect.key_name
  associate_public_ip_address = false
  tags = {
    Name = "NodeA"
  }
}

resource "aws_instance" "node_b" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.subnet_b.id
  vpc_security_group_ids = [aws_security_group.mutual_ssh.id]
  key_name               = aws_key_pair.nodes_connect.key_name
  associate_public_ip_address = false
  tags = {
    Name = "NodeB"
  }
}