import boto3
from ..core.config import OBJ_STORAGE_HOSTNAME, OBJ_STORAGE_DEFAULT_BUCKET, \
                          OBJ_STORAGE_ROOT_USER, OBJ_STORAGE_ROOT_PASSWORD, \
                          OBJ_STORAGE_PORT


session = boto3.Session()
client = session.client('s3', endpoint_url=f"http://{OBJ_STORAGE_HOSTNAME}:{OBJ_STORAGE_PORT}",
    aws_access_key_id=OBJ_STORAGE_ROOT_USER, aws_secret_access_key=OBJ_STORAGE_ROOT_PASSWORD)


def get_default_bucket():
    return OBJ_STORAGE_DEFAULT_BUCKET

def create_default_bucket():
    try:
        client.create_bucket(Bucket=OBJ_STORAGE_DEFAULT_BUCKET)
    except client.exceptions.BucketAlreadyOwnedByYou:
        pass