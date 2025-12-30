/*
VPC names cyber-vpc
cidr: 10.10.0.0/16
public subnetA: 10.10.1.0/24 eu-west-1a
private subnetB: 10.10.2.0/24 eu-west-1b
security group: allow ssh from the internet

ec2 instances:
- t3.micro
- ami: amazon linux 2 AMI (HVM), SSD Volume Type
- key pair: nodes-connect
- sg: the one created above
- public ip
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

# Security Group allowing SSH from the subnets
resource "aws_security_group" "mutual_ssh" {
  name        = var.sg_name
  description = "Allow SSH access from the defined subnets"
  vpc_id      = aws_vpc.cyber_vpc.id
  tags = {
    Name = var.sg_name
  }
}

# Inboud rule to allow SSH from the internet
resource "aws_vpc_security_group_ingress_rule" "allow_ssh_from_internet" {
  security_group_id = aws_security_group.mutual_ssh.id
  cidr_ipv4        = "0.0.0.0/0"
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
  public_key = file("${path.module}/nodes-connect.pub")
}

# Internet Gateway
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.cyber_vpc.id
  tags = {
    Name = "cyber-igw"
  }
}

# Public Route Table
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.cyber_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    Name = "cyber-public-rt"
  }
}

# Associate Public Route Table with Subnet A
resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.subnet_a.id
  route_table_id = aws_route_table.public_rt.id
}


# EC2 Instance in Subnet A
resource "aws_instance" "node_a" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.subnet_a.id
  vpc_security_group_ids = [aws_security_group.mutual_ssh.id]
  key_name               = aws_key_pair.nodes_connect.key_name
  associate_public_ip_address = true
  tags = {
    Name = "NodeA"
  }
}

resource "aws_ec2_instance_connect_endpoint" "ec2_instance_connect_endpoint" {
  subnet_id = aws_subnet.subnet_a.id
  preserve_client_ip = false
  security_group_ids = [aws_security_group.mutual_ssh.id]
  tags = {
    Name = "ec2-instance-connect-endpoint-tf"
  }
}