"""Script for preparing all datasets required for service functioning."""
import os

from dotenv import load_dotenv

from yc_client import YandexCloudClient

# Directory to which files are downloaded
DOWNLOAD_DIR = "data/"
# Files to be downloaded
FILES_TO_DOWNLOAD = [
    "items.parquet",
    "recommendations.parquet",
    "top_popular.parquet",
    "similar.parquet",
]
# Mapping from file's path in S3 to file's path in the local directory
MAPPING = {
    "recsys/data/" + FILES_TO_DOWNLOAD[0]: DOWNLOAD_DIR + FILES_TO_DOWNLOAD[0],
    "recsys/recommendations/"
    + FILES_TO_DOWNLOAD[1]: DOWNLOAD_DIR
    + FILES_TO_DOWNLOAD[1],
    "recsys/recommendations/"
    + FILES_TO_DOWNLOAD[2]: DOWNLOAD_DIR
    + FILES_TO_DOWNLOAD[2],
    "recsys/recommendations/"
    + FILES_TO_DOWNLOAD[3]: DOWNLOAD_DIR
    + FILES_TO_DOWNLOAD[3],
}

if __name__ == "__main__":
    load_dotenv()

    client = YandexCloudClient(
        bucket_name=os.environ.get("S3_BUCKET_NAME"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID_STUDENT"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY_STUDENT"),
    )

    # Loading all files to the set directory
    for s3_path, local_path in MAPPING.items():
        client.download_file(
            s3_file_path=s3_path,
            local_file_path=local_path,
        )
