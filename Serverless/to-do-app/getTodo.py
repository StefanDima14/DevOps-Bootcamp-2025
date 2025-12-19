import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('TABLE_NAME'))

def getTodos(event, context):
    try:
        # Scan returns all items in the table
        response = table.scan()
        items = response.get('Items', [])

        return {
            "statusCode": 200,
            "body": json.dumps(items)
        }
    except Exception as e:
        print(f"Error fetching todos: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": "Internal Server Error"})}