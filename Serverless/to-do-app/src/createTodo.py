import json
import os
import boto3

sqs = boto3.client('sqs')
QUEUE_URL = os.environ.get('QUEUE_URL')

def createTodo(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        task = body.get('task')

        if not task:
            return {"statusCode": 400, "body": json.dumps({"error": "Task is required"})}

        message = {
            'task': task
        }

        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(message)
        )

        return {
            "statusCode": 202,
            "body": json.dumps({"message": "Todo item accepted for processing."})
        }
    except Exception as e:
        print(f"Error: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
