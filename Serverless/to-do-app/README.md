<!--
title: 'AWS Simple HTTP Endpoint example in Python'
description: 'This template demonstrates how to make a simple HTTP API with Python running on AWS Lambda and API Gateway using the Serverless Framework.'
layout: Doc
framework: v4
platform: AWS
language: python
authorLink: 'https://github.com/serverless'
authorName: 'Serverless, Inc.'
authorAvatar: 'https://avatars1.githubusercontent.com/u/13742415?s=200&v=4'
-->

# Serverless Framework Python HTTP API on AWS

This template demonstrates how to make a simple HTTP API with Python running on AWS Lambda and API Gateway using the Serverless Framework.

This template does not include any kind of persistence (database). For more advanced examples, check out the [serverless/examples repository](https://github.com/serverless/examples/) which includes DynamoDB, Mongo, Fauna and other examples.

## Usage

### Deployment

```
serverless deploy
```

After deploying, you should see output similar to:

```
Deploying "aws-python-http-api" to stage "dev" (us-east-1)

✔ Service deployed to stack aws-python-http-api-dev (85s)

endpoint: GET - https://6ewcye3q4d.execute-api.us-east-1.amazonaws.com/
functions:
  hello: aws-python-http-api-dev-hello (2.3 kB)
```

_Note_: In current form, after deployment, your API is public and can be invoked by anyone. For production deployments, you might want to configure an authorizer. For details on how to do that, refer to [http event docs](https://www.serverless.com/framework/docs/providers/aws/events/apigateway/).

### Invocation

After successful deployment, you can call the created application via HTTP:

```
curl https://xxxxxxx.execute-api.us-east-1.amazonaws.com/
```

Which should result in response similar to the following (removed `input` content for brevity):

```json
{
  "message": "Go Serverless v4.0! Your function executed successfully!"
}
```

### Local development

You can invoke your function locally by using the following command:

```
serverless invoke local --function hello
```

Which should result in response similar to the following:

```json
{
  "statusCode": 200,
  "body": "{\n  \"message\": \"Go Serverless v4.0! Your function executed successfully!\"}"
}
```

Alternatively, it is also possible to emulate API Gateway and Lambda locally by using `serverless-offline` plugin. In order to do that, execute the following command:

```
serverless plugin install -n serverless-offline
```

It will add the `serverless-offline` plugin to `devDependencies` in `package.json` file as well as will add it to `plugins` in `serverless.yml`.

After installation, you can start local emulation with:

```
serverless offline
```

To learn more about the capabilities of `serverless-offline`, please refer to its [GitHub repository](https://github.com/dherault/serverless-offline).

### Bundling dependencies

In case you would like to include 3rd party dependencies, you will need to use a plugin called `serverless-python-requirements`. You can set it up by running the following command:

```
serverless plugin install -n serverless-python-requirements
```

Running the above will automatically add `serverless-python-requirements` to `plugins` section in your `serverless.yml` file and add it as a `devDependency` to `package.json` file. The `package.json` file will be automatically created if it doesn't exist beforehand. Now you will be able to add your dependencies to `requirements.txt` file (`Pipfile` and `pyproject.toml` is also supported but requires additional configuration) and they will be automatically injected to Lambda package during build process. For more details about the plugin's configuration, please refer to [official documentation](https://github.com/UnitedIncome/serverless-python-requirements).


```mermaid
graph TD
    %% --- STYLING CLASSES (AWS Standard Colors) ---
    classDef client fill:#ffffff,stroke:#333,stroke-width:2px,color:#000;
    classDef aws_compute fill:#FF9900,stroke:#D17D00,stroke-width:2px,color:white;
    classDef aws_db fill:#3B48CC,stroke:#2E3899,stroke-width:2px,color:white;
    classDef aws_network fill:#F2F7F2,stroke:#3F8624,stroke-width:2px,stroke-dasharray: 5 5,color:#3F8624;
    classDef aws_subnet fill:#FFFFFF,stroke:#3F8624,stroke-width:1px,stroke-dasharray: 2 2,color:#3F8624;
    classDef aws_integration fill:#FF4F8B,stroke:#CC2C64,stroke-width:2px,color:white;
    classDef aws_apigw fill:#A166FF,stroke:#834CCF,stroke-width:2px,color:white;
    classDef aws_vpce fill:#E6F6E6,stroke:#3F8624,stroke-width:2px,color:#3F8624;

    %% --- THE DIAGRAM ---

    subgraph UserSpace ["User Environment"]
        Client([fa:fa-user Client / App]):::client
        Dev([fa:fa-terminal DevOps Engineer]):::client
    end

    subgraph AWS_Cloud ["AWS Cloud Region (eu-west-1)"]
        direction TB

        %% 1. ENTRY POINT
        subgraph APIGW ["API Gateway (HTTP API)"]
            EndpointPost["POST /todo"]:::aws_apigw
            EndpointGet["GET /todos"]:::aws_apigw
        end

        %% 2. VPC NETWORKING
        subgraph VPC ["VPC (10.0.0.0/16)"]
            direction TB
            
            subgraph VPCE ["VPC Endpoints (PrivateLink)"]
                SQS_VPCE(Interface EP: SQS):::aws_vpce
                DDB_VPCE(Gateway EP: DynamoDB):::aws_vpce
            end

            subgraph AZ_A ["AZ A (eu-west-1a)"]
                subgraph SubnetA ["Private Subnet A"]
                    LambdaENI_1[Lambda ENI A]:::aws_subnet
                end
            end

            subgraph AZ_B ["AZ B (eu-west-1b)"]
                subgraph SubnetB ["Private Subnet B"]
                    LambdaENI_2[Lambda ENI B]:::aws_subnet
                end
            end
        end

        %% 3. COMPUTE LAYER (Logical)
        %% Note: These run in the AWS control plane but project ENIs into your VPC
        subgraph Lambdas ["Lambda Functions"]
            Func_Add(fa:fa-server addTodo):::aws_compute
            Func_Get(fa:fa-server getTodos):::aws_compute
            Func_Process(fa:fa-microchip processTodo):::aws_compute
            Func_ReDrive(fa:fa-wrench reDriveDLQ):::aws_compute
        end

        %% 4. STORAGE & QUEUE LAYER
        subgraph ManagedServices ["Managed Services"]
            subgraph SQS ["Amazon SQS"]
                Queue_Main[TodoQueue]:::aws_integration
                Queue_DLQ[TodoDLQ]:::aws_integration
            end

            subgraph DDB ["Amazon DynamoDB"]
                Table_Todo[(TodoTable)]:::aws_db
            end
        end
    end

    %% --- CONNECTIONS ---

    %% Flow 1: Add Todo
    Client -- "1. POST JSON" --> EndpointPost
    EndpointPost -- "2. Invoke" --> Func_Add
    Func_Add -. "3. VPC Access" .-> LambdaENI_1
    LambdaENI_1 -- "4. Send Msg (Interface EP)" --> SQS_VPCE
    SQS_VPCE --> Queue_Main

    %% Flow 2: Get Todos
    Client -- "8. GET" --> EndpointGet
    EndpointGet -- "9. Invoke" --> Func_Get
    Func_Get -. "10. VPC Access" .-> LambdaENI_2
    LambdaENI_2 -- "11. Query (Gateway EP)" --> DDB_VPCE
    DDB_VPCE --> Table_Todo
    Table_Todo -- "12. Return items" --> Func_Get
    Func_Get -- "13. JSON Response" --> Client

    %% Flow 3: Async Processing
    Queue_Main -- "5. Polling Trigger" --> Func_Process
    Func_Process -. "6. VPC Access" .-> LambdaENI_1
    LambdaENI_1 -- "7. Put Item (Gateway EP)" --> DDB_VPCE
    
    %% Flow 4: Error Handling
    Func_Process -- "x3 Failures" --> Queue_Main
    Queue_Main -- "Dead Letter Queue" --> Queue_DLQ
    
    %% Flow 5: Operational Redrive
    Dev -- "Manually Invoke" --> Func_ReDrive
    Func_ReDrive --> Queue_DLQ
    Func_ReDrive --> Queue_Main
```