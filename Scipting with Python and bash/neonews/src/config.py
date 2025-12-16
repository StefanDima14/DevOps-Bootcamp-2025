import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY")
AWS_REGION = os.getenv("AWS_REGION")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

if not NEWSDATA_API_KEY:
    raise ValueError("Missing NEWSDATA_API_KEY in .env file.")
if not AWS_REGION:
    raise ValueError("Missing AWS_REGION in .env file.")
if not DYNAMODB_TABLE:
    raise ValueError("Missing DYNAMODB_TABLE in .env file.")    
if not S3_BUCKET_NAME:
    raise ValueError("Missing S3_BUCKET_NAME in .env file.")