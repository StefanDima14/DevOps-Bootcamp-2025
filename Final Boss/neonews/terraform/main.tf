/*
VPC names neonews-vpc
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

resource "aws_vpc" "neonews_vpc" {
  cidr_block = var.cidr_block
  tags = {
    Name = "neonews-vpc"
  }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.neonews_vpc.id

  tags = {
    Name = "neonews_vpc_gw"
  }
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.neonews_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }
  tags = {
    Name = "neonews_public_rt"
  }
}

resource "aws_route_table_association" "public_rt_assoc" {
  subnet_id = aws_subnet.subnet_a.id
  route_table_id = aws_route_table.public_rt.id
}
resource "aws_subnet" "subnet_a" {
  vpc_id            = aws_vpc.neonews_vpc.id
  cidr_block        = var.subnet_a_cidr
  availability_zone = var.az_subnet_a
  map_public_ip_on_launch = true
  tags = {
    Name = "neonews-subnet-a"
  }
}

# Security Group allowing SSH from the subnets
resource "aws_security_group" "allow_ssh" {
  name        = var.sg_name
  description = "Allow SSH access from the defined subnets"
  vpc_id      = aws_vpc.neonews_vpc.id
  tags = {
    Name = var.sg_name
  }
}

# Inboud rule to allow SSH from subnet A
resource "aws_vpc_security_group_ingress_rule" "allow_22_port" {
  security_group_id = aws_security_group.allow_ssh.id
  cidr_ipv4        = "0.0.0.0/0"
  from_port        = 22
  to_port          = 22
  ip_protocol      = "tcp"
}
# Inboud rule for Web
resource "aws_vpc_security_group_ingress_rule" "allow_80_port" {
  security_group_id = aws_security_group.allow_ssh.id
  cidr_ipv4      = "0.0.0.0/0"
  from_port        = 80
  to_port          = 80
  ip_protocol      = "tcp"
}

# Inboud rule for app port
resource "aws_vpc_security_group_ingress_rule" "allow_8080_port" {
  security_group_id = aws_security_group.allow_ssh.id
  cidr_ipv4      = "0.0.0.0/0"
  from_port        = 8080
  to_port          = 8080
  ip_protocol      = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "allow_all_outbound" {
  security_group_id = aws_security_group.allow_ssh.id
  cidr_ipv4      = "0.0.0.0/0"
  ip_protocol      = "-1"
  
}
# key pair for EC2 instances
resource "aws_key_pair" "nodes_connect" {
  key_name   = var.key_pair_name
  public_key = file("${path.module}/nodes-connect.pub")
}

### IAM ROLE for EC2 Instance

resource "aws_iam_role" "ec2_ecr_role" {
  name = "EC2-ECR-Pull-Role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })
}

# DynamoDB Full Access
resource "aws_iam_role_policy_attachment" "dynamo_db" {
  role       = aws_iam_role.ec2_ecr_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}
# ECR Read Only (to pull your docker images)
resource "aws_iam_role_policy_attachment" "ecr_read" {
  role       = aws_iam_role.ec2_ecr_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}
# S3 Full Access
resource "aws_iam_role_policy_attachment" "s3_full" {
  role       = aws_iam_role.ec2_ecr_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "cw_full" {
  role       = aws_iam_role.ec2_ecr_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchFullAccess"
}

resource "aws_iam_role_policy_attachment" "ssm_full" {
  role       = aws_iam_role.ec2_ecr_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMFullAccess"
}

# EC2 Instance Profile
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "EC2-Instance-Profile"
  role = aws_iam_role.ec2_ecr_role.name
}

# EC2 Instance in Subnet A
resource "aws_instance" "node_a" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.subnet_a.id
  vpc_security_group_ids = [aws_security_group.allow_ssh.id]
  key_name               = aws_key_pair.nodes_connect.key_name
  associate_public_ip_address = true
  iam_instance_profile   = aws_iam_instance_profile.ec2_profile.name
  tags = {
    Name = "NodeA"
  }
}

resource "aws_ec2_instance_connect_endpoint" "ec2_instance_connect_endpoint" {
  subnet_id = aws_subnet.subnet_a.id
  preserve_client_ip = false
  security_group_ids = [aws_security_group.allow_ssh.id]
  tags = {
    Name = "ec2-instance-connect-endpoint-tf"
  }
}