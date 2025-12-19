import json
import uuid
import os
import boto3

# Initialize the DynamoDB resource outside the handler for connection reuse
dynamodb = boto3.resource('dynamodb')
# Use an environment variable for the table name (set in serverless.yml)
TABLE_NAME = os.environ.get('TABLE_NAME', 'todo-table-dev')
table = dynamodb.Table(TABLE_NAME)

def createTodo(event, context):
    try:
        # Parse the request body
        body = json.loads(event.get('body', '{}'))
        todo_text = body.get('task')

        if not todo_text:
            return {"statusCode": 400, "body": json.dumps({"error": "Task is required"})}

        todo_item = {
            'id': str(uuid.uuid4()),
            'task': todo_text,
            'completed': False
        }

        # Write to DynamoDB (via VPC Endpoint)
        table.put_item(Item=todo_item)

        return {
            "statusCode": 201,
            "body": json.dumps(todo_item)
        }
    except Exception as e:
        print(f"Error: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}