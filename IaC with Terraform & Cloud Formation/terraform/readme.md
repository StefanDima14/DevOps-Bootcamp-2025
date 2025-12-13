# Terraform Assignment: AWS EC2 SSH Connectivity

## Steps

1. **Set the AWS provider**
2. **Create the DynamoDB table for state locks**
3. **Create S3 bucket and set the backend in Terraform → `terraform init`**
4. **Create the VPC**
5. **Create the subnets A and B**
6. **Create the security group**
7. **Create inbound and outbound rules**
8. **Create aws_key_pair to enable SSH between instances (create the SSH key on local computer)**
9. **Create both instances**
10. **From UI connect to instances with EC2 Instance Connect → create VPC endpoint → connect on each instance**
11. **Copy on instances the private SSH key generated → `chmod 400 nodes-connect`**
12. **SSH into the instance:**
    ```sh
    ssh -i nodes-connect ec2-user@<private_ip>
    ```

## Screenshots

- **DynamoDB Table:** Used for Terraform state locking to prevent concurrent modifications to the state file.
  ![dynamodb](screenshots/dynamodb.png)
- **S3 Bucket for Terraform State:** Stores the Terraform state file remotely, enabling collaboration and state recovery.
  ![s3-tfstate](screenshots/s3-tfstate.png)
- **S3 Bucket (UI):** S3 bucket as seen in the AWS Console, confirming its creation.
  ![s3](screenshots/s3.png)
- **SSH from Node A to Node B:** Demonstrates successful SSH connection from one EC2 instance to another using the private key.
  ![node-a-to-b](screenshots/node-a-to-b.png)
- **SSH from Node B to Node A:** Shows SSH connectivity in the reverse direction, confirming bidirectional access.
  ![node-b-to-a](screenshots/node-b-to-a.png)

## Terraform Files Overview

- **main.tf**: Contains the main Terraform configuration, including provider setup, VPC, subnets, security groups, EC2 instances, and key pair resources.
- **variables.tf**: Defines all input variables used in the configuration, such as VPC CIDR, subnet CIDRs, instance types, and key names.
- **outputs.tf**: Specifies the outputs from the Terraform run, such as instance private IPs and VPC/subnet IDs.
- **provider.tf**: Configures the AWS provider and backend for remote state storage (S3 and DynamoDB).
- **backend.tf**: Sets up the backend configuration for storing the Terraform state in S3 and locking with DynamoDB.
- **nodes_connect.pub**: The public SSH key used for the EC2 key pair, enabling SSH access between instances.

---

## Instructions

In this assignment Terraform was used to create infrastructure in AWS for two EC2 instances. The scope of this assignment was to create the infrastructure to permit the SSH connections between 2 EC2 instances using private subnets.

The resources created are: 
1. VPC with CIDR 10.10.0.0/16
2. SubnetA: 10.10.1.0/24 AZ: eu-west-1a
3. SubnetB: 10.10.2.0/24 AZ: eu-west-1b
4. Security Group with SSH inbound rule
5. EC2 instances

## Step-by-step guide

### Why use DynamoDB for Terraform state locking?

When using Terraform in a team or with remote state, it is important to prevent multiple people or processes from making changes to the infrastructure at the same time. DynamoDB is used for state locking, which ensures that only one Terraform process can modify the state at a time, preventing conflicts and potential corruption of the state file.

### DynamoDB Table Creation (for state locking)

The following AWS CLI command was used to create the DynamoDB table for Terraform state locking:

```sh
aws dynamodb create-table --table-name terraform-locks --attribute-definitions AttributeName=LockID,AttributeType=S --key-schema AttributeName=LockID,KeyType=HASH --billing-mode PAY_PER_REQUEST --region eu-west-1
```

Sample output:
```json
{
    "TableDescription": {
        "AttributeDefinitions": [
            {
                "AttributeName": "LockID",
                "AttributeType": "S"
            }
        ],
        "TableName": "terraform-locks",
        "KeySchema": [
            {
                "AttributeName": "LockID",
                "KeyType": "HASH"
            }
        ],
        "TableStatus": "CREATING",
        "CreationDateTime": "2025-12-13T18:49:33.036000+02:00",
        "ProvisionedThroughput": {
            "NumberOfDecreasesToday": 0,
            "ReadCapacityUnits": 0,
            "WriteCapacityUnits": 0
        },
        "TableSizeBytes": 0,
        "ItemCount": 0,
        "TableArn": "arn:aws:dynamodb:eu-west-1:xxxxxx:table/terraform-locks",
        "TableId": "xxxxxxxxx",
        "BillingModeSummary": {
            "BillingMode": "PAY_PER_REQUEST"
        }
    }
}
```

This table is referenced in the Terraform backend configuration to enable state locking.
