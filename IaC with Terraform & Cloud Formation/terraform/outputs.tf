output "vpc_id" {
  description = "The ID of the cyber-vpc VPC"
  value       = aws_vpc.cyber_vpc.id
}

output "private_ip_node_a" {
  description = "The private IP address of the EC2 instance in subnet A"
  value       = aws_instance.node_a.private_ip
}

output "private_ip_node_b" {
  description = "The private IP address of the EC2 instance in subnet A"
  value       = aws_instance.node_b.private_ip 
}

output "sg_id" {
  description = "The ID of the security group allowing mutual SSH"
  value       = aws_security_group.mutual_ssh.id
}

output "key_pair_id" {
  description = "The name of the key pair to use for EC2 instances"
  value       = aws_key_pair.nodes_connect.id
  
}

output "ec2_instance_connect_endpoint" {
  description = "The ID of the EC2 Instance Connect Endpoint"
  value       = aws_ec2_instance_connect_endpoint.ec2_instance_connect_endpoint.id
}
