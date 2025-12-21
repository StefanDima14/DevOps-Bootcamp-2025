import json
import os
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def handler(event, context):
    for record in event['Records']:
        body = json.loads(record['body'])
        task = body['task']
        todo_id = str(uuid.uuid4())

        table.put_item(
            Item={
                'id': todo_id,
                'task': task,
                'completed': False
            }
        )
        print(f"Successfully processed todo with id: {todo_id}")

    return {'statusCode': 200}
