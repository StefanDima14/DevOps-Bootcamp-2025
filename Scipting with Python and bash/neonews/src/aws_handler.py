import boto3
import json
import uuid
from datetime import datetime
from rich import print as rprint
from botocore.exceptions import ClientError
from src.config import AWS_REGION, DYNAMODB_TABLE, S3_BUCKET_NAME

class AWSClient:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
        self.s3 = boto3.client('s3', region_name=AWS_REGION)

    def init_resources(self):
        """Checks if Table and Bucket exist, creates them if not."""
        # 1. Check/Create DynamoDB
        try:
            table = self.dynamodb.Table(DYNAMODB_TABLE)
            table.load()
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print(f"⏳ Creating DynamoDB Table: {DYNAMODB_TABLE}...")
                try:
                    table = self.dynamodb.create_table(
                        TableName=DYNAMODB_TABLE,
                        KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
                        AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
                        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                    )
                    print("Waiting for table to become ACTIVE...")
                    table.wait_until_exists()
                    print(f"✅ Table '{DYNAMODB_TABLE}' is now ACTIVE.")
                except Exception as ce:
                    print(f"❌ DynamoDB Table creation failed: {ce}")

        # 2. Check/Create S3
        if S3_BUCKET_NAME:
            try:
                self.s3.head_bucket(Bucket=S3_BUCKET_NAME)
            except ClientError:
                print(f"⏳ Creating S3 Bucket: {S3_BUCKET_NAME}...")
                try:
                    self.s3.create_bucket(
                        Bucket=S3_BUCKET_NAME,
                        CreateBucketConfiguration={
                            'LocationConstraint': AWS_REGION
                        }
                    )
                    print(f"✅ Bucket '{S3_BUCKET_NAME}' created successfully.")
                except Exception as e:
                    print(f"❌ S3 Creation Failed: {e}")

    def save_article(self, article, topic):
        """
        Saves metadata to DynamoDB and raw JSON content to S3.
        """
        article_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        # Save to DynamoDB
        table = self.dynamodb.Table(DYNAMODB_TABLE)
        item = {
            'id': article_id,
            'title': article.get('title', 'No Title'),
            'topic': topic,
            'source': article.get('source_id', 'Unknown'),
            'link': article.get('link', 'Unknown'),
            'published_at': article.get('pubDate', timestamp),
            's3_key': f"{topic}/{article_id}.json"
        }
        try:
            table.put_item(Item=item)
        except Exception as e:
            print(f"[DynamoDB ERROR] Could not save article: {e}")
            return False

        # Save full content to S3
        if S3_BUCKET_NAME:
            try:
                self.s3.put_object(
                    Bucket=S3_BUCKET_NAME,
                    Key=item['s3_key'],
                    Body=json.dumps(article, indent=2),
                    ContentType='application/json'
                )
            except Exception as e:
                print(f"[S3 ERROR] Could not save article content: {e}")
                return False
        
        return True

    def wipe_resources(self):
        """Master command to destroy both DynamoDB and S3 resources."""
        rprint("[bold red]⚠ STARTING RESOURCE DESTRUCTION ⚠[/bold red]")
        self._nuke_dynamodb()
        self._nuke_s3()

    def _nuke_dynamodb(self):
        """Delete the DynamoDB table and wait for confirmation."""
        try:
            table = self.dynamodb.Table(DYNAMODB_TABLE)
            table.delete()
            print(f"⏳ Waiting for table '{DYNAMODB_TABLE}' to be deleted...")
            table.wait_until_not_exists()
            print(f"✅ Table '{DYNAMODB_TABLE}' deleted.")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print(f"✅ Table '{DYNAMODB_TABLE}' already gone.")
            else:
                print(f"❌ Error deleting table: {e}")

    def _nuke_s3(self):
        """Empty and delete the S3 bucket."""
        if not S3_BUCKET_NAME:
            return

        print(f"⏳ Emptying bucket '{S3_BUCKET_NAME}'...")
        try:
            # Empty the bucket
            while True:
                response = self.s3.list_objects_v2(Bucket=S3_BUCKET_NAME)
                if 'Contents' not in response:
                    break

                objects = [{'Key': obj['Key']} for obj in response['Contents']]
                self.s3.delete_objects(Bucket=S3_BUCKET_NAME, Delete={'Objects': objects})
                print(f"   - Deleted batch of {len(objects)} files")

            # Delete the bucket itself
            self.s3.delete_bucket(Bucket=S3_BUCKET_NAME)
            
            # Wait until it's actually gone
            waiter = self.s3.get_waiter('bucket_not_exists')
            waiter.wait(Bucket=S3_BUCKET_NAME)
            print(f"✅ Bucket '{S3_BUCKET_NAME}' deleted.")

        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchBucket':
                print(f"✅ Bucket '{S3_BUCKET_NAME}' already gone.")
            else:
                print(f"❌ Error deleting S3: {e}")