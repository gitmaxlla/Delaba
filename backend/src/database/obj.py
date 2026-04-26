import boto3

from src.core.config import (
    OBJ_STORAGE_DEFAULT_BUCKET,
    OBJ_STORAGE_HOSTNAME,
    OBJ_STORAGE_PORT,
    OBJ_STORAGE_ROOT_PASSWORD,
    OBJ_STORAGE_ROOT_USER,
)


session = boto3.Session()
client = session.client(
    "s3",
    endpoint_url=f"http://{OBJ_STORAGE_HOSTNAME}:{OBJ_STORAGE_PORT}",
    aws_access_key_id=OBJ_STORAGE_ROOT_USER,
    aws_secret_access_key=OBJ_STORAGE_ROOT_PASSWORD,
)


def create_default_bucket():
    try:
        client.create_bucket(Bucket=OBJ_STORAGE_DEFAULT_BUCKET)
    except client.exceptions.BucketAlreadyOwnedByYou:
        print("APP: Using a pre-existing S3 bucket", flush=True)


def get_default_bucket():
    return OBJ_STORAGE_DEFAULT_BUCKET
