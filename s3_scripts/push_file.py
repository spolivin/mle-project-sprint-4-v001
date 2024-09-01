import os

import boto3
from dotenv import load_dotenv

# Constants for specifying file to be uploaded and S3-path for this file
FILE_NAME = "recommendations.parquet"
S3_FILE_DIR = "recsys/recommendations"

# Fixed constants
FILE_DIR = "../data"
LOCAL_FILE_PATH = os.path.join(FILE_DIR, FILE_NAME)
S3_FILE_PATH = os.path.join(S3_FILE_DIR, FILE_NAME)

def get_session():
    """Returns a boto3-client connected to S3 storage."""
    # Loading credentials
    load_dotenv()
    # Instantiating a session
    session = boto3.session.Session()

    return session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID_STUDENT'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY_STUDENT')
    )


if __name__ == "__main__":
    # Creating a session object
    s3 = get_session()
    # Retrieving bucket name
    bucket_name = os.environ.get("S3_BUCKET_NAME")

    # Uploading a file from `LOCAL_FILE_PATH` to `S3_FILE_PATH`
    try:
        s3.upload_file(
            LOCAL_FILE_PATH,
            bucket_name,
            S3_FILE_PATH,
        )
    except:
        print("Error occurred while uploading a file to S3")
    else:
        print(f"File '{FILE_NAME}' has been uploaded successfully")
