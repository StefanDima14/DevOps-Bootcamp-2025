import os
import boto3

sqs = boto3.client('sqs')
dlq_url = os.environ['DLQ_URL']
queue_url = os.environ['QUEUE_URL']

def handler(event, context):
    try:
        messages = sqs.receive_message(
            QueueUrl=dlq_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=5
        )

        if 'Messages' in messages:
            for message in messages['Messages']:
                sqs.send_message(
                    QueueUrl=queue_url,
                    MessageBody=message['Body']
                )
                sqs.delete_message(
                    QueueUrl=dlq_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
                print(f"Message with id {message['MessageId']} re-driven to main queue.")
            return {'statusCode': 200, 'body': f"{len(messages['Messages'])} messages re-driven."}
        else:
            print("No messages to re-drive.")
            return {'statusCode': 200, 'body': 'No messages to re-drive.'}
    except Exception as e:
        print(f"Error re-driving messages: {e}")
        return {'statusCode': 500, 'body': 'Error re-driving messages.'}
