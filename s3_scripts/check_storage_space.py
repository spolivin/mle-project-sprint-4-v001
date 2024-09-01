import argparse
import os

import boto3
from dotenv import load_dotenv

parser = argparse.ArgumentParser()
parser.add_argument("--showall", type=bool, default=False)
args = parser.parse_args()

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
    # Retrieving a bucket name
    bucket_name = os.environ.get("S3_BUCKET_NAME")

    # Listing all S3 objects
    files = []
    sizes = []
    if s3.list_objects(Bucket=bucket_name).get('Contents'):
        for key in s3.list_objects(Bucket=bucket_name)['Contents']:
            cur_key = key['Key']
            response = s3.head_object(Bucket = bucket_name, Key = cur_key)
            cur_size = response['ContentLength']
            if args.showall:
                cur_size_mb = cur_size / (1024**2)
                print(f"file {cur_key} => {cur_size} bytes ({cur_size_mb:.5f} MB)")
            files.append(cur_key)
            sizes.append(cur_size)

    # Computing and printing file sizes
    total_weight = sum(sizes)
    total_weight_gb = total_weight / (1024**3)
    print(f"\nTotal weight of all files in bucket = {total_weight} bytes ({total_weight_gb:.2f} GB)\n")
